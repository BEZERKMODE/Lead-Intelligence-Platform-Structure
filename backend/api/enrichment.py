from fastapi import APIRouter

from backend.services.enrichment_engine import EnrichmentEngine

router 
<truncated 4964 bytes>
 0) > 100:
            score += 20

        if data.get("funding_detected"):
            score += 25

        if data.get("hiring_detected"):
            score += 15

        if data.get("uses_cloud"):
            score += 10

        if data.get("security_stack_detected"):
            score += 20

        if data.get("high_growth"):
            score += 10

        return min(score, 100)
