from django.http import HttpResponse
from django.shortcuts import render, redirect

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .forms import LoginForm, CabinetForm
from django.contrib.auth import authenticate, login

from .serializers import UserSubscriptionSerialaizer
import users.models as users


def Homepage(request):
    if users.UserProfile.objects.filter(phone_number=request.user).exists():
        return redirect('cabinet')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            frm = form.cleaned_data
            user = authenticate(request, phone_number=frm['phone_number'])
            login(request, user, backend='users.backends.AuthBackend')
            return redirect('cabinet')
    form = LoginForm()
    return render(request, 'users/login_page.html', {'forms': form})


def Cabinet(request):

    if request.method == 'POST':
        form = CabinetForm(request.POST)
        try:
            subscription = users.Invite_code_bindings(user_invite_code=request.user,
                                                      invite_code=form.cleaned_data['invite_code'])
            subscription.save()
        except Exception as e:
            form.add_error('subscription', e)
        return HttpResponse(status=202)

    user = users.UserProfile.objects.filter(phone_number=request.user).first()
    content = {}
    content['phone_number'] = user.phone_number
    content['invite_code'] = user.invite_code
    subscriptions = users.Invite_code_bindings.objects.filter(invited_user_id=user.id).values_list(
        'user_invite_code__phone_number', flat=True)
    if subscriptions:
        content['subscriptions'] = ', '.join(subscriptions)
    else:
        subscriptions = 'на вас никто не подписался );'
        content['subscriptions'] = subscriptions
    form = CabinetForm()
    return render(request, 'users/cabinet.html', {'content': content, 'forms': form})


@api_view(['GET'])
def InviteCode(request):
    user = users.UserProfile.objects.filter(phone_number=request.user).first()
    subscriptions = users.Invite_code_bindings.objects.filter(invited_user_id=user.id)
    print(subscriptions)
    serializer = UserSubscriptionSerialaizer(subscriptions, many=True)
    return Response(serializer.data)

