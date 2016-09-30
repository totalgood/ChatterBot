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

    # VADER components
    positive = models.FloatField(default=None, null=True, blank=True,
        help_text="VADER positive valence (emotion) intensity in a statement (see Hutto, C.J. & Gilbert)",)
    negative = models.FloatField(default=None, null=True, blank=True,
        help_text="VADER negative valence (emotion) intensity in a statement (see Hutto, C.J. & Gilbert)",)
    neutral = models.FloatField(default=None, null=True, blank=True,
        help_text="VADER neutral valence (emotion) intensity in a statement (see Hutto, C.J. & Gilbert)",)
    compound = models.FloatField(default=None, null=True, blank=True,
        help_text="VADER compound valence intensity from NLTK.SentimentIntensityAnalyzer (see Hutto, C.J. & Gilbert)",)
    flesch = models.FloatField(default=None, null=True, blank=True,
        help_text='Flesch Reading Ease based on sylable, word, and sentence counts (from `readability.superficial_measures["readability grades"]`).',)
    kincaid = models.FloatField(default=None, null=True, blank=True,
        help_text='Kincaid grade level (from `readbility.superficial_measures["readability grades"]`)',)
    dale_chall = models.FloatField(default=None, null=True, blank=True,
        help_text='Readability percent, 0-100, based on occurrence of 3000 most common English words (from `textstat.dale_chall_readability_score`)',)
    intensity = models.FloatField(default=None, null=True, blank=True,
        help_text="Emotional intensity (from VADER by Hutto, C.J. & Gilbert)",)
    kindness = models.FloatField(default=None, null=True, blank=True,
        help_text="Probability (0-1) of making a kind statement",)
    sarcasm = models.FloatField(default=None, null=True, blank=True,
        help_text="Lack of sincerity in a statement",)
    readability = models.FloatField(default=None, null=True, blank=True,
        help_text="Probability (0-1) of making a kind statement",)
    chat_age = models.FloatField(default=None, null=True, blank=True,
        help_text="Oldfashioned-ness, negative hipness, in mean age of the utterance distribution in time",)

    def __str__(self):
        s = 'emotion: ({:.2f} +{:.2f} -{:.2f}) * {:.2f}'.format(self.neutral or 0, self.positive or 0, self.negative or 0, self.intensity or 0)
        s += ', readability: ({:.1f} {:.1f} {:.1f})'.format(self.flesch or 0, self.kincaid or 0, self.dale_chall or 0)
        s += ', kindness: (+{} -{})'.format(self.kindness or 0, self.sarcasm or 0)
        return s


class Statement(BaseModel):
    """A short (<255) chat message, tweet, forum post, etc"""

    chatuser = models.ForeignKey(ChatUser, null=True)
    score = models.OneToOneField(Score, on_delete=models.CASCADE, primary_key=True)
    text = models.CharField(unique=False, blank=False, null=False, max_length=255)
    possibile = models.ManyToManyField('self', symmetrical=False, through='Response')

    def __str__(self):
        if len(self.text.strip()) > 60:
            return '{}...'.format(self.text[:57])
        elif len(self.text.strip()) > 0:
            return self.text
        return '<empty>'


class Response(BaseModel):
    """Connection from a prompting statement to the response that it invoked

    Comparble to a ManyToMany "through" table, but without the M2M indexing/relations.

    Only the text and number of times it has occurred are currently stored.
    Might be useful to store additional features like language, location(s)/region(s),
    first created datetime(s), username, user full name, user gender, etc.
    A the very least occurrences should be an FK to a meta-data table with this info.
    """

    statement = models.ForeignKey(
        'Statement',
        verbose_name='Prompting statement',
        related_name='in_response_to'
    )

    response = models.ForeignKey(
        'Statement',
        verbose_name='Response statement',
        related_name='+'
    )

    unique_together = (('statement', 'response'),)

    occurrence = models.PositiveIntegerField(default=0)

    def __str__(self):
        s = self.statement.text if len(self.statement.text) <= 64 else self.statement.text[:61] + '...'
        s += ' => '
        s += self.response.text if len(self.response.text) <= 32 else self.response.text[:29] + '...'
        return s
