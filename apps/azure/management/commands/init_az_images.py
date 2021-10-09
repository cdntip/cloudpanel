from django.core.management.base import BaseCommand
from django.core.management import execute_from_command_line
from django.conf import settings

from apps.azure.models import Images

class Command(BaseCommand):
    help = '更新全部azure镜像地址'

    def handle(self, *args, **options):
        images = {
            'OpenLogic:CentOS:7.5:latest': 'CentOS 7.5',
            'OpenLogic:CentOS:7_9:latest': 'CentOS 7.9',
            'Canonical:UbuntuServer:18.04-LTS:latest': 'Ubuntu 18.04',
            'canonical:0001-com-ubuntu-server-focal:20_04-lts-gen2:latest': 'Ubuntu 20.04',
            'Debian:debian-10:10:latest': 'Debian 10',
            'MicrosoftWindowsServer:WindowsServer:2012-Datacenter-zhcn:latest': 'Windows 2012 DC CN',
            'MicrosoftWindowsServer:WindowsServer:2016-Datacenter-zhcn:latest': 'Windows 2016 DC CN',
            'MicrosoftWindowsServer:WindowsServer:2019-Datacenter-smalldisk:latest': 'Windows 2019 DC',
            'MicrosoftWindowsDesktop:Windows-10:21h1-pro:latest	': 'Windows 10 PRO',
        }
        for k, v in images.items():
            # print(k, v)
            if Images.objects.filter(value=k).first(): continue

            Images.objects.create(name=v, value=k)
            continue