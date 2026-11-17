(() => {
  const toggle = document.getElementById('assistantToggle');
  const close = document.getElementById('assistantClose');
  const panel = document.getElementById('assistantPanel');
  const form = document.getElementById('assistantForm');
  const input = document.getElementById('assistantInput');
  const messages = document.getElementById('assistantMessages');
  if (!toggle || !panel || !form) return;
  const show = (open) => { panel.hidden = !open; toggle.setAttribute('aria-expanded', String(open)); if (open) input.focus(); };
  toggle.addEventListener('click', () => show(panel.hidden));
  close.addEventListener('click', () => show(false));
  function bubble(text, kind) { const p = document.createElement('p'); p.className = 'assistant-' + kind; p.textContent = text; messages.appendChild(p); messages.scrollTop = messages.scrollHeight; return p; }
  form.addEventListener('submit', async (e) => {
    e.preventDefault(); const message = input.value.trim(); if (!message) return;
    bubble(message, 'user'); input.value = ''; const wait = bubble('উত্তর তৈরি হচ্ছে...', 'bot');
    const button = form.querySelector('button'); button.disabled = true;
    try {
      const response = await fetch(form.dataset.url, {method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value}, body: JSON.stringify({message})});
      const data = await response.json(); wait.textContent = response.ok ? data.reply : (data.error || 'সমস্যা হয়েছে, আবার চেষ্টা করুন।');
    } catch (err) { wait.textContent = 'সংযোগ সমস্যা। আবার চেষ্টা করুন।'; }
    finally { button.disabled = false; input.focus(); }
  });
})();
