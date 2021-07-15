from rest_framework import serializers
from .models import RequestSolvo


class RequestSolvoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestSolvo

        fields = [
            'solvo_number',
            'subject',
            'solvo_registered_date',
            'row_created',
            'row_modified',
            'is_defect_registered',
        ]