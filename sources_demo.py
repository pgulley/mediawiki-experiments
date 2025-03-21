import pywikibot
from directory.directory import Collection

"""
	This script method creates (overwriting) all of the pages associated
	with each source in a collection:
		- the Base Page
		- the SourceInfobox
		- the SourceCollections
		- the SourceFeeds
		- the SourceChangelog

	And then also all of the pages associated with a collection:
		- the Base Page
		- the CollectionInfobox
		- the CollectionSources
		- the CollectionChangelog

	These are separated out into distinct pages so that other bot processes down the line can edit one component without needing any
	weird and potentially destructive edits to the base page. 

	Edits to the Infobox, and various lists can happen destructively within their own domain, and the edits will just be passed into the base page
	and the Changelog can be setup to be an 'only append' situation.
	BasePage needs to not be touched by a bot ever after creation, so that human-written changes can be preserved
"""	

#Get the site reference
site = pywikibot.Site()
site.login()

def put_collection_pages(id:int) -> None:
	put_page_text(coll.render_base_page)
	put_page_text(coll.render_infobox)
	put_page_text(coll.render_sources)
	cl_name, cl_message = coll.changelog_message("Iterating")
	update_changelog(cl_name, cl_message)

	for source in coll.iter_sources():
		print(source)
		put_source_pages(source)

def put_source_pages(source):
	put_page_text(source.render_base_page)
	put_page_text(source.render_infobox)
	put_page_text(source.render_collections)
	cl_name, cl_message = source.changelog_message("Iterating")
	update_changelog(cl_name, cl_message)

def put_page_text(render_method):
	page_title, page_text = render_method()
	page = pywikibot.Page(site, page_title)
	if page.exists():
		page.text = page_text 
		page.save(summary="Updating source page via bot")
	else:
		page.text = page_text 
		page.save(summary = "Creating new source page via bot")

def update_changelog(page_title, message):
	page = pywikibot.Page(site, page_title)
	if page.exists():
		page.text += message
		page.save(summary="Updating source page via bot")
	else:
		page.text = message 
		page.save(summary = "Creating new source page via bot")



if __name__ == "__main__":
	us_national = 34412234
	coll: Collection = Collection.from_id(us_national)
	put_collection_pages(coll)
