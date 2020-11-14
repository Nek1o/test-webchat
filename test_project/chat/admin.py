from django.contrib import admin

from .models import *
# Register your models here.

def ban_user(modeladmin, request, queryset):
    queryset.update(banned=True)
ban_user.short_description = "Ban users"

def unban_user(modeladmin, request, queryset):
    queryset.update(banned=False)
unban_user.short_description = "Unban users"


class ChatAdmin(admin.ModelAdmin):
    list_display = ['username', 'banned']
    actions = [ban_user, unban_user]

class MessageAdmin(admin.ModelAdmin):
    list_display = ['time', 'sender', 'content', 'get_session_id']

    def get_session_id(self, obj):
        return obj.session.id
    get_session_id.short_description = 'session id'

class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['get_user_one', 'get_user_two']

    def get_user_one(self, obj):
        return User.objects.filter(chatsessions__id=obj.id)[0]
    get_user_one.short_description = "User one"

    def get_user_two(self, obj):
        return User.objects.filter(chatsessions__id=obj.id)[1]
    get_user_two.short_description = "User two"
    

admin.site.register(ChatUser, ChatAdmin)
admin.site.register(ChatSession, ChatSessionAdmin)
admin.site.register(Message, MessageAdmin)
