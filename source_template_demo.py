import pywikibot
from directory.directory import Collection

#Get the site reference
site = pywikibot.Site()
site.login()

us_national = 34412234
coll: Collection = Collection.from_id(us_national)

for t in coll.iter_sources():
	print(t.render_base_template())
	print(t.render_infobox())
	print(t.render_collections())

	break