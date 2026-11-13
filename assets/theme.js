/* Badr Edge theme toggle. The inline script in <head> sets html[data-theme]
   before paint (saved choice, else the system setting); this file wires the
   .theme-btn buttons, saves the visitor's choice and follows system changes
   until the visitor picks a theme. */
(() => {
  const root = document.documentElement, KEY = 'be-theme';
  const saved = () => { try { return localStorage.getItem(KEY); } catch (e) { return null; } };
  const apply = (t, save) => {
    root.setAttribute('data-theme', t);
    const m = document.querySelector('meta[name="theme-color"]');
    if (m) m.setAttribute('content', t === 'light' ? '#f7f4ee' : '#07080a');
    document.querySelectorAll('.theme-btn').forEach(b => {
      const label = t === 'light' ? 'Switch to dark theme' : 'Switch to light theme';
      b.setAttribute('aria-label', label); b.setAttribute('title', label);
    });
    if (save) { try { localStorage.setItem(KEY, t); } catch (e) {} }
  };
  apply(root.getAttribute('data-theme') === 'light' ? 'light' : 'dark');
  document.addEventListener('click', e => {
    if (e.target.closest && e.target.closest('.theme-btn')) apply(root.getAttribute('data-theme') === 'light' ? 'dark' : 'light', true);
  });
  try {
    matchMedia('(prefers-color-scheme: light)').addEventListener('change', e => {
      const s = saved(); if (s !== 'light' && s !== 'dark') apply(e.matches ? 'light' : 'dark');
    });
  } catch (e) {}
})();
