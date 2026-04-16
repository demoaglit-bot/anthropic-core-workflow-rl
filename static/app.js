let state = null;
let activeThreadId = null;

async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: { 'Content-Type': 'application/json' },
    ...options
  });
  return response.json();
}

function currentThread() {
  return state.threads.find((thread) => thread.id === activeThreadId) || state.threads[0];
}

function renderThreads() {
  const root = document.getElementById('thread-list');
  root.innerHTML = '<h2>Threads</h2>' + state.threads.map((thread) => `
    <article class="thread-item ${thread.id === activeThreadId ? 'active' : ''}" data-thread-id="${thread.id}">
      <strong>${thread.title}</strong>
      <div>Status: ${thread.status}</div>
      <div>Messages: ${thread.messages.length}</div>
    </article>
  `).join('');
  root.querySelectorAll('[data-thread-id]').forEach((node) => {
    node.addEventListener('click', () => {
      activeThreadId = node.getAttribute('data-thread-id');
      render();
    });
  });
}

function renderDetail() {
  const thread = currentThread();
  document.getElementById('thread-title').textContent = thread.title;
  document.getElementById('persona').textContent = `${state.persona.name}: ${state.persona.objective}`;
  document.getElementById('draft').value = thread.draft || '';
  document.getElementById('messages').innerHTML = thread.messages.map((message) => `
    <div class="message ${message.role}">
      <strong>${message.author}</strong>
      <p>${message.content}</p>
    </div>
  `).join('');
}

function renderEvents() {
  document.getElementById('events').innerHTML = state.events.slice().reverse().map((event) => `
    <li><strong>${event.type}</strong>: ${event.detail} (reward ${event.reward})</li>
  `).join('');
}

function render() {
  if (!activeThreadId && state.threads.length) {
    activeThreadId = state.threads[0].id;
  }
  renderThreads();
  renderDetail();
  renderEvents();
}

async function refresh() {
  state = await request('/api/state');
  render();
}

document.getElementById('save-draft').addEventListener('click', async () => {
  state = await request('/api/save-draft', {
    method: 'POST',
    body: JSON.stringify({ threadId: activeThreadId, draft: document.getElementById('draft').value })
  });
  render();
});

document.getElementById('send-reply').addEventListener('click', async () => {
  state = await request('/api/send-reply', {
    method: 'POST',
    body: JSON.stringify({ threadId: activeThreadId, message: document.getElementById('draft').value })
  });
  render();
});

document.getElementById('reset-state').addEventListener('click', async () => {
  state = await request('/api/reset', { method: 'POST', body: '{}' });
  render();
});

refresh();
