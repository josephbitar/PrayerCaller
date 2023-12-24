import time
from unittest import TestCase
from prayercall import PrayerCall
from datetime import datetime

class TestPrayerCall(TestCase):
    def test_get_next_day_date_1(self):
        datetime_str = "2023-12-25 08:30:00"
        time_obj = time.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        athan = PrayerCall(1.0, -1.0, -1, 'ISNA')
        next_date = athan.get_next_day_date(time_obj)
        self.assertEqual(26, next_date.tm_mday)
        self.assertEqual(12, next_date.tm_mon)
        self.assertEqual(2023, next_date.tm_year)

    def test_calculate_time_to_sleep_1(self):
        datetime_str = "2023-12-25 08:30:00"
        current_time = time.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        athan = PrayerCall(1.0, -1.0, -1, 'ISNA')
        calculated_time = athan.calculate_time_to_sleep(current_time, current_time, datetime.strptime('08:35', '%H:%M'))
        self.assertEqual(270, calculated_time)

    def test_calculate_time_to_sleep_2(self):
        datetime_str = "2023-12-25 11:58:00"
        current_time = time.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        athan = PrayerCall(1.0, -1.0, -1, 'ISNA')
        calculated_time = athan.calculate_time_to_sleep(current_time, current_time, datetime.strptime('11:59', '%H:%M'))
        self.assertEqual(30, calculated_time)

    def test_calculate_time_to_sleep_3(self):
        datetime_str = "2023-12-25 23:58:45"
        current_time = time.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        datetime_str_to_update = "2023-12-26 00:01:00"
        time_to_update = time.strptime(datetime_str_to_update, '%Y-%m-%d %H:%M:%S')
        athan = PrayerCall(1.0, -1.0, -1, 'ISNA')
        calculated_time = athan.calculate_time_to_sleep(current_time, time_to_update, datetime.strptime('05:09', '%H:%M'))
        self.assertEqual(18630, calculated_time)

