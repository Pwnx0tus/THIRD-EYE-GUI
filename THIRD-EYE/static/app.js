/* ─── THIRD-EYE · Frontend Logic ───────────────────────── */

// ── Tab Navigation ────────────────────────────────────────
function switchTab(name) {
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.classList.remove('active');
    btn.setAttribute('aria-selected', 'false');
  });
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));

  document.getElementById('tab-' + name).classList.add('active');
  document.getElementById('tab-' + name).setAttribute('aria-selected', 'true');
  document.getElementById('panel-' + name).classList.add('active');
}

// Allow Enter key to submit in any input
document.addEventListener('keydown', (e) => {
  if (e.key !== 'Enter') return;
  const active = document.querySelector('.tab-panel.active');
  if (!active) return;
  const btn = active.querySelector('.btn-primary');
  if (btn && !btn.disabled) btn.click();
});

// ── Utility Helpers ───────────────────────────────────────
function setLoading(btnId, state) {
  const btn = document.getElementById(btnId);
  if (state) {
    btn.classList.add('loading');
    btn.disabled = true;
    btn.querySelector('.btn-text').textContent = 'Running…';
  } else {
    btn.classList.remove('loading');
    btn.disabled = false;
  }
}

function badge(type, text) {
  return `<span class="badge badge-${type}">${text}</span>`;
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => showToast('Copied!'));
}

function downloadJSON(data, filename) {
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

function showToast(msg) {
  const t = document.createElement('div');
  t.textContent = msg;
  Object.assign(t.style, {
    position: 'fixed', bottom: '24px', right: '24px',
    background: '#22d3ee', color: '#000', padding: '10px 20px',
    borderRadius: '8px', fontFamily: 'JetBrains Mono,monospace',
    fontSize: '0.82rem', fontWeight: '600', zIndex: '9999',
    animation: 'slideIn 0.2s ease'
  });
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 2200);
}

function collapsible(id, title, contentHtml, badgeHtml = '') {
  return `
    <div class="result-card">
      <div class="result-card-header" onclick="toggleCard('${id}')">
        <span class="result-card-title">${title} ${badgeHtml}</span>
        <span class="chevron" id="chev-${id}">▾</span>
      </div>
      <div class="result-card-body" id="body-${id}">
        ${contentHtml}
      </div>
    </div>`;
}

function toggleCard(id) {
  const body = document.getElementById('body-' + id);
  const chev = document.getElementById('chev-' + id);
  const open = body.classList.toggle('open');
  chev.classList.toggle('open', open);
}

function infoGrid(items) {
  return `<div class="info-grid">
    ${items.map(([label, value]) => `
      <div class="info-item">
        <div class="info-label">${label}</div>
        <div class="info-value">${value ?? '<span style="color:var(--text-3)">—</span>'}</div>
      </div>`).join('')}
  </div>`;
}

function foundList(items) {
  if (!items || items.length === 0) return `<div class="empty-state"><span class="empty-icon">🔍</span>No results found.</div>`;
  return `<ul class="found-list">
    ${items.map((item, i) => `
      <li class="found-item">
        <span class="found-item-idx">${i + 1}.</span>
        <div class="found-item-content">
          <div class="found-item-title">${item.title ?? item.site ?? item}</div>
          ${item.link || item.url ? `<a class="found-item-link" href="${item.link || item.url}" target="_blank" rel="noopener">${item.link || item.url}</a>` : ''}
          ${item.snippet ? `<div style="font-size:0.78rem;color:var(--text-2);margin-top:3px;">${item.snippet}</div>` : ''}
        </div>
      </li>`).join('')}
  </ul>`;
}

function actionBar(data, filename) {
  return `<div class="action-bar">
    <button class="btn btn-secondary btn-sm" onclick='downloadJSON(${JSON.stringify(data)}, "${filename}")'>⬇ Download JSON</button>
    <button class="btn btn-secondary btn-sm" onclick='copyToClipboard(${JSON.stringify(JSON.stringify(data, null, 2))})'>📋 Copy JSON</button>
  </div>`;
}

