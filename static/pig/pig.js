

let players = {};
const WORD = "СВИНЯ";

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
    .then(data => console.log("Сесію гри 'Свиня' збережено"))
    .catch(err => console.error("Помилка збереження результатів:", err));
}

function addInput() {
    const div = document.getElementById('p-list');
    const currentCount = div.children.length + 1;
    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'name-in w-full bg-[#1a0101]/60 border border-white/5 rounded-full px-6 py-4 outline-none text-[10px] uppercase tracking-widest focus:border-white/20 transition-all mt-4';
    input.placeholder = `Гравець ${currentCount}`;
    div.appendChild(input);
}

async function initGame() {
    document.querySelectorAll('.name-in').forEach(i => { 
        if(i.value.trim()) players[i.value.trim()] = ""; 
    });
    
    if (Object.keys(players).length < 2) return alert("Потрібно хоча б 2 гравці!");
    
    document.getElementById('setup').classList.add('hidden');
    document.getElementById('game').classList.remove('hidden');
    
    await getTask(); 
    draw();
}

function draw() {
    const grid = document.getElementById('btns');
    grid.innerHTML = "";
    for (let n in players) {
        const progress = players[n];
        grid.innerHTML += `
            <button onclick="addLetter('${n}')" class="player-card bg-[#1a0101]/60 border border-white/5 w-48 h-48 rounded-[40px] flex flex-col items-center justify-center hover:bg-[#1a0101]/80 hover:border-red-500/40 group shadow-lg">
                <p class="text-[10px] text-white/30 uppercase tracking-widest mb-3 group-hover:text-white/60 transition-colors">${n}</p>
                <p class="text-4xl font-black text-red-600 tracking-widest">${progress || '—'}</p>
            </button>`;
    }
}

async function getTask() {
    try {
        const url = window.PIG_GET_TASK_URL || '/pig/get_task/';
        const r = await fetch(url); 
        const d = await r.json();
        document.getElementById('task').innerText = d.task;
    } catch (e) { 
        console.error(e); 
    }
}

async function addLetter(n) {
    try {
        const url = window.PIG_ADD_LETTER_URL || '/pig/add-letter/';
        const res = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value
            },
            body: JSON.stringify({ player_name: n })
        });
        const data = await res.json();
        
        for (let p in data.players) {
            players[p] = data.players[p];
        }

        if (data.is_game_over) {
            document.getElementById('game').classList.add('hidden');
            document.getElementById('finish').classList.remove('hidden');
            const resDiv = document.getElementById('final-stats');
            resDiv.innerHTML = `<p class="text-4xl text-red-600 font-black mb-8">${data.loser.toUpperCase()} — ГОЛОВНА СВИНЯ!</p>`;
            
            let totalLetters = 0;
            for (let p in players) {
                resDiv.innerHTML += `<p class="text-sm">${p}: <span class="text-red-500 font-bold">${players[p] || 'ЧИСТО'}</span></p>`;
                totalLetters += players[p].length;
            }
            saveSession(2, totalLetters, 5);
        } else {
            draw();
            document.getElementById('task').innerText = data.next_task;
        }
    } catch (e) {
        console.error("Помилка серверного додавання літери:", e);
    }
}