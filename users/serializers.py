import users.models as users
from rest_framework import serializers


class UserSubscriptionSerialaizer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = users.Invite_code_bindings
        fields = '__all__'