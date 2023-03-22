"""
seriealizers for the user API View
"""

from django.contrib.auth import get_user_model

from rest_framework import serializers
# includes all the different tools needed for defining serializers
# SERIALIZERS are a way to convert to/from python objects


class UserSerializer(serializers.ModelSerializer):
    """serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
            }
        }

    def create(self, validated_data):
        """create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)
