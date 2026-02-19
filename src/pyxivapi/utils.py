import requests
from urllib.parse import urlencode, urljoin
from typing import Any, Dict, Optional, Tuple

# The endpoint to use, kept at the top for quick changing (if needed)
endpoint = "https://v2.xivapi.com/api/"

class CustomError(Exception):
    def __init__(self, message: str, name: Optional[str] = None):
        super().__init__(message)
        self.name = name or "XIVAPIError"
        self.message = message
        
def request(*, path: str, params: Optional[Dict[str, Any]] = None, options: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, Any], Optional[list]]:
    url = urljoin(endpoint, path.lstrip("/"))
    params = params or {}
    options = options or {}
    
    # Moves the verbose, if provided, to the options dict
    if not options.get("verbose") and "verbose" in params:
        options["verbose"] = bool(params["verbose"])
        params.pop("verbose", None)
        
    # Flattens the dict params
    flattened = { "query": " ", "fields": ",", "transient": "," }
    for key, sep in flattened.items():
        if key in params and isinstance(params[key], list):
            params[key] = sep.join(str(x) for x in params[key])
        
    # Inject language/version defaults
    if "language" not in params and options.get("language"):
        params["language"] = options["language"]
    if "version" not in params and options.get("version"):
        params["version"] = options["version"]
        
    if params:
        url = f"{url}?{urlencode(params)}"
    
    if options.get("verbose"):
        print(f"[XIVAPI] Requesting {url} with params: {params}")
    
    response = requests.get(url)
    
    if options.get("verbose"):
        print(f"[XIVAPI] Response {response.status_code} for {url} with params: {params}")    
    
    if response.ok:
        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            return response.json(), None
        else:
            # Binary data (icons, textures, etc.)
            return { "data": response.content }, None
    
    try:
        error_json = response.json()
    except Exception:
        error_json = { "message": "Unknown error", "code": response.status_code }
        
    return {}, [error_json]