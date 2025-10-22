from django.db import models
from django.contrib.auth.models import User

class Checklist(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="checklists")
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
        ("incomplete", "Incomplete"),
        ("complete", "Complete"),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="incomplete")

    def __str__(self):
        return self.name

    def update_status(self):
        """Recompute the checklist status based on its items.

        If all items are done -> 'complete', otherwise 'incomplete'.
        """
        items = self.items.all()
        new_status = "incomplete"
        if items.exists() and all(item.is_done for item in items):
            new_status = "complete"

        if self.status != new_status:
            self.status = new_status
            # avoid recursion by saving directly
            Checklist.objects.filter(pk=self.pk).update(status=new_status)

class ChecklistItem(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # keep reference to parent so we can update status after save
        parent = self.checklist
        super().save(*args, **kwargs)
        if parent:
            parent.update_status()

    def delete(self, *args, **kwargs):
        # capture parent before deletion
        parent = self.checklist
        super().delete(*args, **kwargs)
        if parent:
            parent.update_status()
