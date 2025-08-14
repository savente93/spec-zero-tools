from typing import TypeAlias
from urllib.parse import ParseResult, urlparse
from tomlkit import dumps, loads
import json
from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.version import InvalidVersion, Version
from typing import Dict, Sequence, Tuple, TypedDict
from pathlib import Path
from re import compile

# we won't actually do anything with URLs we just need to detect them
Url: TypeAlias = ParseResult

# slightly modified version of https://packaging.python.org/en/latest/specifications/dependency-specifiers/#names
PEP_PACKAGE_IDENT_RE = compile(r"(?im)^([A-Z0-9][A-Z0-9._-]*(?:\[[A-Z0-9._,-]+\])?)(.*)$")


class SupportSchedule(TypedDict):
    start_date: str
    packages: Dict[str, str]


def parse_version_spec(s: str) -> SpecifierSet:
    if s.strip() == "*":
        # python version numeric components must be non-negative so this is ookay
        # see https://packaging.python.org/en/latest/specifications/version-specifiers/
        return SpecifierSet(">=0")
    try:
        # if we can simply parse it return it
        return SpecifierSet(s)
    except InvalidSpecifier:
        try:
            ver = Version(s)
        except InvalidVersion:
            raise ValueError(f"{s} is not a version or specifyer")

        return SpecifierSet(f">={ver}")


def write_toml(path: Path | str, data: dict):
    with open(path, "w") as file:
        contents = dumps(data)
        file.write(contents)


def read_toml(path: Path | str) -> dict:
    with open(path, "r") as file:
        contents = file.read()
        return loads(contents)


def read_schedule(path: Path | str) -> Sequence[SupportSchedule]:
    with open(path, "r") as file:
        return json.load(file)


def parse_pep_dependency(dep_str: str) -> Tuple[str, SpecifierSet | Url | None]:
    match = PEP_PACKAGE_IDENT_RE.match(dep_str)
    if match is None:
        raise ValueError("Could not find any valid python package identifier")

    match_groups = match.groups()

    pkg = match_groups[0]
    # capture group could be empty
    if len(match_groups) > 1 and match_groups[1]:
        spec_str = match_groups[1]
        if is_url_spec(spec_str):
            spec = urlparse(spec_str.split("@")[1])
        else:
            spec = SpecifierSet(spec_str)
    else:
        spec = None

    return (pkg, spec)


def is_url_spec(str_spec: str) -> bool:
    return str_spec.strip().startswith("@")
