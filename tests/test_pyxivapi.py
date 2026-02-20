import pytest
from pyxivapi import XIVAPI, CustomError
from pyxivapi.lib.models import SearchResponse

API_TIMEOUT = 10 # seconds

# List/dict validators
def validate_search(result: SearchResponse):
    assert result is not None
    assert isinstance(result.results, list)
    assert result.schema is not None
    
    if result.results:
        first = result.results[0]
        assert isinstance(first.row_id, int)
        assert isinstance(first.score, (int, float))
        assert isinstance(first.sheet, str)
        assert isinstance(first.fields, dict)
        
def validate_item(result: SearchResponse, expected_sheet="Item"):
    assert len(result.results) > 0
    
    for item in result.results:
        assert item.sheet == expected_sheet
        assert isinstance(item.fields, dict)
        
        if "Name" in item.fields:
            assert isinstance(item.fields["Name"], str)
            assert len(item.fields["Name"]) > 0
        if "ID" in item.fields:
            assert isinstance(item.fields["ID"], int)
            assert len(item.fields["ID"]) > 0
        if "LevelItem" in item.fields:
            assert isinstance(item.fields["LevelItem"], int)
            assert item.fields["LevelItem"] >= 0
            
def validate_action(result: SearchResponse):
    assert len(result.results) > 0
    
    for item in result.results:
        assert item.sheet == "Action"
        assert isinstance(item.fields, dict)
        
        if "Name" in item.fields:
            assert isinstance(item.fields["Name"], str)
            assert len(item.fields["Name"]) > 0
        if "ID" in item.fields:
            assert isinstance(item.fields["ID"], int)
            assert len(item.fields["ID"]) > 0

@pytest.fixture
def client():
    return XIVAPI()

# Version endpoint testing   
def test_versions(client: XIVAPI):
    versions = client.versions()
    assert isinstance(versions, list)
    assert len(versions) > 0
    for v in versions:
        assert isinstance(v, str)
        assert len(v) > 0
     
# Asset endpoint testing   
def test_asset_get(client: XIVAPI):
    assets = client.assets()
    result = assets.get({ "path": "ui/icon/051000/051474_hr1.tex", "format": "png" })
    assert isinstance(result, (bytes, bytearray))
    assert len(result) > 0
    
def test_asset_invalid_path(client: XIVAPI):
    assets = client.assets()
    with pytest.raises(CustomError):
        assets.get({ "path": "invalid/path/does/not/exist.tex", "format": "png" })
    
    
def test_asset_map_invalid(client: XIVAPI):
    assets = client.assets()
    with pytest.raises(CustomError):
        assets.map({ "territory": "invalid", "index": "00", "version": "latest", "format": "png" })
    
# Search endpoint testing
def test_search_exact_name(client: XIVAPI):
    result = client.search({ "query": 'Name="Iron War Axe"', "sheets": "Item", "limit": 5 })
    validate_search(result)
    validate_item(result)
    found = next((i for i in result.results if i.fields.get("Name") == "Iron War Axe"), None)
    assert found is not None
    
def test_search_partial_name(client: XIVAPI):
    result = client.search({ "query": 'Name~"sword"', "sheets": "Item", "limit": 5 })
    validate_search(result)
    validate_item(result)
    for item in result.results:
        if "Name" in item.fields:
            assert "sword" in item.fields["Name"].lower()

def test_search_numeric(client: XIVAPI):
    result = client.search({ "query": 'Recast100ms>3000', "sheets": "Action", "limit": 5 })
    validate_search(result)
    validate_action(result)
    for item in result.results:
        if "Recast100ms" in item.fields:
            assert item.fields["Recast100ms"] > 3000

def test_search_invalid_syntax(client: XIVAPI):
    with pytest.raises(CustomError):
        client.search({ "query": "invalid query syntax that should fail", "sheets": "Item", })
        
# Sheet(s) endpoint testing
def test_list_sheets(client: XIVAPI):
    sheets = client.sheets()
    result = sheets.all()
    assert result.sheets
    assert len(result.sheets) > 0
    for s in result.sheets:
        assert isinstance(s.name, str)
        
def test_list_sheet_rows(client: XIVAPI):
    sheets = client.sheets()
    result = sheets.list("Item", { "limit": 5 })
    assert result.rows
    assert len(result.rows) > 0
    for r in result.rows:
        assert isinstance(r.row_id, int)
        assert isinstance(r.fields, dict)
        
def test_get_row_with_fields(client: XIVAPI):
    sheets = client.sheets()
    result = sheets.get("Item", "1", { "fields": "Name", "language": "en" })
    assert result.row_id == 1
    assert result.fields.get("Name") == "Gil"

def test_get_row_with_field_list(client: XIVAPI):
    sheets = client.sheets()
    result = sheets.get("Item", "1", { "fields": ["Name", "LevelItem"], "language": "en" })
    assert result.row_id == 1
    assert "Name" in result.fields
    assert "LevelItem" in result.fields

def test_list_nonexistent_sheet(client: XIVAPI):
    sheets = client.sheets()
    with pytest.raises(CustomError): sheets.list("NonExistentSheetThatDoesNotExist")

# Custom options testing
def test_custom_options():
    client = XIVAPI(language="ja",verbose=True,version="latest")
    result = client.items.get(1, { "fields": "Name" })
    assert result.row_id == 1
    assert result.fields.get("Name") == "ギル"