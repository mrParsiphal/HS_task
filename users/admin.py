from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import UserProfile, Invite_code_bindings


class UserLoginForm(forms.ModelForm):
    pass


class UserCreationForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=18, label='Номер телефона',)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

    class Meta:
        model = UserProfile
        fields = ('phone_number', )


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm

    list_display = (
        'phone_number', 'invite_code', 'is_active', 'is_staff', 'date_joined')
    search_field = ('phone_number', 'invite_code', )
    filter_horizontal = ()
    list_filter = ()
    ordering = ('phone_number',)
    fieldsets = (
        (None, {'fields': ('phone_number', 'invite_code', 'date_joined')}),
        ('Настройки доступа', {'fields': ('is_superuser', 'is_staff', 'is_active', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', ),
        }),
    )
    readonly_fields = ['invite_code', 'date_joined']
    search_fields = ['phone_number', 'invite_code', ]


admin.site.register(UserProfile, UserAdmin)
admin.site.register(Invite_code_bindings)
