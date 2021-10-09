from django.http.response import JsonResponse
from django.db.models import Q
from django.views import View

from apps.azure import models, forms

from libs.utils import Pagination, DateTimeToStr
from apps.azure.tasks import update_azure_vm, task_update_az
from libs.azure import VM_SIZES

class AzureAccountView(View):
    def get(self, request):
        q = Q()

        if request.GET.get('wd'):
            wd = request.GET.get('wd', '').strip()
            q.add(Q(email__icontains=wd) | Q(password__icontains=wd) |  Q(client_id__icontains=wd)|  Q(subscription_id__icontains=wd)|  Q(note__icontains=wd) | Q(display_name__icontains=wd), Q.AND)

        data_list = models.Account.objects.filter(q).order_by('-id')

        limit = request.GET.get('limit', 25)
        page = request.GET.get('page', 1)
        data_count = data_list.count()
        start, end = Pagination(page, limit, data_count)

        _data_list = []
        for data in data_list[start:end]:
            _data = {
                'id': data.id,
                'email': data.email,
                'password': data.password,
                'client_id': data.client_id,
                'tenant_id': data.tenant_id,
                'login_password': data.login_password,
                'subscription_id': data.subscription_id,
                'display_name': data.display_name,
                'note': data.note,
                'vm_count': data.get_vm_count(),
                'status': data.status,
                'status_text': data.get_status_display(),
                'create_time': DateTimeToStr(data.create_time),
                'update_time': DateTimeToStr(data.update_time)
            }
            _data_list.append(_data)
        return JsonResponse({
            'code': 20000,
            'message': '获取成功',
            'data': {
                'total': data_count,
                'image_list': models.Images.get_images(),
                'location_list': models.Account.location_list(),
                'vm_sizes': VM_SIZES,
                'items': _data_list
            }
        })

    def post(self, request):
        try:
            inputData = forms.AccountForm(request.POST)
            if inputData.is_valid():
                data = inputData.clean()
                dataInfo = data.get('id', False)
                email = data.get('email', '')
                _data = {
                    'client_id': data.get('app_id', ''),
                    'email': data.get('email', ''),
                    'password': data.get('password', ''),
                    'login_password': data.get('login_password', ''),
                    'tenant_id': data.get('tenant_id'),
                    'note': data.get('note', '')
                }
                if not dataInfo:

                    # 测试账号是否正常
                    message, status = models.Account.check_status(data.get('app_id'), data.get('password'), data.get('tenant_id'))

                    if not status:
                        return JsonResponse({'code': 20001, 'message': f'账号添加失败, 只能添加有效的账号'})

                    ret = models.Account.objects.create(**_data)
                    if ret:
                        task_update_az(ret.id)
                        return JsonResponse({'code': 20000, 'message': f'{email} 账号添加成功'})
                    return JsonResponse({'code': 20002, 'message': f'{email} 账号添加失败'})
                if models.Account.objects.filter(id=dataInfo.id).update(**_data):
                    task_update_az.delay(data['id'])
                    return JsonResponse({'code': 20000, 'message': f'{email} 账号添加成功'})

                return JsonResponse({'code': 20000, 'message': f'账号更新失败'})
                #models.Account.objects.create(**_data)

            return JsonResponse({'code': 20001, 'message': '操作失败', 'error_data': inputData.errors})
        except BaseException as e:
            return JsonResponse({'code': 20001, 'message': '添加账号失败', 'error_message': e})

# 删除 Azure 账号
class AzureAccountDeleteView(View):
    def post(self, request):
        account_id = request.POST.get('account_id')
        account_info = models.Account.objects.filter(id=account_id).first()
        if not account_info:
            return JsonResponse({
                'code': 20001,
                'message': '账号不存在'
            })

        if account_info.delete():
            return JsonResponse({
                'code': 20000,
                'message': '删除成功'
            })
        return JsonResponse({
            'code': 20001,
            'message': '删除失败'
        })



