from rest_framework import serializers
from .models import Edl, EdlEntry
import validators


class EdlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edl
        fields = ['id', 'name', 'description', 'edl_type', 'created']


class EdlEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = EdlEntry
        fields = ['id', 'entry_value', 'created', 'valid_until', 'edl']

    def validate(self, data):
        # EDL Type and Value Check
        # Todo:: Improve validation - Domain should support wildcard
        # Todo:: Improve validation - URL should support wildcard
        # Todo:: Ensure valid_til field is in the future
        if data["edl"].edl_type == 'ip_address':
            if not validators.ipv4(data['entry_value']):
                raise serializers.ValidationError("entry_value is not a valid ipv4 address")
        if data["edl"].edl_type == 'url':
            if not validators.url(data['entry_value']):
                raise serializers.ValidationError("entry_value is not a valid url")
        if data["edl"].edl_type == 'domain':
            if not validators.domain(data['entry_value']):
                raise serializers.ValidationError("entry_value is not a valid ipv4 domain")
        return data
