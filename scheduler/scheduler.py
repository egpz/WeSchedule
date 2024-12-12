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
            availability.append({'day': day.lower(), 'start': start, 'end': end})
        except ValueError:
            print("Invalid format. Try again.")
    return pd.DataFrame(availability)

def find_overlap(group_availability):
    """
    Finds overlapping time slots in group availability data.
    Ensures overlaps exist across all participants for the same day.
    """
    if group_availability.empty:
        return pd.DataFrame()

    results = []

    # Group availability by day
    for day, group in group_availability.groupby('day'):
        overlap_start = group['start'].max()  # Latest start time across all users
        overlap_end = group['end'].min()      # Earliest end time across all users

        # Check if this overlap is valid for all participants
        all_participants_available = all(
            any((person['start'] <= overlap_start) and (person['end'] >= overlap_end)
                for _, person in group[group['person_id'] == person_id].iterrows())
            for person_id in group['person_id'].unique()
        )

        if all_participants_available and overlap_start < overlap_end:
            results.append({'day': day, 'start': overlap_start, 'end': overlap_end})

    return pd.DataFrame(results)

def suggest_time():
    """
    Gathers availability from multiple users and suggests the best meeting time.
    """
    print("\nGathering availability for the group.")
    group_availability = pd.DataFrame()
    person_id = 1  # Track individual users

    while True:
        print(f"\nEnter availability for Person {person_id}:")
        person_availability = collect_availability()
        person_availability['person_id'] = person_id
        group_availability = pd.concat([group_availability, person_availability], ignore_index=True)
        add_more = input("Add another person? (yes/no): ").lower()
        if add_more != 'yes':
            break
        person_id += 1

    print("\nFinding overlaps...")
    overlaps = find_overlap(group_availability)

    if overlaps.empty:
        print("\nNo overlapping times found.")
    else:
        print("\nSuggested times:")
        for _, row in overlaps.iterrows():
            print(f"{row['day'].capitalize()}: {row['start']}:00 - {row['end']}:00")

if __name__ == "__main__":
    suggest_time()
