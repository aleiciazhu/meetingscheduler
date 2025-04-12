# Meeting Scheduler

This is a simple Python project that helps schedule meetings by merging overlapping meeting intervals and determining available time slots throughout the day. It’s designed as a lightweight tool for managing and optimizing daily schedules \.

## Overview

The Meeting Scheduler performs two primary functions:
- **Merge Overlapping Meetings:** Combines meeting intervals that overlap so that they appear as a single block on your schedule.
- **Identify Available Time Slots:** Calculates gaps between the scheduled meetings within specified day boundaries, so you know when you’re free.

This solution is optimized for static sets of meeting intervals using a sort-and-merge strategy, which runs in O(n log n) time. For dynamic scheduling scenarios, more advanced data structures, like interval trees, could be considered.

## Features

- **Interval Merging:** Sorts and merges overlapping meeting intervals.
- **Available Time Calculation:** Returns free time slots between your scheduled meetings.
- **Simple and Modular:** Composed of distinct functions that can be extended or integrated into larger systems.
- **Optimized Performance:** Uses an efficient algorithm with a runtime dominated by the initial sort operation.
- **Timezone Conversion:** Harmonize schedules for large teams in timezones across the world.

## Requirements

- **Python 3.x**
- Uses Python’s built-in `datetime` module and standard libraries, so no additional packages are needed.

## Installation and Setup

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/aleiciazhu/meetingscheduler.git
    cd meetingscheduler
    ```

2. **Run the Script:**

    Execute the scheduler by running:

    ```bash
    python meeting_scheduler.py
    ```

## Usage

The script includes an example in its `main()` function:
- It defines a list of sample meeting intervals.
- It merges overlapping intervals.
- It calculates available time slots between the merged meetings given a start-of-day and end-of-day boundary.
- Finally, it prints the scheduled meetings and free slots.

## Code Structure

- **`schedule_meetings(meetings: List[Tuple[datetime, datetime]]) -> List[Tuple[datetime, datetime]]`**
  - Merges overlapping meeting intervals.
- **`get_available_slots(merged: List[Tuple[datetime, datetime]], start_day: datetime, end_day: datetime) -> List[Tuple[datetime, datetime]]`**
  - Computes available time slots between the merged meetings.
- **`main()`**
  - Demonstrates the usage with example data and prints the output.
