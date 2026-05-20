from fastapi import APIRouter

from backend.services.crm_sync import HubspotSync

router = APIRouter()

crm = HubspotSync()

@router.post("/hubspot")
def sync_hubspot(data: dict):

    return crm.sync_contact(data)
