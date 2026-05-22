

let gameData = { teams: [], scores: {}, currentTeam: 0, time: 60, target: 50 };
let roundPoints = 0;
let timer;

async function initGame() {
    const inputs = document.querySelectorAll('.team-input');
    gameData.teams = Array.from(inputs).map(i => i.value || i.placeholder);
    gameData.time = parseInt(document.getElementById('time-input').value) || 60;
    gameData.target = parseInt(document.getElementById('score-input').value) || 50;
    gameData.teams.forEach(t => gameData.scores[t] = 0);

    document.getElementById('setup-screen').classList.add('hidden');
    document.getElementById('game-screen').classList.remove('hidden');
    updateTurnInfo();
}

function updateTurnInfo() {
    document.getElementById('active-team').innerText = gameData.teams[gameData.currentTeam];
    document.getElementById('timer-display').innerText = gameData.time;
    document.getElementById('ready-block').classList.remove('hidden');
    document.getElementById('play-block').classList.add('hidden');
    document.getElementById('word-display').innerText = "---";
    roundPoints = 0;
}

async function startRound() {
    document.getElementById('ready-block').classList.add('hidden');
    document.getElementById('play-block').classList.remove('hidden');

    await nextWord();

    let sec = gameData.time;
    document.getElementById('timer-display').innerText = sec;

    timer = setInterval(() => {
        sec--;
        document.getElementById('timer-display').innerText = sec;
        if (sec <= 0) {
            finishRound();
        }
    }, 1000);
}

async function nextWord() {
    try {
        const res = await fetch("/alias/get-words/");
        const data = await res.json();

        if (data.word) {
            document.getElementById('word-display').innerText = data.word;
        } else {
            document.getElementById('word-display').innerText = "Помилка слів";
        }
    } catch (err) {
        console.error("Помилка завантаження наступного слова:", err);
        document.getElementById('word-display').innerText = "Збій зв'язку";
    }
}

async function handleWord(hit) {
    hit ? roundPoints++ : roundPoints--;
    await nextWord();
}

function finishRound() {
    clearInterval(timer);
    gameData.scores[gameData.teams[gameData.currentTeam]] += roundPoints;

    document.getElementById('game-screen').classList.add('hidden');
    document.getElementById('score-screen').classList.remove('hidden');

    const stats = document.getElementById('final-stats');
    stats.innerHTML = "";
    let winner = null;

    gameData.teams.forEach(t => {
        if (gameData.scores[t] >= gameData.target) winner = t;
        stats.innerHTML += `
            <div class="flex justify-between uppercase text-[10px] tracking-widest py-2 border-b border-white/5">
                <span>${t}</span>
                <span class="font-bold">${gameData.scores[t]}</span>
            </div>`;
    });

    if (winner) {
        document.getElementById('score-title').innerText = "Гра завершена!";
        stats.innerHTML = `<h1 class="text-3xl font-bold py-10 uppercase tracking-widest">${winner} переміг!</h1>`;

        if (typeof saveSession === 'function') {
            saveSession(1, gameData.scores[winner], 0);
        }
    
        document.getElementById('action-btn').innerText = "До правил";
        document.getElementById('action-btn').onclick = () => {
            window.location.href = "/"; 
        };
    }
}

function nextRound() {
    document.getElementById('score-screen').classList.add('hidden');
    document.getElementById('game-screen').classList.remove('hidden');
    
    gameData.currentTeam = (gameData.currentTeam + 1) % gameData.teams.length;
    updateTurnInfo();
}