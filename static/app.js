async function postJSON(url, body) {
  const response = await fetch(url, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(body)
  });
  const data = await response.json().catch(() => ({detail: 'Server returned an invalid response.'}));
  if (!response.ok) throw new Error(data.detail || 'Request failed.');
  return data;
}

function show(id, content, isError = false) {
  const el = document.getElementById(id);
  el.className = `output show${isError ? ' error' : ''}`;
  if (typeof content === 'string') el.textContent = content;
  else el.innerHTML = content;
}

async function runQA() {
  const input = document.getElementById('qa-input').value.trim();
  if (!input) return show('qa-output', 'Enter a question first.', true);
  show('qa-output', 'Thinking…');
  try { const d = await postJSON('/qa', {question: input}); show('qa-output', d.answer); }
  catch (e) { show('qa-output', e.message, true); }
}

async function runExplain() {
  const input = document.getElementById('explain-input').value.trim();
  if (!input) return show('explain-output', 'Enter a topic first.', true);
  show('explain-output', 'Explaining…');
  try { const d = await postJSON('/explain', {topic: input}); show('explain-output', d.explanation); }
  catch (e) { show('explain-output', e.message, true); }
}

async function runSummary() {
  const input = document.getElementById('summary-input').value.trim();
  if (!input) return show('summary-output', 'Paste some text first.', true);
  show('summary-output', 'Summarizing…');
  try { const d = await postJSON('/summarize', {text: input}); show('summary-output', d.summary); }
  catch (e) { show('summary-output', e.message, true); }
}

async function runQuiz() {
  const input = document.getElementById('quiz-input').value.trim();
  const count = Number(document.getElementById('quiz-count').value);
  if (!input) return show('quiz-output', 'Paste a passage or topic first.', true);
  show('quiz-output', 'Generating quiz…');
  try {
    const d = await postJSON('/quiz', {text: input, num_questions: count});
    renderQuiz(d.questions);
  } catch (e) { show('quiz-output', e.message, true); }
}

function renderQuiz(questions) {
  const wrapper = document.getElementById('quiz-output');
  wrapper.className = 'output show';
  wrapper.innerHTML = '';
  let score = 0;
  const scoreEl = document.createElement('div');
  scoreEl.className = 'quiz-result';
  scoreEl.textContent = `Score: 0/${questions.length}`;
  wrapper.appendChild(scoreEl);

  questions.forEach((q, index) => {
    const item = document.createElement('div'); item.className = 'quiz-item';
    const title = document.createElement('strong'); title.textContent = `${index + 1}. ${q.question}`; item.appendChild(title);
    const options = document.createElement('div'); options.className = 'quiz-options';
    q.options.forEach(option => {
      const btn = document.createElement('button'); btn.type = 'button'; btn.textContent = option;
      btn.onclick = () => {
        if (btn.dataset.answered) return;
        btn.dataset.answered = 'true';
        if (option === q.answer) { btn.classList.add('correct'); score++; }
        else {
          btn.classList.add('wrong');
          [...options.children].find(x => x.textContent === q.answer)?.classList.add('correct');
        }
        [...options.children].forEach(x => x.disabled = true);
        scoreEl.textContent = `Score: ${score}/${questions.length}`;
      };
      options.appendChild(btn);
    });
    item.appendChild(options); wrapper.appendChild(item);
  });
}

async function runLearningPath() {
  const topic = document.getElementById('learn-input').value.trim();
  const level = document.getElementById('learn-level').value;
  if (!topic) return show('learn-output', 'Enter a topic first.', true);
  show('learn-output', 'Building your learning path…');
  try { const d = await postJSON('/learn/recommendations', {topic, level}); show('learn-output', d.recommendations); }
  catch (e) { show('learn-output', e.message, true); }
}
