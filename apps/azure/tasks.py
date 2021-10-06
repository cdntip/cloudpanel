from django.db.models import Q

from celery import shared_task

from apps.azure import models

# 更新账号
@shared_task()
def task_update_az(account_id):
    account_info = models.Account.objects.filter(id=account_id).first()

    if not account_info:
        return '账号不存在', False

    account_info.update_subscriptions()
    account_info.update_vm_list()

    for _vm in models.Vm.objects.filter(account_id=account_info.id):
        _vm.update_public_ip()
        _vm.update_vm_info()
    return '更新完成', True

# 更新虚拟机
@shared_task()
def update_azure_vm(vm_id):
    try:
        vm_info = models.Vm.objects.filter(id=vm_id).first()
        if not vm_info:
            return 'VM 实例不存在', False
        vm_info.update_public_ip()
        vm_info.update_vm_info()
        return '更新完成', True
    except:
        return '更新失败', False

# 更新全部账号的订阅
@shared_task()
def beat_update_azure_account():
    account_list = models.Account.objects.filter(status__in=['Enabled', 'Warned'])
    print(f'需要更新的账号数量为 {account_list.count()}')
    for foo in account_list:
        task_update_az.delay(foo.id)
    return True

# 更新全部需要更新的VM
@shared_task()
def beat_update_azure_vm():
    q = Q(ip='') | ~Q(status='running')
    data_list = models.Vm.objects.filter(q)
    print(f'需要更新的VM数量为 {data_list.count()}')
    for foo in data_list:
        update_azure_vm.delay(foo.id)
    return True