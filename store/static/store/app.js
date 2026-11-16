(function () {
  const root = document.documentElement;
  const savedTheme = localStorage.getItem('taza-theme');
  if (savedTheme === 'dark') root.setAttribute('data-theme', 'dark');
  const languageButton = document.querySelector('[data-language-toggle]');
  function applyLanguage(language) {
    document.querySelectorAll('[data-en][data-bn]').forEach((node) => {
      node.textContent = language === 'bn' ? node.dataset.bn : node.dataset.en;
    });
    if (languageButton) languageButton.setAttribute('aria-label', language === 'bn' ? 'Switch interface labels to English' : 'ইন্টারফেসের লেখা বাংলায় দেখুন');
    localStorage.setItem('taza-language', language);
  }
  const savedLanguage = localStorage.getItem('taza-language');
  if (savedLanguage === 'bn') applyLanguage('bn');
  if (languageButton) languageButton.addEventListener('click', () => {
    const current = localStorage.getItem('taza-language') || 'en';
    applyLanguage(current === 'bn' ? 'en' : 'bn');
  });

  const themeButton = document.querySelector('.theme-toggle');
  if (themeButton) {
    themeButton.addEventListener('click', function () {
      const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      localStorage.setItem('taza-theme', next);
    });
  }

  const menuToggle = document.querySelector('.menu-toggle');
  const closeMenu = document.querySelector('.close-menu');
  const sideMenu = document.getElementById('sideMenu');
  const scrim = document.getElementById('menuScrim');
  function setMenu(open) {
    if (!sideMenu || !scrim) return;
    sideMenu.classList.toggle('open', open);
    scrim.classList.toggle('show', open);
    sideMenu.setAttribute('aria-hidden', String(!open));
    if (menuToggle) menuToggle.setAttribute('aria-expanded', String(open));
    document.body.style.overflow = open ? 'hidden' : '';
  }
  if (menuToggle) menuToggle.addEventListener('click', () => setMenu(true));
  if (closeMenu) closeMenu.addEventListener('click', () => setMenu(false));
  if (scrim) scrim.addEventListener('click', () => setMenu(false));
  document.addEventListener('keydown', (event) => { if (event.key === 'Escape') setMenu(false); });

  document.querySelectorAll('.message button').forEach((button) => button.addEventListener('click', () => button.parentElement.remove()));
  document.querySelectorAll('.copy-coupon').forEach((button) => button.addEventListener('click', async () => {
    const code = button.dataset.copy || '';
    try { await navigator.clipboard.writeText(code); button.textContent = 'COPIED ✓'; }
    catch (_) { button.textContent = code; }
  }));
})();
