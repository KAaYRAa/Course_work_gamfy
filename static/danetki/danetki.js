

let currentDanetka = null;

function saveSession(gameId, finalScore, steps = 1) {
    fetch('/games/save_result/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value
        },
        body: JSON.stringify({ game_id: gameId, score: finalScore, steps: steps })
    })
    .then(res => res.json())
    .then(data => console.log("Результат Данеток успішно зафіксовано в БД"))
    .catch(err => console.error("Помилка логування Данеток:", err));
}

class GameState {
    constructor(context) { this.context = context; }
    render() {     throw new Error("Метод render() має бути перевизначений"); }
    next() {       throw new Error("Метод next() має бути перевизначений"); }
}

class HostState extends GameState {
    render() {
        document.getElementById('host-screen').classList.remove('hidden');
        document.getElementById('game-screen').classList.add('hidden');
        document.getElementById('result-screen').classList.add('hidden');
    }
    next() {
        this.context.changeState(new PlayersState(this.context));
    }
}

class PlayersState extends GameState {
    render() {
        document.getElementById('host-screen').classList.add('hidden');
        document.getElementById('game-screen').classList.remove('hidden');
        document.getElementById('result-screen').classList.add('hidden');
    }
    next() {
        saveSession(7, 1, 1);
        this.context.changeState(new ResultState(this.context));
    }
}

class ResultState extends GameState {
    render() {
        document.getElementById('host-screen').classList.add('hidden');
        document.getElementById('game-screen').classList.add('hidden');
        document.getElementById('result-screen').classList.remove('hidden');
    }
    next() {
        location.reload(); 
    }
}

class GameContext {
    constructor() {
        this.currentState = new HostState(this); 
    }
    init() {
        this.currentState.render();
    }
    changeState(state) {
        this.currentState = state;
        this.currentState.render(); 
    }
    nextState() {
        this.currentState.next();
    }
}

const gameContext = new GameContext();

async function initGame() {
    try {
        const url = window.DANETKI_DATA_URL || '/danetki/get_data/';
        const res = await fetch(url);
        if (!res.ok) throw new Error('Помилка завантаження');
        
        currentDanetka = await res.json();
        
        const hostStoryHtml = `
            <div class="space-y-4">
                <p><span class="text-purple-400 font-bold uppercase text-[10px] tracking-widest">СИТУАЦІЯ:</span><br>${currentDanetka.content_text}</p>
                <p><span class="text-purple-400 font-bold uppercase text-[10px] tracking-widest">РОЗГАДКА:</span><br>${currentDanetka.extra_info}</p>
            </div>
        `;
        document.getElementById('full-story-host').innerHTML = hostStoryHtml;
        document.getElementById('puzzle-text').innerText = currentDanetka.content_text;
        document.getElementById('category-tag').innerText = currentDanetka.category || 'Логіка';
        document.getElementById('full-story-final').innerHTML = hostStoryHtml;

        gameContext.init();

    } catch (e) {
        console.error(e);
        document.getElementById('full-story-host').innerText = "Не вдалося завантажити історію. Перевірте з'єднання з базою.";
    }
}

window.onload = initGame;