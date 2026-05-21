INDIA_TECH_CITIES = {

    "Bangalore": [
        "SaaS",
        "Cloud",
        "Cybersecurity",
        "AI"
    ],

    "Hyderabad": [
        "IT",
        "Cloud",
        "Data Centers"
    ],

    "Pune": [
        "FinTech",
        "Manufacturing",
        "IT"
    ],

    "Mumbai": [
        "Banking",
        "Finance",
        "Insurance"
    ],

    "Delhi": [
        "Government",
        "Enterprise",
        "Telecom"
    ],

    "Chennai": [
        "Manufacturing",
        "Automotive",
        "IT"
    ],

    "Kolkata": [
        "Enterprise",
        "Logistics",
        "Manufacturing"
    ]
}


class IndiaGeoEngine:

    @staticmethod
    def analyze_city(city):

        return {
            "city": city,
            "high_value_sectors":
                INDIA_TECH_CITIES.get(city, [])
        }
