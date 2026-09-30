from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_home():
    response = client.get('/')
    assert response.status_code == 200
    assert 'EduGenie' in response.text


def test_qa(monkeypatch):
    monkeypatch.setattr(main, 'answer_question', lambda question: 'The Pacific Ocean is the largest ocean.')
    response = client.post('/qa', json={'question': 'Which is the largest ocean?'})
    assert response.status_code == 200
    assert 'Pacific' in response.json()['answer']


def test_quiz_validation(monkeypatch):
    from quiz_module import QuizItem
    monkeypatch.setattr(main, 'generate_quiz', lambda text, num_questions: [
        QuizItem(question='2+2?', options=['1', '2', '3', '4'], answer='4')
    ])
    response = client.post('/quiz', json={'text': 'Basic arithmetic', 'num_questions': 1})
    assert response.status_code == 200
    assert response.json()['questions'][0]['answer'] == '4'
