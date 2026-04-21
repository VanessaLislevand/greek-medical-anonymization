from __future__ import annotations

from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET


WORDPROCESSING_NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def paragraphs_to_lines(xml_bytes: bytes) -> list[str]:
    """Extract one text line per Word paragraph from a DOCX XML part."""
    root = ET.fromstring(xml_bytes)
    lines: list[str] = []

    for paragraph in root.findall(".//w:p", WORDPROCESSING_NS):
        runs_text = [
            node.text
            for node in paragraph.findall(".//w:t", WORDPROCESSING_NS)
            if node.text is not None
        ]
        lines.append("".join(runs_text))

    return lines


def extract_docx_parts_lines(docx_path: str | Path) -> list[tuple[str, list[str]]]:
    """Return document, header, and footer lines from a DOCX file."""
    path = Path(docx_path)
    parts_with_lines: list[tuple[str, list[str]]] = []

    with zipfile.ZipFile(path, "r") as archive:
        all_names = set(archive.namelist())
        parts_in_order = (
            ["word/document.xml"]
            + sorted(
                name for name in all_names if name.startswith("word/header") and name.endswith(".xml")
            )
            + sorted(
                name for name in all_names if name.startswith("word/footer") and name.endswith(".xml")
            )
        )

        for part_name in parts_in_order:
            if part_name not in all_names:
                continue
            xml_bytes = archive.read(part_name)
            parts_with_lines.append((part_name, paragraphs_to_lines(xml_bytes)))

    return parts_with_lines


def extract_docx_text(docx_path: str | Path) -> str:
    """Flatten DOCX content into newline-separated text, preserving part order."""
    sections: list[str] = []
    for _, lines in extract_docx_parts_lines(docx_path):
        sections.extend(lines)
    return "\n".join(sections)
