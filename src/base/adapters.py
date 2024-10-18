import logging
from typing import Optional
from src.utils.helpers import RequestHelper
from src.utils.constants import Config
from src.base.models import ListResponseModel
from src.utils.funchelper import exception_handler_decorator

LOGGER = logging.getLogger(__name__)


class BoxAdapter(RequestHelper):
    
    def __init__(self):
        self.baseUrl = Config.API_BASE_URL
    
    """List collection APIS"""
    @exception_handler_decorator
    def get_list_collections(self):
        """
        function returns the list of collections available for a user.
        Returns:
            dict: with list of collections available.
        """        
        url = self.baseUrl + Config.LIST_COLLECTIONS
        LOGGER.info(f"List collection Url:- {url}")
        return self.request_helper_with_token_refresh('GET',  url)
    
    @exception_handler_decorator
    def get_list_collections_by_id(self, collection_id):
        """
        function returns the collection details with id.
        Args:-
            collection_id: int
        """ 
        if collection_id is None:
            LOGGER.info("Collection id is required, cannot be None")
            return None
        url = self.baseUrl + Config.LIST_COLLECTION_ITEMS.format(Config.VERSION, collection_id)
        LOGGER.info(f"List collection Url:- {url}")
        return self.request_helper_with_token_refresh('GET',  url)
    
    """FILE RELATED APIS"""
    @exception_handler_decorator
    def get_list_files(self, file_id):
        """Get the authenticated user's details"""
        if file_id is None:
            LOGGER.info("File id is required, cannot be None")
            return None
        url = self.baseUrl + Config.FILE_REQUEST.format(Config.VERSION, file_id) #URL not found in box
        LOGGER.info(f"List files Url:- {url}")
        return self.request_helper_with_token_refresh('GET',  url)
    

    @exception_handler_decorator
    def download_file(self, file_id):
        """Get the authenticated user's details"""
        if file_id is None:
            LOGGER.info("File id is required, cannot be None")
            return None
        url = self.baseUrl + Config.DOWNLOAD_FILE.format(Config.VERSION, file_id)
        LOGGER.info(f"Download file content Url:- {url}")
        return self.request_helper_with_token_refresh('GET',  url)