from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers
from apps.language.models import Language


@extend_schema_serializer(component_name='Languages')
class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = (
            'id',
            'name',
            'description',
            'code'
        )
