from django.contrib import admin

# Register your models here.
# Register your models here.
from apps.azure.models import Account, Vm

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    search_fields = ['tenant_id', 'password', 'client_id', 'subscription_id']

    list_filter = ('status',)
    list_display = ('id', 'display_name', 'email', 'status', 'subscription_id', 'note', 'create_time', 'update_time')

@admin.register(Vm)
class VmAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'vm_id', 'ip', 'status', 'vm_size', 'image', 'os_disk', 'create_time', 'update_time')