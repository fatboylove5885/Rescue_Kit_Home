#!/usr/bin/env python3
"""Generate photographic Pinterest pin compositions and update our claimed-domain RSS feed.

This uses images already licensed/hosted in the What's For Eats repository. It does not
call an external image generator, copy other creators' images, or publish to Pinterest.
Pinterest decides when connected RSS entries are published (not exact scheduling).
"""
from __future__ import annotations

import datetime as dt
import email.utils
import os
import random
import re
import sys
import textwrap
from pathlib import Path
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://whatsforeats.online/"
MEDIA_NS = "http://search.yahoo.com/mrss/"
ET.register_namespace("media", MEDIA_NS)
TODAY = dt.datetime.now(ZoneInfo("America/Detroit")).date()
# An override is only for reproducible local tests, not required for production.
if os.getenv("PIN_DATE"):
    TODAY = dt.date.fromisoformat(os.environ["PIN_DATE"])
DAY_NAME = TODAY.strftime("%A")
DEST = ROOT / "pinterest-daily-pins" / TODAY.isoformat()
RSS_PATH = ROOT / "pinterest-rss.xml"

CREAM = (250, 246, 235)
FOREST = (25, 66, 47)
RUST = (190, 61, 24)
INK = (45, 38, 32)
WHITE = (255, 255, 255)

