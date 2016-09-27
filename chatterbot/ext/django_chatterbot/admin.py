from django.contrib import admin
from chatterbot.ext.django_chatterbot.models import Statement, Response, ChatUser, Score


@admin.register(Statement)
class StatementAdmin(admin.ModelAdmin):
    list_display = ('text', 'score', 'chat_user', 'created', 'modified', )
    list_filter = ('text', 'score', 'chat_user', 'created', 'modified', )
    search_fields = ('text', 'score', 'chat_user', 'created', 'modified', )


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('response', 'prompt', 'occurrence', 'created', 'modified', )
    list_filter = ('response', 'prompt', 'occurrence', 'created', 'modified', )
    search_fields = ('response', 'prompt', 'occurrence', 'created', 'modified', )


@admin.register(ChatUser)
class ChatUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'gender', 'chat_age', 'created', 'modified', )


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('kindness', 'positivity', 'negativity', 'neutrality', 'readability', 'sarcasm', 'chat_age')
