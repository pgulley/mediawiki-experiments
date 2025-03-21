from .classes import SourcePayload, CollectionPayload, FeedPayload
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic_settings import BaseSettings
import mediacloud.api as mc_api
import datetime as dt 


import os
template_dir = os.path.join(os.path.dirname(__file__), 'templates')

jinja_env = Environment(
    loader=FileSystemLoader(template_dir),
    autoescape=select_autoescape()
)

class Config(BaseSettings):
    mc_api_token:str|None=None
    #No collections should have more than this many sources
    # so just set it high so we don't have to worry about paging. 
    mc_api_limit:int=10000 

config = Config()


class Feed():
    """
    Issue detection for a single feed
    """

    def __init__(self):
        pass


class Source():
    """
    Issue detection and reporting logic for a single source. 
    """
    
    @classmethod
    def from_id(cls, source_id:int, skip_feeds: bool = True):
        mc_client = mc_api.DirectoryApi(config.mc_api_token)
        source = mc_client.source(source_id)
        return Source(source, skip_feeds=skip_feeds)


    def __init__(self, data: dict, skip_feeds: bool = True):

        self.source_data = SourcePayload(data)

        self.feed_list = self.get_source_feeds()

        self.collections = self.get_source_collections()
        self.source_issues = []

    def __repr__(self):
        return f"Source({self.source_data.name}, {self.source_data.homepage})"


    def get_source_collections(self):
        mc_client = mc_api.DirectoryApi(config.mc_api_token)
        return mc_client.collection_list(source_id=self.source_data.id)["results"]

    def get_source_feeds(self):
        mc_client = mc_api.DirectoryApi(config.mc_api_token)
        feeds = mc_client.feed_list(source_id=self.source_data.id, return_details=True)["results"]
        return [FeedPayload(f) for f in feeds]

    def render_base_page(self):
        base_template = jinja_env.get_template("sources/source_main.j2")
        return f"Source:{self.source_data.id}", base_template.render(source=self.source_data)

    def render_infobox(self):
        
        link = f"https://search.mediacloud.org/sources/{self.source_data.id}"

        datestr = dt.datetime.now().strftime("%I:%M%p on %B %d, %Y")

        source_message_template = jinja_env.get_template("sources/infobox_source.j2")

        source_message = source_message_template.render(
            source=self.source_data, 
            run_date=datestr,
            link=link)

        return f"SourceInfo:{self.source_data.id}", source_message

    def render_collections(self):
        source_collections_template = jinja_env.get_template("sources/source_collections.j2")
        return f"SourceCollections:{self.source_data.id}", source_collections_template.render(collections=self.collections)

    def render_feeds(self):
        feed_template = jinja_env.get_template("sources/source_feeds.j2")
        datestr = dt.datetime.now().strftime("%I:%M%p on %B %d, %Y")

        return f"SourceFeeds:{self.source_data.id}", feed_template.render(feeds=self.feed_list, run_date=datestr)

    def changelog_message(self, message):
        datestr = dt.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        return f"SourceChangelog:{self.source_data.id}", f"* {datestr}: {message} \n"

class Collection():

    @classmethod
    def from_id(cls, collection_id:int):
        mc_client = mc_api.DirectoryApi(config.mc_api_token)
        collection = mc_client.collection(collection_id)
        return Collection(collection)

    def __init__(self, data:dict):        
        self.collection_data = CollectionPayload(data)
        self.mc_client = mc_api.DirectoryApi(config.mc_api_token)
        self._sources_fetched = False 
        self._source_data = None


    def _get_source_data(self):
        if not self._sources_fetched:
            result = self.mc_client.source_list(collection_id=self.collection_data.id, limit=config.mc_api_limit)
            self._source_data = result['results']
            self._sources_fetched = True
        return self._source_data 

    def iter_sources(self):
        for source_data in self._get_source_data():
            yield Source(source_data)


    def render_base_page(self):
        template = jinja_env.get_template("collections/collection_main.j2")
        return f"Collection:{self.collection_data.id}", template.render(collection=self.collection_data)

    def render_infobox(self):
        
        link = f"https://search.mediacloud.org/collections/{self.collection_data.id}"

        datestr = dt.datetime.now().strftime("%I:%M%p on %B %d, %Y")

        template = jinja_env.get_template("collections/infobox_collection.j2")

        return f"CollectionInfo:{self.collection_data.id}", template.render(
            collection=self.collection_data, 
            run_date=datestr,
            link=link)

    def render_sources(self):
        template = jinja_env.get_template("collections/collection_sources.j2")
        #Not sure the right way to lazy load this one, but that's an older paige's problem
        all_sources = [source for source in self.iter_sources()]
        return f"CollectionSources:{self.collection_data.id}", template.render(sources=all_sources)

    def changelog_message(self, message):
        datestr = dt.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        return f"CollectionChangelog:{self.collection_data.id}", f"* {datestr}: {message} \n"
