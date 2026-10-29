import re
from pathlib import Path

templates_dir = Path(__file__).parent / "accounts" / "templates"
skip = {
    "sidebar.html",
    "print_evaluation.html",
    "print_payment.html",
    "receipt.html",
}

script_pattern = re.compile(
    r"<script>\s*function toggleSidebar\(\)\{.*?\}\s*function closeSidebar\(\)\{.*?\}\s*</script>\s*",
    re.DOTALL,
)


def replace_sidebar_block(content: str) -> tuple[str, bool]:
    marker = 'id="sidebar"'
    idx = content.find(marker)
    if idx == -1:
        return content, False

    div_start = content.rfind("<div", 0, idx)
    overlay_idx = content.rfind('<div class="overlay"', 0, div_start)
    if overlay_idx == -1:
        return content, False

    replace_start = overlay_idx
    comment_idx = content.rfind("<!--", 0, overlay_idx)
    if comment_idx != -1 and overlay_idx - comment_idx < 80:
        replace_start = comment_idx

    pos = content.find(">", div_start) + 1
    depth = 1
    while pos < len(content) and depth > 0:
        next_open = content.find("<div", pos)
        next_close = content.find("</div>", pos)
        if next_close == -1:
            return content, False
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            end_pos = pos + 6
            pos = end_pos

    new_content = (
        content[:replace_start]
        + "{% include 'sidebar.html' %}\n\n"
        + content[end_pos:]
    )
    return new_content, True


for html_file in sorted(templates_dir.glob("*.html")):
    if html_file.name in skip:
        continue
    content = html_file.read_text(encoding="utf-8")
    if 'id="sidebar"' in content and "include 'sidebar.html'" in content:
        continue
    if 'id="sidebar"' not in content:
        continue

    original = content
    content, replaced = replace_sidebar_block(content)
    if not replaced:
        print(f"SKIP (no match): {html_file.name}")
        continue

    while True:
        content, n = script_pattern.subn("", content, count=1)
        if n == 0:
            break

    if content != original:
        html_file.write_text(content, encoding="utf-8")
        print(f"UPDATED: {html_file.name}")
    else:
        print(f"NO CHANGE: {html_file.name}")
