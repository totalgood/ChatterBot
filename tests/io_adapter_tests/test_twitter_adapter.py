from unittest import TestCase
from chatterbot.adapters.io import TwitterAdapter


class TwitterAdapterTests(TestCase):

    def setUp(self):
        self.adapter = TwitterAdapter(
            twitter_consumer_key="blahblahblah",
            twitter_consumer_secret="nullvoidnullvoidnullvoid"
        )

    def test_get_mentions(self):
        from.twitter_data.mentions import MENTIONS

        mentions = self.adapter.get_mentions()

