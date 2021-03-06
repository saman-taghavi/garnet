import copy
from typing import Any, Dict, Optional, TypedDict

from .base import BaseStorage
from .typedef import StorageDataT


class _UserStorageMetaData(TypedDict):
    state: Optional[str]
    data: Optional[Dict[Any, Any]]


class DictStorage(BaseStorage[StorageDataT]):
    """
    Python dictionary data structure based state storage.

    Not the most persistent storage, therefore
    not recommended for in-production environments.
    """

    def __init__(self) -> None:
        self._data: Dict[str, _UserStorageMetaData] = {}

    def _make_spot_for_key(self, key: str) -> None:
        if key not in self._data:
            self._data[key] = _UserStorageMetaData(state=None, data=None)

    async def get_state(self, key: str) -> Optional[str]:
        self._make_spot_for_key(key)
        return self._data[key]["state"]

    async def get_data(self, key: str) -> Optional[StorageDataT]:
        self._make_spot_for_key(key=key)
        return copy.deepcopy(self._data[key]["data"])  # type: ignore

    async def update_data(
        self, key: str, data: Optional[StorageDataT] = None
    ) -> None:
        self._make_spot_for_key(key=key)
        self._data[key]["data"].update({} if data is None else data)  # type: ignore

    async def set_state(self, key: str, state: Optional[str] = None) -> None:
        self._make_spot_for_key(key=key)
        self._data[key]["state"] = state

    async def set_data(
        self, key: str, data: Optional[StorageDataT] = None
    ) -> None:
        self._make_spot_for_key(key=key)
        self._data[key]["data"] = copy.deepcopy(data) or {}  # type: ignore

    async def init(self) -> None:
        pass

    async def close(self) -> None:
        self._data.clear()
