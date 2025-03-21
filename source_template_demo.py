from directory.directory import Collection

def put_collection_pages(id:int) -> None:
	coll: Collection = Collection.from_id(us_national)

	for t in coll.iter_sources():
		print(t)

		put_page_text(t.render_base_page)
		put_page_text(t.render_infobox)
		put_page_text(t.render_collections)
		break

def put_page_text(render_method):
	page_title, page_text = render_method()
	print(page_title)
	print(page_text)

if __name__ == "__main__":
	us_national = 34412234
	put_collection_pages(us_national)