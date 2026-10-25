"""Build a crawlable dinner finder from the site's existing recipe collection."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://whatsforeats.online'
LAZY = '/20-lazy-dinners-for-when-your-brain-has-left-the-building.html'
FIVE = '/5-ingredient-dinners.html'
# Times are planning estimates, including waiting; the linked recipe is authoritative.
DINNERS = [
    ('chicken-plate', 'Rotisserie chicken plate', 10, 'minimal', 'chicken', 'No cooking', 'Fully cooked chicken, crunchy vegetables, pita and a dip. Put the parts on separate plates for a flexible family dinner.', LAZY+'#recipe-1', '/assets/dinners/chicken-plate.jpg'),
    ('burrito-bowl', 'Microwave bean & rice bowl', 10, 'minimal', 'beans rice', 'Microwave', 'Rice pouch, canned beans, frozen corn, cheese and salsa. A warm bowl without switching on the stove.', LAZY+'#recipe-2', '/assets/dinners/burrito-bowl.jpg'),
    ('hummus-wraps', 'Hummus veggie wraps', 10, 'minimal', 'beans bread', 'No cooking', 'Hummus, tortillas, bagged vegetables and cheese. Start with the ingredients your household already likes.', LAZY+'#recipe-3', '/assets/dinners/hummus-wraps.jpg'),
    ('snack-board', 'Snack-board dinner', 10, 'minimal', 'bread other', 'No cooking', 'Cheese, crackers, deli meat, fruit and crunchy vegetables. Keep the ingredients separate and let everyone build a plate.', LAZY+'#recipe-5', '/assets/dinners/snack-board.jpg'),
    ('sweet-potatoes', 'Black bean sweet potatoes', 15, 'minimal', 'beans potatoes', 'Microwave', 'Sweet potatoes, black beans, cheese and salsa. Potato size and microwave power change the cooking time.', FIVE+'#five-recipe-1', '/recipe-1-sweet-potato.jpg'),
    ('bean-quesadillas', 'Cheesy bean quesadillas', 20, 'some', 'beans bread', 'One skillet', 'Tortillas, cheese, beans and salsa. Keep a plain cheese portion available if that makes dinner easier.', FIVE+'#five-recipe-7', '/visuals/picky-night-7-quesadillas.svg'),
    ('fried-rice', 'Egg fried rice', 20, 'some', 'eggs rice', 'One skillet', 'Cooked, safely stored rice, eggs and frozen vegetables. Read the recipe for the reheating steps.', FIVE+'#five-recipe-3', '/assets/dinners/fried-rice.jpg'),
    ('tortellini', 'Tortellini with spinach', 20, 'some', 'pasta', 'Stovetop', 'Refrigerated cheese tortellini, jarred sauce and spinach. The package directions help you time the pasta.', LAZY+'#recipe-7', '/assets/dinners/tortellini.jpg'),
    ('white-bean-pasta', 'Tomato & white-bean pasta', 25, 'some', 'beans pasta', 'Stovetop', 'Pasta, marinara, white beans, spinach and Parmesan. Pantry ingredients do most of the work.', FIVE+'#five-recipe-6', '/visuals/fall-pasta-editorial.svg'),
    ('naan-pizza', 'Build-your-own naan pizzas', 25, 'some', 'bread', 'Oven', 'Naan, sauce, mozzarella and your usual toppings. Let each person choose their combination. Allow time to preheat.', LAZY+'#recipe-12', '/assets/dinners/naan-pizza.jpg'),
    ('sausage-tray', 'Sausage & vegetable tray', 45, 'some', 'other potatoes', 'Sheet pan', 'Fully cooked sausage, potatoes and broccoli. Start the potatoes first so everything finishes together.', FIVE+'#five-recipe-4', '/recipe-2-sheet-pan.jpg'),
    ('salsa-chicken', 'Slow-cooker salsa chicken', 420, 'minimal', 'chicken beans', 'Plan ahead', 'Thawed chicken, salsa, seasoning and beans. About 5–10 minutes of prep, then several hours in the cooker.', FIVE+'#five-recipe-5', '/recipe-3-salsa-chicken.jpg'),
]

def build():
    cards = []
    for key, title, minutes, effort, ingredients, method, desc, link, image in DINNERS:
        time = 'Several hours' if minutes > 60 else f'About {minutes} min'
        cards.append(f'''<article class="dinner-card" id="{key}" data-minutes="{minutes}" data-effort="{effort}" data-ingredients="{ingredients}" data-slow="{str(minutes > 60).lower()}">
<img src="{image}" width="600" height="360" alt="" loading="lazy" decoding="async">
<div class="card-body"><div class="dinner-meta"><span>{time}</span><span>{method}</span></div><h3>{escape(title)}</h3><p>{escape(desc)}</p><a href="{link}">Get the {escape(title.lower())} recipe →</a></div></article>''')
    schema = {'@context':'https://schema.org','@graph':[
        {'@type':'CollectionPage','@id':BASE+'/what-to-make-for-dinner.html','url':BASE+'/what-to-make-for-dinner.html','name':'What Should I Make for Dinner? Free Dinner Finder','description':'Find a dinner from 12 existing recipes by time, effort and main ingredient.','isPartOf':{'@type':'WebSite','url':BASE+'/','name':"What's for Eats"}},
        {'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i+1,'name':r[1],'url':BASE+r[7]} for i,r in enumerate(DINNERS)]}
    ]}
    html = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>What Should I Make for Dinner? Free Dinner Finder | What's for Eats</title>
<meta name="description" content="Not sure what to make for dinner? Find an easy meal by time, energy and main ingredient. Browse 12 dinner ideas with links to full recipes. No signup needed.">
<link rel="canonical" href="https://whatsforeats.online/what-to-make-for-dinner.html"><meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website"><meta property="og:title" content="What should I make for dinner? Try the free dinner finder."><meta property="og:description" content="Choose your time, energy and main ingredient. Get an easy dinner idea with the full recipe."><meta property="og:url" content="https://whatsforeats.online/what-to-make-for-dinner.html"><meta property="og:image" content="https://whatsforeats.online/assets/pins/dinner-finder.jpg"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="https://whatsforeats.online/assets/pins/dinner-finder.jpg">
<link rel="stylesheet" href="/assets/dinner-finder.css"><script src="/assets/dinner-finder.js" defer></script>
<script type="application/ld+json">SCHEMA</script></head><body>
<a href="#finder" class="finder-skip">Skip to dinner finder</a>
<nav class="finder-nav" aria-label="Main navigation"><a class="brand" href="/">What's for Eats</a><div><a href="/blogs.html">Dinner guides</a><a href="/free-pdfs.html">Free printables</a><a href="/5-47-rescue-kit.html">Rescue Kit</a></div></nav>
<main class="finder-wrap"><header class="finder-hero"><div><p class="finder-kicker">A little less deciding. A little more dinner.</p><h1>What should I make for dinner?</h1><p class="finder-intro">Start with the time and energy you actually have. Find one doable idea, open the recipe, and get on with your evening.</p><p><strong>12 dinner ideas · Free to use · No signup</strong></p><div class="finder-share"><button id="share-finder" type="button">Share this dinner finder</button><a href="/free-pdfs.html">Browse the free printables</a><output id="share-status" aria-live="polite"></output></div></div><figure><img src="/assets/pins/dinner-finder.jpg" alt="What's for dinner? Free dinner finder from What's for Eats" width="1024" height="1536" fetchpriority="high"><figcaption class="finder-note">AI-created serving illustration.</figcaption></figure></header>
<section id="finder" aria-label="Find a dinner"><form class="finder-panel" id="dinner-filters"><div class="finder-filters">
<label for="filter-time">When do you want to eat?<select id="filter-time" name="time"><option value="any">Show every option</option><option value="10">In about 10 minutes</option><option value="20">Within about 20 minutes</option><option value="45">Within about 45 minutes</option><option value="slow">Later — slow cooker is fine</option></select></label>
<label for="filter-effort">How much effort feels doable?<select id="filter-effort" name="effort"><option value="any">Any effort level</option><option value="minimal">Minimal prep or assembly</option><option value="some">Some cooking is okay</option></select></label>
<label for="filter-ingredient">What can you start with?<select id="filter-ingredient" name="ingredient"><option value="any">Any main ingredient</option><option value="beans">Beans or hummus</option><option value="chicken">Chicken</option><option value="eggs">Eggs</option><option value="pasta">Pasta</option><option value="rice">Rice</option><option value="potatoes">Potatoes</option><option value="bread">Bread or tortillas</option><option value="other">Sausage or deli meat</option></select></label>
</div><div class="finder-actions"><button class="finder-button" type="submit">Show matching dinners</button><button class="finder-button secondary" id="pick-for-me" type="button">Pick one for me</button><button class="finder-button secondary" type="reset">Reset</button><output class="finder-status" id="result-count" aria-live="polite">12 dinners to choose from</output></div><p class="finder-note">Times are estimates, including cooking and waiting. Slow-cooker meals take hours even when prep is short. Check the linked recipe, ingredient labels and your equipment.</p><noscript><p>Filtering needs JavaScript; all 12 dinners and their recipe links are available below.</p></noscript></form>
<p class="finder-empty" id="no-dinners" hidden>No dinners match that combination yet. Try a longer time, another ingredient, or Reset to see everything.</p><div class="finder-results">CARDS</div></section>
<section><h2>Make the next night easier, too.</h2><div class="finder-guides"><a href="/easy-dinner-ideas-no-energy.html"><strong>Too tired to cook</strong><span>Small-effort ideas for the nights you are running on empty.</span></a><a href="/cheap-family-dinners-cost-per-serving.html"><strong>Stretch the dinner budget</strong><span>Compare meal costs with a calculator using your own prices.</span></a><a href="/7-night-dinner-plan-for-picky-families.html"><strong>Plan for picky families</strong><span>A seven-night plan with flexible serving options.</span></a></div></section>
<section class="finder-cta"><h2>Want the whole week decided?</h2><p>The 5:47 p.m. Rescue Kit brings dinner ideas, a weekly planner, a grocery list and a printable fridge sheet together. Explore what is included before you choose.</p><a class="finder-button" href="/5-47-rescue-kit.html">See the Rescue Kit</a></section>
<section aria-labelledby="questions"><h2 id="questions">A few useful answers</h2><details><summary>What can I make when I have almost no energy?</summary><p>Choose minimal prep and about 10 minutes. A rotisserie chicken plate, hummus wraps or a microwave bean bowl are practical starting points. Use ready-to-eat ingredients and follow the full recipe.</p></details><details><summary>Does the ingredient filter mean I have everything I need?</summary><p>No. It helps you choose a starting ingredient. Open the recipe to check the complete shopping list, quantities, labels and cooking directions before you begin.</p></details><details><summary>Can I save the same filters for another day?</summary><p>Yes. Bookmark the page after choosing your filters, or use “Share this dinner finder.” The link remembers those selections. You can reset them any time.</p></details><details><summary>Are the pictures exact recipe photographs?</summary><p>The cards use illustrative imagery from our guides. Some visuals are AI-created serving suggestions or original drawings. Follow the written recipe for ingredients and portions; the finder is not a claim that every dish has been test-cooked.</p></details></section></main>
<footer class="finder-footer"><a href="/about.html">About our guides</a> · <a href="/privacy.html">Privacy</a> · <a href="/blogs.html">All dinner guides</a><p>What's for Eats · Practical dinner help for busy households.</p></footer></body></html>'''
    (ROOT/'what-to-make-for-dinner.html').write_text(html.replace('SCHEMA',json.dumps(schema)).replace('CARDS','\n'.join(cards)))

if __name__ == '__main__':
    build()
