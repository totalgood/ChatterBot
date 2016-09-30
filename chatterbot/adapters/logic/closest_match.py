# -*- coding: utf-8 -*-
import time

from fuzzywuzzy import fuzz

from .base_match import BaseMatchAdapter


class ClosestMatchAdapter(BaseMatchAdapter):
    """ Compose response based on the historical response for statements most similar to the input

    Use fuzzywuzzy's process class (Levenshtein distance) to find the most similar response to the input
    and that statement object's response can then be used by the caller to respond.

    A thinking "response_time" is configurable to maintain a reasonable chat pace.
    """
    bot_response_time = 1.0

    def get(self, input_statement):
        """ Takes a statement object and findes the closest match in the storage adapter """
        t0 = time.time()
        statement_list = self.context.storage.get_response_statements()

        if not statement_list:
            if self.has_storage_context:
                # Use a randomly picked statement
                self.logger.info(
                    u'No statements have known responses. ' +
                    u'Choosing a random response to return.'
                )
                return 0, self.context.storage.get_random()
            else:
                raise self.EmptyDatasetException()

        confidence = -1
        closest_match = input_statement
        input_statement_text = input_statement.text.lower()

        # fuzzywuzzy has a bestmatch method that's much faster than this
        # Find the closest matching known statement
        for historical_statement in statement_list:
            ratio = fuzz.ratio(input_statement_text, historical_statement.text.lower())

            if ratio > confidence:
                confidence = ratio
                closest_match = historical_statement

        # Convert the confidence integer percent to a float probability between 0.0 and 1.0
        confidence /= 100.0

        t1 = time.time()
        time.sleep(min(max(getattr(self.context, 'bot_response_time', self.bot_response_time) - t1 + t0, 0), 600))
        return confidence, closest_match
