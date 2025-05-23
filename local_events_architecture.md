# Local Events Search Architecture

This document outlines the architecture for the local events search functionality in the Network AI system, focusing on how the system processes and presents local events to users.

## Local Events Search Pipeline

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│                     │     │                     │     │                     │
│  User Profile &     │     │  Target Events      │     │  Keywords           │
│  Business Goals     │────►│  Recommendation     │────►│  Extraction         │
│                     │     │                     │     │                     │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
                                                                │
                                                                ▼
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│                     │     │                     │     │                     │
│  Event Display      │◄────│  Event Relevance    │◄────│  Luma Events        │
│  & Highlighting     │     │  Analysis           │     │  Database           │
│                     │     │                     │     │                     │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
```

## Component Descriptions

### 1. User Profile & Business Goals

**Key Components:**
- User input collection through web interface
- Business profile generation
- Goal selection (find buyers, recruit talent, business partners, investors, networking)

**Process:**
1. User provides information about their business and selects their goals
2. System generates a comprehensive business profile
3. Primary goal is identified for targeted recommendations
4. User location preferences are recorded for event filtering

### 2. Target Events Recommendation

**Key Components:**
- Target events prompt template
- Gemini API integration
- Goal-specific recommendation generation

**Process:**
1. System uses the business profile and selected goals to generate personalized event recommendations
2. Recommendations include types of people/organizations to connect with
3. Recommendations include types of events to attend
4. Goal-specific advice is provided for each selected goal
5. Key information is highlighted using specialized span classes

### 3. Keywords Extraction

**Key Components:**
- Keywords extraction prompt
- Gemini API integration for keyword generation
- Fallback extraction mechanism

**Process:**
1. System extracts 15 relevant keywords from the target events recommendation
2. Keywords focus on specific event types, industries, and roles
3. Keywords are formatted as a JSON array
4. Fallback mechanism extracts basic keywords if API fails
5. Keywords are stored for use in event relevance analysis

### 4. Luma Events Database

**Key Components:**
- Pre-scraped Luma events stored in CSV format
- Event data structure with comprehensive fields
- Future event filtering

**Process:**
1. System loads events from the Luma events CSV file
2. Events are structured with fields like title, summary, date, location, URL
3. Speaker information is extracted and structured
4. Events are categorized (trade show vs. local event)
5. Basic conversion paths are generated for each event

### 5. Event Relevance Analysis

**Key Components:**
- Basic relevance calculation based on keyword matching
- Enhanced relevance analysis using Gemini API
- Structured output processing
- Asynchronous processing for performance

**Process:**
1. System calculates basic relevance scores based on keyword matching
2. Enhanced relevance analysis is performed using Gemini API
3. Analysis considers user's business profile, keywords, and goals
4. Results include relevance scores, matching keywords, and conversion paths
5. Events are sorted by relevance score
6. Fallback to basic scoring if enhanced analysis fails

### 6. Event Display & Highlighting

**Key Components:**
- Event highlighting using specialized tags
- UI components for displaying events
- Formatting for display with relevant information

**Process:**
1. System highlights important entities in event descriptions
2. Different entity types use different highlighting tags
3. Events are formatted for display with all relevant information
4. Events are presented sorted by relevance score
5. User can view detailed information for each event

## Implementation Details

### Event Data Structure

Each event in the system contains the following information:
- `event_name`: Title of the event
- `event_summary`: Description of the event
- `event_date`: Date and time of the event
- `event_location`: Location of the event
- `event_url`: URL to the event page
- `speakers`: List of speakers with name, role, company, and LinkedIn profiles
- `is_trade_show`: Boolean indicating if the event is a trade show
- `conversion_path`: Suggested strategy for leveraging the event
- `relevance_score`: Score indicating relevance to the user (0-1)
- `matching_keywords`: Keywords from the user's profile that match the event

### Event Highlighting

The system uses different tags to highlight important entities in event descriptions:
- `<mark-event>`: Event names, conference titles, exhibition names
- `<mark-user>`: Entities related to the user's product, company, or business domain
- `<mark-target>`: Target companies, sectors, technologies, or markets
- `<mark-persona>`: Target personas like CIOs, CTOs, developers, and other key decision-makers
- `<mark>`: Other relevant entities like industry terms, potential partners, or opportunities

### Integration with Tradeshow Search

The local events search complements the tradeshow search by:
1. Focusing on more localized, smaller events from Luma
2. Using the same keywords and business profile for consistency
3. Applying the same relevance scoring methodology
4. Presenting both local events and tradeshows in the same interface
5. Providing a comprehensive view of networking opportunities

## Key Differences from Tradeshow Search

While the local events and tradeshow search share many components, there are important differences:

1. **Data Source**: 
   - Local events: Pre-scraped from Luma Events and stored in CSV
   - Tradeshows: Dynamically generated using Gemini API with 10times.com as a reference

2. **Search Approach**:
   - Local events: Filter existing database and score for relevance
   - Tradeshows: Generate new results based on user profile and keywords

3. **Processing Flow**:
   - Local events: Load → Filter → Score → Display
   - Tradeshows: Generate → Deduplicate → Format → Display

4. **Scope**:
   - Local events: More focused on smaller, local networking opportunities
   - Tradeshows: Larger industry events, conferences, and exhibitions

This architecture enables a comprehensive event search system that provides users with relevant networking opportunities at both local and national/international levels, all personalized to their specific business needs and goals.
