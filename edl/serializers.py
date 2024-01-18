from rest_framework import serializers
from .models import Edl, EdlEntry, EdlLog
import validators, re
from django.utils import timezone


class EdlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edl
        fields = ['id', 'name', 'description', 'edl_type', 'created']

    def validate_name(self, value):
        if not re.match("^[A-Za-z0-9_]*$", value):
            raise serializers.ValidationError('Name can only contain alphanumeric and underscores characters')
        return value


class EdlEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = EdlEntry
        fields = ['id', 'entry_value', 'created', 'valid_until', 'edl']

    def validate(self, data):
        # EDL Type and Value Check
        # Todo:: Improve validation - Domain should support wildcard
        # Todo:: Improve validation - URL should support wildcard
        # Todo:: Ensure valid_til field is in the future
        def domain_wildcard_validator(value):
            """Validates a domain wildcard entry"""
            if value.startswith('*.'):
                # Validate only the part after '*.'
                if not validators.domain(value[2:]):
                    raise serializers.ValidationError("entry_value is not a valid wildcard domain")
            else:
                if not validators.domain(value):
                    raise serializers.ValidationError("entry_value is not a valid domain")

        def domain_list_entry_validator(value):
            # Validate length
            if len(value) > 255:
                raise serializers.ValidationError("The domain entry cannot exceed 255 characters.")

            # Check for invalid use of protocol
            if value.startswith(('http://', 'https://')):
                raise serializers.ValidationError("Do not prefix the domain name with the protocol (http or https).")

            # Check for invalid use of start character
            if value.startswith(('.',)):
                raise serializers.ValidationError(
                    "Do not prefix the domain name with dot.")

            # Validate the use of wildcards and exact match characters
            if '*' in value and any(char in value for char in '/ ? & = ; + ^'):
                raise serializers.ValidationError("Wildcard characters must be the only character within a token.")

            # # Check for valid use of wildcard and exact match
            # if '*' in value and not all(token in ('*', '') for token in re.split(r'[/?&=;+]', value)):
            #     raise serializers.ValidationError("Wildcard characters must be the only character within a token.")

            # Validate the position of the exact match character (^)
            if '^' in value:
                if not (value.startswith('^') or value.endswith('^')):
                    raise serializers.ValidationError(
                        "The exact match character (^) must be at the start or the end of the domain.")

                # Ensure that ^ is not used in combination with other characters incorrectly
                if value.startswith('^') and value.count('^') > 1:
                    raise serializers.ValidationError(
                        "When used at the start, the exact match character (^) must not appear elsewhere in the domain.")
                if value.endswith('^') and value.count('^') > 1:
                    raise serializers.ValidationError(
                        "When used at the end, the exact match character (^) must not appear elsewhere in the domain.")

            # Check for unsupported characters
            if not re.match(r'^[A-Za-z0-9.*^/=?&;+-]+$', value):
                raise serializers.ValidationError("The domain contains unsupported characters.")

        # Run validation on Entry Value
        if data["edl"].edl_type == 'ip_address':
            if not validators.ipv4(data['entry_value'], cidr=True):
                raise serializers.ValidationError("entry_value is not a valid ipv4 address")
        if data["edl"].edl_type == 'url':
            domain_list_entry_validator(data['entry_value'])
        if data["edl"].edl_type == 'fqdn':
            domain_wildcard_validator(data['entry_value'])

        # Ensure valid_til field is in the future
        if 'valid_until' in data:
            valid_until = data['valid_until']
            if isinstance(valid_until, str):
                valid_until = datetime.strptime(valid_until, '%Y-%m-%dT%H:%M:%SZ')
            if valid_until <= timezone.now():
                raise serializers.ValidationError("valid_until must be in the future")

        return data

class EdlLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EdlLog
        fields = ['id', 'timestamp', 'performed_by', 'edl_name', 'edl_entry', 'action', 'log_message']
