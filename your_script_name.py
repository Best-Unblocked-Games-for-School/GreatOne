import os
import google.generativeai as genai
from github import Github

# Retrieve secrets from environment variables
GITHUB_TOKEN = os.getenv("PAT_TOKEN")  # Use the correct name here
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Gemini API Key from secret

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# GitHub API initialization
g = Github(GITHUB_TOKEN)

# Function to format content with headings, subheadings, bullet points, and quotes
def format_content_with_structure(org_name, content):
    paragraphs = content.split("\n\n")
    formatted_content = f"# {org_name}\n\n"  # Use organization name as H1 heading

    if paragraphs:
        # Add the first paragraph as plain text
        formatted_content += f"{paragraphs[0]}\n\n"
        # Add the special line after the first paragraph
        formatted_content += "#### [✅✅🔴🔴👉👉 UNBLOCKED GAMES PLAY HERE ✅✅🔴🔴👉👉](https://topstoryindia.com)\n\n"

    # Add the rest of the content
    for i, paragraph in enumerate(paragraphs[1:], start=1):
        if i == 1:
            formatted_content += f"## {paragraph}\n\n"  # Second paragraph as subheading
        else:
            formatted_content += f"{paragraph}\n\n"


    return formatted_content

# Function to generate content using Google Gemini API
def generate_readme_content(org_name):
    try:
        prompt = (
            f"Write a comprehensive article about '{org_name}'. Make sure you first address with a welcoming tone and try to be conversational like a 14-year-old child. "
            "Highlight its purpose, mission, and what makes it unique. Include headings, subheadings, bullet points, and quotes. Make it engaging and informative, Must be more than 2500 words."
        )
        response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
        return format_content_with_structure(org_name, response.text)
    except Exception as e:
        print(f"Error generating README content for '{org_name}': {e}")
        return None

# Function to check if a README.md file exists in a repository
def readme_exists(repo, path="README.md"):
    try:
        repo.get_contents(path)
        return True
    except:
        return False

# Function to create repository and setup README for organizations
def setup_readme_for_organizations():
    organizations = g.get_user().get_orgs()

    for org in organizations:
        try:
            org_name = org.login
            org_repos = org.get_repos()

            repo_exists = any(repo.name == org_name for repo in org_repos)

            if repo_exists:
                print(f"Repository '{org_name}' already exists.")
                repo = org.get_repo(org_name)
                if readme_exists(repo):
                    print(f"README.md already exists for '{org_name}', skipping.")
                    continue
                else:
                    print(f"Creating README.md for '{org_name}'.")
                    readme_content = generate_readme_content(org_name)
                    if readme_content:
                        repo.create_file("README.md", "Add organization profile README", readme_content)
                        print(f"README.md created for '{org_name}'.")
            else:
                print(f"Repository '{org_name}' does not exist. Creating...")
                repo = org.create_repo(name=org_name)
                print(f"Repository '{org_name}' created.")

                readme_content = generate_readme_content(org_name)
                if readme_content:
                    repo.create_file("README.md", "Add organization profile README", readme_content)
                    print(f"README.md created for '{org_name}'.")

        except Exception as e:
            print(f"Error processing organization '{org_name}': {e}")

if __name__ == "__main__":
    setup_readme_for_organizations()
