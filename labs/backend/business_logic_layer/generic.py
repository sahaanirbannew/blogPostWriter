import pandas as pd
from datetime import datetime   

# Convert and split
def format_datetime(dt_str):
    try:
        dt = datetime.strptime(dt_str, "%Y:%m:%d %H:%M:%S")
        date_str = dt.strftime("%d %B %Y")        # e.g., 21 March 2025
        time_str = dt.strftime("%-H:%M:%S") + " hours"  # e.g., 8:22:58 hours (use %-H for non-padded hour on Unix)
        return pd.Series([date_str, time_str])
    except Exception:
        return pd.Series([None, None])  