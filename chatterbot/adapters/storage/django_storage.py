import logging

from chatterbot.adapters.storage import StorageAdapter
from chatterbot.conversation import Statement, Response

logger = logging.getLogger(__name__)


class DjangoStorageAdapter(StorageAdapter):

    def __init__(self, **kwargs):
        super(DjangoStorageAdapter, self).__init__(**kwargs)

    def count(self):
        from chatterbot.ext.django_chatterbot.models import Statement as StatementModel
        return StatementModel.objects.count()

    def model_to_object(self, statement_record):
        """
        Convert a Django model object into a ChatterBot Statement object.
        """
        statement = Statement(statement_record.text)

        for response_record in statement_record.in_response_to.all():
            # logger.info(str(response_object))
            statement.add_response(Response(
                response_record.statement.text,
                occurrence=response_record.occurrence
            ))

        return statement

    def find(self, statement_text):
        """Find any existing Django record of this statement and return a Statement object or None"""
        from chatterbot.ext.django_chatterbot.models import Statement as StatementModel
        try:
            statement = StatementModel.objects.get(
                text=statement_text
            )
            return self.model_to_object(statement)
        except StatementModel.DoesNotExist:
            return None

    def filter(self, **kwargs):
        """
        Returns a list of statements in the database
        that match the parameters specified.
        """
        from chatterbot.ext.django_chatterbot.models import Statement as StatementModel

        kwargs_copy = kwargs.copy()

        for kwarg in kwargs_copy:
            value = kwargs[kwarg]
            del kwargs[kwarg]
            kwarg = kwarg.replace('__contains', '__responses__text')
            kwargs[kwarg] = value

        if 'in_response_to' in kwargs:
            prompts = kwargs.pop('in_response_to')

            if prompts:
                kwargs['prompts__text__in'] = []
                for p in prompts:
                    kwargs['prompts__text__in'].append(p.text)
            else:
                kwargs['prompts'] = None

        statement_records = StatementModel.objects.filter(**kwargs)

        results = []

        for statement_record in statement_records:
            results.append(self.model_to_object(statement_record))

        return results

    def update(self, statement_object):
        """Add a new statement object to Django database as Statement and Response table records"""
        from chatterbot.ext.django_chatterbot.models import Statement as StatementModel
        from chatterbot.ext.django_chatterbot.models import Response as ResponseModel
        # Do not alter the database unless writing is enabled
        if not self.read_only:
            django_statement, created = StatementModel.objects.get_or_create(
                text=statement_object.text
            )

            # The statement could have been made in response to multiple other in_response_to statements
            # FIXME: only update the occurence count for the one input statement this response is to,
            #        not all the past in_response_to statements (which is what this does)
            for in_response_to in statement_object.in_response_to:
                logger.info("in_response_to: " + str(in_response_to))
                # the in_response_to Response record is a directed edge or connection between 2 Statement records
                #     from the Response.in_response_to Statement record
                #     to the Response.statement Statement record
                #     with occurrence number of times it has been used as a response
                in_response_to_django_statement, created = StatementModel.objects.get_or_create(
                    text=in_response_to.text)
                # response_statement, created = StatementModel.objects.get_or_create(
                #     text=in_response_to.statement.text)
                response_record, created = ResponseModel.objects.get_or_create(
                    statement=django_statement,
                    response_to=in_response_to_django_statement)
                # count has already been incremented in the RAM Response(object) instance
                response_record.occurrence = in_response_to.occurrence
                response_record.save()

            django_statement.save()

        return statement_object

    def get_random(self):
        """
        Returns a random statement from the database
        """
        from chatterbot.ext.django_chatterbot.models import Statement as StatementModel
        statement = StatementModel.objects.order_by('?').first()
        return self.model_to_object(statement)

    def remove(self, statement_text):
        """
        Removes the statement that matches the input text.
        Removes any responses from statements if the response text matches the
        input text.
        """
        from chatterbot.ext.django_chatterbot.models import Statement as StatementModel
        from chatterbot.ext.django_chatterbot.models import Response as ResponseModel
        from django.db.models import Q
        statements = StatementModel.objects.filter(text=statement_text)

        responses = ResponseModel.objects.filter(
            Q(statement__text=statement_text) | Q(response_to__text=statement_text)
        )

        responses.delete()
        statements.delete()

    def drop(self):
        """
        Remove the database.
        """
        pass
