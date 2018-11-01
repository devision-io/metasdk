import datetime
from unittest import TestCase

from metasdk.schedule.Schedule import Schedule


class TestSchedule(TestCase):
    def test_get_next_time(self):
        now = datetime.datetime(2005, 1, 1, 0, 0)
        schedule = Schedule()
        exprs = [
            {
                "value": "0 0 * * *"
            },
        ]
        actual = schedule.get_next_time(exprs, True, now)
        self.assertEqual('2005-01-02 00:00:00', actual)

    def test_get_next_time_min_date(self):
        now = datetime.datetime(2005, 1, 1, 0, 0)
        schedule = Schedule()
        exprs = [
            {
                "value": "0 0 3 * *"
            },
            {
                "value": "10 4 * * *"
            }
        ]
        actual = schedule.get_next_time(exprs, False, now)
        self.assertEqual(datetime.datetime(2005, 1, 1, 4, 10), actual)

    def test_get_next_time_empty_schedules(self):
        schedule = Schedule()
        exprs = []
        actual = schedule.get_next_time(exprs)
        self.assertEqual(None, actual)
