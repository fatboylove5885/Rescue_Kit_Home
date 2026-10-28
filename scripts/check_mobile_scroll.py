#!/usr/bin/env python3
"""Guard against mobile scroll regressions across the HTML website."""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
pages = sorted(root.glob("*.html")) + sorted((root / "pinterest-command-center").glob("*.html"))
assert len(pages) >= 25, "Page audit unexpectedly discovered fewer HTML pages"
problems = []
for page in pages:
    text = page.read_text(encoding="utf-8")
    if 'src="/nav.js?v=2"' not in text:
        problems.append(f"{page.relative_to(root)}: missing cache-busted site-wide Safari scroll script")
    if "content-visibility:auto;contain-intrinsic-size:auto 850px" in text:
        problems.append(f"{page.relative_to(root)}: unstable recipe virtual sizing must not return")
shared = (root / "nav.js").read_text(encoding="utf-8")
if "__wfeScrollIntegrityInstalled" not in shared:
    problems.append("nav.js: missing scroll guard")
if "savedY" not in shared or "aria-modal" not in shared:
    problems.append("nav.js: missing restored-position lock for modal backgrounds")
if problems:
    raise SystemExit("MOBILE SCROLL AUDIT FAILED:\n" + "\n".join(problems))
print(f"PASS: {len(pages)} HTML pages use versioned shared scroll guard; old recipe virtual sizing is absent.")
