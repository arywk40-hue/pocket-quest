import base64
import io
import json

import httpx
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from backend import app as companion


@pytest.fixture
def client(monkeypatch, tmp_path):
    monkeypatch.setattr(companion, "TRACE_PATH", tmp_path / "receipts.jsonl")
    return TestClient(companion.app)


def photo():
    output = io.BytesIO()
    Image.new("RGB", (16, 16), "green").save(output, format="PNG")
    return "data:image/png;base64," + base64.b64encode(output.getvalue()).decode()


def request():
    return {"clue_id": "leaf", "note": "I see a branching line.", "image": photo()}


async def ready():
    return True


def install_model_stub(monkeypatch, responses):
    monkeypatch.setattr(companion, "model_ready", ready)
    calls = []
    class ModelClient:
        def __init__(self, **_kwargs): pass
        async def __aenter__(self): return self
        async def __aexit__(self, *_args): pass
        async def post(self, url, **kwargs):
            calls.append(kwargs["json"])
            content = responses[min(len(calls) - 1, len(responses) - 1)]
            return httpx.Response(200, request=httpx.Request("POST", url), json={"choices": [{"message": {"content": content}}], "usage": {"prompt_tokens": 100, "completion_tokens": 20}})
    monkeypatch.setattr(companion.httpx, "AsyncClient", ModelClient)
    return calls


def decision(status="accepted"):
    return json.dumps({"status": status, "summary": "A visible central vein branches into smaller lines.", "pattern": "branching" if status == "accepted" else "unclear"})


def test_static_case_is_served(client):
    assert client.get("/").status_code == 200
    assert client.get("/case.json").json()["id"] == "missing-field-notes"


def test_unknown_clue_refused(client):
    payload = request(); payload["clue_id"] = "fake"
    assert client.post("/api/review", json=payload).status_code == 422


def test_foreign_origin_refused(client):
    assert client.post("/api/review", json=request(), headers={"origin": "https://foreign.example"}).status_code == 403


def test_absent_model_does_not_fake_acceptance(client, monkeypatch):
    async def not_ready(): return False
    monkeypatch.setattr(companion, "model_ready", not_ready)
    assert client.post("/api/review", json=request()).status_code == 503
    receipt=json.loads(companion.TRACE_PATH.read_text())
    assert receipt['failure_type']=='ModelUnavailable' and receipt['attempts']==0
    assert receipt['status']=='failed'


@pytest.mark.parametrize("bad", ["data:image/svg+xml;base64,PHN2Zy8+", "data:image/png;base64,bad!", "data:image/jpeg;base64,YWJj"])
def test_non_photo_refused(client, monkeypatch, bad):
    monkeypatch.setattr(companion, "model_ready", ready)
    payload = request(); payload["image"] = bad
    assert client.post("/api/review", json=payload).status_code == 422


