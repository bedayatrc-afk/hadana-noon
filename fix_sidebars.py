from pathlib import Path

templates_dir = Path(__file__).parent / "accounts" / "templates"

SB_MARKERS = (
    "sb-close",
    "sb-user",
    "sb-section",
    "sb-link",
    "sb-bottom",
    "sb-logout",
    "sb-icon",
    "sb-uname",
    "sb-role",
    "sb-avatar",
    "sb-section-label",
    "sb-head",
    "sb-logo",
)


def is_sidebar_remnant(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    if any(marker in line for marker in SB_MARKERS):
        return True
    if stripped == "</div>":
        return True
    if stripped.startswith("<a href") and "sb-" in line:
        return True
    if stripped.startswith("<button") and "closeSidebar" in line:
        return True
    return False


def cleanup_orphan_sidebar(content: str) -> str:
    include = "{% include 'sidebar.html' %}"
    if include not in content:
        return content

    lines = content.split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        if include in line:
            i += 1
            while i < len(lines) and is_sidebar_remnant(lines[i]):
                i += 1
            continue
        i += 1
    return "\n".join(out)


for html_file in sorted(templates_dir.glob("*.html")):
    original = html_file.read_text(encoding="utf-8")
    if include := "{% include 'sidebar.html' %}" not in original:
        continue
    cleaned = cleanup_orphan_sidebar(original)
    if cleaned != original:
        html_file.write_text(cleaned, encoding="utf-8")
        print(f"FIXED: {html_file.name}")
