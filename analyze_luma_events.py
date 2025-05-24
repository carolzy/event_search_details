#!/usr/bin/env python3
"""
Luma Events Diff Analysis

This script analyzes the differences between luma_all_events.csv and luma_bay_area_events.csv
by event date, providing insights into date distribution and differences between the datasets.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from collections import Counter

# File paths
ALL_EVENTS_FILE = "luma_all_events.csv"
BAY_AREA_EVENTS_FILE = "luma_bay_area_events.csv"

def parse_date(date_str):
    """Parse date string into datetime object"""
    if pd.isna(date_str) or date_str == "Not specified":
        return None
    
    # Try different date formats
    date_formats = [
        "%Y-%m-%d",
        "%B %d, %Y",
        "%b %d, %Y",
        "%A, %B %d",
        "%A, %b %d",
        "%B %d",
        "%b %d",
        "%m/%d/%Y",
        "%m/%d/%y"
    ]
    
    # Extract year if present
    year_present = False
    if "2025" in date_str:
        year_present = True
    
    for fmt in date_formats:
        try:
            date = datetime.strptime(date_str, fmt)
            # If no year in format and not already in string, set to current year
            if "%Y" not in fmt and "%y" not in fmt and not year_present:
                current_year = datetime.now().year
                date = date.replace(year=current_year)
            return date
        except ValueError:
            continue
    
    print(f"Could not parse date: {date_str}")
    return None

def analyze_events():
    """Analyze and compare the two event CSV files"""
    # Check if files exist
    if not os.path.exists(ALL_EVENTS_FILE):
        print(f"Error: {ALL_EVENTS_FILE} not found")
        return
    
    if not os.path.exists(BAY_AREA_EVENTS_FILE):
        print(f"Error: {BAY_AREA_EVENTS_FILE} not found")
        return
    
    # Load the CSV files
    all_events = pd.read_csv(ALL_EVENTS_FILE)
    bay_area_events = pd.read_csv(BAY_AREA_EVENTS_FILE)
    
    print(f"Total events in {ALL_EVENTS_FILE}: {len(all_events)}")
    print(f"Total events in {BAY_AREA_EVENTS_FILE}: {len(bay_area_events)}")
    
    # Parse dates
    all_events['parsed_date'] = all_events['event_date'].apply(parse_date)
    bay_area_events['parsed_date'] = bay_area_events['event_date'].apply(parse_date)
    
    # Remove events with unparseable dates
    all_events_valid = all_events.dropna(subset=['parsed_date'])
    bay_area_events_valid = bay_area_events.dropna(subset=['parsed_date'])
    
    print(f"Events with valid dates in {ALL_EVENTS_FILE}: {len(all_events_valid)}")
    print(f"Events with valid dates in {BAY_AREA_EVENTS_FILE}: {len(bay_area_events_valid)}")
    
    # Extract month and day for analysis
    all_events_valid['month'] = all_events_valid['parsed_date'].dt.month
    all_events_valid['day'] = all_events_valid['parsed_date'].dt.day
    bay_area_events_valid['month'] = bay_area_events_valid['parsed_date'].dt.month
    bay_area_events_valid['day'] = bay_area_events_valid['parsed_date'].dt.day
    
    # Count events by month
    all_events_by_month = Counter(all_events_valid['month'])
    bay_area_events_by_month = Counter(bay_area_events_valid['month'])
    
    # Print monthly distribution
    print("\nMonthly Distribution:")
    print("Month | All Events | Bay Area Events | Difference")
    print("-" * 50)
    
    for month in sorted(set(all_events_by_month.keys()) | set(bay_area_events_by_month.keys())):
        month_name = datetime(2025, month, 1).strftime("%B")
        all_count = all_events_by_month.get(month, 0)
        bay_count = bay_area_events_by_month.get(month, 0)
        diff = bay_count - all_count
        print(f"{month_name:10} | {all_count:10} | {bay_count:14} | {diff:10}")
    
    # Find events that are in bay_area but not in all_events (new events)
    all_events_urls = set(all_events['event_url'])
    bay_area_events_urls = set(bay_area_events['event_url'])
    
    new_events_urls = bay_area_events_urls - all_events_urls
    new_events = bay_area_events[bay_area_events['event_url'].isin(new_events_urls)]
    
    print(f"\nNew events in {BAY_AREA_EVENTS_FILE} not found in {ALL_EVENTS_FILE}: {len(new_events)}")
    
    if len(new_events) > 0:
        print("\nSample of new events:")
        sample_size = min(5, len(new_events))
        for i, (_, event) in enumerate(new_events.head(sample_size).iterrows()):
            print(f"{i+1}. {event['event_name']} on {event['event_date']} at {event['event_location']}")
    
    # Find events that are in all_events but not in bay_area (removed events)
    removed_events_urls = all_events_urls - bay_area_events_urls
    removed_events = all_events[all_events['event_url'].isin(removed_events_urls)]
    
    print(f"\nEvents in {ALL_EVENTS_FILE} not found in {BAY_AREA_EVENTS_FILE}: {len(removed_events)}")
    
    if len(removed_events) > 0:
        print("\nSample of removed events:")
        sample_size = min(5, len(removed_events))
        for i, (_, event) in enumerate(removed_events.head(sample_size).iterrows()):
            print(f"{i+1}. {event['event_name']} on {event['event_date']} at {event['event_location']}")
    
    # Create visualizations
    plt.figure(figsize=(12, 6))
    
    months = range(1, 13)
    month_names = [datetime(2025, m, 1).strftime("%b") for m in months]
    
    all_counts = [all_events_by_month.get(m, 0) for m in months]
    bay_counts = [bay_area_events_by_month.get(m, 0) for m in months]
    
    x = np.arange(len(months))
    width = 0.35
    
    plt.bar(x - width/2, all_counts, width, label=f'{ALL_EVENTS_FILE}')
    plt.bar(x + width/2, bay_counts, width, label=f'{BAY_AREA_EVENTS_FILE}')
    
    plt.xlabel('Month')
    plt.ylabel('Number of Events')
    plt.title('Luma Events by Month')
    plt.xticks(x, month_names)
    plt.legend()
    
    plt.savefig('luma_events_comparison.png')
    print("\nVisualization saved as 'luma_events_comparison.png'")

if __name__ == "__main__":
    analyze_events()
