# Network AI Architecture - This part only covers Tradeshow Search

This document outlines the high-level architecture of the Network AI system, focusing on how the Target Events, Keywords, Business Profile, and Tradeshow Search components interact.

## System Architecture Pipeline

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│                     │     │                     │     │                     │
│  User Input &       │     │  Business Profile   │     │  Target Events      │
│  Website Analysis   │────►│  Generation         │────►│  Recommendation     │
│                     │     │                     │     │                     │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
                                                                │
                                                                ▼
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│                     │     │                     │     │                     │
│  Event Display      │◄────│  Tradeshow Search   │◄────│  Keywords           │
│  & Highlighting     │     │  (Parallel Queries) │     │  Extraction         │
│                     │     │                     │     │                     │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
```

## Component Descriptions

### 1. User Input & Website Analysis

**Key Components:**
- User questionnaire for business profile information
- Website analyzer (website_analyzer.py) for extracting business information from URLs
- Data collection for user preferences and goals

**Process:**
1. Collect basic information about the user's business through a questionnaire
2. If a website URL is provided, analyze it using Playwright to extract relevant business information
3. Store collected information for use in business profile generation

### 2. Business Profile Generation

**Key Components:**
- Question engine with Gemini API integration
- Business profile generation prompts (3 variants based on available data)

**Process:**
1. Combine user input with website analysis data (if available)
2. Select appropriate prompt based on available data
3. Generate a comprehensive business profile summary using Gemini API
4. Store the business profile for use in target events recommendation

### 3. Target Events Recommendation

**Key Components:**
- Target events prompt template
- Gemini API integration for generating recommendations
- Goal-specific recommendation sections

**Process:**
1. Use the business profile and user's selected goals to generate personalized event recommendations
2. Format recommendations with highlighted key information
3. Include specific advice for each of the user's selected goals
4. Store the recommendation for use in keywords extraction

### 4. Keywords Extraction

**Key Components:**
- Keywords extraction prompt
- Gemini API integration for extracting keywords

**Process:**
1. Extract relevant keywords from the target events recommendation
2. Focus on specific event types, industries, and roles
3. Generate a JSON array of 15 keywords or short phrases
4. Store the keywords for use in tradeshow search

### 5. Tradeshow Search (Parallel Queries)

**Key Components:**
- Three distinct tradeshow search prompts focusing on different aspects:
  - Technology and AI events
  - Industry-specific events
  - Networking and business development events
- Parallel API calls to Gemini
- Result deduplication and processing

**Process:**
1. Make three parallel API calls with different prompts to get diverse results
2. Combine and deduplicate results based on event title and website
3. Format events with structured information (title, date, location, description, etc.)
4. Store the events for display

### 6. Event Display & Highlighting

**Key Components:**
- Event highlighting prompt
- UI components for displaying events
- Highlighting tags for different entity types

**Process:**
1. Highlight important entities in event descriptions using specialized tags
2. Display events with highlighted information in the UI
3. Provide conversion paths and relevance scores for each event

## Data Flow

1. **User Data → Business Profile**: User inputs and website analysis are combined to generate a comprehensive business profile.
2. **Business Profile → Target Events**: The business profile is used to generate personalized target events recommendations.
3. **Target Events → Keywords**: Keywords are extracted from the target events recommendation.
4. **Keywords + Business Profile → Tradeshow Search**: Keywords and business profile are used to search for relevant tradeshows.
5. **Tradeshows → Display**: Tradeshows are processed, highlighted, and displayed to the user.

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python with FastAPI
- **AI Integration**: Gemini API (Google), Claude API (Anthropic)
- **Web Scraping**: Playwright for website analysis
- **Event Data Sources**: Luma Events CSV, 10times.com (via Gemini)

This architecture enables a highly personalized event recommendation system that leverages AI to understand the user's business and goals, and to find the most relevant events for their specific needs.
