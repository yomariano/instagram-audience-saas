import pytest
from unittest.mock import Mock, patch
from app.services.analyzer import GeminiAnalyzer, analyze_commenter_batch

class TestGeminiAnalyzer:
    
    @pytest.fixture
    def analyzer(self):
        return GeminiAnalyzer()
    
    @patch('app.services.analyzer.requests.get')
    @patch('app.services.analyzer.requests.post')
    async def test_analyze_profile_picture_success(self, mock_post, mock_get, analyzer):
        # Mock image download
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"fake_image_data"
        
        # Mock Gemini API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [{
                "content": {
                    "parts": [{
                        "text": '{"gender": "female", "age_range": "25-34", "account_type": "public", "confidence_score": 85}'
                    }]
                }
            }]
        }
        mock_post.return_value = mock_response
        
        # Test analysis
        result = await analyzer.analyze_profile_picture("https://example.com/image.jpg")
        
        expected = {
            "gender": "female",
            "age_range": "25-34", 
            "account_type": "public",
            "confidence_score": 85
        }
        assert result == expected
    
    @patch('app.services.analyzer.requests.get')
    async def test_analyze_profile_picture_download_failure(self, mock_get, analyzer):
        # Mock failed image download
        mock_get.return_value.status_code = 404
        
        # Test analysis with download failure
        result = await analyzer.analyze_profile_picture("https://example.com/image.jpg")
        
        assert result == {"error": "Could not download image"}
    
    @patch('app.services.analyzer.requests.get')
    @patch('app.services.analyzer.requests.post')
    async def test_analyze_profile_picture_api_failure(self, mock_post, mock_get, analyzer):
        # Mock successful image download
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"fake_image_data"
        
        # Mock Gemini API failure
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "API Error"
        mock_post.return_value = mock_response
        
        # Test API failure
        result = await analyzer.analyze_profile_picture("https://example.com/image.jpg")
        
        assert "error" in result
        assert "API error" in result["error"]

@pytest.mark.asyncio
async def test_analyze_commenter_batch():
    commenters = [
        {"username": "user1", "profile_pic_url": "https://example.com/pic1.jpg"},
        {"username": "user2", "profile_pic_url": "https://example.com/pic2.jpg"},
        {"username": "user3"}  # No profile pic
    ]
    
    with patch.object(GeminiAnalyzer, 'analyze_profile_picture') as mock_analyze:
        mock_analyze.return_value = {"gender": "male", "age_range": "18-24"}
        
        results = await analyze_commenter_batch(commenters)
        
        # Should analyze 2 users (those with profile pics)
        assert len(results) == 2
        assert results[0]["username"] == "user1"
        assert results[1]["username"] == "user2"
        assert mock_analyze.call_count == 2