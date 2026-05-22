

let players = [];
let questions = [];
let currentIndex = 0;
let currentQuestionIndex = 0; 
let timerSeconds = 5;
let winScore = 5;
let timerInterval;
let timeLeft;

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
    .then(data => console.log("Сесію гри '5 секунд' збережено"))
    .catch(err => console.error("Помилка збереження результатів:", err));
}

function addPlayerInput() {
    const container = document.getElementById('p-inputs');
    const input = document.createElement('input');
    input.className = "p-name w-full bg-white/5 border border-white/10 rounded-2xl px-6 py-4 outline-none mt-2";
    input.placeholder = `Гравець ${container.querySelectorAll('.p-name').length + 1}`;
    container.appendChild(input);
}

async function startGame() {
    const inputs = document.querySelectorAll('.p-name');
    players = []; 
    inputs.forEach(i => { if(i.value.trim()) players.push({ name: i.value.trim(), score: 0 }); });
    if(players.length < 2) return alert("Потрібно хоча б 2 гравці!");

    timerSeconds = parseInt(document.getElementById('timer-choice').value);
    winScore = parseInt(document.getElementById('win-score').value);

    try {
        const url = window.FIVESEC_GET_QUESTIONS_URL || '/five_seconds/get_questions/';
        const res = await fetch(url);
        const data = await res.json();
        questions = data.questions;
        currentQuestionIndex = 0; 

        document.getElementById('setup').classList.add('hidden');
        document.getElementById('game').classList.remove('hidden');
        nextTurn();
    } catch (e) {
        alert("Помилка завантаження питань");
    }
}

function startTimer() {
    timeLeft = timerSeconds;
    const timerContainer = document.getElementById('timer-container');
    const timerText = document.getElementById('timer-text');
    const progressLine = document.getElementById('progress-line');
    
    timerContainer.classList.remove('timer-panic', 'border-red-600');
    progressLine.style.width = '100%';
    
    clearInterval(timerInterval);
    timerInterval = setInterval(() => {
        timeLeft -= 0.1;
        timerText.innerText = Math.ceil(timeLeft);
        progressLine.style.width = `${(timeLeft / timerSeconds) * 100}%`;

        if(timeLeft <= 2) {
            timerContainer.classList.add('timer-panic', 'border-red-600');
        }

        if(timeLeft <= 0) {
            clearInterval(timerInterval);
            handleAnswer(false); 
        }
    }, 100); 
}

async function handleAnswer(isSuccess) {
    clearInterval(timerInterval);

    try {
        const url = window.FIVESEC_VALIDATE_URL || '/five_seconds/validate-answer/';
        const res = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value
            },
            body: JSON.stringify({ is_success: isSuccess, selected_ttl: timerSeconds })
        });
        const data = await res.json();

        if(data.is_valid) {
            players[currentIndex].score += 1;
            if(players[currentIndex].score >= winScore) return showFinal();
        } else if (!data.is_valid && isSuccess) {
            alert("Запізно! Сервер зафіксував перевищення ліміту часу.");
        }
    } catch (e) {
        console.error(e);
    }

    currentIndex = (currentIndex + 1) % players.length;
    nextTurn();
}

async function nextTurn() {
    document.getElementById('current-player-display').innerText = `Зараз відповідає: ${players[currentIndex].name}`;
    document.getElementById('question-card').innerText = questions[currentQuestionIndex];
    currentQuestionIndex = (currentQuestionIndex + 1) % questions.length;

    try {
        const url = window.FIVESEC_START_TIMER_URL || '/five_seconds/start-timer/';
        await fetch(url);
    } catch (e) {
        console.error(e);
    }
    
    startTimer();
}

function showFinal() {
    document.getElementById('game').classList.add('hidden');
    document.getElementById('finish').classList.remove('hidden');
    
    players.sort((a,b) => b.score - a.score);
    document.getElementById('winner-text').innerText = `${players[0].name} ПЕРЕМІГ!`;

    const table = document.getElementById('stats-table');
    table.innerHTML = players.map((p, i) => `
        <div class="flex justify-between items-center py-2 border-b border-white/5">
            <span class="opacity-50 text-[10px] uppercase font-bold">${i+1}. ${p.name}</span>
            <span class="text-xl font-black text-yellow-500">${p.score}</span>
        </div>
    `).join('');

    saveSession(6, players[0].score, winScore);
}