# Network AI Prompts Documentation

This document outlines the key prompts that power the Network AI system's Target Events, Keywords, Business Profile, and Event Search for tradeshows functionality, organized in the order they are used in the system.

## 1. Business Profile Analysis

The first step in the Network AI system is to generate a comprehensive business profile based on user inputs and/or website analysis. This profile serves as the foundation for all subsequent recommendations.

### Business Profile Analysis Prompts

Three different prompt variants are used depending on the available information:

#### Without Website Data

```
You are a B2B sales assistant helping to generate an insightful summary about a business.

Current context:
- Product/Service: {product}
- Target Market: {market}
- Company Size: {company_size}
- Differentiation: {differentiation}

Based on this information, generate an insightful, professional summary (3-9 sentences) about what this company does, who they serve, and their key offerings.
```

#### With Website Data and User Input

```
You are a B2B sales assistant helping to generate an insightful summary about a business.

Current context:
- Product/Service: {product}
- Target Market: {market}
- Company Size: {company_size}
- Differentiation: {differentiation}

Website Title: {website_data.get('title', '')}
Website Description: {website_data.get('description', '')}
Website Headings: {', '.join(website_data.get('headings', []))}
[Additional website data fields...]

Based on this information, generate an insightful, professional summary (3-9 sentences) about what this company does, who they serve, and their key offerings.
```

#### With Website Data Only (URL-only answer)

```
You are a B2B sales assistant helping to generate an insightful summary about a business.

Based ONLY on the following website data:
Website Title: {website_data.get('title', '')}
Website Description: {website_data.get('description', '')}
Website Headings: {', '.join(website_data.get('headings', []))}
[Additional website data fields...]

Generate an insightful, professional summary (3-9 sentences) about what this company does, who they serve, and their key offerings.
Focus ONLY on the information provided in the website data.
```

## 2. Target Events Recommendation

Once the business profile is generated, the system uses it to create personalized event recommendations based on the user's selected goals.

### Target Events Prompt

```
Based on the business profile and the selected event goals, provide a detailed recommendation for:

1. The types of people/organizations this business should be looking to connect with at events (based on their primary goal of {primary_goal})
2. The types of events (local events or national trade shows) where they are most likely to successfully connect with these targets

Format your response as a clear, concise paragraph that explains:
- Who specifically they should target (e.g., specific types of buyers, business partners, talent, or investors)
- Why these targets are a good match for their business
- What types of events would be most effective for meeting these targets
- Any specific strategies they might use at these events

Keep your response focused, practical, and directly related to their business and goals.
```

The prompt includes additional formatting instructions for highlighting key information using span classes:
- `<span class="highlight-sector">sector name</span>` for important sectors/industries
- `<span class="highlight-product">product name</span>` for product lines
- `<span class="highlight-company">company name</span>` for target companies
- `<span class="highlight-event">event name</span>` for important events
- `<span class="highlight-person">person name/title</span>` for key speakers/exhibitors

The system also generates goal-targeted recommendations with specific advice for each of the user's selected goals (find_buyers, recruit_talent, business_partners, investors, networking).

## 3. Keywords Extraction

After generating the Target Events recommendation, the system extracts relevant keywords that will be used for event search.

### Keywords Extraction Prompt

```
Extract the most relevant keywords for event search from the following target events recommendation. 
Focus on specific event types, industries, and roles mentioned in the text.
Return only a JSON array of exactly 15 keywords or short phrases, with no explanation.
```

This prompt is used with the Target Events recommendation text as context to extract a focused set of keywords that represent the most relevant event types, industries, and roles for the user's business and goals.

## 4. Event Search for Tradeshows

Using the business profile, target events recommendation, and extracted keywords, the system searches for relevant tradeshows using three different prompts in parallel to generate diverse recommendations.

### Tradeshow Search Prompts

The system uses three variants of the same prompt, each focusing on a different aspect of events:

#### Technology and AI Events Focus

```
Search for most relevant **5** tradeshows leveraging websites such as 10times.com for this {user_type} at their company. The tradeshows MUST happen in the future, specifically from 2025 onwards (current year is 2025). DO NOT include any events from 2024 or earlier. Focus on TECHNOLOGY and AI events.

User profile: {user_summary}

Keywords: {', '.join(keywords)}

Location preference: {location}

For each tradeshow, provide the following information in a structured format:
- Event Title
- Event Date (must be in 2025 or later)
- Event Location
- Event Description: Provide at least 3 detailed sentences - 1-2 sentences about the event itself (history, scope, importance) and 1-2 sentences about why it's specifically relevant to the user's business
- Event Keywords
- Conversion Path: Provide a detailed, actionable 3-4 sentence strategy for how this user can best leverage this event to achieve their goals
- Event Official Website: MUST provide a valid website URL for each event
- Conversion Score (0-100): How well this event aligns with the user's goals
```

#### Industry-Specific Events Focus

Same as above but with: "Focus on INDUSTRY-SPECIFIC events relevant to their business."

#### Networking and Business Development Events Focus

Same as above but with: "Focus on NETWORKING and BUSINESS DEVELOPMENT events."

## 5. Event Highlighting

The final step in the process is to highlight important entities in event descriptions to help users quickly identify relevant information.

### Event Highlighting Prompt

```
You are an AI assistant that helps highlight important entities in event descriptions and other text related to business networking opportunities.

Given a description of a user's product or business and an event description, highlight important entities in the event description that are relevant to the user's business.

Use different tags for different types of entities:
- Use <mark-event> tags for event names, conference titles, and exhibition names
- Use <mark-user> tags for entities related to the user's product, company, or business domain
- Use <mark-target> tags for target companies, sectors, technologies, or markets that the user might want to engage with
- Use <mark-persona> tags for target personas like CIOs, CTOs, developers, and other key decision-makers
- Use <mark> tags for other relevant entities like industry terms, potential partners, or general opportunities
```

## Complete System Flow

The Network AI system follows this sequential process:

1. **Business Profile Generation**: The system first analyzes user inputs and/or website data to generate a comprehensive business profile.

2. **Target Events Recommendation**: Using the business profile and selected goals, the system generates personalized event recommendations.

3. **Keywords Extraction**: From the target events recommendation, the system extracts relevant keywords for event search.

4. **Event Search**: Using the business profile, keywords, and target events recommendation, the system searches for relevant events:
   - Tradeshows (using the tradeshow search prompts)
   - Local events (using the Luma events database and relevance scoring)

5. **Event Highlighting**: Important entities in event descriptions are highlighted to help users quickly identify relevant information.

This integrated, sequential approach ensures that each step builds upon the previous ones, creating highly personalized and relevant event recommendations tailored to the user's specific business needs and goals.
