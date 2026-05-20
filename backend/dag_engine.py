from networkx import DiGraph
from celery import chord, group

class DAGEngine:
    def __init__(self):
        self.dag = DiGraph()
        self._build_default_pipeline()
        
    def _build_default_pipeline(self):
        # Define dependencies (source -> target)
        self.dag.add_edge("enrich_company", "enrich_person")
        self.dag.add_edge("enrich_person", "verify_email")
        self.dag.add_edge("enrich_company", "ai_score")
        self.dag.add_edge("verify_email", "save_vector_embedding")
        self.dag.add_edge("ai_score", "save_vector_embedding")
        
    def execute_pipeline(self, lead_id):
        from backend.tasks import (
            enrich_company, enrich_person, verify_email, 
            ai_score, save_vector_embedding
        )
        import threading
        
        def run_sync():
            try:
                print(f"[DAG Engine] [Sync Background Thread] Starting enrichment pipeline for Lead ID {lead_id}...")
                enrich_company(lead_id)
                enrich_person(lead_id)
                verify_email(lead_id)
                ai_score(lead_id)
                save_vector_embedding(lead_id)
                print(f"[DAG Engine] [Sync Background Thread] Pipeline finished successfully for Lead ID {lead_id}!")
            except Exception as inner_e:
                print(f"[DAG Engine] [Sync Background Thread Error] Pipeline failed for Lead ID {lead_id}: {inner_e}")
                
        # Check if Redis is online on port 6379 to decide on Celery vs Thread
        redis_available = False
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect(("localhost", 6379))
            s.close()
            redis_available = True
        except Exception:
            redis_available = False

        if redis_available:
            try:
                # We manually build the Celery chord for this DAG layout
                pipeline = (
                    enrich_company.s(lead_id) |
                    chord(
                        [
                            (enrich_person.s() | verify_email.s()),
                            ai_score.s()
                        ],
                        save_vector_embedding.s()
                    )
                )
                pipeline.delay()
                print(f"[DAG Engine] Dispatched pipeline asynchronously via Celery (Redis online).")
                return True
            except Exception as e:
                print(f"[DAG Engine] Celery dispatch failed ({e}). Falling back to background thread.")
        
        # Fallback to local background thread (no-docker, no-redis mode)
        print(f"[DAG Engine] Redis is offline. Running DAG pipeline in-process via daemon thread.")
        threading.Thread(target=run_sync, daemon=True).start()
        return True
