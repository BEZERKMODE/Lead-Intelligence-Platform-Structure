from backend.databases.apollo_provider import ApolloProvider
from backend.intelligence.sector_classifier import SectorClassifier


class IndiaCompanyEngine:

    def discover(
        self,
        city,
        sector
    ):

        apollo = ApolloProvider()

        companies = apollo.search_companies(
            city=city,
            sector=sector,
            country="India"
        )

        enriched = []

        for company in companies:

            detected_sector = SectorClassifier.classify(
                str(company)
            )

            enriched.append({

                "company": company,

                "detected_sector": detected_sector
            })

        return enriched
