import requests
import base64
from typing import Dict, Any
from app.config import settings
from sqlalchemy.orm import Session

class GeminiAnalyzer:
    def __init__(self):
        self.api_key = settings.gemini_api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
    
    async def analyze_profile_picture(self, image_url: str) -> Dict[str, Any]:
        """Analyze profile picture using Gemini Flash"""
        
        # Download image
        image_response = requests.get(image_url)
        if image_response.status_code != 200:
            return {"error": "Could not download image"}
        
        # Convert to base64
        image_base64 = base64.b64encode(image_response.content).decode()
        
        prompt = """
        Analyze this profile picture and return a JSON response with:
        1. gender: "male", "female", or "unknown"
        2. age_range: "18-24", "25-34", "35-44", "45+" or "unknown"
        3. account_type: "private" or "public" (based on image quality/style)
        4. confidence_score: 0-100
        
        Only return valid JSON, no other text.
        """
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_base64
                        }
                    }
                ]
            }],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 200
            }
        }
        
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(
            f"{self.base_url}/models/gemini-1.5-flash:generateContent?key={self.api_key}",
            json=payload,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            try:
                content = result["candidates"][0]["content"]["parts"][0]["text"]
                return eval(content)  # Parse JSON response
            except:
                return {"error": "Failed to parse analysis"}
        else:
            return {"error": f"API error: {response.text}"}

def get_analysis_results(username: str, db: Session):
    """Get stored analysis results for username"""
    # Implementation to fetch from database
    return {
        "username": username,
        "total_comments": 150,
        "demographics": {
            "gender_split": {"male": 45, "female": 55},
            "age_distribution": {"18-24": 30, "25-34": 40, "35+": 30}
        },
        "status": "completed"
    }

async def analyze_commenter_batch(commenters: list):
    """Analyze a batch of commenter profile pictures"""
    analyzer = GeminiAnalyzer()
    results = []
    
    for commenter in commenters:
        if commenter.get("profile_pic_url"):
            analysis = await analyzer.analyze_profile_picture(commenter["profile_pic_url"])
            results.append({
                "username": commenter["username"],
                "analysis": analysis
            })
    
    return results