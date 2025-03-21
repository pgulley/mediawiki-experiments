import pywikibot
from directory.directory import Collection

#Get the site reference
site = pywikibot.Site()
site.login()



def put_collection_pages(id:int) -> None:
	"""
	This method creates (overwriting) all of the pages associated with each source in a collection:
		- the Base Page
		- the SourceInfobox
		- the SourceCollections
	and eventually
		- the SourceFeeds
		- the SourceChangelog

	These are separated out into distinct pages so that other bot processes down the line can edit one component without needing any
	weird and potentially destructive edits to the base page. 

	Edits to the Infobox, Collections, and Feeds, will all be things that can happen destructively within their own domain
	and the Changelog can be setup to be an 'only append' situation, but the BasePage needs to not be touched by a bot ever,
	so that human-written changes can be preserved
	"""	
	coll: Collection = Collection.from_id(us_national)

	for t in coll.iter_sources():
		print(t)

		put_page_text(t.render_base_page)
		put_page_text(t.render_infobox)
		put_page_text(t.render_collections)

def put_page_text(render_method, append_only=False):
	page_title, page_text = render_method()
	page = pywikibot.Page(site, page_title)
	if page.exists():
		page.text = page_text 
		page.save(summary="Updating source page via bot")
	else:
		if append_only:
			page_text += page_text
		else:
			page.text = page_text 
		page.save(summary = "Creating new source page via bot")



if __name__ == "__main__":
	us_national = 34412234
	put_collection_pages(us_national)