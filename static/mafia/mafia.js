

let totalPlayersCount = 0;
let currentPlayerId = 1;
let currentStep = 1;
let timerInterval;

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
    .then(data => console.log("Сесію Мафії збережено"))
    .catch(err => console.error("Помилка збереження Мафії:", err));
}

async function distributeRoles() {
    const counts = {
        'Мирний': parseInt(document.getElementById('count-civil').value) || 0,
        'Мафія': parseInt(document.getElementById('count-mafia').value) || 0,
        'Шериф': parseInt(document.getElementById('count-sheriff').value) || 0,
        'Лікар': parseInt(document.getElementById('count-doctor').value) || 0
    };

    let total = Object.values(counts).reduce((a, b) => a + b, 0);
    if (total < 2) return alert("Потрібно хоча б 2 гравці!");

    try {

        const url = window.MAFIA_DISTRIBUTE_URL || "/mafia/distribute_roles/";
        const res = await fetch(url, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json', 
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value 
            },
            body: JSON.stringify({ counts: counts })
        });

        const data = await res.json();
        totalPlayersCount = data.total_players;
        currentStep = data.current_step;

        document.getElementById('setup').classList.add('hidden');
        document.getElementById('role-reveal').classList.remove('hidden');
        updateRevealScreen();
    } catch (e) {
        alert("Помилка розподілу ролей на сервері");
    }
}

async function updateRevealScreen() {
    document.getElementById('player-label').innerText = `Гравець ${currentPlayerId}`;

    const res = await fetch(`/mafia/get_my_role/?player_id=${currentPlayerId}`);
    const data = await res.json();

    document.getElementById('role-name').innerText = data.role;
    document.getElementById('role-name').style.color = data.role === 'Мафія' ? '#dc2626' : '#10b981';

    document.getElementById('card-front').classList.remove('hidden');
    document.getElementById('card-back').classList.add('hidden');
    document.getElementById('next-player-btn').classList.add('hidden');
}

function revealRole() {
    document.getElementById('card-front').classList.add('hidden');
    document.getElementById('card-back').classList.remove('hidden');
    document.getElementById('next-player-btn').classList.remove('hidden');
}

function nextPlayer() {
    currentPlayerId++;
    if (currentPlayerId <= totalPlayersCount) {
        updateRevealScreen();
    } else {
        document.getElementById('role-reveal').classList.add('hidden');
        document.getElementById('game-flow').classList.remove('hidden');

        runTimer(60, "Ніч 1", "Знайомство гравців з ведучим. Місто засинає...", () => {
            document.getElementById('next-phase-btn').classList.remove('hidden');
            const btn = document.getElementById('next-phase-btn');
            btn.innerText = "Ранок: Хто загинув?";
            
            let initialAlive = [];
            for(let i = 1; i <= totalPlayersCount; i++) {
                initialAlive.push({id: i, name: `Гравець ${i}`});
            }
            btn.onclick = () => startDayPhase(initialAlive);
        });
    }
}

function runTimer(seconds, title, desc, callback) {
    document.getElementById('phase-title').innerText = title;
    document.getElementById('phase-desc').innerText = desc;
    let timeLeft = seconds;

    clearInterval(timerInterval);
    timerInterval = setInterval(() => {
        let mins = Math.floor(timeLeft / 60);
        let secs = timeLeft % 60;
        document.getElementById('timer').innerText = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            if (callback) callback();
        }
        timeLeft--;
    }, 1000);
}

