(function (root) {
  'use strict';
  const VALID = new Set(['pending', 'accepted', 'uncertain', 'rejected', 'manual']);
  function freshState() { return { version: 1, startedAt: null, active: 0, evidence: {}, elapsedScreenMs: 0 }; }
  function restoreState(raw) {
    try {
      const value = JSON.parse(raw);
      if (value?.version !== 1 || !Number.isInteger(value.active) || value.active < 0 || value.active > 2) return freshState();
      const state = freshState();
      state.active = value.active;
      state.startedAt = typeof value.startedAt === 'string' ? value.startedAt : null;
      state.elapsedScreenMs = Math.max(0, Number(value.elapsedScreenMs) || 0);
      for (const key of ['leaf', 'bark', 'ground']) {
        const e = value.evidence?.[key];
        if (e && typeof e.note === 'string' && VALID.has(e.status)) {
          state.evidence[key] = { note: e.note.slice(0, 1200), status: e.status, summary: String(e.summary || '').slice(0, 600), next_chapter: String(e.next_chapter || '').slice(0, 1000), reviewedBy: String(e.reviewedBy || 'none'), createdAt: String(e.createdAt || ''), photo: !!e.photo, pattern: String(e.pattern || 'unclear').slice(0,20), review_kind: String(e.review_kind || 'none').slice(0,20), trace_id: String(e.trace_id || '').slice(0,50), elapsed_ms: Math.max(0,Number(e.elapsed_ms)||0) };
        }
      }
      return state;
    } catch { return freshState(); }
  }
  function canAdvance(evidence) { return !!evidence && (evidence.status === 'accepted' || evidence.status === 'manual' || evidence.status === 'pending' || evidence.status === 'uncertain'); }
  function ending(state) { return ['leaf', 'bark', 'ground'].every(id => ['accepted', 'manual'].includes(state.evidence[id]?.status)) ? 'complete' : 'open'; }
  function resolution(state, caseData) {
    const entries = caseData.clues.map(c => {
      const e = state.evidence[c.id];
      const eligible = e && (e.status === 'accepted' || e.status === 'manual' || e.review_kind === 'text_only');
      const pattern = eligible && caseData.branches?.[c.id]?.[e.pattern] ? e.pattern : 'unclear';
      return { id: c.id, pattern, ...(caseData.branches?.[c.id]?.[pattern] || {title:'Open clue',text:c.reveal}) };
    });
    const resolved = entries.every(e => e.pattern !== 'unclear');
    const leaf = entries[0].pattern, bark = entries[1].pattern, ground = entries[2].pattern;
    let title = 'The missing page stays open.';
    let text = 'Your observations have changed the case, but some clues remain unresolved. Keep their uncertainty in the record.';
    if (resolved) {
      title = leaf === 'parallel' ? 'A page layout, not a map.' : leaf === 'fan' ? 'Several witnesses. One record.' : 'Separate clues. A connected record.';
      text = (leaf === 'parallel' ? 'In this version of the fiction, Mira was designing a field journal.' : leaf === 'fan' ? 'In this version of the fiction, Mira was gathering different viewpoints.' : 'In this version of the fiction, Mira was connecting separate observations.') + ' ' + (bark === 'flaky' ? 'The repeating mark points to an archive of layers.' : bark === 'smooth' ? 'The witness account contains a missing mark.' : 'The repeated mark becomes the rhythm of the record.') + ' ' + (ground === 'similar' ? 'The last clue was a test: do not invent a contrast.' : ground === 'bare' ? 'The exposed page was waiting for your own entry.' : 'The scattered pages belong to the cover you noticed.');
    }
    return {title,text,entries,signature:entries.map(e=>e.pattern).join('/'),resolved};
  }
  function exportJournal(state, caseData) {
    return { project: 'Outside Case', case: caseData.title, exportedAt: new Date().toISOString(), screenTimeSeconds: Math.round(state.elapsedScreenMs / 1000), ending: ending(state), story: resolution(state, caseData), observations: caseData.clues.map(c => ({ clue: c.title, ...(state.evidence[c.id] || { status: 'missing' }) })), notice: 'Manual observations are player-confirmed, not AI-verified. Photos are exported separately in the full field journal.' };
  }
  const api = { freshState, restoreState, canAdvance, ending, resolution, exportJournal };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.OutsideCore = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
