
class Config:
    VERSION="2.0"
    API_BASE_URL = "https://api.box.com"
    OAUTH_PATH = "/oauth2/token"
    LIST_COLLECTIONS=f"/{VERSION}/collections"
    LIST_COLLECTION_ITEMS = "/{0}/collections/{1}/items"
    FILE_REQUEST="/{0}/file_requests/{1}"
    DOWNLOAD_FILE="/{0}/files/{1}/content"