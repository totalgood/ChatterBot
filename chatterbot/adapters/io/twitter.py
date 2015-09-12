# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from chatterbot.adapters.io import IOAdapter
from chatterbot.conversation import Statement
import twitter

try:
    from queue import Queue
except ImportError:
    # Use the python 2 queue import
    from Queue import Queue


class TwitterAdapter(IOAdapter):

    def __init__(self, **kwargs):

        self.api = twitter.Api(
            consumer_key=kwargs["twitter_consumer_key"],
            consumer_secret=kwargs["twitter_consumer_secret"],
            access_token_key=kwargs["twitter_access_token"],
            access_token_secret=kwargs["twitter_access_token_secret"]
        )

        self.mention_queue = Queue()
        self.direct_message_queue = Queue()

    def post_update(self, message):
        return self.api.PostUpdate(message)

    def favorite(self, tweet_id):
        return self.api.CreateFavorite(id=tweet_id)

    def follow(self, username):
        return self.api.CreateFriendship(screen_name=username)

    def get_list_users(self, username, slug):
        return self.api.GetListMembers(None, slug, owner_screen_name=username)

    def get_mentions(self):
        return self.api.GetMentions()

    def search(self, q, count=1, result_type="mixed"):
        url = "https://api.twitter.com/1.1/search/tweets.json"
        url += "?q=" + q
        url += "&result_type=" + result_type
        url += "&count=" + str(count)

        response = requests.get(url=endpoint, auth=self.oauth)

        return response.json()

    def get_related_messages(self, text):
        results = search(text, count=50)
        replies = []
        non_replies = []

        for result in results["statuses"]:

            # Select only results that are replies
            if result["in_reply_to_status_id_str"] is not None:
                message = result["text"]
                replies.append(message)

            # Save a list of other results in case a reply cannot be found
            else:
                message = result["text"]
                non_replies.append(message)

        if len(replies) > 0:
            return replies

        return non_replies

    def reply(self, tweet_id, message):
        """
        Reply to a tweet
        """
        url = "https://api.twitter.com/1.1/statuses/update.json"
        url += "?status=" + message.replace(" ", "%20")
        url += "&in_reply_to_status_id=" + str(tweet_id)

        response = requests.get(url=url, auth=self.oauth)

        return response.json()

    def tweet_to_friends(self, username, slug, greetings, debug=False):
        """    
        Tweet one random message to the next friend in a list every hour.
        The tweet will not be sent and will be printed to the console when in
        debug mode.
        """
        from time import time, sleep
        from random import choice

        # Get the list of robots
        robots = get_list_users(username, slug=slug)

        for robot in robots:
            message = ("@" + robot + " " + choice(greetings)).strip("\n")

            if debug is True:
                print(message)
            else:
                sleep(3600-time() % 3600)
                t.statuses.update(status=message)

    def has_responeded_to_message(self, message_id):
        # TODO
        pass

    def process_input(self):
        """
        This method should check twitter for new mentions and
        return them as Statement objects.
        """
        # Download a list of recent mentions
        mentions = self.get_mentions()

        print "MENTIONS:", mentions

        for mention_data in mentions:

            mention = Statement()

            # Check if a response has been made
            if self.has_responeded_to_message(mention.id)

            # If a response has not been made, add the mention to the mention queue
            self.mention_queue.put()

    def process_response(self, input_statement):
        pass

