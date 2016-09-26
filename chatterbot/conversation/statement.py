# -*- coding: utf-8 -*-
from .response import Response


class Statement(object):
    """
    A statement represents a single spoken entity, sentence or
    phrase that someone can say.
    """

    def __init__(self, text, in_response_to=(), **kwargs):
        self.text = text
        self.in_response_to = list(in_response_to)
        # self.in_response_to_text = list(kwargs.pop('in_response_to_text', )

        self.extra_data = dict(kwargs)

    def __str__(self):
        return self.text

    def __repr__(self):
        return "<Statement text:%s>" % (self.text)

    def __eq__(self, other):
        if not other:
            return False

        if isinstance(other, Statement):
            return self.text == other.text

        return self.text == other

    def add_extra_data(self, key, value):
        """
        This method allows additional data to be stored on the
        statement object.
        """
        self.extra_data[key] = value

    def add_response(self, response_to):
        """
        Add the response to the list if it does not already exist.
        """
        if not isinstance(response_to, Response):
            raise Statement.InvalidTypeException(
                'A {} was recieved when a {} instance was expected'.format(
                    type(response_to),
                    type(Response(''))
                )
            )

        # # this may not work for Response Django Model instances without overriding __equal__ there too
        # try:
        #     self.in_response_to[self.in_response_to.index(response_to)].occurrence += 1
        # except:
        #     self.in_response_to.append(response_to)

        # FIXME: This won't scale!
        #        Instead, self.in_response_to should be a collections.Counter() dict
        updated = False
        for index in range(0, len(self.in_response_to)):
            if response_to.text == self.in_response_to[index].text:
                self.in_response_to[index].occurrence += 1
                updated = True

        if not updated:
            self.in_response_to.append(response_to)

    def remove_response(self, response_text):
        """
        Removes a response from the statement's response list based
        on the value of the response text.
        """
        for response in self.in_response_to:
            if response_text == response.text:
                self.in_response_to.remove(response)
                return True
        return False

    def get_response_count(self, statement):
        """
        Return the number of times the statement occurs in the database.
        """
        for response in self.in_response_to:
            if statement.text == response.text:
                return response.occurrence

        return 0

    def serialize(self):
        """
        Returns a dictionary representation of the current object.
        """
        data = {}

        data["text"] = self.text
        data["in_response_to"] = []
        data.update(self.extra_data)

        for response in self.in_response_to:
            data["in_response_to"].append(response.serialize())

        return data

    class InvalidTypeException(Exception):

        def __init__(self, value='Recieved an unexpected value type.'):
            self.value = value

        def __str__(self):
            return repr(self.value)
