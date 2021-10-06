from django.core.management.base import BaseCommand
from django.core.management import execute_from_command_line
from django.conf import settings

from apps.azure.models import Account, Vm
import time

class Command(BaseCommand):
    help = '更新全部azure账号信息'

    def handle(self, *args, **options):
        for _account in Account.objects.filter(status__in=['Enabled', 'Warned']):
            _account.update_subscriptions()
            _account.update_vm_list()

        for _vm in Vm.objects.filter():
            _vm.update_public_ip()
            _vm.update_vm_info()