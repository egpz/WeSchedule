import pandas as pd

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

def find_overlap(group_availability):
    """
    Finds overlapping time slots in group availability data.
    Input: pandas DataFrame with 'day', 'start', and 'end' columns.
    Output: pandas DataFrame with overlapping times.
    """
    grouped = group_availability.groupby('day')
    results = []
    for day, slots in grouped:
        slots = slots.sort_values(by='start').reset_index(drop=True)
        # Initialize overlap range with the first slot
        overlap_start = slots.iloc[0]['start']
        overlap_end = slots.iloc[0]['end']

        for i in range(1, len(slots)):
            current_start = slots.iloc[i]['start']
            current_end = slots.iloc[i]['end']

            # Update the overlap range
            overlap_start = max(overlap_start, current_start)
            overlap_end = min(overlap_end, current_end)

            # If there is no overlap, reset the range
            if overlap_start >= overlap_end:
                overlap_start = current_start
                overlap_end = current_end
            else:
                # Store the overlapping range
                results.append({'day': day, 'start': overlap_start, 'end': overlap_end})

    return pd.DataFrame(results)



def suggest_time():
    """
    Gathers availability from multiple users and suggests the best meeting time.
    """
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

