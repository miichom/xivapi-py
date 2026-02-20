from pydantic import BaseModel
from typing import Dict, List, Optional, Union, Any, TypedDict, NotRequired
from enum import Enum

class VersionQuery(BaseModel):
    """
    Query parameters accepted by endpoints that interact with versioned game data.
    
    See: https://v2.xivapi.com/api/docs#model/versionquery
    """
    version: Optional[str] = None
    """Game version to utilise for this query."""
    
class SchemaFormat(str, Enum):
    """See: https://v2.xivapi.com/api/docs#model/schemaformat"""
    jpg = "jpg"
    png = "png"
    webp = "webp"
    
class AssetQuery(BaseModel):
    """
    Query parameters accepted by the asset endpoint.
    
    See: https://v2.xivapi.com/api/docs#model/assetquery
    """
    format: SchemaFormat | str
    path: str
    """Game path of the asset to retrieve. E.g. `ui/icon/051000/051474_hr1.tex`"""

    
class ErrorResponse(BaseModel):
    """
    General purpose error response structure.
    
    See: https://v2.xivapi.com/api/docs#model/errorresponse
    """
    code: int
    message: str
    """Description of what went wrong."""

# status code

class MapPath(BaseModel):
    """
    Path segments expected by the asset map endpoint.
    
    See: https://v2.xivapi.com/api/docs#model/mappath
    """
    index: str
    """
    Index of the map within the territory. This invariably takes the form of a two-digit zero-padded number. See Map's Id field for examples of possible combinations of `territory` and `index`.
    E.g. `00`
    """
    territory: str
    """
    Territory of the map to be retrieved. This typically takes the form of 4 characters, `[letter][number][letter][number]`. See Map's Id field for examples of possible combinations of `territory` and `index`.
    E.g. `s1d1`
    """
    
QueryString = Union[str, List[str], Dict[str,str|int|bool], None]
    
class SearchQuery(BaseModel):
    """
    Query paramters accepted by the search endpoint.
    
    See: https://v2.xivapi.com/api/docs#model/searchquery
    """
    cursor: Optional[str] = None
    """Continuation token to retrieve further results from a prior search request. If specified, takes priority over query."""
    limit: Optional[int] = None
    """Maximum number of rows to return. To paginate, provide the cursor token provided in `next` to the `cursor` parameter."""
    query: QueryString = None
    """
    A query string for searching excel data.
    Queries are formed of clauses, which take the basic form of `[specifier][operation][value]`, i.e. `Name="Example"`. Multiple clauses may be specified by seperating them with whitespace, i.e. `Foo=1 Bar=2`.
    
    See: https://v2.xivapi.com/docs/guides/search/#query
    """
    sheets: Optional[str] = None
    """List of excel sheets that the query should be run against. At least one must be specified if not querying a cursor."""

class SchemaLanguage(str, Enum):
    """See: https://v2.xivapi.com/api/docs#model/schemalanguage"""
    none = "none"
    en = "en"
    ja = "ja"
    de = "de"
    fr = "fr"
    chs = "chs"
    cht = "cht"
    kr = "kr"
    
SchemaSpecifier = str
FilterString = Union[str, List[str]]

class RowReaderQuery(BaseModel):
    """
    Query parameters accepted by endpoints that retrieve excel row data.

    See: https://v2.xivapi.com/api/docs#model/rowreaderquery
    """
    fields: Optional[FilterString] = None
    """Comma-separated list of field paths to select."""
    language: Optional[Union[str, SchemaLanguage]] = None
    """Language to read row data with."""
    schema: Optional[SchemaSpecifier] = None # pyright: ignore[reportIncompatibleMethodOverride]
    """Schema specifier for row data."""
    transient: Optional[FilterString] = None
    """Transient row field selection."""
    
class SearchResult(BaseModel):
    """
    Result found by a search query.
    
    See: https://v2.xivapi.com/api/docs#model/searchresult
    """
    fields: dict[str, Any]
    row_id: int
    """ID of this row."""
    score: float
    """
    Relevance score for this entry.
    These values only loosely represent the relevance of an entry to the search query. No guarantee is given that the discrete values, nor resulting sort order, will remain stable.
    """
    sheet: SchemaSpecifier
    """Excel sheet this result was found in."""
    subrow_id: Optional[int] = None
    """Subrow ID of this row, when relevant."""
    transient: Optional[dict[str, Any]] = None
    """Field values for this row's transient row, if any is present, according to the current schema and transient filter."""    
    
