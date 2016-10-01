from django.contrib import admin
from chatterbot.ext.django_chatterbot.models import Statement, Response


class StatementAdmin(admin.ModelAdmin):
    list_display = ('text',)  # , 'response')
    list_filter = list_display
    search_fields = list_display


class ResponseAdmin(admin.ModelAdmin):
    list_display = ('statement', 'response', 'occurrence', )
    list_filter = list_display
    search_fields = list_display


admin.site.register(Statement, StatementAdmin)
admin.site.register(Response, ResponseAdmin)
