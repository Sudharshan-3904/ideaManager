import requests
import json
import numpy as np
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIHandler:
    """
    Interfaces with the local Ollama instance for AI-powered features.
    Provides methods for summarization, suggestion, and semantic embedding.
    """
    def __init__(self, base_url=None, model=None):
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = model or os.getenv("MODEL_NAME", "llama3.2:latest")
        self.provider = os.getenv("MODEL_PROVIDER", "ollama")

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
        """
        Generates potential obstacles for an idea using the AI model.
        """
        prompt = f"Suggest 3 potential hurdles for this startup idea. Return only a JSON array of strings. Title: {title}\nDescription: {description}"
        response = self._generate(prompt, system_prompt="You are a startup consultant. Only output JSON.")
        try:
            # Strip markdown formatting if present
            clean = response.strip('`').replace('json', '').strip()
            return json.loads(clean)
        except (ValueError, json.JSONDecodeError):
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
        """
        Generates a vector embedding for the given text using the 'nomic-embed-text' model.
        """
        payload = {
            "model": "nomic-embed-text", 
            "prompt": text
        }
        try:
            response = requests.post(f"{self.base_url}/api/embeddings", json=payload, timeout=10)
            if response.status_code == 200:
                return response.json().get('embedding', [])
            return []
        except requests.RequestException:
            return []

    def chat(self, messages, system_prompt="You are a helpful startup consultant."):
        """
        Handles a multi-turn conversation using the Ollama chat API.
        """
        url = f"{self.base_url.rstrip('/')}/api/chat"
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": system_prompt}] + messages,
            "stream": False
        }
        print(f"DEBUG: Sending chat request to {url} with model {self.model}")
        try:
            response = requests.post(url, json=payload, timeout=60)
            if response.status_code == 200:
                return response.json().get('message', {}).get('content', "").strip()
            print(f"DEBUG: Chat request failed with status {response.status_code}: {response.text}")
            return f"Error: {response.status_code}"
        except Exception as e:
            print(f"DEBUG: Chat request error: {str(e)}")
            return f"AI Connection Error: {str(e)}"

    @staticmethod
    def cosine_similarity(v1, v2):
        if not v1 or not v2: return 0
        v1 = np.array(v1)
        v2 = np.array(v2)
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