# Azure Vm 实例列表
class AzureVmListView(View):
    def get(self, request):
        q = Q()
        # 搜索
        if request.GET.get('wd'):
            wd = request.GET.get('wd', '').strip()
            q.add(Q(name__icontains=wd) | Q(ip__icontains=wd)| Q(vm_size__icontains=wd)| Q(vm_id__icontains=wd)| Q(username__icontains=wd)| Q(password__icontains=wd) | Q(group__icontains=wd)| Q(location__icontains=wd) , Q.AND)

        if request.GET.get('account_name'):
            wd = request.GET.get('account_name', '').strip()
            q.add(Q(account__display_name__icontains=wd) | Q(account__email__icontains=wd)| Q(account__subscription_id__icontains=wd)| Q(account__password__icontains=wd)| Q(account__tenant_id__icontains=wd)| Q(account__client_id__icontains=wd), Q.AND)

        if request.GET.get('username'):
            wd = request.GET.get('username', '').strip()
            q.add(Q(account__username__icontains=wd), Q.AND)

        _data_list = []
        data_list = models.Vm.objects.filter(q).order_by('-create_time', 'id')

        limit = request.GET.get('limit', 25)
        page = request.GET.get('page', 1)
        data_count = data_list.count()
        start, end = Pagination(page, limit, data_count)

        for data in data_list[start:end]:
            _data = {
                'id': data.id,
                'name': data.name,
                'ip': data.ip,
                'vm_id': data.vm_id,
                'username': data.username,
                'password': data.password,
                'vm_size': data.vm_size,
                'os_disk': data.os_disk,
                'image': models.Images.get_name(data.image),
                'region': models.Account.location_list(data.location),
                'group': data.group,
                'status': data.status,
                'status_text': data.get_status_display(),
                'create_time': DateTimeToStr(data.create_time),
                'update_time': DateTimeToStr(data.update_time),
                'account': data.account.email,
                'subscription_id': data.account.subscription_id
            }
            _data_list.append(_data)

        return JsonResponse({
            'code': 20000,
            'message': '获取成功',
            'data': {
                'total': data_count,
                'items': _data_list
            }
        })

# Azure Vm 操作
class AzureVmActionView(View):
    def post(self, request):
        vm_id = request.POST.get('vm_id')
        action = request.POST.get('action', '')

        if action in '':
            return JsonResponse({
                'code': 20001,
                'message': '操作无效'
            })

        vm_info = models.Vm.objects.filter(vm_id=vm_id).first()
        if not vm_info:
            return JsonResponse({
                'code': 20001,
                'message': 'VM不存在, 请核实后操作'
            })

        action_map = {
            'start': '开机',
            'stop': '关机',
            'restart': '重启',
            'delete': '删除',
            'update': '更新',
        }

        if action in ['start', 'stop', 'restart', 'delete']:
            # 电源操作
            if vm_info.vm_action(action):
                update_azure_vm(vm_info.id)
                return JsonResponse({
                    'code': 20000,
                    'message': f'{vm_info.vm_id} {action_map.get(action, action)} 操作成功, 状态需要更新之后才会显示'
                })
            return JsonResponse({
                'code': 20001,
                'message': '操作失败'
            })

        if action in 'update':
            vm_info.update_public_ip()
            vm_info.update_vm_info()
            return JsonResponse({
                'code': 20000,
                'message': '操作成功'
            })

        if action in ['resetip']:
            if vm_info.reset_ip():
                # update_azure_vm(vm_info.id)
                return JsonResponse({
                    'code': 20000,
                    'message': f'更换IP操作已完成, 新IP需要几分钟才能显示。'
                })
            return JsonResponse({
                'code': 20001,
                'message': '更换IP失败'
            })

# 创建 Azure Vm 实例
class AzureVmCreateView(View):
    def post(self, request):
        account_id = request.POST.get('account_id')
        password = request.POST.get('password', '')
        image_id = request.POST.get('image_id', '')
        vm_size = request.POST.get('type', '')
        os_disk = request.POST.get('os_disk', 64)
        region = request.POST.get('region', '')
        name = request.POST.get('name')
        account_info = models.Account.objects.filter(id=account_id).first()
        if not account_info:
            return JsonResponse({
                'code': 20001,
                'message': '创建失败, 账号不存在!'
            })

        if models.Vm.objects.filter(account_id=account_info.id, name=name).first():
            return JsonResponse({
                'code': 20001,
                'message': '创建失败, 实例名称不可重复!'
            })

        if '' in [region, vm_size, image_id, password]:
            return JsonResponse({
                'code': 20001,
                'message': '创建失败, 异常操作!'
            })
        message, status = account_info._creae_vm(location=region, vm_size=vm_size, password=password, vm_name=name, image=image_id, os_disk=os_disk)
        if status:
            return JsonResponse({
                'code': 20000,
                'message': '创建成功, 请返回实例列表查看!'
            })
        return JsonResponse({
            'code': 20001,
            'message': f'创建失败, {message}!'
        })