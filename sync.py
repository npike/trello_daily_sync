#!/usr/bin/env python
import sys 
sys.path.append("py-trello-master")
sys.path.append("python-dateutil-1.5")

import os
from trello import TrelloClient, Unauthorized, ResourceUnavailable
from pprint import pprint
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config.properties')

# setup: pip install requests_oauthlib

client = TrelloClient(
	api_key=config.get('Trello', 'trello.api_key'), 
	api_secret=config.get('Trello', 'trello.api_secret'), 
	token=config.get('Trello', 'trello.token')
)

client.list_boards()

for board in client.list_boards():
	lists = board.all_lists()
	# find any list called "Daily"
	for aList in lists:
		#print aList.name, aList.board
		if aList.name == "Daily":
			print "[found daily list] " + aList.name, aList.board.name
			# board dailie tasks are stored in [boardName.toLower].txt
			dailyListIn  = open(aList.board.name.lower()+".txt", "rb")
			# archive all existing cards in this list FIRST
			print "Archiving old daily cards"
			aList.archive_all_cards()

			# each line of dailyListIn represends a new card.
			# if the line starts with a -, the card has a checklist and this is a list item

			dailyCard = None
			dailyCardChecklist = []
			for line in dailyListIn:
				if not line.startswith("-"):
					# check to make sure we werent processing a list
					if dailyCardChecklist:
						print "Added checklist for " + dailyCard.name
						checklist = dailyCard.add_checklist("Checklist",
                                       dailyCardChecklist)
						dailyCardChecklist = []
					# create a new card
					print "Creating card for "+line
					dailyCard = aList.add_card(line)
				if line.startswith("-"):
					# track all of the list items for this card
					# we will add them all to the card later
					dailyCardChecklist.append(line[1:].strip())

			# clean up.  we might have a pending dailyCardChecklist
			if dailyCardChecklist:
				print "Added checklist for " + dailyCard.name
				checklist = dailyCard.add_checklist("Checklist",  dailyCardChecklist)
				dailyCardChecklist = []


			dailyListIn.close()

print "Sync done."