// ── PHONE ─────────────────────────────────────────────────
async function runPhone() {
  const number = document.getElementById('phone-number').value.trim();
  const apiKey = document.getElementById('numverify-key').value.trim();
  if (!number) { showToast('Enter a phone number'); return; }

  const container = document.getElementById('phone-results');
  container.innerHTML = '';
  setLoading('btn-phone', true);

  let btn_restore_text = 'btn-phone';
  try {
    const res = await fetch('/api/phone', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ number, numverify_key: apiKey || null })
    });
    const json = await res.json();
    if (!res.ok) throw new Error(json.detail || res.statusText);
    renderPhone(json, container);
  } catch (err) {
    container.innerHTML = `<div class="error-banner">❌ ${err.message}</div>`;
  } finally {
    setLoading('btn-phone', false);
    document.getElementById(btn_restore_text).querySelector('.btn-text').textContent = '🔍 Investigate';
  }
}

function renderPhone(json, container) {
  const d = json.data;
  let html = '';

  // Google Results
  const g = d.google;
  if (g && g.success && g.results.length > 0) {
    html += collapsible('ph-google', '🔍 Google Search Results',
      foundList(g.results),
      badge('cyan', g.results.length + ' results')
    );
  } else {
    html += collapsible('ph-google', '🔍 Google Search Results',
      `<div class="empty-state"><span class="empty-icon">🔍</span>No Google results.</div>`,
      badge('amber', 'no results')
    );
  }

  // Phone Validation
  const v = d.validation;
  if (v) {
    const vBadge = v.valid ? badge('green', 'VALID') : badge('red', 'INVALID');
    const vContent = v.valid ? infoGrid([
      ['Number', v.number],
      ['Country', v.country],
      ['Location', v.location],
      ['Carrier', v.carrier],
      ['Line Type', v.line_type],
      ['Intl Format', v.international_format],
    ]) : `<div class="error-banner">⚠️ ${v.error || 'Invalid number'}</div>`;
    html += collapsible('ph-valid', '✅ Phone Validation', vContent, vBadge);
  }

  // Links
  const l = d.links;
  if (l) {
    html += collapsible('ph-links', '🔗 Messaging Links',
      infoGrid([
        ['WhatsApp', `<a href="${l.whatsapp_url}" target="_blank" class="found-item-link">${l.whatsapp_url}</a>`],
        ['Telegram', `<a href="${l.telegram_url}" target="_blank" class="found-item-link">${l.telegram_url}</a>`],
      ])
    );
  }

  // WhatsApp Info
  const w = d.whatsapp;
  if (w && w.success) {
    html += collapsible('ph-wa', '💬 WhatsApp Profile',
      infoGrid([
        ['Phone', w.phone],
        ['About', w.about],
        ['Profile Pic', w.profile_pic ? `<a href="${w.profile_pic}" target="_blank" class="found-item-link">View Image</a>` : null],
      ])
    );
  }

  // Instagram Check
  const ig = d.instagram_check;
  if (ig) {
    const igBadge = ig.found ? badge('green', 'FOUND') : badge('red', 'NOT FOUND');
    html += collapsible('ph-ig', '📸 Instagram Status',
      infoGrid([['Status', ig.status || 'N/A']]),
      igBadge
    );
  }

  html += actionBar(json, `phone_${json.number}_results.json`);
  container.innerHTML = html;
  // Auto-expand first card
  toggleCard('ph-google');
}

