import pytest
import asyncio
from unittest.mock import Mock, patch
from app.services.scraper import ApifyScraper, start_scraping_job

class TestApifyScraper:
    
    @pytest.fixture
    def scraper(self):
        return ApifyScraper()
    
    @patch('app.services.scraper.requests.post')
    async def test_scrape_instagram_account_success(self, mock_post, scraper):
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"data": {"id": "test_run_id"}}
        mock_post.return_value = mock_response
        
        # Test scraping
        result = await scraper.scrape_instagram_account("test_username")
        
        assert result == "test_run_id"
        mock_post.assert_called_once()
    
    @patch('app.services.scraper.requests.post')
    async def test_scrape_instagram_account_failure(self, mock_post, scraper):
        # Mock failed API response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad request"
        mock_post.return_value = mock_response
        
        # Test scraping failure
        with pytest.raises(Exception, match="Failed to start scraping"):
            await scraper.scrape_instagram_account("test_username")
    
    @patch('app.services.scraper.requests.get')
    async def test_get_scraping_results_success(self, mock_get, scraper):
        # Mock successful results
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": "test_data"}
        mock_get.return_value = mock_response
        
        # Test getting results
        result = await scraper.get_scraping_results("test_run_id")
        
        assert result == {"results": "test_data"}
        mock_get.assert_called_once()

    @patch('app.services.queue.add_job')
    def test_start_scraping_job(self, mock_add_job):
        # Mock job creation
        mock_add_job.return_value = "test_job_id"
        
        # Test job start
        result = start_scraping_job("test_username")
        
        assert result == "test_job_id"
        mock_add_job.assert_called_once_with("scrape_instagram", {"username": "test_username"})