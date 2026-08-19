const state = { claims: [], selected: null };
const $ = (selector) => document.querySelector(selector);
const money = (value) => `Rs ${(value || 0).toLocaleString('en-IN')}`;

async function api(path, options) {
  const response = await fetch(path, options);
  if (!response.ok) { const error = await response.json(); throw new Error(error.detail || 'Request failed'); }
  return response.json();
}

function renderClaims() {
  const filter = $('#status-filter').value;
  const items = state.claims.filter((claim) => !filter || claim.status === filter);
  $('#claims-list').innerHTML = items.map((claim) => `<article class="claim-row ${state.selected?.claim_id === claim.claim_id ? 'selected' : ''}" data-id="${claim.claim_id}"><div><span class="claim-number">${claim.claim_number}</span><div class="claim-name">${claim.customer_name} / ${claim.claim_type}</div><span class="claim-meta">${claim.policy_number} · ${claim.incident_location}</span><br><span class="status ${claim.status.toLowerCase().replaceAll('_','-')}">${claim.status.replaceAll('_',' ')}</span></div><div><div class="claim-amount">${money(claim.claimed_amount)}</div><div class="risk">${claim.risk_level} risk · ${claim.risk_score}/100</div></div></article>`).join('') || '<p class="claim-meta">No claims match this filter.</p>';
  document.querySelectorAll('.claim-row').forEach((row) => row.addEventListener('click', () => selectClaim(row.dataset.id)));
  $('#open-count').textContent = state.claims.length;
  $('#attention-count').textContent = state.claims.filter((claim) => ['MANUAL_REVIEW','FRAUD_REVIEW'].includes(claim.status)).length;
  $('#risk-total').textContent = money(state.claims.reduce((total, claim) => total + claim.claimed_amount, 0));
}

function renderDetail(claim) {
  $('#detail-panel').innerHTML = `<div class="detail-card"><div class="detail-top"><div><span class="claim-number">${claim.claim_number}</span><h2>${claim.customer_name}</h2><span class="claim-meta">${claim.policy_number} · ${claim.claim_type}</span></div><span class="status ${claim.status.toLowerCase().replaceAll('_','-')}">${claim.status.replaceAll('_',' ')}</span></div><div class="detail-grid"><div><span>Incident date</span><strong>${claim.incident_date}</strong></div><div><span>Location</span><strong>${claim.incident_location}</strong></div><div><span>Claimed</span><strong>${money(claim.claimed_amount)}</strong></div><div><span>Deductible</span><strong>${money(claim.deductible)}</strong></div></div><h3>Attached evidence <span class="doc-title">(${claim.documents.length})</span></h3>${claim.documents.map((doc) => `<div class="doc"><span class="doc-icon">⌁</span><div><strong>${doc.file_name}</strong><div class="claim-meta">${doc.document_type} · ${(doc.size_bytes / 1000).toFixed(0)} KB</div></div></div>`).join('') || '<p class="claim-meta">No documents attached yet.</p>'}<button class="primary validate" id="validate-claim">Run validation checks ↗</button><div id="validation-result"></div></div>`;
  $('#validate-claim').addEventListener('click', () => validateClaim(claim.claim_id));
}

async function selectClaim(id) { state.selected = state.claims.find((claim) => claim.claim_id === id); renderClaims(); renderDetail(state.selected); }
async function validateClaim(id) { const result = await api(`/api/claims/${id}/validate`, { method: 'POST' }); $('#validation-result').innerHTML = `<div class="validation-summary"><strong>${result.valid ? 'Ready for review' : 'Review required'}</strong><div class="claim-meta">${result.risk_level} risk · ${result.risk_score}/100</div>${result.checks.map((check) => `<div class="doc"><span>${check.passed ? '✓' : '!'}</span><div><strong>${check.name}</strong><div class="claim-meta">${check.detail}</div></div></div>`).join('')}</div>`; }

async function load() { state.claims = await api('/api/claims'); renderClaims(); const policies = await api('/api/policies'); $('#policy-number').innerHTML = policies.map((policy) => `<option value="${policy.policy_number}">${policy.policy_number} · ${policy.customer_name}</option>`).join(''); }
$('#status-filter').addEventListener('change', renderClaims);
$('#new-claim').addEventListener('click', () => $('#modal').classList.remove('hidden'));
$('#close-modal').addEventListener('click', () => $('#modal').classList.add('hidden'));
$('#claim-form').addEventListener('submit', async (event) => { event.preventDefault(); const data = Object.fromEntries(new FormData(event.target)); data.claimed_amount = Number(data.claimed_amount); try { const claim = await api('/api/claims', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(data) }); state.claims.unshift(claim); renderClaims(); $('#modal').classList.add('hidden'); event.target.reset(); selectClaim(claim.claim_id); } catch (error) { $('#form-message').textContent = error.message; } });
load().catch((error) => { $('#claims-list').innerHTML = `<p class="claim-meta">Unable to load claims: ${error.message}</p>`; });