// ── USERNAME ──────────────────────────────────────────────
function runUsername() {
  const username = document.getElementById('username-input').value.trim();
  if (!username) { showToast('Enter a username'); return; }

  const container = document.getElementById('username-results');
  const btn = document.getElementById('btn-username');

  btn.disabled = true;
  btn.querySelector('.btn-text').textContent = 'Scanning…';

  let foundItems = [];
  let checked = 0;
  let total = 0;
  let allData = { username, found: [], extras: {} };

  container.innerHTML = `
    <div class="card">
      <p class="card-title">📡 Live Scan — <code style="font-size:0.85em;color:var(--magenta)">${username}</code></p>
      <div class="progress-label">
        <span id="u-progress-text">Starting…</span>
        <span id="u-progress-pct">0%</span>
      </div>
      <div class="progress-wrap"><div class="progress-bar" id="u-pbar" style="width:0%"></div></div>
      <div class="live-feed" id="u-feed"></div>
      <div id="u-found-section" style="display:none">
        <p class="card-title" style="margin-top:16px;">✅ Found On</p>
        <div id="u-found-list"></div>
      </div>
    </div>`;

  const evtSource = new EventSource(`/api/username/stream?dummy=${Date.now()}`);

  // SSE uses POST but browser EventSource is GET — use fetch with ReadableStream instead
  evtSource.close();

  // Use fetch-based SSE for POST
  fetchSSE('/api/username/stream', { username }, (event) => {
    const d = event;

    if (d.done) {
      // Scan complete
      btn.disabled = false;
      btn.querySelector('.btn-text').textContent = '🔍 Scan Platforms';
      document.getElementById('u-progress-text').textContent = `✅ Complete — ${foundItems.length} found on ${total} platforms`;
      document.getElementById('u-progress-pct').textContent = '100%';
      document.getElementById('u-pbar').style.width = '100%';

      // Show extras
      if (Object.keys(allData.extras).length > 0) {
        const extHtml = renderUsernameExtras(allData.extras);
        container.querySelector('.card').insertAdjacentHTML('beforeend', extHtml);
      }
      container.querySelector('.card').insertAdjacentHTML('beforeend', actionBar(allData, `username_${username}_results.json`));
      return;
    }

    total = d.total || total;
    checked = d.checked || checked;
    const pct = d.progress || 0;

    document.getElementById('u-pbar').style.width = pct + '%';
    document.getElementById('u-progress-pct').textContent = pct + '%';
    document.getElementById('u-progress-text').textContent = `Checked ${checked} / ${total} platforms`;

    const feed = document.getElementById('u-feed');
    const dotClass = d.found === true ? 'feed-dot-green' : d.found === false ? 'feed-dot-red' : 'feed-dot-gray';
    const entry = document.createElement('div');
    entry.className = 'feed-entry';
    entry.innerHTML = `
      <span class="feed-dot ${dotClass}"></span>
      <span class="feed-site">${d.site}</span>
      ${d.url ? `<a class="feed-url" href="${d.url}" target="_blank" rel="noopener">${d.url}</a>` : ''}`;
    feed.appendChild(entry);
    feed.scrollTop = feed.scrollHeight;

    if (d.found === true) {
      foundItems.push({ site: d.site, url: d.url });
      allData.found.push({ site: d.site, url: d.url });

      const foundSection = document.getElementById('u-found-section');
      foundSection.style.display = 'block';
      const foundList = document.getElementById('u-found-list');
      const item = document.createElement('div');
      item.style.cssText = 'display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid var(--border);';
      item.innerHTML = `
        <span class="badge badge-green">FOUND</span>
        <strong style="color:var(--text-1);font-family:var(--font-mono);font-size:0.85rem;">${d.site}</strong>
        <a href="${d.url}" target="_blank" rel="noopener" class="found-item-link" style="flex:1;min-width:0;">${d.url}</a>`;
      foundList.appendChild(item);
    }

    if (d.extras && Object.keys(d.extras).length > 0) {
      Object.assign(allData.extras, d.extras);
    }

  }, () => {
    btn.disabled = false;
    btn.querySelector('.btn-text').textContent = '🔍 Scan Platforms';
  });
}

