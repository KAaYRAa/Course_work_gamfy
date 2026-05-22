
let players = [];
let currentIndex = 0;
let matrixData = []; 
let secretWord = "";
let targetScore = 10;
let totalPuzzlesSolved = 0;
let revealedCount = 0;

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
    .then(data => console.log("Статистику Пазлів успішно збережено"))
    .catch(err => console.error("Помилка збереження:", err));
}

function addPlayerInput() {
    const container = document.getElementById('p-inputs');
    const input = document.createElement('input');
    input.type = 'text';
    input.className = "p-name w-full bg-white/5 border border-white/10 rounded-2xl px-6 py-4 outline-none focus:border-cyan-500/30 transition-all mt-2";
    input.placeholder = `Гравець ${container.querySelectorAll('.p-name').length + 1}`;
    container.appendChild(input);
}

async function startGame() {
    players = [];
    document.querySelectorAll('.p-name').forEach(i => {
        if(i.value.trim()) players.push({ name: i.value.trim(), score: 0 });
    });
    if(players.length < 2) return alert("Введіть мінімум 2 імені!");

    targetScore = parseInt(document.getElementById('win-score').value) || 10;
    document.getElementById('total-progress').innerText = `Ціль: ${targetScore} балів`;

    await loadNewPuzzle();
    document.getElementById('setup').classList.add('hidden');
    document.getElementById('game').classList.remove('hidden');
}

async function loadNewPuzzle() {
    try {
        const url = window.PUZZLE_GET_DATA_URL || '/puzzle/get_data/';
        const res = await fetch(url);
        const data = await res.json();
        if (data.error) return alert(data.error);

        matrixData = data.puzzle_matrix;
        secretWord = data.secret_word.toLowerCase().trim();
        revealedCount = 0;

        renderMatrixHTML(); 
        revealRandomMatrixCell(); 
        updateUI();
    } catch (e) {
        alert("Помилка завантаження даних матриці");
    }
}

function renderMatrixHTML() {
    const container = document.getElementById('puzzle-matrix-container');
    container.innerHTML = "";
    
    for(let r=0; r<3; r++) {
        for(let c=0; c<3; c++) {
            container.innerHTML += `
                <div id="cell-${r}-${c}" class="puzzle-segment w-full h-full bg-cyan-950/60 border border-cyan-500/20 rounded-xl flex items-center justify-center p-2 text-[10px] text-cyan-400 font-bold tracking-tighter uppercase shadow-inner">
                    🧩
                </div>`;
        }
    }
}

function revealRandomMatrixCell() {
    let closedCells = [];
    for(let r=0; r<3; r++) {
        for(let c=0; c<3; c++) {
            if(!matrixData[r][c].is_revealed) {
                closedCells.push({row: r, col: c});
            }
        }
    }

    if(closedCells.length > 0) {
        let randomPick = closedCells[Math.floor(Math.random() * closedCells.length)];
        let cell = matrixData[randomPick.row][randomPick.col];
        cell.is_revealed = true;
        revealedCount++;

        const element = document.getElementById(`cell-${randomPick.row}-${randomPick.col}`);
        element.className = "w-full h-full bg-white/5 border border-white/10 rounded-xl flex items-center justify-center p-2 text-[9px] text-white font-light transition-all duration-500 scale-95";
        element.innerText = cell.text;

        if (revealedCount > 1) nextTurn();
    } else {
        alert("Весь пазл відкрито!");
    }
}

function calculatePoints() {
    if (revealedCount <= 2) return 5;
    if (revealedCount <= 4) return 4;
    if (revealedCount <= 6) return 3;
    if (revealedCount <= 8) return 2;
    return 1;
}

function updateUI() {
    document.getElementById('current-player').innerText = `Зараз ходить: ${players[currentIndex].name}`;
    document.getElementById('score-info').innerText = `Балів за вгадування: ${calculatePoints()}`;
}

function nextTurn() {
    currentIndex = (currentIndex + 1) % players.length;
    document.getElementById('guess-input-block').classList.add('hidden');
    updateUI();
}

function showGuessInput() {
    document.getElementById('guess-input-block').classList.toggle('hidden');
    if (!document.getElementById('guess-input-block').classList.contains('hidden')) {
        document.getElementById('guess-text').focus();
    }
}

async function checkGuess() {
    const val = document.getElementById('guess-text').value.toLowerCase().trim();
    
    try {
        const url = window.PUZZLE_CHECK_GUESS_URL || '/puzzle/check-guess/';
        const res = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value
            },
            body: JSON.stringify({ guess: val, secret_word: secretWord })
        });
        const data = await res.json();

        if (data.is_correct) {
            let earned = calculatePoints();
            players[currentIndex].score += earned;
            totalPuzzlesSolved++;
            
            if (players[currentIndex].score >= targetScore) {
                showFinalResults();
            } else {
                alert(`Правильно! +${earned} балів.`);
                loadNewPuzzle();
            }
        } else {
            alert("Невірно! Хід переходить далі.");
            nextTurn();
        }
    } catch (e) {
        console.error("Помилка серверної валідації:", e);
    }
}

function showFinalResults() {
    document.getElementById('game').classList.add('hidden');
    document.getElementById('finish').classList.remove('hidden');
    players.sort((a,b) => b.score - a.score);
    document.getElementById('winner-announce').innerText = `ПЕРЕМІГ ${players[0].name.toUpperCase()}!`;

    const table = document.getElementById('final-table');
    table.innerHTML = players.map(p => `
        <div class="flex justify-between border-b border-white/5 py-4 uppercase text-[10px] tracking-widest">
            <span>${p.name}</span>
            <span class="text-cyan-400 font-black">${p.score} / ${targetScore}</span>
        </div>
    `).join('');

    saveSession(4, players[0].score, totalPuzzlesSolved);
}