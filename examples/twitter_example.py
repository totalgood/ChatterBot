from chatterbot import ChatBot
from settings import TWITTER
import time

'''
To use this example, create a new settings.py file.
Define the following in settings.py:

    TWITTER = {}
    TWITTER["CONSUMER_KEY"] = "your-twitter-public-key"
    TWITTER["CONSUMER_SECRET"] = "your-twitter-sceret-key"
'''


chatbot = ChatBot("ChatterBot",
    storage_adapter="chatterbot.adapters.storage.JsonDatabaseAdapter",
    logic_adapter="chatterbot.adapters.logic.ClosestMatchAdapter",
    io_adapter="chatterbot.adapters.io.TwitterAdapter",
    database="../database.db",
    twitter_consumer_key=TWITTER["CONSUMER_KEY"],
    twitter_consumer_secret=TWITTER["CONSUMER_SECRET"]
)

'''
Respond to mentions on twitter.
The bot will follow the user who mentioned it and
favorite the post in which the mention was made.
'''

while True:
    try:
        user_input = chatbot.get_input()

        bot_input = chatbot.get_response(user_input)

        # Pause before checking for the next message
        time.sleep(25)

    except (KeyboardInterrupt, EOFError, SystemExit):
        break

