from directory.directory import Collection
#Just tests rendering out a set of templates for a source, to validate before streaming to the mediawiki

us_national = 34412234
coll: Collection = Collection.from_id(us_national)

for t in coll.iter_sources():
	print(t.render_base_template())
	print(t.render_infobox())
	print(t.render_collections())

	break