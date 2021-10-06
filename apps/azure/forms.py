from django import forms

from apps.azure import models


class AccountForm(forms.Form):
    id = forms.IntegerField(required=False)
    email = forms.CharField(max_length=255)
    app_id = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)
    login_password = forms.CharField(max_length=255, required=False)
    tenant_id = forms.CharField(max_length=255)
    note = forms.CharField(max_length=255, required=False)

    def clean_id(self):
        try:
            id = self.cleaned_data.get('id', False)
            if not id: return False
            nodeInfo = models.Account.objects.filter(id=id).first()
            if not nodeInfo:
                raise forms.ValidationError(message='账号不存在')
            return nodeInfo
        except:
            return False


