# Import Flask.
from flask import Flask, render_template, request

# Import the shared database connection.
from database import get_db_connection

# Create the Flask application.
app = Flask(__name__)

# Display all companies on the dashboard.
@app.route("/")
def dashboard():
    connection = get_db_connection()

    companies = connection.execute("""
        SELECT *
        FROM companies
        ORDER BY company_name
    """).fetchall()

    connection.close()

    return render_template(
        "dashboard.html",
        companies=companies
    )

# Display the intelligence profile for one company.
@app.route("/company/<int:company_id>")
def company_detail(company_id):
    connection = get_db_connection()

    company = connection.execute("""
        SELECT *
        FROM companies
        WHERE company_id = ?
    """, (company_id,)).fetchone()

    # Get all contacts for this company.
    contacts = connection.execute("""
        SELECT *
        FROM contacts
        WHERE company_id = ?
        ORDER BY last_name, first_name
    """, (company_id,)).fetchall()

    # Get the detected signals for this company.
    signals = connection.execute("""
        SELECT
            signals.signal_name,
            signals.signal_category,
            company_signals.signal_value,
            company_signals.confidence,
            company_signals.source_url,
            company_signals.date_detected
        FROM company_signals
        JOIN signals
            ON company_signals.signal_id = signals.signal_id
        WHERE company_signals.company_id = ?
        ORDER BY signals.signal_category, signals.signal_name
    """, (company_id,)).fetchall()

    # Get the company's most recent lead score.
    lead_score = connection.execute("""
        SELECT *
        FROM lead_scores
        WHERE company_id = ?
        ORDER BY date_scored DESC, lead_score_id DESC
        LIMIT 1
    """, (company_id,)).fetchone()

    # Get all identified opportunities for this company.
    opportunities = connection.execute("""
        SELECT *
        FROM opportunities
        WHERE company_id = ?
        ORDER BY priority, opportunity_id
    """, (company_id,)).fetchall()

    connection.close()

    return render_template(
        "company_detail.html", 
        company=company,
        contacts=contacts,
        signals=signals,
        lead_score=lead_score,
        opportunities=opportunities
    )

# Display and process the lead search form.
@app.route("/search", methods=["GET", "POST"])
def search():
    search_data = None

    if request.method == "POST":
        industry = request.form.get("industry")
        location = request.form.get("location")
        employee_min = request.form.get("employee_min")
        employee_max = request.form.get("employee_max")

        # Save the search criteria to the database.
        connection = get_db_connection()

        cursor = connection.execute("""
            INSERT INTO searches (
                industry,
                location,
                employee_min,
                employee_max,
                date_run
            )
            VALUES (?, ?, ?, ?, DATE('now'))
        """, (
            industry,
            location,
            employee_min,
            employee_max
        ))

        connection.commit()

        search_id = cursor.lastrowid

        connection.close()

        search_data = {
            "search_id": search_id,
            "industry": industry,
            "location": location,
            "employee_min": employee_min,
            "employee_max": employee_max,
        }

    return render_template("search.html", search_data=search_data)

# Run the application.
if __name__ == "__main__":
    app.run(debug=True)
