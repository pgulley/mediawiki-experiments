from directory.directory import Collection

def put_collection_pages(coll) -> None:
	put_page_text(coll.render_base_page)
	put_page_text(coll.render_infobox)
	put_page_text(coll.render_sources)

	for source in coll.iter_sources():
		print(source)
		put_source_pages(source)
		break


def put_source_pages(source):
	put_page_text(source.render_base_page)
	put_page_text(source.render_infobox)
	put_page_text(source.render_collections)

def put_page_text(render_method):
	page_title, page_text = render_method()
	print("###"*10,)
	print(page_title,)

	print(page_text)

if __name__ == "__main__":
	us_national = 34412234
	coll: Collection = Collection.from_id(us_national)
	put_collection_pages(coll)