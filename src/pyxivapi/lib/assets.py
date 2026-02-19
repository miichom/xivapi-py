from typing import Dict, Any
from .models import AssetQuery, MapPath, VersionQuery
from ..utils import request, CustomError

class Assets:
    """
    Endpoints for accessing game data on a file-by-file basis. Commonly useful for fetching icons or other textures.
    
    See https://v2.xivapi.com/api/docs#tag/assets
    """
    def get(self, params: AssetQuery) -> bytes:
        """
        Read an asset from the game at the specified path, converting it into a usable format (`GET /asset`).
        
        See: https://v2.xivapi.com/api/docs#tag/assets/get/asset
        """
        if isinstance(params, dict):
            params = AssetQuery(**params)
        data, errors = request(path="/asset", params=params.model_dump(exclude_none=True))
        if errors:
            raise CustomError(errors[0]["message"])
        return data.get("data", data)
    
    def map(self, params: MapPath | VersionQuery | Dict[str, Any]) -> bytes:
        """
        Retrieve the specified map, composing it from split source files if necessary (`GET /asset/map`).

        See: https://v2.xivapi.com/api/docs#tag/assets/get/asset/map/{territory}/{index}
        """
        if isinstance(params, dict):
            # MapPath + VersionQuery + {"format": ...}
            params = {k: v for k, v in params.items()}
        data, errors = request(path="/asset",params=params)
        if errors:
            raise CustomError(errors[0]["message"])
        return data.get("data", data)