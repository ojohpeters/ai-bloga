import requests
import os
import time
from dotenv import load_dotenv
from typing import Optional, Dict, Any

# --------------------------
# Configuration Management
# --------------------------

class ConfigLoader:
    """Handles environment configuration with validation"""
    
    def __init__(self, env_path: str = '.env'):
        self.env_path = env_path
        self._load_environment()
    
    def _load_environment(self) -> None:
        """Load variables from .env file"""
        if not load_dotenv(self.env_path):
            raise EnvironmentError(f"Could not load .env file from {self.env_path}")
    
    @property
    def api_key(self) -> str:
        """Get validated API key"""
        key = os.getenv("HF_API_KEY")
        if not key:
            raise ValueError("HF_API_KEY not found in environment variables")
        return key
    
    @property
    def api_url(self) -> str:
        """Get validated API endpoint"""
        url = os.getenv("HF_API_URL")
        if not url:
            raise ValueError("HF_API_URL not found in environment variables")
        return url

# --------------------------
# API Communication
# --------------------------
class APIClient:
    """Handles robust API communication with retries"""
    
    def __init__(self, config: ConfigLoader):
        self.config = config
        self.headers = {"Authorization": f"Bearer {self.config.api_key}"}
        self.retry_delay = 10  # Seconds between retries
    
    def post(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send POST request with error handling and retries"""
        try:
            response = requests.post(
                url=self.config.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            # Handle model loading state
            if response.status_code == 503:
                return self._handle_model_loading(response, payload)
                
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise APICommunicationError(f"API request failed: {str(e)}") from e
    
    def _handle_model_loading(self, response, payload) -> Dict[str, Any]:
        """Retry logic for model loading scenario"""
        retry_after = int(response.headers.get("Retry-After", self.retry_delay))
        print(f"Model loading - retrying in {retry_after} seconds...")
        time.sleep(retry_after)
        return self.post(payload)

# --------------------------
# Article Generation
# --------------------------
class NFLArticleGenerator:
    """Generates structured NFL articles with proper formatting"""
    
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.base_payload = {
            "inputs": self._base_prompt(),
            "parameters": {
                "temperature": 0.72,
                "max_new_tokens": 850,
                "top_p": 0.92,
                "repetition_penalty": 1.15,
                "return_full_text": False,
                "do_sample": True
            }
        }
    
    @staticmethod
    def _base_prompt() -> str:
        """Structured prompt template"""
        return """Generate a comprehensive NFL news article with these sections:

## Recent Game Highlights
[Summarize key games from last week with scores and standout moments]

## Player Performances
[Detail top 3 offensive and defensive players with stats]

## Upcoming Matchups
[Preview next week's must-watch games with predictions]

## Expert Analysis
[Include quotes and insights from league analysts]

Use markdown-style headers and bullet points where appropriate:"""
    
    def generate_article(self, custom_prompt: Optional[str] = None) -> str:
        """Generate and format article text"""
        payload = self.base_payload.copy()
        if custom_prompt:
            payload["inputs"] = custom_prompt
        
        try:
            response = self.api_client.post(payload)
            return self._format_response(response)
        except APICommunicationError as e:
            return f"Error generating article: {str(e)}"
    
    def _format_response(self, response: Dict[str, Any]) -> str:
        """Extract and clean generated text"""
        if isinstance(response, list):
            text = response[0].get('generated_text', '')
        elif isinstance(response, dict):
            text = response.get('generated_text', '')
        else:
            text = str(response)
        
        # Post-processing cleanup
        return text.split("## Expert Analysis")[0].strip()

# --------------------------
# Custom Exceptions
# --------------------------
class APICommunicationError(Exception):
    """Specialized exception for API failures"""
    pass

# --------------------------
# Main Execution
# --------------------------
if __name__ == "__main__":
    try:
        # Initialize components
        config = ConfigLoader()
        api_client = APIClient(config)
        generator = NFLArticleGenerator(api_client)
        
        # Generate and display article
        print("🚀 Generating NFL article...\n")
        article = generator.generate_article()
        
        # Format output
        print("\n" + "="*50 + "\n")
        print(article)
        print("\n" + "="*50)
        print("\n✅ Article generated successfully!")
        
    except Exception as e:
        print(f"\n❌ Critical error: {str(e)}")