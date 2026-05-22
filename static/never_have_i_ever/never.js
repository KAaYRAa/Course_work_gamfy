

let sessionSteps = 0; 

function saveSession(gameId, finalScore, steps = 0) {
    fetch('/games/save_result/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value
        },
        body: JSON.stringify({
            game_id: gameId,
            score: finalScore,
            steps: steps
        })
    })
    .then(res => res.json())
    .then(data => console.log("Крок гри 'Я ніколи не...' збережено в БД"))
    .catch(err => console.error("Помилка логування сесії:", err));
}

function startGame() {
    document.getElementById('setup').classList.add('hidden');
    document.getElementById('game').classList.remove('hidden');
    nextRound(); 
}

async function nextRound() {
    sessionSteps++; 
    const card = document.getElementById('game-card');
    

    card.classList.remove('card-anim');
    void card.offsetWidth; 
    card.classList.add('card-anim');

    try {

        const url = window.NEVER_GET_DATA_URL || '/never_have_i_ever/get_data/';
        const res = await fetch(url);
        const data = await res.json();

        if (data.error) {
            console.error("Сервер повернув помилку:", data.error);
            document.getElementById('question-text').innerText = "Питання закінчилися або не знайдені.";
            return;
        }

        document.getElementById('question-text').innerText = data.question;
        document.getElementById('action-text').innerText = data.action;

        saveSession(8, sessionSteps, sessionSteps);

    } catch (e) {
        console.error("Критичний збій завантаження раунду:", e);
        document.getElementById('question-text').innerText = "Не вдалося отримати унікальне питання від сервера.";
        document.getElementById('action-text').innerText = "Зроби ковток напою";
    }
}