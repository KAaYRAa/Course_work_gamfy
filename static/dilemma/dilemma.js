

let allDilemmas = [];
let currentIndex = 0;
let agreedCount = 0;
let totalAnswered = 0;

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
    .then(data => console.log("Підсумкову статистику Дилеми успішно зафіксовано в БД"))
    .catch(err => console.error("Помилка збереження результату:", err));
}

async function startGame() {
    try {
        const url = window.DILEMMA_DATA_URL || '/dilemma/get_data/';
        const res = await fetch(url);
        const data = await res.json();
        allDilemmas = data.dilemmas; 
        
        document.getElementById('setup').classList.add('hidden');
        document.getElementById('game').classList.remove('hidden');
        showDilemma();
    } catch (e) { 
        alert("Помилка завантаження"); 
    }
}

function showDilemma() {
    if (currentIndex >= allDilemmas.length) {
        finishGame();
        return;
    }
    
    document.getElementById('stats-overlay').classList.add('hidden');
    document.getElementById('btn-next').classList.add('hidden');
    document.getElementById('vote-buttons').classList.remove('opacity-20', 'pointer-events-none');

    document.getElementById('dilemma-text').innerText = allDilemmas[currentIndex].content_text;
    document.getElementById('q-counter').innerText = `Питання: ${currentIndex + 1}`;
    
    const card = document.getElementById('card');
    card.classList.remove('dilemma-card');
    void card.offsetWidth; 
    card.classList.add('dilemma-card');
}

async function handleVote(isAgreed) {
    totalAnswered++;
    if (isAgreed) agreedCount++;

    const currentDilemmaId = allDilemmas[currentIndex].id;
    document.getElementById('vote-buttons').classList.add('opacity-20', 'pointer-events-none');

    try {
        const url = window.DILEMMA_VOTE_URL || '/dilemma/vote_dilemma/';
        const res = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value
            },
            body: JSON.stringify({ dilemma_id: currentDilemmaId, is_agreed: isAgreed })
        });
        
        const data = await res.json();

        const targetPercent = isAgreed ? data.global_agreed_percent : data.global_disagreed_percent;
        document.getElementById('community-stat').innerText = `${targetPercent}% користувачів відповіли так само (всього голосів: ${data.total_community_votes})`;
        document.getElementById('stats-overlay').classList.remove('hidden');
        document.getElementById('btn-next').classList.remove('hidden');

    } catch (e) {
        console.error("Статистичний аналізатор недоступний", e);
        showNextDilemma(); 
    }
}

function showNextDilemma() {
    currentIndex++;
    showDilemma();
}

function finishGame() {
    document.getElementById('game').classList.add('hidden');
    document.getElementById('back-home').classList.add('hidden'); 
    document.getElementById('finish').classList.remove('hidden');
    
    const percent = totalAnswered > 0 ? Math.round((agreedCount / totalAnswered) * 100) : 0;
    document.getElementById('final-stats').innerText = `${percent}%`;
    document.getElementById('total-q').innerText = `Усього питань: ${totalAnswered}`;
    document.getElementById('match-q').innerText = `Спільних відповідей: ${agreedCount}`;

    saveSession(9, agreedCount, totalAnswered);
}