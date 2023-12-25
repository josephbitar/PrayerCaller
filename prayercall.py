import time

import pygame
from praytimes import PrayTimes
import time as tm
from time import struct_time
from datetime import datetime

class PrayerCall:
    def __init__(self, longitude: float, latitude: float, timezone: int, calculation_method : str = 'ISNA'):
        self.next_prayer_name = None
        self.pt = PrayTimes()
        self.pt.adjust({'method': calculation_method})
        # TODO: please change the lat and lon according to your city
        self.latitude = longitude
        self.longitude = latitude
        self.timezone = timezone
        self.prayer_names = ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha']

    def play_athan(self):
        """
         A void function to play call for prayer audio
        """
        pygame.mixer.init()
        pygame.mixer.music.load('046.mp3')  # Replace with your Athan sound file path
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

    def set_next_prayer_name(self, times):
        """
         A function to determine the next prayer name
        :param times: dictionary that has the prayer names and times as key value pairs
        :return:
        """
        # Get current time and convert it to datetime
        current_time_str = tm.strftime('%H:%M')
        current_time = datetime.strptime(current_time_str, '%H:%M')

        # Get Prayer Times
        fajr_time = datetime.strptime(times['fajr'], '%H:%M')
        dhuhr_time = datetime.strptime(times['dhuhr'], '%H:%M')
        asr_time = datetime.strptime(times['asr'], '%H:%M')
        maghrib_time = datetime.strptime(times['maghrib'], '%H:%M')
        isha_time = datetime.strptime(times['isha'], '%H:%M')

        # Determine what the next prayer name is
        if current_time <= fajr_time:
            self.next_prayer_name = 'fajr'
        elif fajr_time < current_time <= dhuhr_time:
            self.next_prayer_name = 'dhuhr'
        elif dhuhr_time < current_time <= asr_time:
            self.next_prayer_name = 'asr'
        elif asr_time < current_time <= maghrib_time:
            self.next_prayer_name = 'maghrib'
        elif maghrib_time < current_time <= isha_time:
            self.next_prayer_name = 'isha'
        elif current_time > isha_time:
            self.next_prayer_name = 'midnight'

    def get_next_day_date(self, current_time) -> struct_time:
        """
        A function to get the next day date from the current time
        :param current_time:
        :return: next day date
        """
        # Calculate seconds in a day
        seconds_in_a_day = 24 * 60 * 60  # 24 hours * 60 minutes * 60 seconds

        # Calculate timestamp for the next day
        next_day_timestamp = tm.mktime(current_time) + seconds_in_a_day

        # Convert the timestamp of the next day to a struct_time object
        return tm.localtime(next_day_timestamp)

    def calculate_time_to_sleep(self, start_time, end_time, target_time) -> int:
        """
        A function to calculate how many seconds left to the next prayer
        :param start_time:current time
        :param target_time: next prayer call time
        :param end_time: the time to updated with target time
        :return: the remaining seconds to the next prayer call
        """
        # Create the next prayer time with the right date and target time
        updated_end_time = time.struct_time((end_time.tm_year, end_time.tm_mon, end_time.tm_mday,
                                         target_time.hour, target_time.minute, 00,
                                         end_time.tm_wday, end_time.tm_yday,
                                         end_time.tm_isdst))
        updated_start_time = time.struct_time((start_time.tm_year, start_time.tm_mon, start_time.tm_mday,
                                         start_time.tm_hour, start_time.tm_min, 00,
                                         start_time.tm_wday, start_time.tm_yday,
                                         start_time.tm_isdst))

        # Calculate how many seconds are remaining till next prayer time
        return tm.mktime(updated_end_time) - tm.mktime(updated_start_time) - start_time.tm_sec + 5

    def print_remaining_to_next_prayer(self, seconds: int) -> str:
        hours, remainder = divmod(seconds, 3600)
        minutes, secs = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(secs):02d}"

    def main(self):
        # Get prayer times for the current date
        prayer_times = self.pt.getTimes(tm.localtime(), (self.latitude, self.longitude), self.timezone, 'auto')
        while True:
            self.set_next_prayer_name(prayer_times)
            current_time = tm.localtime()

            # if it is at the end of the day, then get the next day prayers times
            if self.next_prayer_name == 'midnight':
                # Get the next day prayer times
                next_day = self.get_next_day_date(tm.localtime())
                prayer_times = self.pt.getTimes(next_day, (self.latitude, self.longitude), -7, 'auto')
                self.next_prayer_name = 'fajr'
                target_time = datetime.strptime(prayer_times['fajr'], '%H:%M')
                time_to_update = next_day
            else:
                target_time = datetime.strptime(prayer_times[self.next_prayer_name], '%H:%M')
                time_to_update = current_time

            time_to_sleep = self.calculate_time_to_sleep(current_time, time_to_update, target_time)
            prayer_time = prayer_times[self.next_prayer_name]
            print(f"Next prayer is : {self.next_prayer_name}: {prayer_time}")

            if self.next_prayer_name in self.prayer_names and tm.strftime('%H:%M') == prayer_time:
                self.play_athan()
            else:
                tm.sleep(time_to_sleep)


if __name__ == "__main__":
    athan_instance = PrayerCall(32.7767, -96.808891, -7, 'ISNA')
    athan_instance.main()