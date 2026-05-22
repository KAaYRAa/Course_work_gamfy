

let players = [];
let characters = [];
let currentIndex = 0;
let currentCharacter = ""; 
let timer;
let timeLeft;
let winScore = 5;
let totalRoundsPlayed = 0;

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
    .then(data => console.log("ACL статистика успішно зафіксована в БД"))
    .catch(err => console.error("Помилка збереження сесії:", err));
}

function addPlayerInput() {
    const container = document.getElementById('p-inputs');
    const input = document.createElement('input');
    input.className = "p-name w-full bg-white/5 border border-white/10 rounded-2xl px-6 py-4 outline-none mt-2";
    input.placeholder = `Ім'я гравця ${container.querySelectorAll('.p-name').length + 1}`;
    container.appendChild(input);
}

async function startGame() {
    const nameInputs = document.querySelectorAll('.p-name');
    players = []; // Очищуємо масив перед стартом
    nameInputs.forEach(input => {
        if(input.value.trim()) players.push({ name: input.value.trim(), score: 0 });
    });
    if(players.length < 2) return alert("Мінімум 2 гравці");

    winScore = parseInt(document.getElementById('win-score').value);

    try {
        const url = window.WHOAMI_GET_CHARACTERS_URL || '/who_am_i/get_characters/';
        const response = await fetch(url);
        const data = await response.json();
        characters = data.characters;

        document.getElementById('setup').classList.add('hidden');
        document.getElementById('game').classList.remove('hidden');
        startRound();
    } catch (e) {
        alert("Помилка завантаження персонажів з сервера");
    }
}

function startRound() {
    clearInterval(timer);
    timeLeft = parseInt(document.getElementById('round-time').value);
    
    document.getElementById('current-player-name').innerText = players[currentIndex].name;
    
    currentCharacter = characters[Math.floor(Math.random() * characters.length)];
    
    enforceAccessPolicy(false);
    
    updateTimerDisplay();
    timer = setInterval(() => {
        timeLeft--;
        updateTimerDisplay();
        if(timeLeft <= 0) {
            clearInterval(timer);
            alert("Час вийшов!");
            nextTurn();
        }
    }, 1000);
}

function enforceAccessPolicy(hasAccess) {
    const card = document.getElementById('char-card');
    const btnReveal = document.getElementById('btn-reveal');
    const btnHide = document.getElementById('btn-hide');
    const actionControls = document.getElementById('action-controls');

    if (hasAccess) {
        card.innerText = currentCharacter;
        card.classList.remove('text-white/20');
        card.classList.add('text-cyan-400');
        
        btnReveal.classList.add('hidden');
        btnHide.classList.remove('hidden');
        
        actionControls.classList.remove('opacity-40', 'pointer-events-none');
    } else {
        card.innerText = "❓ ❓ ❓";
        card.classList.remove('text-cyan-400');
        card.classList.add('text-white/20');
        
        btnReveal.classList.remove('hidden');
        btnHide.classList.add('hidden');
        
        actionControls.classList.add('opacity-40', 'pointer-events-none');
    }
}

function updateTimerDisplay() {
    const m = Math.floor(timeLeft / 60);
    const s = timeLeft % 60;
    document.getElementById('timer').innerText = `${m.toString().padStart(2,'0')}:${s.toString().padStart(2,'0')}`;
}

function handleResult(isWin) {
    clearInterval(timer);
    totalRoundsPlayed++;
    
    if(isWin) {
        players[currentIndex].score += 1;
        if(players[currentIndex].score >= winScore) return endGame();
    }
    nextTurn();
}

function nextTurn() {
    currentIndex = (currentIndex + 1) % players.length;
    startRound();
}

function endGame() {
    clearInterval(timer);
    document.getElementById('game').classList.add('hidden');
    document.getElementById('finish').classList.remove('hidden');

    players.sort((a,b) => b.score - a.score);
    document.getElementById('winner-name').innerText = `${players[0].name.toUpperCase()} ПЕРЕМІГ!`;

    const table = document.getElementById('results-table');
    table.innerHTML = players.map((p, i) => `
        <div class="flex justify-between items-center py-2 border-b border-white/5 uppercase text-[10px] tracking-widest">
            <span class="opacity-50">${i+1}. ${p.name}</span>
            <span class="text-xl font-black text-cyan-400">${p.score}</span>
        </div>
    `).join('');

    saveSession(4, players[0].score, totalRoundsPlayed);
}