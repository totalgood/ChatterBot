import logging

from django.db import models

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Statement(models.Model):
    """A short (<255) chat message, tweet, forum post, etc"""

    text = models.CharField(
        unique=True,
        blank=False,
        null=False,
        max_length=255
    )

    responses = models.ManyToManyField('self', through='Response', symmetrical=False, default=None)

    def __str__(self):
        if len(self.text.strip()) > 60:
            return '{}...'.format(self.text[:57])
        elif len(self.text.strip()) > 0:
            return self.text
        return '<empty>'


class Response(models.Model):
    """Connection between a response and the statement that triggered it

    Comparble to a ManyToMany "through" table, but without the M2M indexing/relations.

    Only the text and number of times it has occurred are currently stored.
    Might be useful to store additional features like language, location(s)/region(s),
    first created datetime(s), username, user full name, user gender, etc.
    A the very least occurrences should be an FK to a meta-data table with this info.
    """

    statement = models.ForeignKey(
        'Statement',
        related_name='in_response_to'
    )

    response = models.ForeignKey(
        'Statement',
        related_name='+'
    )

    occurrence = models.PositiveIntegerField(default=0)

    def __str__(self):
        s = self.statement.text if len(self.statement.text) <= 64 else self.statement.text[:61] + '...'
        s += ' => '
        s += self.response.text if len(self.response.text) <= 64 else self.response.text[:61] + '...'
        return s

    class Meta:
        unique_together = (('statement', 'response'),)
