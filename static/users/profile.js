

function removeFav(gameId) {
    fetch(`/favorite/toggle/${gameId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'removed') {
            const item = document.getElementById(`fav-item-${gameId}`);
            if (item) {
                item.style.opacity = '0';
                item.style.transform = 'scale(0.95)';
                setTimeout(() => item.remove(), 300);
            }
        }
    })
    .catch(err => console.error("Помилка видалення:", err));
}