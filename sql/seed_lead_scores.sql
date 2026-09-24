INSERT INTO lead_scores (
    company_id,
    score,
    priority_level,
    score_reason,
    scoring_model_version,
    date_scored
)
VALUES
(
    1,
    86,
    'High',
    'Limited digital intake capabilities and multiple manual contact signals suggest a strong CRM and workflow automation opportunity.',
    'v1.0',
    '2026-09-10'
),
(
    2,
    68,
    'Medium',
    'Online scheduling and contact intake are already present, but additional lead management and follow-up opportunities may exist.',
    'v1.0',
    '2026-09-10'
);