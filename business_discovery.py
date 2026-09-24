# Import tools for API requests and environment variables.
import os
import requests
from dotenv import load_dotenv

# Import the shared database connection.
from database import get_db_connection

# Load environment variables from the .env file.
load_dotenv()

# Get the Geoapify API key.
GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")

# Get the Foursquare Service API key.
FOURSQUARE_API_KEY = os.getenv("FOURSQUARE_API_KEY")

# Test the Geoapify Places API connection.
def test_geoapify_connection():
    url = "https://api.geoapify.com/v2/places"

    params = {
        "categories": "commercial",
        "filter": "circle:-112.0740,33.4484,5000",
        "limit": 5,
        "apiKey": GEOAPIFY_API_KEY
    }

    response = requests.get(url, params=params)

    print("Status code:", response.status_code)

    data = response.json()

    print("Results returned:", len(data.get("features", [])))

        # Display the returned businesses for inspection.
    for feature in data.get("features", []):
        properties = feature.get("properties", {})

        print(
            properties.get("name"),
            properties.get("address_line2")
        )

# Convert a city and state into latitude and longitude
def geocode_location(city, state):
    url = "https://api.geoapify.com/v1/geocode/search"

    params = {
        "text": f"{city}, {state}",
        "type": "city",
        "filter": "countrycode:us",
        "limit": 1,
        "apiKey": GEOAPIFY_API_KEY
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    features = data.get("features", [])

    if not features:
        return None

    coordinates = features[0]["geometry"]["coordinates"]

    longitude = coordinates[0]
    latitude = coordinates[1]

    return latitude, longitude

# Discover businesses using Foursquare
def discover_businesses(search_criteria):
    industry = search_criteria.get("industry")
    city = search_criteria.get("city")
    state = search_criteria.get("state")

    url = "https://places-api.foursquare.com/places/search"

    headers = {
        "Authorization": f"Bearer {FOURSQUARE_API_KEY}",
        "X-Places-Api-Version": "2025-06-17"
    }

    params = {
        "query": industry,
        "near": f"{city}, {state}",
        "limit": 20
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    response.raise_for_status()

    data = response.json()

    discovered_businesses = []

    for place in data.get("results", []):
        location = place.get("location", {})

        business = {
            "company_name": place.get("name"),
            "website": place.get("website"),
            "phone": place.get("tel"),
            "industry": industry,
            "city": location.get("locality"),
            "state": location.get("region"),
            "categories": [
                category.get("name")
                for category in place.get("categories", [])
            ]
        }
        if (
             is_relevant_business(business)
            and has_required_business_data(business)
        ):
            discovered_businesses.append(business)

    return discovered_businesses

# Normalize discovered business data into our standard company format
def normalize_business(business):
    """
    Convert discovered business data into our standard company format.
    """

    normalized_business = {
        "company_name": business.get("company_name"),
        "website": business.get("website"),
        "phone": business.get("phone"),
        "industry": business.get("industry"),
        "city": business.get("city"),
        "state": business.get("state")
    }

    return normalized_business

# Check whether a discovered business already exists
def is_duplicate_business(business, existing_businesses):
    for existing_business in existing_businesses:
        same_name = (
            business.get("company_name") == existing_business.get("company_name")
        )

        same_city = (
            business.get("city") == existing_business.get("city")
        )

        same_state = (
            business.get("state") == existing_business.get("state")
        )

        if same_name and same_city and same_state:
            return True

    return False

# Filter discovered businesses and keep only unique records
def filter_unique_businesses(discovered_businesses, existing_businesses):
    unique_businesses = []

    for business in discovered_businesses:
        if not is_duplicate_business(business, existing_businesses):
            unique_businesses.append(business)

    return unique_businesses

# Load existing businesses from the database
def get_existing_businesses():
    connection = get_db_connection()

    businesses = connection.execute(
        """
        SELECT company_name, website, phone, industry, city, state
        FROM companies
        """
    ).fetchall()

    connection.close()

    existing_businesses = []

    for business in businesses:
        existing_businesses.append(dict(business))

    return existing_businesses

# Save a discovered business to the database
def save_business(business):
    connection = get_db_connection()

    cursor = connection.execute(
        """
        INSERT INTO companies (
            company_name,
            website,
            phone,
            industry,
            city,
            state,
            source,
            date_discovered
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, DATE('now'))
        """,
        (
            business.get("company_name"),
            business.get("website"),
            business.get("phone"),
            business.get("industry"),
            business.get("city"),
            business.get("state"),
            "Business Discovery"
        )
    )

    connection.commit()

    company_id = cursor.lastrowid

    connection.close()

    return company_id

# Save only businesses that are not already in the database
def save_unique_businesses(discovered_businesses):
    existing_businesses = get_existing_businesses()

    unique_businesses = filter_unique_businesses(
        discovered_businesses,
        existing_businesses
    )

    saved_company_ids = []

    for business in unique_businesses:
        company_id = save_business(business)
        saved_company_ids.append(company_id)

    return saved_company_ids

# Test the Foursquare Places API connection.
def test_foursquare_connection():
    url = "https://places-api.foursquare.com/places/search"

    headers = {
        "Authorization": f"Bearer {FOURSQUARE_API_KEY}",
        "X-Places-Api-Version": "2025-06-17"
    }

    params = {
        "query": "solar",
        "near": "Phoenix, AZ",
        "limit": 20
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    print("Foursquare status code:", response.status_code)

    data = response.json()

    # Inspect business names and Foursquare categories.
    for place in data.get("results", []):
        category_names = []

        for category in place.get("categories", []):
            category_names.append(category.get("name"))

        print(place.get("name"), "->", category_names)

    print("Foursquare results returned:", len(data.get("results", [])))

# Check whether a discovered business is relevant to the requested industry
def is_relevant_business(business):
    categories = business.get("categories", [])

    excluded_categories = {
        "Automotive Repair Shop",
        "Tire Repair Shop",
        "Plaza",
        "Plane",
        "Legal Service"
    }

    for category in categories:
        if category in excluded_categories:
            return False

    return True

# Check whether a discovered business has enough usable data
def has_required_business_data(business):
    if not business.get("company_name"):
        return False

    if not business.get("city"):
        return False

    if not business.get("state"):
        return False

    return True

# test block
if __name__ == "__main__":
    test_criteria = {
        "industry": "Solar",
        "city": "Phoenix",
        "state": "AZ"
    }

    results = discover_businesses(test_criteria)
    print("Discovered businesses:", results)

    # Normalize each discovered business
    normalized_results = []

    for business in results:
        normalized_business = normalize_business(business)
        normalized_results.append(normalized_business)

    # Load existing businesses from the database
    existing_businesses = get_existing_businesses()

    print("Existing businesses:", existing_businesses)

    # Create a business that should not be considered a duplicate
    new_business = {
        "company_name": "Desert Sun Energy",
        "website": "https://desertsun.example.com",
        "phone": "480-555-0199",
        "industry": "Solar",
        "city": "Mesa",
        "state": "AZ"
    }

    # Test duplicate detection
    for business in normalized_results:
        duplicate = is_duplicate_business(business, existing_businesses)
        print(f"{business['company_name']} duplicate: {duplicate}")
        print(normalized_results)

        # Test a non-duplicate business
        duplicate = is_duplicate_business(new_business, existing_businesses)
        print(f"{new_business['company_name']} duplicate: {duplicate}")

    # Filter discovered businesses using the reusable function
    unique_businesses = filter_unique_businesses(
        normalized_results,
        existing_businesses
    )

    # Test the Geoapify API connection.
    test_geoapify_connection()

    # Test the Foursquare API connection.
    test_foursquare_connection()

    print("Unique businesses:", unique_businesses) 