async function handleElimination(playerId) {
    const res = await fetch("/mafia/eliminate_player/", {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json', 
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value 
        },
        body: JSON.stringify({ player_id: playerId })
    });
    const data = await res.json();

    if (data.game_over) {
        showWinner(data.winner, data.final_distribution);
        return;
    }

    currentStep = data.current_step;
    document.getElementById('role-reveal').classList.add('hidden');
    document.getElementById('game-flow').classList.remove('hidden');

    let roundNumber = Math.floor(currentStep / 2) + 1;
    
    if (currentStep % 2 === 0) {
        buildSelectionGrid(data.alive_players, "night");
        runTimer(60, `Ніч ${roundNumber}`, "Мафія обирає жертву, Лікар рятує...", () => {
            document.getElementById('next-phase-btn').classList.remove('hidden');
            document.getElementById('next-phase-btn').innerText = "Ранок: Хто загинув?";
            document.getElementById('next-phase-btn').onclick = () => startDayPhase(data.alive_players);
        });
    } else {
        startDiscussion(data.alive_players);
    }
}

function startDayPhase(alivePlayers) {
    document.getElementById('next-phase-btn').classList.add('hidden');
    let roundNumber = Math.floor(currentStep / 2) + 1;
    document.getElementById('phase-title').innerText = `Ранок ${roundNumber}`;
    document.getElementById('phase-desc').innerText = "Оберіть гравця, який вибуває за результатами ночі";
    document.getElementById('timer').innerText = "💀";
    buildSelectionGrid(alivePlayers, "day-kill");
}

function buildSelectionGrid(alivePlayers, mode) {
    const container = document.getElementById('alive-players');
    container.innerHTML = "";

    if (mode === "day-kill") {
        const nobodyBtn = document.createElement('button');
        nobodyBtn.className = "col-span-2 md:col-span-4 bg-green-500/10 border border-green-500/20 py-4 rounded-2xl text-[9px] uppercase tracking-widest text-green-400 mb-4";
        nobodyBtn.innerText = "Ніхто не загинув (Пропустити)";
        nobodyBtn.onclick = () => startDiscussion(alivePlayers);
        container.appendChild(nobodyBtn);
    }

    alivePlayers.forEach(p => {
        const btn = document.createElement('button');
        btn.className = "bg-white/5 border border-white/10 p-6 rounded-[25px] hover:bg-red-600/20 transition-all text-[10px] uppercase tracking-widest";
        btn.innerText = p.name;
        btn.onclick = () => {
            if (mode === "day-kill" || mode === "vote") {
                handleElimination(p.id); 
            }
        };
        container.appendChild(btn);
    });
}

function startDiscussion(alivePlayers) {
    let idx = 0;
    function nextTurn() {
        if (idx < alivePlayers.length) {
            runTimer(30, "Обговорення", `Слово має ${alivePlayers[idx].name}`, nextTurn);
            idx++;
        } else {
            startVoting(alivePlayers);
        }
    }
    nextTurn();
}

function startVoting(alivePlayers) {
    let roundNumber = Math.floor(currentStep / 2) + 1;
    document.getElementById('phase-title').innerText = `Голосування ${roundNumber}`;
    document.getElementById('phase-desc').innerText = "Оберіть, кого виганяє місто на загальному голосуванні";
    document.getElementById('timer').innerText = "🗳️";
    buildSelectionGrid(alivePlayers, "vote");
}

function showWinner(winner, finalDistribution) {
    document.getElementById('game-flow').classList.add('hidden');
    document.getElementById('finish').classList.remove('hidden');

    const title = document.getElementById('winner-title');
    title.innerText = `ПЕРЕМОГА: ${winner}`;
    title.style.color = winner === 'Мафія' ? '#dc2626' : '#10b981';

    const list = document.getElementById('roles-list');
    list.innerHTML = "";
    for (let pid in finalDistribution) {
        list.innerHTML += `
            <div class="flex justify-between items-center py-2 border-b border-white/5">
                <span class="text-[10px] uppercase tracking-widest opacity-40">Гравець ${pid}</span>
                <span class="text-[10px] uppercase font-bold ${finalDistribution[pid] === 'Мафія' ? 'text-red-500' : 'text-green-400'}">${finalDistribution[pid]}</span>
            </div>`;
    }

    saveSession(3, Object.keys(finalDistribution).length, currentStep);
}