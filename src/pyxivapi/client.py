from typing import Any, Dict, Unpack
from .lib.models import (SearchQuery, VersionQuery, RowReaderQuery, SearchResponse, XIVAPIOptions)
from .lib.sheets import Sheet, Sheets
from .lib.assets import Assets
from .lib.versions import Versions
from .utils import request, CustomError
    
class XIVAPI:
    """Python wrapper for the XIVAPI v2 API."""
    def __init__(self, **options: Unpack[XIVAPIOptions]) -> None:
        self.options = XIVAPIOptions(**options)
    
        # Typed endpoints
        self.achievements = Sheet("Achievement", **self.options)
        self.minions = Sheet("Companion", **self.options)
        self.mounts = Sheet("Mount", **self.options)
        self.items = Sheet("Item", **self.options)
        
        # Raw endpoints
        self.assets = lambda: Assets()
        self.sheets = lambda: Sheets(**self.options)
        self.versions = lambda: [v.names[0] for v in Versions().all().versions]
        
    def search(self, params: Dict[str, Any] | SearchQuery | VersionQuery | RowReaderQuery) -> SearchResponse:
        """
        Fetch information about rows matching the provided search query (`GET /search`).
        
        See: https://v2.xivapi.com/api/docs#tag/search/get/search
        """
        if isinstance(params, dict):
            params = SearchQuery(**params)
        data, errors = request(path="/search", params=params.model_dump(exclude_none=True), options=self.options)
        if errors:
            raise CustomError(errors[0]["message"])
        return SearchResponse(**data)
