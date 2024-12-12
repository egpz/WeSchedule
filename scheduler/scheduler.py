import pandas as pd
from calendar_utils import authenticate_google_calendar, create_calendar_event
from datetime import datetime

def collect_availability():
    """
    Collects availability from a user via command line input.
    Returns a pandas DataFrame containing the availability data.
    """
    print("Enter your availability in the format: Day Start-End (e.g., Mon 14-16).")
    print("Type 'done' when finished.")
    availability = []
    while True:
        entry = input("Availability: ")
        if entry.lower() == 'done':
            break
        try:
            day, time_range = entry.split()
            start, end = map(int, time_range.split('-'))
            availability.append({'day': day, 'start': start, 'end': end})
        except ValueError:
            print("Invalid format. Try again.")
    return pd.DataFrame(availability)

def find_overlap(group_availability, event_duration=None):
    """
    Finds overlapping time slots in group availability data.
    Input:
        - group_availability: pandas DataFrame with 'day', 'start', and 'end' columns.
        - event_duration: (int or None) Event duration in hours. If None, no intervals are calculated.
    Output:
        pandas DataFrame with overlapping times or intervals of the given duration.
    """
    grouped = group_availability.groupby('day')
    results = []
    fallback_results = []  # To store shorter overlaps
    for day, slots in grouped:
        slots = slots.sort_values(by='start').reset_index(drop=True)
        overlap_start = slots.iloc[0]['start']
        overlap_end = slots.iloc[0]['end']

        for i in range(1, len(slots)):
            current_start = slots.iloc[i]['start']
            current_end = slots.iloc[i]['end']

            # Update overlap range
            overlap_start = max(overlap_start, current_start)
            overlap_end = min(overlap_end, current_end)

            if overlap_start >= overlap_end:
                overlap_start = current_start
                overlap_end = current_end
            else:
                # Store valid intervals if duration is provided
                if event_duration:
                    interval_start = overlap_start
                    while interval_start + event_duration <= overlap_end:
                        results.append({
                            'day': day,
                            'start': interval_start,
                            'end': interval_start + event_duration
                        })
                        interval_start += event_duration
                    # Store fallback for shorter overlaps if no full-duration matches
                    if overlap_end - overlap_start > 0:
                        fallback_results.append({
                            'day': day,
                            'start': overlap_start,
                            'end': overlap_end
                        })
                else:
                    # Store full overlap if no duration is provided
                    results.append({'day': day, 'start': overlap_start, 'end': overlap_end})

    # Return results or fallback if no full-duration overlaps are found
    if results:
        return pd.DataFrame(results)
    elif fallback_results:
        print("\nNo full-duration overlaps found. Suggesting shorter overlap times:")
        return pd.DataFrame(fallback_results)
    else:
        return pd.DataFrame()

def suggest_time():
    """
    Gathers availability from multiple users and suggests the best meeting time with a specific date.
    """
    print("\nWhat is the name of the event?")
    event_name = input("Event name: ")

    print("\nWould you like to specify a duration for the event? (yes/no)")
    specify_duration = input().lower()
    event_duration = None
    if specify_duration == 'yes':
        try:
            event_duration = int(input("Enter the duration in hours: "))
        except ValueError:
            print("Invalid input. No duration will be set.")
            event_duration = None

    print("\nGathering availability for the group.")
    group_availability = pd.DataFrame()
    while True:
        print("\nEnter availability for one person:")
        person_availability = collect_availability()
        group_availability = pd.concat([group_availability, person_availability])
        add_more = input("Add another person? (yes/no): ").lower()
        if add_more != 'yes':
            break

    print("\nFinding overlaps...")
    overlaps = find_overlap(group_availability, event_duration)
    if overlaps.empty:
        print(f"\nNo overlapping times found for the event '{event_name}'.")
    else:
        print(f"\nSuggested times for the event '{event_name}':")
        for idx, row in overlaps.iterrows():
            print(f"{idx + 1}. {row['day']}: {row['start']}:00 - {row['end']}:00")

        # Allow the user to select a time
        choice = int(input("\nSelect a time slot (enter the number): ")) - 1
        selected_row = overlaps.iloc[choice]

        # Get attendee emails
        print("\nEnter the email addresses of attendees (comma-separated):")
        attendees = input().split(',')

        # Get the date for the event
        print("\nEnter the date for the event (format: YYYY-MM-DD):")
        date = input("Date: ")
        try:
            # Validate the date
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please enter in YYYY-MM-DD format.")
            return

        # Authenticate and create the event
        creds = authenticate_google_calendar()
        create_calendar_event(
            creds,
            event_name,
            f"{selected_row['start']:02d}:00",
            f"{selected_row['end']:02d}:00",
            attendees,
            date
        )

if __name__ == "__main__":
    suggest_time()
