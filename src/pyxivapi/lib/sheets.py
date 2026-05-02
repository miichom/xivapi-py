from typing_extensions import Optional, Unpack
from .models import (RowReaderQuery, SheetQuery, RowResponse, SheetResponse, ListResponse, SchemaSpecifier, XIVAPIOptions)
from ..utils import request, CustomError

class Sheet:
    """
    Typed wrapper for a single XIVAPI sheet.
    
    See: https://v2.xivapi.com/api/docs#tag/sheets
    """
    def __init__(self, sheet: SchemaSpecifier, **options: Unpack[XIVAPIOptions]) -> None:
        self.type = sheet
        self.options = XIVAPIOptions(**options)
    
    def get(self, row_id: str | int, params: Optional[RowReaderQuery] = None) -> RowResponse:
        """
        Fetch a single row from the sheet (`GET /sheet/{sheet}/{row}`).
        
        See: https://v2.xivapi.com/api/docs#tag/sheets/get/sheet/{sheet}/{row}
        """
        try:
            row_id = str(row_id)
            return Sheets(**self.options).get(self.type, row_id, params or RowReaderQuery())
        except Exception as e:
            raise CustomError(str(e))
        
    def list(self, params: Optional[SheetQuery] = None) -> SheetResponse:
        """
        Fetches multiple rows from the sheet (`GET /sheet/{sheet}`).
        
        See: https://v2.xivapi.com/api/docs#tag/sheets/get/sheet/{sheet}
        """
        try:
            return Sheets(**self.options).list(self.type, params or SheetQuery())
        except Exception as e:
            raise CustomError(str(e))
        
class Sheets:
    """
    Raw endpoints for reading data from XIVAPI sheets.
    
    See: https://v2.xivapi.com/api/docs#tag/sheets
    """
    def __init__(self, **options: Unpack[XIVAPIOptions]) -> None:
        self.options = XIVAPIOptions(**options)
    
    def all(self) -> ListResponse:
        """List all known sheets."""
        data, errors = request(path="/sheet", params={}, options=dict(self.options)) # pyright: ignore[reportUnknownVariableType, reportCallIssue]
        if errors:
            raise CustomError(errors[0]["message"]) # pyright: ignore[reportUnknownArgumentType]
        return ListResponse(**data) # pyright: ignore[reportUnknownArgumentType]
    
    def list(self, sheet: SchemaSpecifier, params: Optional[SheetQuery] = None) -> SheetResponse:
        """Fetch multiple rows from a sheet."""
        params = SheetQuery() if params is None else params
        if isinstance(params, dict):
            params = SheetQuery(**params) # pyright: ignore[reportUnknownArgumentType]
        data, errors = request(path=f"/sheet/{sheet}", params=params.model_dump(exclude_none=True), options=dict(self.options)) # pyright: ignore[reportArgumentType]
        if errors:
            raise CustomError(errors[0]["message"])
        return SheetResponse(**data)
    
    def get(self, sheet: SchemaSpecifier, row: str, params: Optional[RowReaderQuery] = None) -> RowResponse:
        """Fetch a single row from a sheet."""
        params = RowReaderQuery() if params is None else params
        if isinstance(params, dict):
            params = RowReaderQuery(**params) # pyright: ignore[reportUnknownArgumentType]
        data, errors = request(path=f"/sheet/{sheet}/{row}", params=params.model_dump(exclude_none=True), options=dict(self.options)) # pyright: ignore[reportArgumentType, reportOptionalMemberAccess]
        if errors:
            raise CustomError(errors[0]["message"])
        return RowResponse(**data)