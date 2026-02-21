from django.contrib import admin
from .models import ContactMessage, Reply

class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 0
    readonly_fields = ['created_at']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'is_replied', 'created_at']
    list_filter = ['is_read', 'is_replied', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    inlines = [ReplyInline]
    
    fieldsets = (
        ('Sender Information', {
            'fields': ('name', 'email')
        }),
        ('Message Details', {
            'fields': ('subject', 'message', 'created_at')
        }),
        ('Status', {
            'fields': ('is_read', 'is_replied')
        }),
    )

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['original_message', 'replied_by', 'created_at', 'reply_message_truncated']
    list_filter = ['created_at']
    search_fields = ['reply_message']
    readonly_fields = ['created_at']
    
    def reply_message_truncated(self, obj):
        return obj.reply_message[:50] + '...' if len(obj.reply_message) > 50 else obj.reply_message
    reply_message_truncated.short_description = 'Reply'