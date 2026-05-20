import logging

def setup_l
<truncated 3650 bytes>
prefix="/scoring",
    tags=["Scoring"]
)

router.include_router(
    crm_router,
    prefix="/crm",
    tags=["CRM"]
)

router.include_router(
    workflows_router,
    prefix="/workflow",
    tags=["Workflow"]
)
