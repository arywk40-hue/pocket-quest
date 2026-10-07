const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {JSDOM, VirtualConsole} = require('jsdom');
const root = path.join(__dirname, '..', 'dist');
const caseData = JSON.parse(fs.readFileSync(path.join(root, 'case.json'), 'utf8'));
const tick = () => new Promise(resolve => setTimeout(resolve, 20));
async function setup(html, offline = false, api = null) {
  const errors = [], tools = new Map();
  const virtualConsole = new VirtualConsole(); virtualConsole.on('jsdomError', e => errors.push(e.message));
  const dom = new JSDOM(html || fs.readFileSync(path.join(root, 'index.html'), 'utf8'), { url: offline ? 'file:///field-kit.html' : 'https://test.example/', runScripts: offline ? 'dangerously' : 'outside-only', virtualConsole,
    beforeParse(window) {
      window.HTMLElement.prototype.showModal = function() {this.open = true;}; window.HTMLElement.prototype.close = function() {this.open = false;};
      window.URL.createObjectURL = blob => {window.lastDownload = blob; return 'blob:test';}; window.URL.revokeObjectURL = () => {};
      window.HTMLAnchorElement.prototype.click = function() {window.lastFilename = this.download;};
      window.confirm = () => true;
      window.document.modelContext = {registerTool: async tool => tools.set(tool.name, tool)};
      window.fetch = async url => {
        if (url === '/api/status') return api ? {ok:true,headers:{get:()=> 'application/json'},json:async()=>api.status} : {ok: false};
        if (api && url.startsWith('/api/')) return {ok:true,json:async()=>api.responses[url]};
        const source = fs.readFileSync(path.join(root, url));
        return {ok: true, text: async () => source.toString(), json: async () => JSON.parse(source), blob: async () => new window.Blob([source])};
      };
    }
  });
  if (!offline) {dom.window.FIELD_CASE = caseData; dom.window.eval(fs.readFileSync(path.join(root,'core.js'),'utf8')); dom.window.eval(fs.readFileSync(path.join(root,'app.js'),'utf8'));}
  await tick(); return {window:dom.window,document:dom.window.document,errors,tools};
}
async function collect(document, note, confirm = false) {
  document.querySelector('#observation').value = note;
  document.querySelector('#evidence-form').dispatchEvent(new document.defaultView.Event('submit', {bubbles:true,cancelable:true}));
  await tick(); if(confirm)document.querySelector('#confirm-observation').click();
}
test('walkthrough completes three real-input manual observations without fake AI', async () => {
  const {document,window,errors}=await setup();
  assert.match(document.body.textContent,/AI not connected/);
  document.querySelector('#start-case').click(); await tick();
  assert.equal(document.querySelector('#ai-review').disabled,true);
  assert.equal(document.querySelector('#next-clue').disabled,true);
  for(const note of ['Veins branch from a central line.','The bark has vertical ridges.','There are more fallen leaves under the tree.']){
    await collect(document,note,true);document.querySelector('#next-clue').click();await tick();
  }
  assert.match(document.body.textContent,/The missing page stays open/);
  assert.match(document.body.textContent,/Player-confirmed/);
  assert.deepEqual(errors,[]); window.close();
});
test('uncertain notebook gets open ending, and notes cannot execute HTML', async () => {
  const {document,window}=await setup();document.querySelector('#start-case').click();await tick();
  for(let i=0;i<3;i++){await collect(document,'<img src=x onerror="globalThis.injected=true"> I cannot tell.'); document.querySelector('#next-clue').click();await tick();}
  assert.match(document.body.textContent,/The missing page stays open/);assert.equal(window.injected,undefined);window.close();
});
test('downloaded field kit executes without fetching a case or scripts', async () => {
  const online=await setup();online.document.querySelector('#download-kit').click();await tick();await tick();
  assert.equal(online.window.lastFilename,'Outside-Case-Offline-Field-Kit.html');
  const html=await new Promise(resolve=>{const reader=new online.window.FileReader();reader.onload=()=>resolve(reader.result);reader.readAsText(online.window.lastDownload);});
  assert.ok(html.includes('globalThis.FIELD_CASE='));
  const offline=await setup(html,true);assert.equal(offline.document.querySelector('script[src]'),null);assert.ok(offline.document.querySelector('#start-case'));offline.document.querySelector('#start-case').click();await tick();assert.ok(offline.document.querySelector('#observation'));assert.deepEqual(offline.errors,[]);
  online.window.close();offline.window.close();
});
test('WebMCP contract validates parameters and uses visible case state', async () => {
  const {tools,document,window}=await setup();assert.ok(tools.has('start_outside_case'));const start=tools.get('start_outside_case');await assert.rejects(async()=>start.execute({unexpected:true}));const result=await start.execute({});assert.equal(result.activeClue,'leaf');assert.ok(document.querySelector('#observation'));const read=tools.get('read_case_progress');assert.equal(read.annotations.readOnlyHint,true);assert.deepEqual(Object.keys(read.execute({}).clues),[]);window.close();
});
test('player-selected patterns reconstruct a distinct fictional ending', async () => {
  const {document,window}=await setup();document.querySelector('#start-case').click();await tick();
  for(const [pattern,note] of [['parallel','Veins run alongside each other.'],['flaky','The bark has flakes.'],['similar','The two patches look similar.']]) {
    await collect(document,note);
    document.querySelector('#manual-pattern').value=pattern;
    document.querySelector('#confirm-observation').click();
    document.querySelector('#next-clue').click();await tick();
  }
  assert.match(document.body.textContent,/A page layout, not a map/);
  assert.match(document.body.textContent,/The last clue was a test/);
  assert.match(document.body.textContent,/Player-confirmed/);window.close();
});

test('connection settings show account results safely and label tracing diagnostic', async () => {
  const {document,window,errors}=await setup(null,false,{status:{model:false,elevenlabs:true,sentry:true},responses:{
    '/api/integrations/check':{elevenlabs:{verified:true,voice_name:'<img src=x onerror="window.injected=true">'},sentry:{configured:true}},
    '/api/trace-check':{event_id:'actual-test-id',sentry_trace_id:'test-trace',notice:'This diagnostic is not an AI run.'}
  }});
  document.querySelector('#settings-button').click();
  assert.equal(document.querySelector('#check-connections').disabled,false);
  document.querySelector('#check-connections').click(); await tick();
  assert.match(document.querySelector('#connection-result').textContent,/img src/);
  assert.equal(document.querySelector('#connection-result img'),null);
  document.querySelector('#trace-check').click(); await tick();
  assert.match(document.querySelector('#connection-result').textContent,/diagnostic/i);
  assert.match(document.querySelector('#connection-result').textContent,/test-trace/);
  assert.deepEqual(errors,[]);window.close();
});