function renderUsernameExtras(extras) {
  let html = '<p class="card-title" style="margin-top:24px;">🔎 Profile Details</p>';
  if (extras.github) {
    const g = extras.github;
    html += collapsible('u-github', '🐙 GitHub Profile',
      infoGrid([
        ['Full Name', g.full_name], ['Handle', g.handle],
        ['Bio', g.bio], ['Org', g.org],
        ['Country', g.country], ['Status', g.status],
        ['Followers', g.followers], ['Following', g.following],
        ['Avatar', g.avatar_url ? `<a href="${g.avatar_url}" target="_blank" class="found-item-link">View</a>` : null],
      ])
    );
  }
  if (extras.chess) {
    const c = extras.chess;
    html += collapsible('u-chess', '♟ Chess.com Profile',
      infoGrid([['Name', c.name], ['Joined', c.joined], ['Location', c.location]])
    );
  }
  if (extras.instagram) {
    const ig = extras.instagram;
    const p = ig.profile;
    if (p && p.success) {
      html += collapsible('u-insta', '📸 Instagram Profile',
        infoGrid([
          ['Full Name', p.full_name], ['Bio', p.bio],
          ['Followers', p.followers], ['Following', p.following],
          ['Posts', p.posts], ['User ID', p.user_id],
          ['Profile Pic', p.profile_pic_url ? `<a href="${p.profile_pic_url}" target="_blank" class="found-item-link">View</a>` : null],
        ])
      );
    }
  }
  return html;
}

async function fetchSSE(url, body, onMessage, onDone) {
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop(); // keep incomplete line
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6));
            onMessage(data);
          } catch (_) {}
        }
      }
    }
  } catch (err) {
    console.error('SSE error:', err);
  } finally {
    if (onDone) onDone();
  }
}

// ── EMAIL ─────────────────────────────────────────────────
async function runEmail() {
  const email = document.getElementById('email-input').value.trim();
  if (!email) { showToast('Enter an email address'); return; }

  const container = document.getElementById('email-results');
  container.innerHTML = '';
  setLoading('btn-email', true);

  try {
    const res = await fetch('/api/email', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    });
    const json = await res.json();
    if (!res.ok) throw new Error(json.detail || res.statusText);
    renderEmail(json, container);
  } catch (err) {
    container.innerHTML = `<div class="error-banner">❌ ${err.message}</div>`;
  } finally {
    setLoading('btn-email', false);
    document.getElementById('btn-email').querySelector('.btn-text').textContent = '🔍 Investigate';
  }
}

