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
        base_template = jinja_env.get_template("source_main.j2")
        return f"Source:{self.source_data.id}", base_template.render(source=self.source_data)

    def render_infobox(self):
        
        link = f"https://search.mediacloud.org/sources/{self.source_data.id}"

        datestr = dt.datetime.now().strftime("%I:%M%p on %B %d, %Y")

        source_message_template = jinja_env.get_template("infobox_source.j2")

        source_message = source_message_template.render(
            source=self.source_data, 
            run_date=datestr,
            link=link)

        return f"SourceInfo:{self.source_data.id}", source_message

    def render_collections(self):
        source_collections_template = jinja_env.get_template("collection_list.j2")
        return f"SourceCollections:{self.source_data.id}", source_collections_template.render(collections=self.collections)

    def render_feeds(self):
        pass


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

    #def render_source_templates(self):
    #    for source in self.sources:
    #        yield source.render_template()

    def render_template(self):
        return f"Collection({self.collection_data.name})"
