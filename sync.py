#!/usr/bin/env python
import os
import sys 
sys.path.append(os.path.abspath(os.path.split(sys.argv[0])[0])+"/py-trello-master")
sys.path.append(os.path.abspath(os.path.split(sys.argv[0])[0])+"/python-dateutil-1.5")
import os
from trello import TrelloClient, Unauthorized, ResourceUnavailable
from pprint import pprint
import ConfigParser
import calendar
from datetime import date

config = ConfigParser.RawConfigParser()
config.read(os.path.abspath(os.path.split(sys.argv[0])[0])+'/config.properties')

# today is a [day of week]
dayOfWeek = calendar.day_name[date.today().weekday()]
print "Starting sync for " + dayOfWeek

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
			boardConfigFile = os.path.abspath(os.path.split(sys.argv[0])[0])+'/'+aList.board.name.lower()+".txt"
			if not os.path.exists(boardConfigFile):
				print "No configuration file found for "+aList.board.name +", skipping."
				continue
			dailyListIn  = open(boardConfigFile, "rb")
			# archive all existing cards in this list FIRST
			print "Archiving old daily cards"
			aList.archive_all_cards()

			# each line of dailyListIn represends a new card.
			# if the line starts with a -, the card has a checklist and this is a list item

			shouldAddCard = True
			dailyCard = None
			dailyCardChecklist = []
			
			for line in dailyListIn:

				# skip empty lines
				if not line.strip():
					continue

				# process sections as cards for specific days of the week
				if line.startswith("["):
					if "["+dayOfWeek+"]" in line:
						print "Found section specific for this day of the week "+dayOfWeek
						shouldAddCard = True
					else:
						shouldAddCard = False
					continue

				if shouldAddCard:
					if not line.startswith("-"):
						# check to make sure we werent processing a list
						if dailyCardChecklist:
							print "Added checklist for " + dailyCard.name
							checklist = dailyCard.add_checklist("Checklist",dailyCardChecklist)
							dailyCardChecklist = []
						# create a new card
						print "Creating card for "+line
						dailyCard = aList.add_card(line)
					elif line.startswith("-"):
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
