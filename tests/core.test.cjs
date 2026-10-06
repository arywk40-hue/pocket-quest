const test = require('node:test');
const assert = require('node:assert/strict');
const Core = require('../dist/core.js');
test('damaged notebook restores safely', () => { assert.deepEqual(Core.restoreState('bad'), Core.freshState()); assert.deepEqual(Core.restoreState('{"version":1,"active":99}'), Core.freshState()); });
test('unrelated evidence cannot advance; uncertain evidence remains open', () => { assert.equal(Core.canAdvance({status:'rejected'}), false); assert.equal(Core.canAdvance({status:'uncertain'}), true); assert.equal(Core.ending(Core.freshState()), 'open'); });
test('player confirmation is distinguished from model review', () => { const state=Core.freshState(); for(const id of ['leaf','bark','ground'])state.evidence[id]={status:'manual'}; assert.equal(Core.ending(state),'complete'); state.evidence.ground.status='pending'; assert.equal(Core.ending(state),'open'); });
test('restore rejects unknown status and bounds notes', () => { const s=Core.restoreState(JSON.stringify({version:1,active:0,evidence:{leaf:{note:'x'.repeat(5000),status:'manual'},bark:{note:'x',status:'verified'}}}));assert.equal(s.evidence.leaf.note.length,1200);assert.equal(s.evidence.bark,undefined); });

test('observation branches change finale and uncertainty does not resolve it', () => {
  const c=require('../dist/case.json'), state=Core.freshState();
  for(const [id,pattern] of [['leaf','branching'],['bark','ridged'],['ground','similar']]) state.evidence[id]={status:'accepted',pattern};
  const first=Core.resolution(state,c); assert.equal(first.resolved,true);
  state.evidence.leaf.pattern='parallel'; assert.notEqual(Core.resolution(state,c).title,first.title);
  state.evidence.bark.status='uncertain'; assert.equal(Core.resolution(state,c).resolved,false);
});
