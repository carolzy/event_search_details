#!/usr/bin/env python3
"""
Filter Events with Speaker Insights

This script:
1. Reads events from luma_all_events.csv
2. Filters out past events using a simple date parsing approach
3. Adds a Speaker_insight column using Gemini API
4. Saves the filtered events to a new CSV file
"""

import os
import csv
import re
from datetime import datetime, timedelta
import logging
import time
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('filter_events_with_insights')

# Initialize Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY not found in environment variables")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)
gemini = genai.GenerativeModel('gemini-2.0-flash')

# Constants
CURRENT_DATE = datetime.now()
DATE_STR = CURRENT_DATE.strftime("%m%d")  # Format: MMDD (e.g., 0425 for April 25)

# File names
INPUT_FILE = "luma_all_events.csv"
OUTPUT_FILE = "luma_filtered_events_with_insights.csv"

def parse_date(date_str):
    """
    Parse date string into a datetime object using a simpler approach
    
    Args:
        date_str: Date string to parse
        
    Returns:
        Datetime object or None if parsing fails
    """
    if not date_str or date_str == 'Not specified':
        return None
    
    # Clean up the date string
    date_str = date_str.strip().lower()
    
    # Handle "Today", "Tomorrow", etc.
    if "today" in date_str:
        return CURRENT_DATE
    if "tomorrow" in date_str:
        return CURRENT_DATE + timedelta(days=1)
    
    # Extract month, day, and year using regex
    # Look for patterns like "April 15" or "Apr 15, 2025"
    month_names = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
        'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12,
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'jun': 6, 'jul': 7, 'aug': 8, 
        'sep': 9, 'sept': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }
    
    # Pattern: Monday, April 15
    weekday_pattern = r'(monday|tuesday|wednesday|thursday|friday|saturday|sunday),?\s+'
    date_str = re.sub(weekday_pattern, '', date_str)
    
    # Try to extract month and day
    month_day_pattern = re.search(r'(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[,\s]+(\d{1,2})', date_str)
    
    if month_day_pattern:
        month_name = month_day_pattern.group(1).lower()
        day = int(month_day_pattern.group(2))
        month = month_names.get(month_name)
        
        # Extract year if present, otherwise use current year
        year_pattern = re.search(r'\b(20\d{2})\b', date_str)
        year = int(year_pattern.group(1)) if year_pattern else CURRENT_DATE.year
        
        try:
            event_date = datetime(year, month, day)
            
            # If the date is in the past and no year was specified, assume it's next year
            if event_date < CURRENT_DATE and not year_pattern:
                event_date = datetime(CURRENT_DATE.year + 1, month, day)
                
            return event_date
        except (ValueError, TypeError):
            logger.warning(f"Failed to create date from: {month}, {day}, {year}")
            return None
    
    # Try standard date formats as a fallback
    formats = ['%Y-%m-%d', '%B %d, %Y', '%b %d, %Y', '%m/%d/%Y', '%m/%d/%y']
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    logger.warning(f"Could not parse date: {date_str}")
    return None

def is_future_event(date_str):
    """
    Determine if an event is in the future
    
    Args:
        date_str: Date string to check
        
    Returns:
        True if the event is in the future, False otherwise
    """
    event_date = parse_date(date_str)
    if not event_date:
        logger.warning(f"Could not determine if date is in future: {date_str}. Excluding it.")
        return False
    
    # Compare the date with current date
    return event_date.date() >= CURRENT_DATE.date()

