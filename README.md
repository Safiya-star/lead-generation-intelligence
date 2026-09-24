# Lead Generation Intelligence System

An in-development business intelligence and lead generation platform designed to discover, evaluate, and prioritize small and mid-sized business prospects.

The system combines external business data, relational data modeling, and business intelligence workflows to move beyond traditional lead lists. Its goal is to identify businesses, evaluate observable signals, prioritize potential leads, and connect identified business needs with relevant technology and automation solutions.

## Project Status

🚧 **Active Development**

The application currently includes a working Flask and SQLite foundation, business discovery through external APIs, data normalization and duplicate prevention, company intelligence profiles, lead search tracking, and database structures for business signals, lead scoring, and opportunity identification.

Automated signal detection, lead score calculation, and opportunity generation are planned development stages and are not yet fully integrated into the application workflow.

## Business Problem

Small and mid-sized businesses often have technology and operational gaps that are difficult to identify through traditional lead-generation methods. A standard prospect list may provide company names and contact information, but it does not explain which businesses may have a need, what that need might be, or which solution could address it.

This project explores a more intelligence-driven approach to lead generation by combining business discovery with observable operational and digital signals.

## Solution Architecture

The system is being developed around a multi-stage intelligence workflow:

**Business Discovery → Data Normalization & Deduplication → Company Intelligence → Signal Detection → Lead Scoring → Opportunity Identification**

### 1. Business Discovery
External APIs are used to discover businesses based on industry and location. Current integrations include Foursquare Places and Geoapify.

### 2. Data Normalization & Deduplication
Discovered business data is converted into a consistent company structure and compared with existing database records before new companies are saved.

### 3. Company Intelligence
Company profiles bring together business information, contacts, detected signals, lead scores, and identified opportunities through a relational database.

### 4. Signal Detection
The data model supports business signals across areas such as digital maturity, lead management, and operations. Automated detection of these signals is a planned development stage.

### 5. Lead Scoring
The database supports numeric lead scores, priority classifications, scoring explanations, model versions, and score history. Automated score calculation is currently under development.

### 6. Opportunity Identification
The system is structured to connect business evidence with potential operational or technology needs and recommended services. Automated opportunity generation is a planned development stage.

## Technology Stack

**Backend**
- Python
- Flask

**Database**
- SQLite
- SQL
- Relational database design

**APIs & Data Sources**
- Foursquare Places API
- Geoapify API
- REST API integration
- JSON data processing

**Frontend**
- HTML
- Jinja2

**Development**
- Git
- GitHub
- Python virtual environments
- Environment variables for API credential management

## Implemented Functionality

### Business Discovery
- Discover businesses by industry and geographic location
- Retrieve business information through the Foursquare Places API
- Use Geoapify for location and geocoding functionality
- Filter irrelevant business categories
- Validate required business data before processing

### Data Processing
- Normalize external business data into a consistent company structure
- Compare discovered businesses with existing database records
- Prevent duplicate company records based on company name and location
- Persist unique discovered businesses to SQLite

### Lead Intelligence Dashboard
- Display stored companies through a Flask web interface
- Access individual company intelligence profiles
- Retrieve associated contacts and business signals
- Display the most recent lead score
- Display identified business opportunities

### Lead Search
- Capture industry, location, and employee-count search criteria
- Store searches with execution dates for future search tracking and analysis

### Relational Data Model
The current database supports:

- Companies
- Contacts
- Business signals
- Company-to-signal relationships
- Lead scores and scoring history
- Business opportunities
- Lead searches
- Search results

## Intelligence Model

The system is designed to evaluate observable business signals rather than treating every discovered company as an equally valuable lead.

Current signal categories include:

**Digital Maturity**
- Online scheduling
- Website chat
- Client portal capabilities

**Lead Management**
- Contact and intake forms
- Phone-first calls to action

**Operational**
- Administrative hiring activity

These signals are designed to eventually contribute to lead scoring and opportunity identification. For example, a business with limited digital intake capabilities may represent an opportunity for CRM development or workflow automation.

The scoring model is structured to maintain a numeric score, priority level, scoring rationale, model version, and scoring date. This creates a foundation for testing and refining scoring logic over time.

## Development Roadmap

### Current Development
- Connect the web search workflow directly to the business discovery engine
- Persist discovered businesses and associate them with individual searches
- Expand business filtering and data-quality rules
- Develop automated signal detection
- Implement rule-based lead score calculation
- Generate opportunity recommendations from detected signals

### Future Development
- Expand external business and market data sources
- Add configurable scoring criteria and weighting
- Track changes in business signals over time
- Develop richer dashboard filtering and lead prioritization
- Add outreach and lead-status workflows
- Explore LLM-assisted analysis of business signals and opportunity reasoning
- Evaluate AI-assisted recommendation generation with traceable supporting evidence

## Project Structure

```text
lead-generation-intelligence/
├── app.py                     # Flask application and web routes
├── business_discovery.py      # Business discovery, API integration, filtering, and deduplication
├── database.py                # Shared database connection
├── create_database.py         # Database creation utility
├── seed_database.py           # Development data seeding
├── requirements.txt           # Python dependencies
├── sql/
│   ├── init_database.sql      # Relational database schema
│   ├── seed_company_signals.sql
│   ├── seed_contacts.sql
│   ├── seed_data.sql
│   ├── seed_lead_scores.sql
│   ├── seed_opportunities.sql
│   ├── seed_signals.sql
│   └── test_queries.sql
└── templates/
    ├── dashboard.html
    ├── company_detail.html
    └── search.html

## Running Locally

1. Clone the repository.

2. Create and activate a Python virtual environment.

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file and provide the required API credentials:

```text
GEOAPIFY_API_KEY=your_api_key
FOURSQUARE_API_KEY=your_api_key
```

5. Initialize and seed the local database:

```bash
python create_database.py
python seed_database.py
```

6. Start the Flask application:

```bash
python app.py
```

7. Open the local Flask address shown in the terminal.

> API credentials, local databases, virtual environments, and other environment-specific files are excluded from version control.

## My Role

I designed and developed this project as an end-to-end business intelligence solution, combining my background in business and financial analysis with hands-on application development.

My work includes requirements definition, solution architecture, relational database design, Python and Flask development, SQL, external API integration, data normalization, duplicate prevention, business-rule design, testing, and iterative development.

The project is also being used to explore how business intelligence, automation, and applied AI can work together to identify higher-value opportunities rather than simply generate larger prospect lists.

## Repository Status

This repository represents an actively developed portfolio project. Features and architecture will continue to evolve as additional intelligence, scoring, automation, and AI capabilities are implemented.
