import pywikibot
from directory.directory import Collection

#Get the site reference
site = pywikibot.Site()
site.login()

us_national = 34412234
coll: Collection = Collection.from_id(us_national)

for t in coll.iter_sources():
	print(t.wiki_name())

	page_title = t.wiki_name()

	page = pywikibot.Page(site, page_title)
	if page.exists():
		pass
	else:
		page.text = t.render_infobox()
		page.save(summary="Creating new source page via bot")