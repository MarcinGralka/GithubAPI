from django.test import TestCase, Client
from unittest.mock import patch, MagicMock

class GitHubAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('github_api.views.requests.get')
    def test_search_repositories_success(self, mock_get):
        # Simulating a response from the GitHub API
        mock_response = MagicMock()
        mock_response.status_code = 200

        # Define the JSON data that the response will return when
        mock_response.json.return_value = {
            'items': [
                {'name': 'repo1', 'owner': {'login': 'user1'}, 'html_url': 'url1'},
                {'name': 'repo2', 'owner': {'login': 'user2'}, 'html_url': 'url2'}
            ]
        }

        mock_get.return_value = mock_response

        response = self.client.get('/github/search/?keyword=test')

        # Checking the correctness of the response
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content.decode('utf-8'),
            {
                'keyword': 'test',
                'repositories': [
                    {'name': 'repo1', 'owner_login': 'user1', 'url': 'url1'},
                    {'name': 'repo2', 'owner_login': 'user2', 'url': 'url2'}
                ]
            }
        )

    @patch('github_api.views.requests.get')
    def test_search_repositories_missing_keyword(self, mock_get):
        # Calling the view without passing the keyword parameter
        response = self.client.get('/github/search/')

        # Checking the correctness of the response
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content.decode('utf-8'),
            {'error': 'Keyword parameter is required'}
        )

    @patch('github_api.views.requests.get')
    def test_search_repositories_api_failure(self, mock_get):
        # Simulating failure response from the GitHub API
        mock_response = {
            'status_code': 500
        }
        mock_get.return_value = MagicMock(**mock_response)

        # Calling the view with a valid keyword parameter
        response = self.client.get('/github/search/?keyword=test')

        # Checking the correctness of the response
        self.assertEqual(response.status_code, 500)
        self.assertJSONEqual(
            response.content.decode('utf-8'),
            {'error': 'Failed to retrieve data from GitHub API'}
        )

    @patch('github_api.views.requests.get')
    def test_search_repositories_nonexistent_keyword(self, mock_get):
        # Simulating empty response from the GitHub API for a nonexistent keyword
        mock_response = {
            'status_code': 200,
            'json_data': {
                'items': []
            }
        }
        mock_get.return_value = MagicMock(**mock_response)

        # Calling the view with a nonexistent keyword
        response = self.client.get('/github/search/?keyword=nonexistent')

        # Checking the correctness of the response
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content.decode('utf-8'),
            {
                'keyword': 'nonexistent',
                'repositories': []
            }
        )
