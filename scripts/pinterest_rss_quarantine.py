#!/usr/bin/env python3
"""Never allow the retired Pinterest RSS feed to generate unbranded pins."""
from pathlib import Path
from xml.etree import ElementTree as ET

publisher = Path("scripts/pinterest_publisher.py").read_text()
if "ensure(mode=='manual'" not in publisher:
    raise RuntimeError("Pinterest publisher is not locked to MANUAL mode")

feed = Path("pinterest-rss.xml")
tree = ET.parse(feed)
channel = tree.getroot().find("channel")
if channel is None:
    raise RuntimeError("Retired feed missing RSS channel")
items = channel.findall("item")
for item in items:
    channel.remove(item)
if items:
    ET.indent(tree, space="  ")
    tree.write(feed, encoding="utf-8", xml_declaration=True)
    print("REMOVED unsafe RSS items:", len(items))
else:
    print("PASS: Pinterest RSS feed has zero published item entries")
assert len(ET.parse(feed).getroot().find("channel").findall("item")) == 0
