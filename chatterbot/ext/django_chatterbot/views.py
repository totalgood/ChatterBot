import logging

from django.views.generic import View
from django.http import JsonResponse
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings

from pugnlp.util import PrettyDict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatterBotView(View):

    chatterbot = ChatBot(**settings.CHATTERBOT)

    def post(self, request, *args, **kwargs):
        # logger.info(str(request.__dict__))
        input_statement = request.POST.get('text')
        # logger.info(str(request.POST.__dict__))

        # response_data is a dict!
        response_data = self.chatterbot.get_response(input_statement)
        # logger.info(PrettyDict(response_data))

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        logger.info(PrettyDict(request.__dict__))
        input_statement = request.GET.get('text')
        logger.info(PrettyDict(request.POST.__dict__))

        if input_statement is not None:
            response_data = self.chatterbot.get_response(input_statement)
            response_data.add_extra_data('input_statement')
            return JsonResponse(response_data, status=200)
        data = {
            'detail': 'The GET API requires a "?text=..." query. And POST is the prefered endpoint anyway.',
            'name': self.chatterbot.name,
            'input_statement': repr(input_statement),
            'text': repr(getattr(input_statement, 'get', dict)().get('text', None)),
        }
        # Return a "method not allowed" response
        return JsonResponse(data, status=405)

    def patch(self, request, *args, **kwargs):
        logger.info(PrettyDict(request.__dict__))
        data = {
            'detail': 'You are in `ChatterBotView.patch()`. Try POST for more reliable results.',
            'name': self.chatterbot.name,
        }

        # Return a method not allowed response
        return JsonResponse(data, status=405)

    def delete(self, request, *args, **kwargs):
        logger.info(PrettyDict(request.__dict__))
        data = {
            'detail': 'You are in `ChatterBotView.delete()`. Try POST for more reliable results.',
            'name': self.chatterbot.name,
        }

        # Return a method not allowed response
        return JsonResponse(data, status=405)