# Each page is an existing, verified link in the site repository. Each photo is
# from the same site repository and reasonably aligned with that page's content.
PAGES = [
    ("easy-sheet-pan-dinners.html", "EASY SHEET PAN DINNERS", "Minimal cleanup. Big weeknight flavor.", "recipe-2-sheet-pan.jpg", "sheet-pan-vs-slow-cooker-vs-one-pot-vs-air-fryer-sheet-pan.jpg", "Easy Sheet Pan Dinners for Busy Weeknights", "Easy sheet pan dinners with simple proteins, colorful vegetables, and minimal cleanup for hectic weeknights."),
    ("20-lazy-dinners-for-when-your-brain-has-left-the-building.html", "20 LAZY DINNERS", "For the nights you're DONE cooking.", "blog-1-hero.jpg", "make-ahead-dinners-hero.jpg", "20 Lazy Dinner Ideas for Tired Weeknights", "Low-effort dinner ideas and realistic time-saving shortcuts for evenings when you're exhausted."),
    ("weekly-meal-plan-for-busy-families.html", "7 DAYS OF EASY DINNERS", "Less stress at dinnertime.", "recipe-3-salsa-chicken.jpg", "recipe-1-sweet-potato.jpg", "A Simple Weekly Family Meal Plan", "Find a seven-day family meal plan with easy weeknight dinners and a practical shopping list."),
    ("cheap-family-dinners-cost-per-serving.html", "BUDGET FAMILY DINNERS", "Stretch your grocery money.", "recipe-1-sweet-potato.jpg", "budget-pantry-shelf.jpg", "Budget Family Dinners and Cost-Per-Serving Tips", "Find cheap dinner ideas for families and learn to compare grocery costs per serving."),
    ("slow-cooker-dinners-for-busy-families.html", "SLOW COOKER DINNERS", "Hands-off meals for busy families.", "recipe-3-salsa-chicken.jpg", "sheet-pan-vs-slow-cooker-vs-one-pot-vs-air-fryer-slow-cooker.jpg", "Slow Cooker Dinner Ideas for Busy Families", "Explore practical slow cooker dinners, prep shortcuts and food-safety tips for busy weeknights."),
    ("22-cozy-fall-dinners-that-taste-like-wearing-your-favorite-sweater.html", "COZY FALL DINNERS", "Comfort food for chilly nights.", "make-ahead-night-before.jpg", "sheet-pan-vs-slow-cooker-vs-one-pot-vs-air-fryer-one-pot.jpg", "22 Cozy Fall Dinner Ideas", "Warm up with easy fall dinner ideas including comforting soups, casseroles and family favorites."),
    ("freezer-meals-for-busy-weeknights.html", "FREEZER MEALS", "Cook ahead. Relax later.", "make-ahead-containers-labels.jpg", "make-ahead-dinners-hero.jpg", "Freezer Meal Ideas for Busy Weeknights", "Make-ahead dinner ideas plus practical freezing, labeling and safe thawing tips."),
    ("leftover-chicken-recipes.html", "LEFTOVER CHICKEN IDEAS", "One chicken. More easy dinners.", "visuals/leftover-chicken-hero.jpg", "visuals/leftover-chicken-quesadillas.jpg", "Leftover Chicken Recipes for Easy Dinners", "Turn leftover cooked chicken into quesadillas, taco bowls, soups and other easy second-night dinners."),
    ("picky-eater-dinner-ideas.html", "PICKY EATER DINNERS", "Flexible meals for the whole family.", "final-family-table.jpg", "recipe-1-sweet-potato.jpg", "Picky Eater Dinner Ideas for Families", "Build-your-own family meals and easy dinner ideas to make mealtimes more flexible."),
    ("15-minute-dinners-for-busy-weeknights.html", "15-MINUTE DINNERS", "Quick. Simple. Delicious.", "visuals/15-minute-garlic-butter-shrimp-fajitas.jpg", "visuals/15-minute-honey-garlic-chicken-stir-fry.jpg", "15-Minute Dinner Ideas for Busy Nights", "Explore fast family dinners including shrimp fajitas, chicken stir-fry, pasta and other quick meals."),
    ("18-make-ahead-dinners.html", "MAKE AHEAD DINNERS", "Dinner prep without the rush.", "make-ahead-dinners-hero.jpg", "make-ahead-sunday-cook.jpg", "Make-Ahead Dinners to Simplify Your Week", "Prep dinner ingredients or complete meals ahead to make busy weeknights easier."),
    ("5-ingredient-dinners.html", "5-INGREDIENT DINNERS", "Less shopping. More dinner.", "recipe-1-sweet-potato.jpg", "recipe-3-salsa-chicken.jpg", "Easy Five-Ingredient Dinner Ideas", "Simple five-ingredient dinner ideas that cut grocery stress and help you get dinner done."),
    ("7-night-dinner-plan-for-picky-families.html", "7 EASY DINNER NIGHTS", "Dinner ideas for picky families.", "final-family-table.jpg", "visuals/15-minute-beef-tacos.jpg", "A Seven-Night Dinner Plan for Picky Families", "A flexible, low-stress week of family dinners with familiar ingredients and easy swaps."),
    ("easy-dinner-ideas-no-energy.html", "DINNERS FOR TIRED NIGHTS", "Very little energy required.", "make-ahead-dinners-hero.jpg", "blog-1-hero.jpg", "Easy Dinner Ideas When You Have No Energy", "Realistic low-effort dinner ideas for evenings when you have no time or energy to cook."),
    ("easy-weeknight-dinner-recipes.html", "EASY WEEKNIGHT RECIPES", "Family dinners made easier.", "recipe-2-sheet-pan.jpg", "visuals/15-minute-creamy-chicken-spinach-pasta.jpg", "Easy Weeknight Dinner Recipes", "Practical family dinner ideas featuring simple prep, familiar ingredients and delicious food."),
    ("pantry-staples-list-for-budget-cooking.html", "BUDGET PANTRY STAPLES", "Always have dinner options.", "budget-pantry-shelf.jpg", "recipe-1-sweet-potato.jpg", "Budget Pantry Staples for Easy Dinners", "Build a useful pantry with affordable, flexible staples and quick family dinner combinations."),
    ("20-lazy-dinners-sorted-by-how-tired-you-are.html", "DINNERS BY ENERGY LEVEL", "Choose how much cooking you can do.", "blog-1-hero.jpg", "recipe-3-salsa-chicken.jpg", "Lazy Dinner Ideas for Every Energy Level", "Pick a dinner based on how tired you feel, with practical shortcuts and easy meals."),
    ("sheet-pan-vs-slow-cooker-vs-one-pot-vs-air-fryer.html", "4 EASY DINNER METHODS", "Find the one that fits tonight.", "sheet-pan-vs-slow-cooker-vs-one-pot-vs-air-fryer-hero.jpg", "sheet-pan-vs-slow-cooker-vs-one-pot-vs-air-fryer-air-fryer.jpg", "Sheet Pan vs Slow Cooker vs One Pot vs Air Fryer", "Compare four convenient ways to cook dinner based on effort, cleanup and timing."),
]


