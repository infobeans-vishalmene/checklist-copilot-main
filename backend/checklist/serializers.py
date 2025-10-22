from rest_framework import serializers
from .models import Checklist, ChecklistItem
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ChecklistRelatedField(serializers.PrimaryKeyRelatedField):
    """Writable PK field that represents the Checklist as a nested object on read.

    Accepts an integer checklist id on write, but returns a nested checklist dict on read
    so the response contains the full checklist under the `checklist` key.
    """
    def to_representation(self, value):
        # value is a Checklist instance
        if value is None:
            return None
        # DRF may pass a PKOnlyObject for performance; resolve it to the real instance
        try:
            obj = value
            # PKOnlyObject has .pk but not attribute access for fields
            if not hasattr(obj, 'id') and hasattr(obj, 'pk'):
                obj = Checklist.objects.filter(pk=getattr(obj, 'pk')).first()
                if obj is None:
                    return None
        except Exception:
            obj = Checklist.objects.filter(pk=value).first()

        return {
            'id': obj.id,
            'name': obj.name,
            'created_by': UserSerializer(obj.created_by).data if obj.created_by else None,
            'created_at': obj.created_at,
            'status': obj.status,
        }

    def get_choices(self, cutoff=None):
        """Return choices for the browsable API as a mapping of hashable keys to labels.

        DRF's default uses to_representation(item) as keys which can be unhashable
        if to_representation returns a dict. We return stringified PKs instead so
        the browsable form renders without raising "unhashable type: 'dict'".
        """
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        if cutoff is None:
            cutoff = self.html_cutoff

        choices = {}
        for item in queryset[:cutoff]:
            # use string PK as a stable, hashable key and the object's str() as label
            choices[str(item.pk)] = str(item)

        return choices


class ChecklistItemSerializer(serializers.ModelSerializer):
    updated_by = UserSerializer(read_only=True)
    # single field 'checklist' that is writable by id and readable as nested object
    checklist = ChecklistRelatedField(queryset=Checklist.objects.all(), required=False)

    class Meta:
        model = ChecklistItem
        fields = ['id', 'title', 'is_done', 'updated_by', 'updated_at', 'checklist']


class ChecklistItemCompactSerializer(serializers.ModelSerializer):
    """Compact serializer for list responses when checklist is provided once.

    Excludes the nested checklist to avoid repetition.
    """
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = ChecklistItem
        fields = ['id', 'title', 'is_done', 'updated_by', 'updated_at']


class ChecklistCompactSerializer(serializers.ModelSerializer):
    """Compact checklist serializer without items for single-checklist list responses."""
    created_by = UserSerializer(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Checklist
        fields = ['id', 'name', 'created_by', 'created_at', 'status']

class ChecklistSerializer(serializers.ModelSerializer):
    items = ChecklistItemSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    status = serializers.CharField(read_only=True)
    class Meta:
        model = Checklist
        fields = ['id', 'name', 'created_by', 'created_at', 'items', 'status']
