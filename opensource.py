import requests

# Replace with your GitHub username
USERNAME = "smritidoneria"

# GitHub API headers (optional, add a token if needed)
HEADERS = {
    "Accept": "application/vnd.github.v3+json"
}

def get_contributions(contribution_type):
    """Fetches PRs or Issues created by the user"""
    url = f"https://api.github.com/search/issues?q=author:{USERNAME}+type:{contribution_type}"
    response = requests.get(url, headers=HEADERS).json()

    contributions = {}
    if "items" in response:
        for item in response["items"]:
            repo_name = "/".join(item["repository_url"].split("/")[-2:])
            title = item["title"]
            url = item["html_url"]

            if repo_name not in contributions:
                contributions[repo_name] = []
            
            contributions[repo_name].append(f"- [{title}]({url})")
    
    return contributions

def generate_report():
    """Generates a Markdown report with PRs and Issues"""
    prs = get_contributions("pr")
    issues = get_contributions("issue")

    with open("OpenSourceReport.md", "w") as file:
        file.write("# Open Source Contributions\n\n")

        for repo, pr_list in prs.items():
            file.write(f"## {repo}\n\n### Pull Requests:\n")
            file.write("\n".join(pr_list) + "\n\n")

            if repo in issues:
                file.write("### Issues:\n")
                file.write("\n".join(issues[repo]) + "\n\n")

    print("Report generated: OpenSourceReport.md")

if __name__ == "__main__":
    generate_report()