def font_path(serif=False, bold=True):
    candidates = (["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", "/usr/share/fonts/truetype/liberation2/LiberationSerif-Bold.ttf"] if serif else ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"])
    for c in candidates:
        if Path(c).exists():
            return c
    raise RuntimeError("Required system font missing")


def get_font(size, serif=False):
    return ImageFont.truetype(font_path(serif=serif), size)


def multiline_fit(draw, words, max_width, max_height, size=104, serif=True, max_lines=3):
    for sz in range(size, 39, -2):
        f = get_font(sz, serif)
        lines=[]; current=""
        for w in words.split():
            attempt=(current+" "+w).strip()
            if draw.textbbox((0,0), attempt, font=f)[2] <= max_width:
                current=attempt
            else:
                if current: lines.append(current)
                current=w
        if current:lines.append(current)
        step=int(sz*1.24)
        if len(lines)<=max_lines and len(lines)*step<=max_height:
            return f,lines,step
    raise ValueError("Could not fit title into available space")


def center_title(draw, title, x, y, width, height, style, max_lines=3):
    f, lines, step=multiline_fit(draw,title,width,height,size=108,serif=True,max_lines=max_lines)
    full_h = step*len(lines)
    top=y+(height-full_h)//2
    for i,line in enumerate(lines):
        ink=RUST if (style==1 and i==len(lines)-1) or (style==0 and i==0) else FOREST
        draw.text((x+width//2,top+i*step+step//2),line,font=f,fill=ink,anchor="mm",stroke_width=0)


def crop_photo(path,size):
    p = ROOT / path
    if not p.is_file():raise FileNotFoundError(f"Site image missing: {p}")
    with Image.open(p) as im:
        photo = ImageOps.exif_transpose(im).convert("RGB")
    return ImageOps.fit(photo,size,method=Image.Resampling.LANCZOS,centering=(0.5,0.5))


def footer(img,draw,button_text="SEE THE EASY RECIPES"):
    draw.rectangle((0,1320,1000,1500),fill=CREAM)
    draw.rounded_rectangle((145,1340,855,1440),radius=50,fill=RUST,outline=WHITE,width=4)
    ff=get_font(32)
    draw.text((500,1388),button_text,font=ff,fill=WHITE,anchor="mm")
    brand=get_font(25)
    draw.text((500,1470),"whatsforeats.online",font=brand,fill=INK,anchor="mm")


def draw_pin(main_photo,second_photo,title,subtitle,style):
    im=Image.new("RGB",(1000,1500),CREAM)
    d=ImageDraw.Draw(im)
    if style==0:
        im.paste(crop_photo(main_photo,(1000,840)),(0,480))
        d.rectangle((0,0,1000,480),fill=CREAM)
        d.text((500,50),"WHAT'S FOR EATS",font=get_font(31),fill=INK,anchor="mm")
        center_title(d,title,42,125,916,285,0)
        d.text((500,430),subtitle,font=get_font(31,serif=True),fill=INK,anchor="mm")
    elif style==1:
        im.paste(crop_photo(main_photo,(1000,540)),(0,0))
        d.rectangle((0,540,1000,790),fill=CREAM)
        d.text((500,574),"WHAT'S FOR EATS",font=get_font(28),fill=INK,anchor="mm")
        center_title(d,title,35,603,930,145,1,max_lines=2)
        im.paste(crop_photo(second_photo,(1000,530)),(0,790))
    else:
        d.rectangle((0,0,1000,442),fill=CREAM)
        d.text((500,56),"WHAT'S FOR EATS",font=get_font(30),fill=INK,anchor="mm")
        center_title(d,title,35,120,930,240,2,max_lines=3)
        d.text((500,408),subtitle,font=get_font(29,serif=True),fill=INK,anchor="mm")
        im.paste(crop_photo(main_photo,(499,878)),(0,442))
        im.paste(crop_photo(second_photo,(499,878)),(501,442))
        d.rectangle((498,442,502,1320),fill=CREAM)
    footer(im,d)
    return im


def load_feed():
    if RSS_PATH.exists():
        tree=ET.parse(RSS_PATH)
        root=tree.getroot()
        channel=root.find("channel")
        if channel is None:raise RuntimeError("RSS channel missing")
        return tree,channel
    root=ET.Element("rss",{"version":"2.0"})
    channel=ET.SubElement(root,"channel")
    ET.SubElement(channel,"title").text="What's For Eats — Dinner Ideas"
    ET.SubElement(channel,"link").text=BASE
    ET.SubElement(channel,"description").text="Easy recipes and weeknight meal plans from What's For Eats."
    ET.SubElement(channel,"language").text="en-us"
    return ET.ElementTree(root),channel


def main():
    tree,channel=load_feed()
    datecode=TODAY.isoformat()
    if any((e.findtext("guid") or "").startswith("wfe-auto-"+datecode) for e in channel.findall("item")):
        print(f"Already generated entries for {datecode}. Skipping to avoid duplicates.")
        return
    # Rotate through the verified page library instead of spamming the same 9 URLs daily.
    # Relative day index keeps creative rotation deterministic on reruns.
    day_idx=(TODAY-dt.date(2026,10,27)).days
    rotation = (day_idx*9) % len(PAGES)
    selected = [PAGES[(rotation+i)%len(PAGES)] for i in range(9)]
    # Before editing feed, validate all source files and destination article paths.
    for slug, title, subtitle, pic_a, pic_b, seo, desc in selected:
        for f in (slug,pic_a,pic_b):
            if not (ROOT/f).is_file():raise FileNotFoundError(f"Missing source: {f}")
    DEST.mkdir(parents=True,exist_ok=True)
    now=dt.datetime.combine(TODAY,dt.time(7,0),ZoneInfo("America/Detroit"))
    pub_date=email.utils.format_datetime(now.astimezone(dt.timezone.utc))
    for i,(slug,title,subtitle,pic_a,pic_b,seo,desc) in enumerate(selected,1):
        day_style=(day_idx+i)%3
        # Rotate original site photographs and multi-photo layouts, avoiding stock graphics.
        photo1,photo2 = (pic_a,pic_b) if day_idx%2==0 else (pic_b,pic_a)
        graphic=draw_pin(photo1,photo2,title,subtitle,day_style)
        safe=re.sub(r"[^a-z0-9]+","-",seo.lower()).strip("-")[:65]
        filename=f"{i:02d}-{safe}.jpg"
        graphic.save(DEST/filename,"JPEG",quality=91,optimize=True,subsampling=0)
        entry=ET.SubElement(channel,"item")
        ET.SubElement(entry,"title").text=seo
        ET.SubElement(entry,"link").text=BASE+slug
        ET.SubElement(entry,"guid",{"isPermaLink":"false"}).text=f"wfe-auto-{datecode}-{i:02d}-{safe}"
        ET.SubElement(entry,"pubDate").text=pub_date
        ET.SubElement(entry,"description").text=desc
        ET.SubElement(entry,f"{{{MEDIA_NS}}}content",{"url":BASE+f"pinterest-daily-pins/{datecode}/{filename}","medium":"image","type":"image/jpeg"})
        print(f"Created {filename} => {slug}")
    # Keep recently published entries long enough to account for Pinterest's polling interval.
    items=channel.findall("item")
    for old in items[:-135]:channel.remove(old)
    # Updating lastBuildDate helps RSS clients detect fresh content, but does not guarantee ingestion.
    built=channel.find("lastBuildDate")
    if built is None:built=ET.SubElement(channel,"lastBuildDate")
    built.text=pub_date
    ET.indent(tree,space="  ")
    tree.write(RSS_PATH,encoding="utf-8",xml_declaration=True)
    print(f"Feed updated: {len(channel.findall('item'))} entries; new images in {DEST}")

if __name__=="__main__":main()
