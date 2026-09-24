INSERT INTO opportunities (
    company_id,
    opportunity_type,
    description,
    recommended_service,
    confidence,
    priority,
    evidence_summary,
    date_identified
)
VALUES
(
    1,
    'Lead Management',
    'Potential opportunity to improve how new client inquiries are captured and followed up.',
    'Custom CRM System',
    'High',
    'High',
    'Phone-first CTA detected, while online scheduling and client portal functionality were not detected.',
    '2026-09-10'
),
(
    1,
    'Client Intake',
    'Potential opportunity to automate portions of the client intake process.',
    'Intake Workflow Automation',
    'Medium',
    'Medium',
    'Contact form exists, but additional interactive intake functionality was not detected.',
    '2026-09-10'
),
(
    2,
    'Lead Management',
    'Potential opportunity to improve lead tracking and sales follow-up.',
    'CRM and Lead Follow-Up System',
    'Medium',
    'Medium',
    'The company has digital intake capabilities, but additional lead management opportunities may exist.',
    '2026-09-10'
);
