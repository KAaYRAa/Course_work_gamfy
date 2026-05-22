

let players = [];
let words = [];
let currentGroupIdx = 0;
let roundNum = 1;
let timeLeft;
let timerInterval;
let isOvertime = false;
let roundStartTime = 60;
let currentRoundVotes = 0; 
let pointsPerWord = 2; 
const WIN_SCORE = 15; 

function saveSession(gameId, finalScore, steps = 0) {
    fetch('/games/save_result/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value
        },
        body: JSON.stringify({ game_id: gameId, score: finalScore, steps: steps })
    })
    .then(res => res.json())
    .then(data => console.log("Сесію Крокодила успішно зафіксовано в БД"))
    .catch(err => console.error("Помилка збереження результату Крокодила:", err));
}

async function startGame() {
    players = [];
    document.querySelectorAll('.p-name').forEach(i => {
        if(i.value.trim()) players.push({ name: i.value.trim(), score: 0 });
    });
    
    if (players.length < 2) return alert("Введіть мінімум 2 команди!");
    
    roundStartTime = parseInt(document.getElementById('round-time').value) || 60;
    
    const diff = document.getElementById('difficulty-select').value;
    const cat = document.getElementById('category-select').value;

    if (diff === 'easy') pointsPerWord = 1;
    if (diff === 'medium') pointsPerWord = 2;
    if (diff === 'hard') pointsPerWord = 3;

    try {
        const baseUrl = window.CROCODILE_WORDS_URL || "/crocodile/get-words/";
        const url = baseUrl + "?difficulty=" + diff + "&category=" + cat;
        
        const res = await fetch(url);
        const data = await res.json();
        
        words = data.words;
        
        if (!words || words.length === 0) {
            words = ["Крокодил", "Машина", "Сонце"];
        }

        document.getElementById('setup').classList.add('hidden');
        document.getElementById('game').classList.remove('hidden');
        startGroupTurn();
        
    } catch (e) {
        console.error("Критична помилка завантаження слів Крокодила:", e);
        alert("Помилка зв'язку з сервером. Гра запущена в автономному режимі.");
        
        words = ["Крокодил", "Телефон", "Ноутбук", "Кава", "Курсова"];
        document.getElementById('setup').classList.add('hidden');
        document.getElementById('game').classList.remove('hidden');
        startGroupTurn();
    }
}

function startGroupTurn() {
    isOvertime = false;
    timeLeft = roundStartTime;
    document.getElementById('overtime-msg').classList.add('hidden');
    document.getElementById('card').classList.remove('overtime-pulse');
    document.getElementById('current-player-display').innerText = `Показує: ${players[currentGroupIdx].name}`;
    document.getElementById('round-info').innerText = `Раунд ${roundNum}`;
    
    getNewWord();
    runTimer();
}

function runTimer() {
    clearInterval(timerInterval);
    timerInterval = setInterval(() => {
        timeLeft--;
        updateUI();
        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            enterOvertime();
        }
    }, 1000);
}

function updateUI() {
    const m = Math.floor(Math.max(0, timeLeft) / 60);
    const s = Math.max(0, timeLeft) % 60;
    document.getElementById('timer-display').innerText = `${m.toString().padStart(2,'0')}:${s.toString().padStart(2,'0')}`;
    document.getElementById('time-bar').style.width = `${(Math.max(0, timeLeft) / roundStartTime) * 100}%`;
}

function enterOvertime() {
    isOvertime = true;
    document.getElementById('overtime-msg').classList.remove('hidden');
    document.getElementById('card').classList.add('overtime-pulse');
    document.getElementById('timer-display').innerText = "00:00";
    document.getElementById('time-bar').style.width = "0%";
}

function getNewWord() {
    document.getElementById('word-text').innerText = words[Math.floor(Math.random() * words.length)];
}

function handleWord(success) {
    if (success) players[currentGroupIdx].score += pointsPerWord;

    if (!isOvertime) {
        getNewWord();
    } else {
        endGroupTurn();
    }
}

function endGroupTurn() {
    currentRoundVotes++;
    let winner = players.find(p => p.score >= WIN_SCORE);

    if (winner && currentRoundVotes === players.length) {
        showFinal(winner); 
    } else if (currentRoundVotes < players.length) {
        currentGroupIdx = (currentGroupIdx + 1) % players.length;
        alert(`Хід переходить до команди: ${players[currentGroupIdx].name}`);
        startGroupTurn();
    } else {
        showRoundResults();
    }
}

function showRoundResults() {
    document.getElementById('game').classList.add('hidden');
    document.getElementById('round-results').classList.remove('hidden');
    
    const stats = document.getElementById('round-stats');
    stats.innerHTML = players.map(p => `
        <div class="flex justify-between items-center border-b border-white/5 py-3 uppercase text-[10px] tracking-widest">
            <span class="opacity-40">${p.name}</span>
            <span class="text-green-400 font-black">${p.score} БАЛІВ</span>
        </div>
    `).join('');
}

function showFinal(winner) {
    document.getElementById('game').classList.add('hidden');
    document.getElementById('round-results').classList.add('hidden');
    document.getElementById('finish-screen').classList.remove('hidden'); 
    document.getElementById('winner-announce').innerText = `КОМАНДА ${winner.name.toUpperCase()} ПЕРЕМОГЛА З РЕЗУЛЬТАТОМ ${winner.score} БАЛІВ!`;
    
    saveSession(10, winner.score, roundNum);
}

function nextRound() {
    roundNum++;
    currentRoundVotes = 0;
    currentGroupIdx = 0; 
    document.getElementById('round-results').classList.add('hidden');
    document.getElementById('game').classList.remove('hidden');
    startGroupTurn();
}