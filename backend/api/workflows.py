from fastapi import APIRouter

from backend.services.workflow_engine import WorkflowEngine

router = APIRouter()

workflow = WorkflowEngine()

@router.post("/")
def run_workflow(data: dict):

    return workflow.execute_workflow(data)
