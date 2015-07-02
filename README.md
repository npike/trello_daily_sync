Script that runs nightly (via cron on some box) that will add recurring daily tasks to my Trello boards.

Things like:
- Morning Medicine (with checklist)
- Nightly Medicine (with checklist)
- Log breakfast
- Log lunch
- Log dinner

Script will search for any list called "Daily" (in any board), and then if there's a local file with the same name (in lowercase) it will populate that Trello list with new cards.

(All existing cards in that list will be archived.)

**Example daily config file:**

    Morning Vitamins

    Floss

    Check blood pressure

    10 minutes of German class

    Exercise
    - 10 pushups
    - 1 minute plank

    [Tuesday]
    Bike to work

    [Thursday]
    Rock climbing

    [Friday]


    [Saturday]
    Clean apartment
    Laundry


**To setup:**

1. Get your developer api key and secret:  https://trello.com/app-key
2. Authorize a user to use this application: Visit this page in a browser (after replacing your_api_key with value above): https://trello.com/1/authorize?response_type=token&key=[your_api_key]&return_url=https%3A%2F%2Ftrello.com&callback_method=fragment&scope=read,write&expiration=never&name=Daily+Trello
3. Grab token out of URL from response
4. Configure DailyTrello:  rename config.properties.sample to config.properties
5. Populate config.properties with appropriate values
6. Run
    sudo pip install requests
    sudo pip install requests-oauthlib
7. Run DailyTrello:  python sync.py


**To do:**

* Add setup mode to script that will generate the user auth URL
