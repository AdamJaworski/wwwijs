function href_js(page) {
    window.location.href = page;
}

function logout() {
    fetch('/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    window.location.href = '/login';
}

const REFRESH_INTERVAL = 14 * 60 * 1000;

function refreshAccessToken() {
    fetch('/refresh', {
        method: 'POST',
        credentials: 'same-origin' // Important to send cookies
    })
    .then(response => {
        if (response.ok) {
            localStorage.setItem('lastRefresh', Date.now());
        } else {
            console.error('Failed to refresh access token');
        }
    })
    .catch(error => console.error('Error:', error));
}

function checkAndRefreshToken() {
    const lastRefresh = localStorage.getItem('lastRefresh');
    if (!lastRefresh || (Date.now() - lastRefresh) > REFRESH_INTERVAL) {
        refreshAccessToken();
    } else {
        const remainingTime = REFRESH_INTERVAL - (Date.now() - lastRefresh);
        setTimeout(refreshAccessToken, remainingTime);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    checkAndRefreshToken();
});

setInterval(refreshAccessToken, REFRESH_INTERVAL);