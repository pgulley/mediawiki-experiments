import pywikibot

# Load site configuration from user-config.py
site = pywikibot.Site()

# Log in using stored credentials
site.login()

# Verify connection
print(f"Logged in as: {site.user()} on {site}")

# Example: Fetch and print text from a specific page
page_title = "Main Page"  # Change this to any page name
page = pywikibot.Page(site, page_title)

print(f"Content of {page_title}:")
print(page.text)
