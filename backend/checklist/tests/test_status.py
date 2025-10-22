from django.test import TestCase
from django.contrib.auth.models import User
from checklist.models import Checklist, ChecklistItem


class ChecklistStatusTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser')

    def test_empty_checklist_is_incomplete(self):
        cl = Checklist.objects.create(name='Empty', created_by=self.user)
        self.assertEqual(cl.status, 'incomplete')

    def test_all_items_done_marks_complete(self):
        cl = Checklist.objects.create(name='AllDone', created_by=self.user)
        ChecklistItem.objects.create(checklist=cl, title='a', is_done=True, updated_by=self.user)
        ChecklistItem.objects.create(checklist=cl, title='b', is_done=True, updated_by=self.user)
        cl.refresh_from_db()
        self.assertEqual(cl.status, 'complete')

    def test_any_item_incomplete_marks_incomplete(self):
        cl = Checklist.objects.create(name='Mixed', created_by=self.user)
        ChecklistItem.objects.create(checklist=cl, title='a', is_done=True, updated_by=self.user)
        ChecklistItem.objects.create(checklist=cl, title='b', is_done=False, updated_by=self.user)
        cl.refresh_from_db()
        self.assertEqual(cl.status, 'incomplete')

    def test_deleting_items_updates_status(self):
        cl = Checklist.objects.create(name='DeleteFlow', created_by=self.user)
        i1 = ChecklistItem.objects.create(checklist=cl, title='a', is_done=True, updated_by=self.user)
        i2 = ChecklistItem.objects.create(checklist=cl, title='b', is_done=False, updated_by=self.user)
        # delete the incomplete one, leaving only done items -> complete
        i2.delete()
        cl.refresh_from_db()
        self.assertEqual(cl.status, 'complete')
        # delete the last item, checklist becomes empty -> incomplete
        i1.delete()
        cl.refresh_from_db()
        self.assertEqual(cl.status, 'incomplete')
