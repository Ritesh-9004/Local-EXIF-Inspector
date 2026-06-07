from __future__ import annotations
import json
from typing import Any, Dict, List, Tuple


def format_json(data: Dict[str, Any], only: str = "all") -> str:
    output = _select_section(data, only)
    return json.dumps(output, indent=2, ensure_ascii=False)


def format_text(data: Dict[str, Any], only: str = "all") -> str:
    output = _select_section(data, only)
    lines: List[str] = []

    def render(prefix: str, value: Any) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                render(f"{prefix}{key}.", item)
        else:
            lines.append(f"{prefix[:-1]}: {value}")

    render("", output)
    return "\n".join(lines)


def format_table(data: Dict[str, Any], only: str = "all") -> str:
    output = _select_section(data, only)
    rows: List[Tuple[str, str]] = []

    def collect(prefix: str, value: Any) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                collect(f"{prefix}{key}.", item)
        else:
            rows.append((prefix[:-1], str(value)))

    collect("", output)
    if not rows:
        return "(no metadata found)"

    key_width = max(len(key) for key, _ in rows)
    formatted_rows = [f"{key.ljust(key_width)} | {value}" for key, value in rows]
    separator = "-" * (key_width + 3 + max(len(value) for _, value in rows))
    return "\n".join([separator, *formatted_rows, separator])


def format_data(data: Dict[str, Any], style: str = "json", only: str = "all") -> str:
    formatter = {
        "json": format_json,
        "text": format_text,
        "table": format_table,
    }.get(style, format_json)
    return formatter(data, only)


def _select_section(data: Dict[str, Any], only: str) -> Dict[str, Any]:
    if only == "all":
        return data
    return {only: data.get(only, {})}
