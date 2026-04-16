#!/usr/bin/env python3
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import json
import os
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / 'data'
STATIC_DIR = ROOT / 'static'
SEED_PATH = DATA_DIR / 'seed_state.json'
STATE_PATH = DATA_DIR / 'runtime_state.json'


def load_json(path: Path):
    with path.open('r', encoding='utf-8') as handle:
        return json.load(handle)


def save_json(path: Path, payload):
    with path.open('w', encoding='utf-8') as handle:
        json.dump(payload, handle, indent=2)


def ensure_state():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not STATE_PATH.exists():
        save_json(STATE_PATH, load_json(SEED_PATH))


class Handler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        parsed = urlparse(path)
        clean = parsed.path.lstrip('/')
        if not clean:
            clean = 'index.html'
        return str((STATIC_DIR / clean).resolve())

    def _json(self, payload, code=200):
        body = json.dumps(payload).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/api/state':
            ensure_state()
            self._json(load_json(STATE_PATH))
            return
        if parsed.path == '/api/spec':
            spec = (ROOT / 'api' / 'openapi.yaml').read_text(encoding='utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/yaml; charset=utf-8')
            self.end_headers()
            self.wfile.write(spec.encode('utf-8'))
            return
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        ensure_state()
        length = int(self.headers.get('Content-Length', '0'))
        body = self.rfile.read(length) if length else b'{}'
        payload = json.loads(body or b'{}')
        state = load_json(STATE_PATH)

        if parsed.path == '/api/reset':
            seed = load_json(SEED_PATH)
            save_json(STATE_PATH, seed)
            self._json(seed)
            return

        if parsed.path == '/api/send-reply':
            thread_id = payload.get('threadId')
            message = (payload.get('message') or '').strip()
            if not thread_id or not message:
                self._json({'error': 'threadId and message are required'}, code=400)
                return
            thread = next((item for item in state['threads'] if item['id'] == thread_id), None)
            if thread is None:
                self._json({'error': 'thread not found'}, code=404)
                return
            thread['messages'].append({
                'role': 'assistant',
                'author': 'RL Agent',
                'content': message,
                'status': 'sent'
            })
            state['events'].append({
                'type': 'send_reply',
                'threadId': thread_id,
                'reward': 1.0,
                'detail': 'Agent sent a reply in the active thread.'
            })
            save_json(STATE_PATH, state)
            self._json(state)
            return

        if parsed.path == '/api/save-draft':
            thread_id = payload.get('threadId')
            draft = payload.get('draft', '')
            thread = next((item for item in state['threads'] if item['id'] == thread_id), None)
            if thread is None:
                self._json({'error': 'thread not found'}, code=404)
                return
            thread['draft'] = draft
            state['events'].append({
                'type': 'save_draft',
                'threadId': thread_id,
                'reward': 0.2,
                'detail': 'Agent updated the draft state.'
            })
            save_json(STATE_PATH, state)
            self._json(state)
            return

        self._json({'error': 'unknown endpoint'}, code=404)


if __name__ == '__main__':
    os.chdir(STATIC_DIR)
    ensure_state()
    port = int(os.environ.get('PORT', '8000'))
    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    print(f'Anthropic core workflow RL environment running at http://127.0.0.1:{port}')
    server.serve_forever()
