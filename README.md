# GitHub API Integration

This Django application integrates with the GitHub API to search for repositories based on a keyword provided by the user.

## Setup and Usage

1. Clone the repository:
  git clone https://github.com/MarcinGralka/GithubAPI.git

2. Install the required packages:
  pip install -r packages.txt

3. Run the Django development server:
  python manage.py runserver


4. Open your web browser and go to http://localhost:8000/github/search/?keyword=<keyword> to search for repositories. Replace `<keyword>` with your search term.

## API Endpoint

### Search Repositories
- **URL:** /github/search/
- **Method:** GET
- **Parameters:**
- `keyword`: The keyword to search for repositories
- **Response Format:**
- {
"repositories": 
