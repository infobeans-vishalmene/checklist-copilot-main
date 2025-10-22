from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Checklist, ChecklistItem
from .serializers import ChecklistSerializer, ChecklistItemSerializer

class ChecklistViewSet(viewsets.ModelViewSet):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(created_by=user)

class ChecklistItemViewSet(viewsets.ModelViewSet):
    queryset = ChecklistItem.objects.all()
    serializer_class = ChecklistItemSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        # serializer may include a 'checklist' PK via the PrimaryKeyRelatedField
        serializer.save(updated_by=user)

    def perform_update(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(updated_by=user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # if no items, return default response
        if not queryset.exists():
            return super().list(request, *args, **kwargs)

        # Group items by checklist_id while preserving order
        from collections import OrderedDict
        groups = OrderedDict()
        # select_related to avoid N+1
        for item in queryset.select_related('checklist'):
            cid = item.checklist_id
            groups.setdefault(cid, []).append(item)

        # build grouped response
        from .serializers import ChecklistItemCompactSerializer, ChecklistCompactSerializer
        result = []
        for cid, items in groups.items():
            checklist = Checklist.objects.filter(pk=cid).first()
            checklist_data = ChecklistCompactSerializer(checklist).data
            items_data = ChecklistItemCompactSerializer(items, many=True).data
            result.append({
                'checklist': checklist_data,
                'items': items_data,
            })

        return Response(result)
