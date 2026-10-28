#!/usr/bin/env python3
"""Site-wide iPhone nested scroll/overscroll containment.
Preserves standard page scrolling and prevents scrolling into an ancestor
when a page or modal reaches its vertical scroll boundary in supported browsers.
Does NOT claim to control Pinterest's native iOS in-app browser sheet.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
MARKER='id="wfe-mobile-scroll-containment"'
STYLE='''<style id="wfe-mobile-scroll-containment">
/* Preserve natural document scrolling while reducing nested browser scroll chaining. */
html,body { overscroll-behavior-y: contain; overscroll-behavior-x: none; }
dialog[open], [role="dialog"][aria-modal="true"],[data-wfe-scroll-lock="true"] {
  overscroll-behavior-y:contain;
  -webkit-overflow-scrolling:touch;
}
/* Scroll inside a modal, not behind it, with safe mobile viewport sizing. */
dialog[open], [role="dialog"][aria-modal="true"] {
  max-height:min(95dvh,100%);
  overflow-y:auto;
}
</style>'''
paths=sorted(list(ROOT.glob("*.html"))+list((ROOT/"pdfs").glob("*.html"))+list((ROOT/"pinterest-command-center").glob("*.html")))
assert len(paths)>35, f"Expected complete set of live HTML pages, found {len(paths)}"
changed=[]
for p in paths:
 s=p.read_text(encoding="utf-8")
 if MARKER in s:continue
 if "</head>" not in s.lower():continue
 pos=s.lower().find("</head>")
 s=s[:pos]+STYLE+"\n"+s[pos:]
 p.write_text(s,encoding="utf-8")
 changed.append(str(p.relative_to(ROOT)))
print("Mobile scroll containment installed across",len(changed),"pages:",", ".join(changed))