def get_speaker_insight(speaker_name, speaker_company=None, speaker_title=None):
    """
    Get insights about a speaker using Gemini API with quality checks
    
    Args:
        speaker_name: Name of the speaker
        speaker_company: Company of the speaker (optional)
        speaker_title: Title of the speaker (optional)
        
    Returns:
        Dictionary containing speaker insights, LinkedIn URL, and interview link
    """
    if not speaker_name or speaker_name == 'Not specified':
        return {"insight": "", "linkedin": "", "interview_link": ""}
    
    # Create a more specific prompt with available information
    prompt_details = speaker_name
    if speaker_company and speaker_company != 'Not specified':
        prompt_details += f" from {speaker_company}"
    if speaker_title and speaker_title != 'Not specified':
        prompt_details += f", {speaker_title}"
    
    # Enhanced prompt with quality requirements and structured output
    prompt = f"""Use LinkedIn or search for relevant interviews/podcasts/articles or any useful recent data (within the past 2 years) about {prompt_details} and provide the following information in a structured format:

    REQUIRED INFORMATION:
    1. LinkedIn Profile: Find and provide their LinkedIn profile URL. The URL MUST start with 'https://www.linkedin.com/in/' or 'https://linkedin.com/in/'.
    2. Interview/Podcast/Article: Find ONE recent interview, podcast appearance, or article featuring this person and provide the FULL URL.
    3. Background: Provide a brief background about the person (no more than 5 sentences).

    IMPORTANT REQUIREMENTS:
    - Format your response in three clearly labeled sections: "LinkedIn:", "Interview:", and "Background:"
    - For LinkedIn, provide ONLY the URL, not a markdown link
    - For Interview, provide ONLY the URL, not a markdown link
    - For Background, provide only factual information
    - DO NOT include Luma profile URLs (lu.ma) or any other non-LinkedIn profile URLs in the LinkedIn section
    - Only include URLs that you are confident are valid and directly relevant
    
    Focus on finding high-quality information from LinkedIn and reputable news/media sources."""
    
    try:
        response = gemini.generate_content(prompt)
        full_text = response.text.strip()
        
        # Initialize result dictionary
        result = {
            "insight": "",
            "linkedin": "",
            "interview_link": ""
        }
        
        # Extract LinkedIn URL
        linkedin_match = re.search(r'LinkedIn:\s*(https?://(?:www\.)?linkedin\.com/in/[^\s]+)', full_text, re.IGNORECASE)
        if linkedin_match:
            result["linkedin"] = linkedin_match.group(1).strip()
            logger.info(f"Found LinkedIn URL for {speaker_name}: {result['linkedin']}")
        else:
            # Fallback to regex search in the entire text
            linkedin_urls = re.findall(r'(https?://(?:www\.)?linkedin\.com/in/[^\s\)\]]+)', full_text)
            if linkedin_urls:
                result["linkedin"] = linkedin_urls[0].strip()
                logger.info(f"Found LinkedIn URL for {speaker_name} via fallback: {result['linkedin']}")
            else:
                logger.warning(f"No LinkedIn URL found for {speaker_name}")
        
        # Extract Interview/Article URL
        interview_match = re.search(r'Interview:\s*(https?://[^\s]+)', full_text, re.IGNORECASE)
        if interview_match:
            result["interview_link"] = interview_match.group(1).strip()
            logger.info(f"Found interview link for {speaker_name}: {result['interview_link']}")
        else:
            # Fallback to finding any non-LinkedIn URL
            article_urls = re.findall(r'(https?://(?!(?:www\.)?(?:linkedin\.com|lu\.ma))[^\s\)\]]+)', full_text)
            if article_urls:
                result["interview_link"] = article_urls[0].strip()
                logger.info(f"Found interview link for {speaker_name} via fallback: {result['interview_link']}")
            else:
                logger.warning(f"No interview link found for {speaker_name}")
        
        # Extract background information (everything else)
        background_match = re.search(r'Background:(.*?)(?=LinkedIn:|Interview:|$)', full_text, re.IGNORECASE | re.DOTALL)
        if background_match:
            result["insight"] = background_match.group(1).strip()
        else:
            # If structured format wasn't followed, use the full text as insight
            # but remove the LinkedIn and Interview URLs
            cleaned_text = full_text
            if result["linkedin"]:
                cleaned_text = cleaned_text.replace(result["linkedin"], "")
            if result["interview_link"]:
                cleaned_text = cleaned_text.replace(result["interview_link"], "")
            result["insight"] = re.sub(r'LinkedIn:.*?(?=Interview:|Background:|$)', '', cleaned_text, flags=re.IGNORECASE | re.DOTALL)
            result["insight"] = re.sub(r'Interview:.*?(?=LinkedIn:|Background:|$)', '', result["insight"], flags=re.IGNORECASE | re.DOTALL)
            result["insight"] = re.sub(r'Background:', '', result["insight"], flags=re.IGNORECASE).strip()
        
        logger.info(f"Generated insight for {speaker_name}")
        return result
    except Exception as e:
        logger.error(f"Error generating insight for {speaker_name}: {str(e)}")
        return {"insight": "", "linkedin": "", "interview_link": ""}

def filter_events_and_add_insights():
    """
    Filter events from CSV file and add speaker insights
    """
    logger.info(f"Reading events from {INPUT_FILE}")
    
    # Check if input file exists
    if not os.path.exists(INPUT_FILE):
        logger.error(f"Input file not found: {INPUT_FILE}")
        return
    
    try:
        # Read events from CSV
        events = []
        with open(INPUT_FILE, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                events.append(row)
        
        logger.info(f"Read {len(events)} events from {INPUT_FILE}")
        
        # Filter events and add insights
        filtered_events = []
        for event in events:
            event_name = event.get('event_name', 'Not specified')
            event_date = event.get('event_date', 'Not specified')
            
            # Check if event is in the future
            if is_future_event(event_date):
                # Add speaker insight
                speaker_name = event.get('speaker_name', 'Not specified')
                speaker_company = event.get('speaker_company', 'Not specified')
                speaker_title = event.get('speaker_title', 'Not specified')
                
                # Only get insights if we have a speaker name
                if speaker_name and speaker_name != 'Not specified':
                    insight_data = get_speaker_insight(
                        speaker_name, speaker_company, speaker_title
                    )
                    event['speaker_insight'] = insight_data['insight']
                    event['speaker_linkedin'] = insight_data['linkedin']
                    event['speaker_interview_link'] = insight_data['interview_link']
                else:
                    event['speaker_insight'] = ""
                    event['speaker_linkedin'] = ""
                    event['speaker_interview_link'] = ""
                
                filtered_events.append(event)
                logger.info(f"Keeping future event: {event_name} on {event_date}")
            else:
                logger.info(f"Filtering out past event: {event_name} on {event_date}")
        
        logger.info(f"Filtered to {len(filtered_events)} future events")
        
        # Save filtered events to CSV
        if filtered_events:
            fieldnames = list(filtered_events[0].keys())
            with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(filtered_events)
            
            logger.info(f"Saved {len(filtered_events)} events to {OUTPUT_FILE}")
        else:
            logger.warning("No future events found to save")
    
    except Exception as e:
        logger.error(f"Error filtering events: {str(e)}")

if __name__ == "__main__":
    filter_events_and_add_insights()
