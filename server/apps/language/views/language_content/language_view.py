from rest_framework import generics
from rest_framework.permissions import AllowAny
from apps.language.models import Language
from apps.language.serializers import LanguageSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(tags=['Языки'])
class LanguageListView(generics.ListAPIView):
    """
    Получение списка языков
    """
    permission_classes = [AllowAny]
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
