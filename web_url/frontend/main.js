// frontend/main.js

const dataContainer = document.getElementById('data-container');
const socket = new WebSocket('ws://192.168.78.71:8000/ws');

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    displayData(data);
};

function displayData(data) {
    const dataItem = document.createElement('div');
    dataItem.classList.add('data-item');

    for (const key in data) {
        const span = document.createElement('span');
        span.classList.add(key);
        span.textContent = `${key}: ${data[key]}`;
        dataItem.appendChild(span);
    }

    dataContainer.appendChild(dataItem);
    dataContainer.scrollTop = dataContainer.scrollHeight;
}
