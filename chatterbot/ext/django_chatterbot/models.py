from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ChatUser(BaseModel):
    """A short (<255) chat message, tweet, forum post, etc"""

    user = models.ForeignKey(User, null=False)
    username = models.CharField(
        unique=True,
        blank=False,
        null=False,
        max_length=64,
    )
    full_name = models.CharField(
        blank=True,
        null=False,
        max_length=128,
    )
    gender = models.CharField(
        help_text="Categorical variable to facilitate personality learning",
        blank=True,
        null=False,
        max_length=32,
    )
    chat_age = models.FloatField(
        help_text="Scalar between 0 and 100 estimating age of a user based solely on their chat style, word choice.",
        blank=True,
        null=True,
        max_length=32,
    )
    kindness = models.FloatField(
        help_text="Probability (0-1) of making a kind statement",
        default=0.,
        null=False,
        blank=True,
    )
    hurtfulness = models.FloatField(
        help_text="Probability (0-1) of making an unkind, cruel, hurtful statement",
        default=0.
    )

    def __str__(self):
        return '{}: {}'.format(self.username, self.full_name)


class Score(BaseModel):
    """Multidimensional score including sentiment (valence and intensity), readability, topic vectors, slangness, age, etc"""
    positivity = models.FloatField(
        help_text="Positive valence (emotion) in a statement (VADER by Hutto, C.J. & Gilbert)",
        default=0.
    )
    negativity = models.FloatField(
        help_text="Negative valence (emotion) in a statement (VADER by Hutto, C.J. & Gilbert)",
        default=0.
    )
    neutrality = models.FloatField(
        help_text="Negative valence (emotion) in a statement (VADER by Hutto, C.J. & Gilbert)",
        default=0.
    )
    intensity = models.FloatField(
        help_text="Emotional intensity (from VADER by Hutto, C.J. & Gilbert)",
        default=0.
    )
    kindness = models.FloatField(
        help_text="Probability (0-1) of making a kind statement",
        default=0.
    )
    sarcasm = models.FloatField(
        help_text="Lack of sincerity in a statement",
        default=0.
    )
    readability = models.FloatField(
        help_text="Probability (0-1) of making a kind statement",
        default=0.
    )
    chat_age = models.FloatField(
        help_text="Oldfashioned-ness, negative hipness, in mean age of the utterance distribution in time",
        default=0.
    )

    def __str__(self):
        s = 'emotion: ({} +{} -{}) * {}'.format(self.neutrality, self.postivity, self.negativity, self.intensity)
        s += ', kindness: (+{} -{})'.format(self.kindness, self.sarcasm)
        s += ', age: (+{} +{})'.format(self.readability, self.sarcasm)

        return s


class Statement(BaseModel):
    """A short (<255) chat message, tweet, forum post, etc"""

    chat_user = models.ForeignKey(ChatUser, null=True)
    score = models.ForeignKey(Score, null=True)
    text = models.CharField(max_length=255)

    def __str__(self):
        if len(self.text.strip()) > 60:
            return '{}...'.format(self.text[:57])
        elif len(self.text.strip()) > 0:
            return self.text
        return '<empty>'


class Response(BaseModel):
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

    response_to = models.ForeignKey(
        'Statement',
        related_name='+'
    )

    unique_together = (('statement', 'response'),)

    occurrence = models.PositiveIntegerField(
        help_text='Number of times this statement has been used to respond to the statement in `in_response_to`.',
        default=0,
        )

    def __str__(self):
        s = self.response_to.text if len(self.response_to.text) <= 40 else self.response.text[:37] + '...'
        s += ' => '
        s = self.statement.text if len(self.statement.text) <= 20 else self.statement.text[:17] + '...'
        return s
