from pywikibot import family

class Family(family.Family):
    """Custom family file for a local MediaWiki instance."""

    name = "mctest"  # This must match the `family` variable in user-config.py
    langs = {
        "en": "bly.angwin:8080",  # Your local wiki hostname and port
    }

    def scriptpath(self, code):
        """Define the script path for the MediaWiki instance."""
        return ""  # Change this if your API is at a different path

    def protocol(self, code):
        """Define protocol (http or https)."""
        return "http"  # Change to "https" if your local wiki supports it
