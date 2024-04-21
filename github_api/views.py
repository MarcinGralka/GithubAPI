import json
import requests
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET

# Define the base URL for searching GitHub repositories
GITHUB_API_URL = 'https://api.github.com/search/repositories'


@require_GET
def search_repositories(request):
    """
    This function handles searching for repositories on GitHub based on a keyword provided in the request.

    It expects a 'keyword' parameter in the GET request and performs the following actions:

    1. Validates the presence of the 'keyword' parameter.
    2. Retrieves the API token (replace with your actual token).
    3. Builds the request parameters with the provided keyword.
    4. Sends a GET request to the GitHub API, optionally including the authorization header if a token is provided.
    5. Parses the JSON response from the API.
    6. Extracts relevant information about repositories and creates a list.
    7. Serializes the data into a JSON string with proper indentation for readability.
    8. Returns a successful HTTP response with the search results (JSON data).
    9. In case of errors (missing keyword, API call failure), returns an appropriate error response with status code.
    """

    keyword = request.GET.get('keyword')

    if not keyword:
        # Return error response if keyword is missing
        return JsonResponse({'error': 'Keyword parameter is required'}, status=400)

    # Replace with your actual GitHub API token for better rate limits and access control
    api_token = 'api_token'

    params = {
        'q': keyword
    }

    # Check if an API token is provided
    if not api_token or api_token == 'api_token':
        # If no token, make a basic request
        response = requests.get(GITHUB_API_URL, params=params)
    else:
        # If token provided, include it in the authorization header
        headers = {
            'Authorization': f'token {api_token}'
        }
        response = requests.get(GITHUB_API_URL, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        repositories = []

        for item in data.get('items', []):
            repository_info = {
                'name': item['name'],
                'owner_login': item['owner']['login'],
                'url': item['html_url']
            }
            repositories.append(repository_info)

        # Prepare JSON data with keyword and search results
        json_data = json.dumps({'keyword': keyword, 'repositories': repositories}, indent=4)

        # Return successful response with JSON data
        return HttpResponse(json_data, content_type='application/json')
    else:
        # Return error response with details from the API call
        return JsonResponse({'error': 'Failed to retrieve data from GitHub API'}, status=response.status_code)