class SearchResponse(BaseModel):
    """
    Response structure for the search endpoint.
    
    See: https://v2.xivapi.com/api/docs#model/searchresponse
    """
    results: List[SearchResult]
    schema: SchemaSpecifier # pyright: ignore[reportIncompatibleMethodOverride]
    next: Optional[str] = None
 
class SheetMetadata(BaseModel):
    """
    Metadata about a single sheet.
    
    See: https://v2.xivapi.com/api/docs#model/sheetmetadata
    """
    name: str
    """The name of the sheet."""
    
class ListResponse(BaseModel):
    """
    Response structure for the list endpoint.
    
    See: https://v2.xivapi.com/api/docs#model/listresponse
    """
    sheets: List[SheetMetadata]
    """List of sheets known to the API."""
    
class SheetQuery(BaseModel):
    """
    Query parameters accepted by the sheet endpoint.
    
    See: https://v2.xivapi.com/api/docs#model/sheetquery
    """
    after: Optional[SchemaSpecifier] = None
    """Fetch rows after the specified row. Behavior is undefined if both `rows` and `after` are provided."""
    limit: Optional[int] = None
    """Maximum number of rows to return. To paginate, provide the last returned row to the next request's `after` parameter."""
    rows: Optional[str] = None
    """
    Rows to fetch from the sheet, as a comma-separated list. Behavior is undefined if both `rows` and `after` are provided.
    """
    
class SheetPath(BaseModel):
    """
    Path variables accepted by the sheet endpoint.
    
    See: https://v2.xivapi.com/api/docs#model/sheetpath
    """
    sheet: SchemaSpecifier
    """Name of the sheet to read."""
    
class RowResult(BaseModel):
    """
    Row retrieved by the sheet endpoint.
    
    See: https://v2.xivapi.com/api/docs#model/rowresult
    """
    fields: dict[str, Any]
    row_id: int
    """ID of this row."""
    subrow_id: Optional[int] = None
    """Subrow ID of this row, when relevant."""
    transient: Optional[dict[str, Any]] = None
    """Field values for this row's transient row, if any is present, according to the current schema and transient filter."""
    
class SheetResponse(BaseModel):
    """
    Response structure for the sheet endpoint.
    
    See: https://v2.xivapi.com/api/docs#model/sheetresponse
    """
    rows: List[RowResult]
    """
    List of rows retrieved by the query.
    
    See: https://v2.xivapi.com/api/docs#model/rowresult
    """
    schema: SchemaSpecifier # type: ignore - schema exists on BaseModel
    """The canonical specifier for the schema used in this response."""
    
class RowPath(BaseModel):
    """
    Path variables accepted by the row endpoint.
    
    See: https://v2.xivapi.com/api/docs#model/rowpath
    """
    row: str
    sheet: SchemaSpecifier
    """Name of the sheet to read."""
    
class RowResponse(BaseModel):
    """
    Response structure for the row endpoint.
    
    See: https://v2.xivapi.com/api/docs#model/rowresponse
    """
    fields: dict[str, Any]
    row_id: int
    """ID of this row."""
    schema: SchemaSpecifier # pyright: ignore[reportIncompatibleMethodOverride]
    """The canonical specifier for the schema used in this response."""
    subrow_id: Optional[int] = None
    """Subrow ID of this row, when relevant."""
    transient: Optional[dict[str, Any]] = None
    """Field values for this row's transient row, if any is present, according to the current schema and transient filter."""
    
class VersionMetadata(BaseModel):
    """
    Metadata about a single version supported by the API.
    
    See: https://v2.xivapi.com/api/docs#model/versionmetadata
    """
    names: List[str]
    """Names associated with this version. Version names specified here are accepted by the `version` query parameter throughout the API."""
    
class VersionsResponse(BaseModel):
    """
    Response structure for the versions endpoint.
    
    See: https://v2.xivapi.com/api/docs#model/versionsresponse
    """
    versions: List[VersionMetadata]
    """List of versions available in the API."""
    
class XIVAPIOptions(TypedDict,total=False):
    version: NotRequired[str]
    """
    All API endpoints that serve data derived from game files accept a `version` parameter.
    If omitted, the version `latest` will be used
    
    See: https://v2.xivapi.com/docs/guides/pinning/#game-versions
    """
    language: NotRequired[SchemaLanguage | str]
    """
    Sheets with user-facing strings are commonly localised into all the languages supported by the game client.
    
    See: https://v2.xivapi.com/docs/guides/sheets/#language
    """
    verbose: NotRequired[bool]