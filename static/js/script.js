const questionForm = document.getElementById('question-form');
const questionInput = document.getElementById('question-input');
const resultForm = document.getElementById('result-form');
const loadingMessage = document.getElementById('loading-message');

function showResult(result) {
    resultForm.innerText = result;
}

questionForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const question = questionInput.value;
    questionInput.value = '';

    loadingMessage.innerText = 'Ожидание ответа...';

    try {
        const response = await fetch('/messageAI', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "question": question })
        });

        const data = await response.json();
        showResult(data.result);
        loadingMessage.innerText = ''; // Скрыть сообщение о загрузке после получения ответа
    } catch (error) {
        console.error(error);
        loadingMessage.innerText = ''; // Скрыть сообщение о загрузке в случае ошибки
    }
});