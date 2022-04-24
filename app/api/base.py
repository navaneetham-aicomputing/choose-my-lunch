import re
from typing import Optional

from fastapi import APIRouter


def extract_version(name: str) -> Optional[str]:
    if match := re.search(r'(v\d+(?:_\d+)?)', name):
        return match.groups()[0].replace("_", ".")


def router_factory(name: str) -> APIRouter:
    version = extract_version(name)
    rt = APIRouter(prefix=F"/{version}" if version else "")
    return rt
