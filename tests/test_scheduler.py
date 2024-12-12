import pandas as pd
from scheduler.scheduler import find_overlap

def test_find_overlap():
    # Sample data
    data = [
        {'day': 'Mon', 'start': 14, 'end': 16},
        {'day': 'Mon', 'start': 15, 'end': 17},
        {'day': 'Tue', 'start': 10, 'end': 12},
        {'day': 'Tue', 'start': 11, 'end': 13},
    ]
    df = pd.DataFrame(data)
    expected = pd.DataFrame([
        {'day': 'Mon', 'start': 15, 'end': 16},
        {'day': 'Tue', 'start': 11, 'end': 12},
    ])
    result = find_overlap(df)
    pd.testing.assert_frame_equal(result, expected)

if __name__ == "__main__":
    test_find_overlap()
    print("All tests passed!")
