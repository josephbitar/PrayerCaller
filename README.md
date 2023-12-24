# Prayer Time Reminder

This Python program retrieves prayer times based on latitude and longitude coordinates and notifies users when it's time for prayers by playing the Athan MP3 file.

## Description

The application uses the PrayTimes library to calculate prayer times for a given location. It requires latitude and longitude coordinates to determine the prayer timings accurately.

Once the program calculates prayer times, it continuously checks the current time and compares it with the prayer times. When the time for a prayer is reached, it triggers the Athan sound to remind users of the prayer.

## Requirements

- Python 3.x
- PrayTimes library (installation instructions provided in the project's setup section)

## Installation and Setup

1. Clone or download the repository.

2. Install PrayTimes library:
   ```bash
   pip install praytimes