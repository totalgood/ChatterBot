from django.contrib import admin
from chatterbot.ext.django_chatterbot.models import Statement, Response, ChatUser, Score


@admin.register(Statement)
class StatementAdmin(admin.ModelAdmin):
    list_display = ('text', 'score', 'chatuser', 'created', 'modified', )
    list_filter = list_display
    search_fields = list_display


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('statement', 'response', 'occurrence', 'created', 'modified', )
    list_filter = list_display
    search_fields = list_display
    # list_display = ('response', 'prompt', 'occurrence', 'created', 'modified', )
    # list_filter = ('response', 'prompt', 'occurrence', 'created', 'modified', )
    # search_fields = ('response', 'prompt', 'occurrence', 'created', 'modified', )


@admin.register(ChatUser)
class ChatUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'gender', 'chat_age', 'created', 'modified', )
    list_filter = list_display
    search_fields = list_display


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('kindness', 'positive', 'negative', 'neutral', 'readability', 'flesch', 'kincaid', 'dale_chall', 'sarcasm', 'chat_age')
    list_filter = list_display
    search_fields = list_display
