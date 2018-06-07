from django.conf import settings
from django.test import TestCase

from djaludir.core.models import Activity

from djtools.utils.logging import seperator


class CoreActivityTestCase(TestCase):

    fixtures = ['user.json', 'activity.json']

    def setUp(self):
        self.cid = settings.TEST_USER_COLLEGE_ID

    def test_activity(self):

        print("\n")
        print("test activity ORM data model")
        print(seperator())

        # obtain our health insturance object
        activities = Activity.objects.filter(user__id=self.cid)

        for activity in activities:
            print(activity)

        self.assertGreaterEqual(len(activities), 1)