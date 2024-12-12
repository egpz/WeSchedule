import pandas as pd
from datetime import datetime, timedelta

def collect_availability():
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

def find_overlap(group_availability):
    grouped = group_availability.groupby('day')
    results = []
    for day, slots in grouped:
        slots = slots.sort_values(by='start')
        overlap_start = max(slots['start'])
        overlap_end = min(slots['end'])
        if overlap_start < overlap_end:
            results.append({'day': day, 'start': overlap_start, 'end': overlap_end})
    return pd.DataFrame(results)

def suggest_time():
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
    overlaps = find_overlap(group_availability)
    if overlaps.empty:
        print("\nNo overlapping times found.")
    else:
        print("\nSuggested times:")
        for _, row in overlaps.iterrows():
            print(f"{row['day']}: {row['start']}:00 - {row['end']}:00")

if __name__ == "__main__":
    suggest_time()

