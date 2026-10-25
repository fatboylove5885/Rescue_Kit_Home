/* Progressive enhancement: every dinner and recipe link also works without JS. */
(function () {
  'use strict';
  const form = document.getElementById('dinner-filters');
  if (!form) return;
  const cards = Array.from(document.querySelectorAll('.dinner-card'));
  const fields = ['time', 'effort', 'ingredient'];
  const allowed = Object.fromEntries(fields.map(name => [name, Array.from(form.elements[name].options, option => option.value)]));
  const params = new URLSearchParams(location.search);
  fields.forEach(name => { if (allowed[name].includes(params.get(name))) form.elements[name].value = params.get(name); });

  function applyFilters(track) {
    const time = form.elements.time.value;
    const effort = form.elements.effort.value;
    const ingredient = form.elements.ingredient.value;
    let count = 0;
    cards.forEach(card => {
      const visible = (time === 'any' || (time === 'slow' ? card.dataset.slow === 'true' : Number(card.dataset.minutes) <= Number(time))) &&
        (effort === 'any' || card.dataset.effort === effort) &&
        (ingredient === 'any' || card.dataset.ingredients.split(' ').includes(ingredient));
      card.hidden = !visible;
      if (visible) count += 1;
    });
    document.getElementById('result-count').textContent = count + (count === 1 ? ' dinner matches' : ' dinners match');
    document.getElementById('no-dinners').hidden = count > 0;
    const next = new URL(location.href);
    fields.forEach(name => { const value = form.elements[name].value; if (value === 'any') next.searchParams.delete(name); else next.searchParams.set(name, value); });
    history.replaceState(null, '', next.pathname + next.search + next.hash);
    if (track && window.wfeTrack) window.wfeTrack('dinner_finder_filter', {time, effort, ingredient, result_count: count});
  }
  form.addEventListener('submit', event => { event.preventDefault(); applyFilters(true); });
  form.addEventListener('change', () => applyFilters(true));
  form.addEventListener('reset', () => { fields.forEach(name => { form.elements[name].value = 'any'; }); applyFilters(true); });
  document.getElementById('pick-for-me').addEventListener('click', () => {
    applyFilters(false);
    const matching = cards.filter(card => !card.hidden);
    if (!matching.length) return;
    const selected = matching[Math.floor(Math.random() * matching.length)];
    matching.forEach(card => { card.hidden = card !== selected; });
    document.getElementById('result-count').textContent = 'One idea picked for you';
    selected.querySelector('a').focus({preventScroll:true});
    selected.scrollIntoView({behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block:'center'});
    if (window.wfeTrack) window.wfeTrack('dinner_finder_pick', {recipe_id: selected.id});
  });
  document.getElementById('share-finder').addEventListener('click', async () => {
    const url = new URL('https://whatsforeats.online/what-to-make-for-dinner.html');
    fields.forEach(name => { const value = form.elements[name].value; if (value !== 'any') url.searchParams.set(name, value); });
    const status = document.getElementById('share-status');
    try {
      if (navigator.share) await navigator.share({title:'What should I make for dinner?', url:url.href});
      else if (navigator.clipboard) { await navigator.clipboard.writeText(url.href); status.textContent = 'Link copied — your filters are included.'; }
      else { status.textContent = url.href; }
      if (window.wfeTrack) window.wfeTrack('share', {method:'dinner_finder', content_type:'tool'});
    } catch (error) { if (error.name !== 'AbortError') status.textContent = 'Copy this link: ' + url.href; }
  });
  applyFilters(false);
})();
