PRAGMA foreign_keys = ON;

CREATE TABLE companies (
    company_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    website TEXT,
    phone TEXT,
    industry TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    employee_count INTEGER,
    company_size TEXT,
    description TEXT,
    source TEXT,
    date_discovered TEXT,
    status TEXT DEFAULT 'New'
);

CREATE TABLE contacts (
    contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    first_name TEXT,
    last_name TEXT,
    job_title TEXT,
    email TEXT,
    phone TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE signals (
    signal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    signal_name TEXT NOT NULL,
    signal_category TEXT NOT NULL,
    description TEXT
);

CREATE TABLE company_signals (
    company_signal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    signal_id INTEGER NOT NULL,
    signal_value TEXT,
    confidence TEXT,
    source_url TEXT,
    date_detected TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id),
    FOREIGN KEY (signal_id) REFERENCES signals(signal_id)
);

CREATE TABLE lead_scores (
    lead_score_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    priority_level TEXT,
    score_reason TEXT,
    scoring_model_version TEXT,
    date_scored TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE opportunities (
    opportunity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    opportunity_type TEXT NOT NULL,
    description TEXT,
    recommended_service TEXT,
    confidence TEXT,
    priority TEXT,
    evidence_summary TEXT,
    date_identified TEXT,
    status TEXT DEFAULT 'Open',
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE searches (
    search_id INTEGER PRIMARY KEY AUTOINCREMENT,
    industry TEXT,
    location TEXT,
    employee_min INTEGER,
    employee_max INTEGER,
    date_run TEXT
);

CREATE TABLE search_results (
    search_result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    search_id INTEGER NOT NULL,
    company_id INTEGER NOT NULL,
    result_rank INTEGER,
    date_found TEXT,
    FOREIGN KEY (search_id) REFERENCES searches(search_id),
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
)
