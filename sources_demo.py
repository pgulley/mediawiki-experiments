import pywikibot
from directory.directory import Collection

#Get the site reference
site = pywikibot.Site()
site.login()



def put_collection_pages(id:int) -> void:
	coll: Collection = Collection.from_id(us_national)

	for t in coll.iter_sources():
		print(t)

		put_page_text(t.render_base_page)
		put_page_text(t.render_infobox)
		put_page_text(t.render_collections)

def put_page_text(render_method):
	page_title, page_text = render_method()
	page = pywikibot.Page(site, page_title)
	if page.exists():
		page.text = page_text 
		page.save(summary="Updating source page via bot")
	else:
		page.text = page_text 
		page.save(summary = "Creating new source page via bot")

if __name__ == "__main__":
	us_national = 34412234
	put_collection_pages(us_national)