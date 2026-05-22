

function toggleFav(gameId) {
    const heart = document.getElementById('heart');
    
    fetch(`/favorite/toggle/${gameId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'added') {
            heart.innerText = '♥';
            heart.style.color = '#ef4444';
        } else if (data.status === 'removed') {
            heart.innerText = '♡';
            heart.style.color = 'white';
        } else if (data.error) {
            console.error("Помилка бази даних:", data.error);
        }
    })
    .catch(err => console.error("Помилка асинхронного зв'язку:", err));
}