@pytest.mark.parametrize("status", ["accepted", "uncertain", "rejected"])
def test_structured_outcomes_and_private_receipt(client, monkeypatch, status):
    calls = install_model_stub(monkeypatch, [decision(status)])
    payload = request(); payload["note"] = "PRIVATE PLAYER NOTE"
    response = client.post("/api/review", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == status
    assert len(calls) == 1
    receipt = companion.TRACE_PATH.read_text()
    assert "PRIVATE PLAYER NOTE" not in receipt and "data:image" not in receipt
    assert json.loads(receipt)["attempts"] == 1


def test_malformed_response_retried_once(client, monkeypatch):
    calls = install_model_stub(monkeypatch, ["not json", decision()])
    assert client.post("/api/review", json=request()).status_code == 200
    assert len(calls) == 2


def test_repeated_malformed_response_fails_closed(client, monkeypatch):
    calls = install_model_stub(monkeypatch, ["not json"])
    assert client.post("/api/review", json=request()).status_code == 502
    assert len(calls) == 2
    assert json.loads(companion.TRACE_PATH.read_text())["status"] == "failed"


def test_unstructured_or_invented_pattern_refused():
    with pytest.raises(ValueError):
        companion.parse_decision('{"status":"accepted","summary":"Bark.","pattern":"ridged","directions":"Turn left"}')


def test_schema_extra_keys_and_fabricated_status_refused():
    with pytest.raises(ValueError): companion.parse_decision('{"status":"certain","summary":"x","pattern":"branching"}')
    with pytest.raises(ValueError): companion.parse_decision('{"status":"accepted","summary":"x","pattern":"branching","confidence":1}')


def test_image_metadata_stripped():
    raw = companion.normalize_image(photo())
    with Image.open(io.BytesIO(base64.b64decode(raw.split(",")[1]))) as image:
        assert image.format == "JPEG"
        assert not image.getexif()


def test_narration_does_not_claim_partner_without_key(client, monkeypatch):
    monkeypatch.delenv("ELEVENLABS_API_KEY", raising=False)
    assert client.post("/api/audio-pack", json={"language": "en-IN"}).status_code == 503


def test_narration_rejects_unsupported_language(client):
    assert client.post("/api/audio-pack", json={"language": "fake"}).status_code == 422


def test_different_evidence_patterns_change_story(client, monkeypatch):
    install_model_stub(monkeypatch, [decision(), json.dumps({"status":"accepted","summary":"Veins run alongside one another.","pattern":"parallel"})])
    first = client.post("/api/review", json=request()).json()
    second = client.post("/api/review", json=request()).json()
    assert first["next_chapter"] != second["next_chapter"]
    assert first["pattern"] == "branching" and second["pattern"] == "parallel"


def test_wrong_clue_pattern_fails_closed(client, monkeypatch):
    install_model_stub(monkeypatch, [json.dumps({"status":"accepted","summary":"Bark.","pattern":"ridged"})])
    assert client.post("/api/review", json=request()).status_code == 502


def test_gemma2_text_mode_never_reviews_photo(client, monkeypatch):
    monkeypatch.setattr(companion, "MODEL_MODE", "text")
    monkeypatch.setattr(companion, "MODEL_NAME", "gemma2:2b")
    calls = install_model_stub(monkeypatch, [decision()])
    payload = request(); payload["image"] = "not an image"
    response = client.post("/api/review", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "uncertain"
    assert response.json()["review_kind"] == "text_only"
    assert isinstance(calls[0]["messages"][1]["content"], str)
    assert "not an image" not in json.dumps(calls)


def test_gemma2_vision_mode_is_refused(client, monkeypatch):
    monkeypatch.setattr(companion, "model_ready", ready)
    monkeypatch.setattr(companion, "MODEL_NAME", "gemma2:2b")
    assert client.post("/api/review", json=request()).status_code == 422


def test_elevenlabs_chapters_are_cached_and_do_not_send_observations(client, monkeypatch, tmp_path):
    monkeypatch.setattr(companion, 'ROOT', tmp_path)
    monkeypatch.setenv('ELEVENLABS_API_KEY', 'test-only')
    monkeypatch.setenv('ELEVENLABS_VOICE_ID', 'testvoice')
    calls=[]
    class AudioClient:
        def __init__(self, **kwargs): pass
        async def __aenter__(self): return self
        async def __aexit__(self, *args): pass
        async def post(self, url, **kwargs):
            calls.append(kwargs['json'])
            return httpx.Response(200, request=httpx.Request('POST',url), headers={'content-type':'audio/mpeg'}, content=b'test-audio-contract')
    monkeypatch.setattr(companion.httpx, 'AsyncClient', AudioClient)
    first=client.post('/api/audio-pack',json={'language':'en-IN'})
    second=client.post('/api/audio-pack',json={'language':'en-IN'})
    assert first.status_code == second.status_code == 200
    assert len(calls)==3 and first.json()['audio']==second.json()['audio']
    assert all(set(call)=={'text','model_id'} for call in calls)
    assert set(first.json()['audio'])=={'leaf','bark','ground'}


def test_sentry_span_contract_and_failure_are_captured_without_evidence(client, monkeypatch):
    import sentry_sdk
    from sentry_sdk.transport import Transport
    captured=[]
    streamed=[]
    class MemoryTransport(Transport):
        def capture_envelope(self, envelope):
            for item in envelope.items:
                if item.type == 'transaction':
                    captured.append(item.payload.json)
                elif item.type == 'span':
                    streamed.extend(item.payload.json['items'])
    monkeypatch.setattr(companion,'SENTRY_ENABLED',True)
    install_model_stub(monkeypatch,['not json'])
    with sentry_sdk.isolation_scope() as scope:
        scope.set_client(sentry_sdk.Client(dsn='https://test@example.invalid/1',transport=MemoryTransport,
                         traces_sample_rate=1.0,default_integrations=False,include_local_variables=False))
        with sentry_sdk.start_transaction(name='local_review_test',op='test'):
            payload=request(); payload['note']='PRIVATE SENTINEL OBSERVATION'
            response=client.post('/api/review',json=payload)
            assert response.status_code==502
    assert any(item.get('transaction')=='outside_case.review' for item in captured)
    def attr(span, key):
        return span.get('attributes',{}).get(key,{}).get('value')
    assert any(attr(s,'sentry.op')=='gen_ai.invoke_agent' and s['status']=='error' for s in streamed)
    assert sum(attr(s,'sentry.op')=='gen_ai.chat' for s in streamed)==2
    assert any(attr(s,'gen_ai.request.model')==companion.MODEL_NAME for s in streamed)
    serialized=json.dumps({'transactions':captured,'streamed_spans':streamed})
    assert 'PRIVATE SENTINEL OBSERVATION' not in serialized and 'data:image' not in serialized


@pytest.mark.parametrize('http_status,content_type,body', [(200,'application/json',b'{}'),(200,'audio/mpeg',b''),(401,'application/json',b'{}'),(429,'application/json',b'{}')])
def test_audio_provider_failure_returns_error_and_private_receipt(client,monkeypatch,tmp_path,http_status,content_type,body):
    monkeypatch.setattr(companion,'ROOT',tmp_path)
    monkeypatch.setenv('ELEVENLABS_API_KEY','PRIVATE_KEY_SENTINEL')
    monkeypatch.setenv('ELEVENLABS_VOICE_ID','testvoice')
    class BadClient:
        def __init__(self,**kwargs): pass
        async def __aenter__(self): return self
        async def __aexit__(self,*args): pass
        async def post(self,url,**kwargs):
            return httpx.Response(http_status,request=httpx.Request('POST',url),headers={'content-type':content_type},content=body)
    monkeypatch.setattr(companion.httpx,'AsyncClient',BadClient)
    response=client.post('/api/audio-pack',json={'language':'en-IN'})
    assert response.status_code==502
    receipt=(tmp_path/'runtime/audio-pack-receipts.jsonl').read_text()
    assert 'PRIVATE_KEY_SENTINEL' not in receipt
    assert json.loads(receipt)['status']=='failed'
    assert not list((tmp_path/'runtime/audio').glob('*.mp3'))


def test_account_check_is_not_paid_generation_and_hides_key(client,monkeypatch):
    monkeypatch.setenv('ELEVENLABS_API_KEY','PRIVATE_KEY_SENTINEL')
    monkeypatch.setenv('ELEVENLABS_VOICE_ID','testvoice')
    calls=[]
    class VoiceClient:
        def __init__(self,**kwargs): pass
        async def __aenter__(self): return self
        async def __aexit__(self,*args): pass
        async def get(self,url,**kwargs):
            calls.append(url)
            return httpx.Response(200,request=httpx.Request('GET',url),json={'voice_id':'testvoice','name':'Selected test voice'})
    monkeypatch.setattr(companion.httpx,'AsyncClient',VoiceClient)
    response=client.post('/api/integrations/check')
    assert response.json()['elevenlabs']['verified'] is True
    assert calls==['https://api.elevenlabs.io/v1/voices/testvoice']
    assert 'PRIVATE_KEY_SENTINEL' not in response.text
    assert response.json()['sentry']['verified_remote'] is False


def test_trace_check_missing_dsn_is_not_fake_success(client,monkeypatch):
    monkeypatch.setattr(companion,'SENTRY_ENABLED',False)
    assert client.post('/api/trace-check').status_code==503


def test_evidence_export_excludes_extra_private_fields(client,monkeypatch,tmp_path):
    monkeypatch.setattr(companion,'ROOT',tmp_path)
    companion.TRACE_PATH.parent.mkdir(parents=True,exist_ok=True)
    companion.TRACE_PATH.write_text(json.dumps({'id':'x','status':'accepted','note':'PRIVATE_NOTE','image':'data:image/private'})+'\n')
    result=client.get('/api/integrations/evidence')
    assert result.status_code==200
    assert result.json()['reviews']==[{'id':'x','status':'accepted'}]
    assert 'PRIVATE_NOTE' not in result.text and 'data:image/private' not in result.text
