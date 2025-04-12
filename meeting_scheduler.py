#!/usr/bin/env python3
import datetime
from typing import List, Tuple

# Define types for clarity
Meeting = Tuple[datetime.datetime, datetime.datetime]
TimeSlot = Tuple[datetime.datetime, datetime.datetime]

def schedule_meetings(meetings: List[Meeting]) -> List[Meeting]:
    """
    Merge overlapping meetings to create a set of non-overlapping scheduled intervals.

    Args:
        meetings (List[Meeting]): A list of meetings as tuples (start, end).

    Returns:
        List[Meeting]: A list of merged meeting intervals.
    """
    if not meetings:
        return []
    
    # Sort meetings by start time
    meetings.sort(key=lambda interval: interval[0])
    
    merged = [meetings[0]]
    for current in meetings[1:]:
        last_start, last_end = merged[-1]
        current_start, current_end = current
        
        # If current meeting overlaps with last, merge them
        if current_start <= last_end:
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            merged.append(current)
    return merged

def get_available_slots(merged: List[Meeting], start_day: datetime.datetime, end_day: datetime.datetime) -> List[TimeSlot]:
    """
    Calculate available time slots between scheduled meetings within a day.

    Args:
        merged (List[Meeting]): A list of non-overlapping meetings.
        start_day (datetime.datetime): Start time of the day.
        end_day (datetime.datetime): End time of the day.

    Returns:
        List[TimeSlot]: A list of available time intervals.
    """
    available: List[TimeSlot] = []
    current_time = start_day

    for meeting in merged:
        meeting_start, meeting_end = meeting
        if current_time < meeting_start:
            available.append((current_time, meeting_start))
        # Ensure current_time moves to at least meeting_end to handle back-to-back meetings.
        current_time = max(current_time, meeting_end)
    
    if current_time < end_day:
        available.append((current_time, end_day))
    
    return available

def main() -> None:
    # Example meetings data
    meetings: List[Meeting] = [
        (datetime.datetime(2025, 4, 12, 9, 0), datetime.datetime(2025, 4, 12, 10, 0)),
        (datetime.datetime(2025, 4, 12, 10, 30), datetime.datetime(2025, 4, 12, 11, 30)),
        (datetime.datetime(2025, 4, 12, 11, 0), datetime.datetime(2025, 4, 12, 12, 0))
    ]
    
    # Merge overlapping meetings
    merged_meetings = schedule_meetings(meetings)
    
    # Define the day boundaries for available slots
    start_day = datetime.datetime(2025, 4, 12, 8, 0)
    end_day = datetime.datetime(2025, 4, 12, 17, 0)
    
    available_slots = get_available_slots(merged_meetings, start_day, end_day)
    
    # Print scheduled meetings
    print("Scheduled Meetings:")
    for start, end in merged_meetings:
        print(f" - {start.strftime('%Y-%m-%d %H:%M')} to {end.strftime('%Y-%m-%d %H:%M')}")
    
    # Print available slots
    print("\nAvailable Slots:")
    for start, end in available_slots:
        print(f" - {start.strftime('%Y-%m-%d %H:%M')} to {end.strftime('%Y-%m-%d %H:%M')}")
    
if __name__ == '__main__':
    main()
