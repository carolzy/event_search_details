# Network AI Product Feature Description

## Product Overview

https://docs.google.com/document/d/1Z76svNE3VzaoMAWTPzUjmTXfAMYedZCyd0znHcjyw_A/edit?tab=t.0 

## Key Features (for now - Carol is revising)

### 1. Business Profile Analysis

**Description:**
The system intelligently analyzes the user's business profile through a combination of direct user input and website analysis. It generates a comprehensive understanding of the business, including its products/services, target market, unique value proposition, and company size.

**Capabilities:**
- Multi-source business information collection (questionnaire + website analysis)
- Intelligent extraction of business details from company websites
- Synthesis of information into a coherent business profile
- Adaptation to different business types and industries

### 2. Target Events Recommendation

**Description:**
Based on the business profile and the user's selected goals (finding buyers, recruiting talent, meeting business partners, connecting with investors, or general networking), the system generates personalized recommendations for the types of events to attend and the people to connect with.

**Capabilities:**
- Goal-specific event recommendations
- Identification of target personas and organizations
- Strategic advice for maximizing event value
- Highlighting of key information using visual cues
- Customized recommendations for each selected goal

### 3. Keywords Generation

**Description:**
The system automatically extracts relevant keywords from the target events recommendation, focusing on specific event types, industries, and roles that are most relevant to the user's business and goals.

**Capabilities:**
- Extraction of 15 highly relevant keywords or phrases
- Focus on specific event types, industries, and roles
- Automatic generation without user intervention
- Optimization for event search relevance

### 4. Tradeshow Search and Local Events Search 

**Description:**
Using the business profile, extracted keywords, and target events recommendation, the system searches for and identifies the most relevant tradeshows and conferences that align with the user's business needs and goals.

**Capabilities:**
- Parallel search across multiple event categories:
  - Technology and AI events
  - Industry-specific events
  - Networking and business development events
- Comprehensive event details including:
  - Event title, date, and location
  - Detailed event description
  - Relevance to the user's business
  - Official website link
  - Conversion score (0-100)
- Deduplication and ranking of results
- Focus on future events (2025 onwards)

### 5. Event Highlighting

**Description:**
The system intelligently highlights important entities in event descriptions that are relevant to the user's business, making it easier to quickly identify the most valuable information.

**Capabilities:**
- Differentiated highlighting for various entity types:
  - Event names and conference titles
  - User's product and business domain
  - Target companies, sectors, and technologies
  - Target personas and decision-makers
  - Industry terms and potential partners
- Visual distinction of different entity types
- Focus on truly relevant entities (10-12 per description)

### 6. Conversion Path Generation

**Description:**
For each recommended event, the system generates a detailed, actionable strategy for how the user can best leverage the event to achieve their specific goals.

**Capabilities:**
- Personalized conversion strategies
- 3-4 sentence actionable plans
- Goal-specific recommendations
- Practical networking advice

### 6. Conversion Path Generation
Advanced Features:
- Annonoymous Invite / Open Invite
- Event Deep Research/ Auto registration
  
## Target Users

- **Founders and Entrepreneurs**: Looking to connect with potential customers, investors, or business partners
- **Business Development Professionals**: Seeking to identify new partnership opportunities and expand their network
- **Sales Professionals**: Looking to connect with potential customers and clients
- **Investors**: Seeking promising startups and investment opportunities
(maybe: - **Recruiters and HR Professionals**: Searching for events to find qualified talent)

## Value Proposition

https://docs.google.com/document/d/1Z76svNE3VzaoMAWTPzUjmTXfAMYedZCyd0znHcjyw_A/edit?tab=t.0 

## Technical Implementation

The product is implemented as a web application with:

- A Python backend using FastAPI
- Integration with Gemini API for AI-powered analysis and generation
- Website analysis capabilities using Playwright
- Event data sourced from Luma Events and web sources like 10times.com
- A responsive web interface for user interaction

