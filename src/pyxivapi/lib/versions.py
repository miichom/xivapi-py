from .models import VersionsResponse
from ..utils import request, CustomError

class Versions:
    """Raw versions endpoint."""
    def all(self) -> VersionsResponse:
        data, errors = request(path="/version", params={})
        if errors:
            raise CustomError(errors[0]["message"])
        return VersionsResponse(**data)
