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


page_title = "Test Page"
page = pywikibot.Page(site, page_title)

message = "\n* This is a new message added by the bot."

if page.exists():
    print(f"📄 Page '{page_title}' exists. Appending message...")
    page.text += message  # Append message to the existing content
    page.save(summary="Appending a new message via bot")  # Save with an edit summary
    print("Message appended successfully!")
else:
    print(f"📄 Page '{page_title}' does not exist. Creating it...")
    page.text = "== Welcome to this page ==\nThis page was created by the bot.\n" + message
    page.save(summary="Creating a new page via bot")  # Save with an edit summary
    print("Page created successfully!")
