import requests

# Function to fetch GitHub user information and repositories using GitHub API

def fetch_github_data(github_url):
    github_user = github_url.strip().split('/')[-1]
    
    # GitHub API endpoint to get the user data
    api_url = f"https://api.github.com/users/{github_user}"

    # Get user details
    response = requests.get(api_url)

    if response.status_code == 200:
        user_data = response.json()
        
        print(f"\nUser Found: {user_data['login']}")
        print("<Loading Information>")

        # Extract user information
        user_info = {
            'Username': user_data.get('login', 'N/A'),
            'Name': user_data.get('name', 'N/A'),
            'Bio': user_data.get('bio', 'No bio available'),
            'Followers': user_data.get('followers', 'N/A'),
            'Following': user_data.get('following', 'N/A'),
            'Public Repos': user_data.get('public_repos', 'N/A'),
            'Avatar': user_data.get('avatar_url', 'N/A'),
            'Blog': user_data.get('blog', 'N/A')
        }

        # Print user information
        print("\n::::: User Information :::::")
        for key, value in user_info.items():
            print(f"{key}: {value}")

        # Now, get repositories of the user
        repos_url = user_data['repos_url']
        repos_response = requests.get(repos_url)
        
        if repos_response.status_code == 200:
            repos_data = repos_response.json()
            print("\n::::: Repositories :::::")
            
            if not repos_data:
                print("<No repositories found>")
            else:
                for repo in repos_data:
                    repo_name = repo['name']
                    repo_desc = repo['description'] if repo['description'] else "No description available"
                    repo_url = repo['html_url']
                    
                    print(f"\n- Project Name (Title): {repo_name}")
                    print(f"  Description: {repo_desc}")
                    print(f"  URL: {repo_url}")
        else:
            print("<Error fetching repositories>")

    else:
        print(f"<User {github_user} not found or error with API call>")

# Ask the user to input the full GitHub profile URL
github_url = input("Input GitHub profile URL: ")
fetch_github_data(github_url)