function renderEmail(json, container) {
  const d = json.data;
  let html = '';

  // Platform Registrations
  const pc = d.platform_check;
  if (pc) {
    const regItems = pc.results.filter(r => r.is_registered === true);
    const regBadge = badge(regItems.length > 0 ? 'green' : 'amber', regItems.length + ' registered');

    const regHtml = regItems.length > 0
      ? foundList(regItems.map(r => ({ title: r.site, url: r.url, snippet: `HTTP ${r.status_code}` })))
      : `<div class="empty-state"><span class="empty-icon">📋</span>No registrations detected.</div>`;
    html += collapsible('em-platforms', '🌐 Platform Registrations', regHtml, regBadge);

    // Gravatar
    if (pc.gravatar) {
      const gv = pc.gravatar;
      html += collapsible('em-gravatar', '👤 Gravatar Profile',
        infoGrid([
          ['Username', gv.username],
          ['Display Name', gv.display_name],
          ['Profile URL', gv.profile_url ? `<a href="${gv.profile_url}" target="_blank" class="found-item-link">${gv.profile_url}</a>` : null],
          ['Thumbnail', gv.thumbnail ? `<a href="${gv.thumbnail}" target="_blank" class="found-item-link">View Image</a>` : null],
        ]),
        badge('magenta', 'GRAVATAR')
      );
    }
  }

  // Firefox
  const ff = d.firefox;
  if (ff) {
    const ffBadge = ff.registered === true ? badge('green', 'REGISTERED') : ff.registered === false ? badge('red', 'NOT REGISTERED') : badge('amber', 'UNKNOWN');
    html += collapsible('em-firefox', '🦊 Firefox Accounts', infoGrid([['Status', ff.status]]), ffBadge);
  }

  // Breach Data
  const bd = d.breach_data;
  if (bd) {
    const bdBadge = bd.success ? badge('cyan', 'CHECKED') : badge('red', 'ERROR');
    const bdContent = bd.success
      ? `<div class="json-viewer">${JSON.stringify(bd.data, null, 2)}</div>`
      : `<div class="error-banner">${bd.error}</div>`;
    html += collapsible('em-breach', '🔓 Breach Data (HudsonRock)', bdContent, bdBadge);
  }

  // Pastebin
  const pb = d.pastebin;
  if (pb) {
    const pbBadge = pb.found ? badge('red', pb.count + ' FOUND') : badge('green', 'CLEAN');
    const pbContent = pb.found
      ? foundList(pb.links.map(l => ({ title: l, url: l })))
      : `<div class="empty-state"><span class="empty-icon">📋</span>No Pastebin exposures found.</div>`;
    html += collapsible('em-paste', '📋 Pastebin Exposure', pbContent, pbBadge);
  }

  // Instagram
  const ig = d.instagram;
  if (ig) {
    const igBadge = ig.found ? badge('green', 'LINKED') : badge('red', 'NOT LINKED');
    html += collapsible('em-insta', '📸 Instagram Association',
      infoGrid([['Contact Email', ig.contact_email || '—'], ['Found', ig.found ? 'Yes' : 'No']]),
      igBadge
    );
  }

  html += actionBar(json, `email_${json.email}_results.json`);
  container.innerHTML = html;
  toggleCard('em-platforms');
}

// ── IP ────────────────────────────────────────────────────
async function runIP() {
  const ip = document.getElementById('ip-input').value.trim();
  if (!ip) { showToast('Enter an IP address'); return; }

  const container = document.getElementById('ip-results');
  container.innerHTML = '';
  setLoading('btn-ip', true);

  try {
    const res = await fetch('/api/ip', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ip })
    });
    const json = await res.json();
    if (!res.ok) throw new Error(json.detail || res.statusText);
    renderIP(json, container);
  } catch (err) {
    container.innerHTML = `<div class="error-banner">❌ ${err.message}</div>`;
  } finally {
    setLoading('btn-ip', false);
    document.getElementById('btn-ip').querySelector('.btn-text').textContent = '🔍 Geolocate';
  }
}

function renderIP(json, container) {
  const d = json.data;
  let html = '';

  if (!d.success) {
    html = `<div class="error-banner">❌ ${d.error}</div>`;
    container.innerHTML = html;
    return;
  }

  const ipBadge = badge('cyan', d.ip || ip);
  html += collapsible('ip-geo', '🌍 Geolocation & ISP',
    infoGrid([
      ['IP Address', d.ip],
      ['Country', d.country],
      ['Region', d.region],
      ['City', d.city],
      ['Latitude', d.latitude],
      ['Longitude', d.longitude],
      ['ISP', d.isp],
      ['Language', d.language],
    ]),
    ipBadge
  );

  if (d.latitude && d.longitude) {
    const lat = d.latitude, lon = d.longitude;
    const mapUrl = `https://www.openstreetmap.org/?mlat=${lat}&mlon=${lon}&zoom=10`;
    html += `
      <div class="result-card">
        <div class="map-card">
          <div class="map-coords">📍 ${lat}, ${lon}</div>
          <p style="color:var(--text-2);font-size:0.8rem;margin-bottom:8px;">${d.city || ''} ${d.region || ''}, ${d.country || ''}</p>
          <a class="map-link" href="${mapUrl}" target="_blank" rel="noopener">🗺 View on OpenStreetMap →</a>
        </div>
      </div>`;
  }

  html += actionBar(json, `ip_${d.ip}_results.json`);
  container.innerHTML = html;
  toggleCard('ip-geo');
}
