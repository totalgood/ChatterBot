from django.contrib import admin
from chatterbot.ext.django_chatterbot.models import Statement, Response, ChatUser, Score


@admin.register(Statement)
class StatementAdmin(admin.ModelAdmin):
    list_display = ('text', 'chat_user', 'created', 'modified', )
    list_filter = ('text', 'chat_user', 'created', 'modified', )
    search_fields = ('text', 'chat_user', 'created', 'modified', )


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('statement', 'response', 'occurrence', 'created', 'modified', )


@admin.register(ChatUser)
class ChatUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'gender', 'chat_age', 'created', 'modified', )


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('kindness', 'positivity', 'negativity', 'neutrality', 'readability', 'sarcasm', 'chat_age')
