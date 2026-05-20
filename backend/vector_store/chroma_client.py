import os
import json

class ChromaClient:
    def __init__(self):
        self.use_fallback = True
        self.client = None
        self.collection = None
        
        # Try to import and instantiate chromadb client
        try:
            import chromadb
            from chromadb.config import Settings
            
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db")
            os.makedirs(db_path, exist_ok=True)
            
            self.client = chromadb.PersistentClient(path=db_path)
            self.collection = self.client.get_or_create_collection("premium_leads")
            self.use_fallback = False
            print("[✓] ChromaDB PersistentClient initiated successfully.")
        except Exception:
            # Safe Fallback JSON database file
            self.fallback_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 
                "chroma_db_fallback.json"
            )
            print("[!] chromadb library not present. Switched to JSON-based Vector Store Fallback.")

    def save_embedding(self, lead_id, document, metadata):
        """
        Stores lead profile document and metadata in ChromaDB (or JSON fallback).
        """
        if not self.use_fallback and self.collection:
            try:
                # Add document to collection (ChromaDB automatically generates simple embeddings if not provided)
                self.collection.upsert(
                    ids=[str(lead_id)],
                    documents=[document],
                    metadatas=[metadata]
                )
                return True
            except Exception as e:
                print(f"[!] ChromaDB upsert failed: {str(e)}. Retrying with fallback...")
                
        # Fallback JSON Implementation
        try:
            store = {}
            if os.path.exists(self.fallback_path):
                with open(self.fallback_path, 'r') as f:
                    store = json.load(f)
            
            store[str(lead_id)] = {
                "document": document,
                "metadata": metadata
            }
            
            with open(self.fallback_path, 'w') as f:
                json.dump(store, f, indent=4)
                
            return True
        except Exception as e:
            print(f"[x] Critical: Fallback vector store save failed: {str(e)}")
            return False

    def query_semantic(self, query_text, n_results=5):
        """
        Perform semantic similarity queries on leads dataset.
        """
        if not self.use_fallback and self.collection:
            try:
                results = self.collection.query(
                    query_texts=[query_text],
                    n_results=n_results
                )
                return results
            except Exception as e:
                print(f"[!] ChromaDB query failed: {str(e)}. Falling back to token matching...")
                
        # Simple fallback token matching search
        results = []
        try:
            if os.path.exists(self.fallback_path):
                with open(self.fallback_path, 'r') as f:
                    store = json.load(f)
                
                query_tokens = set(query_text.lower().split())
                for lead_id, data in store.items():
                    doc = data["document"].lower()
                    score = sum(1 for token in query_tokens if token in doc)
                    if score > 0:
                        results.append({
                            "id": lead_id,
                            "document": data["document"],
                            "metadata": data["metadata"],
                            "score": score
                        })
                # Sort by search rank match score
                results = sorted(results, key=lambda x: x["score"], reverse=True)[:n_results]
        except Exception:
            pass
            
        return results
