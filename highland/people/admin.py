from django.contrib import admin

from .models import ExecutivePosition, ExecutiveMember, Committee, CommitteeMember

class ExecutivePositionAdmin(admin.ModelAdmin):
    list_display = ('order_index', 'position_title')
    ordering = ('order_index',)

class ExecutiveMemberAdmin(admin.ModelAdmin):
    list_display = ('position', 'person_name', 'person_email', 'person_photo')
    ordering = ('position',)

class CommitteeAdmin(admin.ModelAdmin):
    list_display = ('committee_title',)
    ordering = ('committee_title',)

class CommitteeMemberAdmin(admin.ModelAdmin):
    list_display = ('committee', 'person_name', 'person_email')
    ordering = ('committee',)

admin.site.register(ExecutivePosition, ExecutivePositionAdmin)
admin.site.register(ExecutiveMember, ExecutiveMemberAdmin)
admin.site.register(Committee, CommitteeAdmin)
admin.site.register(CommitteeMember, CommitteeMemberAdmin)
