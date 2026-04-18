import requests
import json
import numpy as np

class AIHandler:
    def __init__(self, base_url="http://localhost:11434", model="llama3"):
        self.base_url = base_url
        self.model = model

    def set_model(self, model):
        self.model = model

    def _generate(self, prompt, system_prompt="You are a helpful assistant."):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False
        }
        try:
            response = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=30)
            if response.status_code == 200:
                return response.json().get('response', "").strip()
            return f"Error: {response.status_code}"
        except Exception as e:
            return f"AI Connection Error: {str(e)}"

    def summarize_idea(self, title, description):
        prompt = f"Summarize this idea in exactly 3 concise sentences. Title: {title}\nDescription: {description}"
        return self._generate(prompt)

    def suggest_hurdles(self, title, description):
        prompt = f"Suggest 3 potential hurdles for this startup idea. Return only a JSON array of strings. Title: {title}\nDescription: {description}"
        response = self._generate(prompt, system_prompt="You are a startup consultant. Only output JSON.")
        try:
            # Basic cleanup in case LLM adds markdown
            clean = response.strip('`').replace('json', '').strip()
            return json.loads(clean)
        except:
            return [response]

    def rate_feasibility(self, title, description):
        prompt = f"Rate this idea on local feasibility (Effort, Novelty, Market Fit) from 1-10. Return valid JSON: {{'effort': 0, 'novelty': 0, 'market_fit': 0, 'explanation': ''}}. Title: {title}\nDescription: {description}"
        response = self._generate(prompt, system_prompt="You are a VC analyst. Only output JSON.")
        try:
            clean = response.strip('`').replace('json', '').strip()
            return json.loads(clean)
        except:
            return {"error": "Failed to parse feasibility report", "raw": response}

    def expand_idea(self, title, description):
        prompt = f"Based on this idea, suggest 3 'Minimal Deliverables' and 3 'Future Extensions'. Return JSON: {{'deliverables': [], 'extensions': []}}. Title: {title}\nDescription: {description}"
        response = self._generate(prompt, system_prompt="You are a product manager. Only output JSON.")
        try:
            clean = response.strip('`').replace('json', '').strip()
            return json.loads(clean)
        except:
            return {"error": "Failed to expand idea", "raw": response}

    def generate_tags(self, title, description):
        prompt = f"Suggest 5 short tags for this idea. Return a JSON array of strings. Title: {title}\nDescription: {description}"
        response = self._generate(prompt, system_prompt="You are an SEO expert. Only output JSON.")
        try:
            clean = response.strip('`').replace('json', '').strip()
            return json.loads(clean)
        except:
            return []

    def get_embedding(self, text):
        payload = {
            "model": "nomic-embed-text", # Standard embedding model in Ollama
            "prompt": text
        }
        try:
            response = requests.post(f"{self.base_url}/api/embeddings", json=payload, timeout=10)
            if response.status_code == 200:
                return response.json().get('embedding', [])
            return []
        except:
            return []

    @staticmethod
    def cosine_similarity(v1, v2):
        if not v1 or not v2: return 0
        v1 = np.array(v1)
        v2 = np.array(v2)
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
