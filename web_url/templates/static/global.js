const ipAddress = '192.168.78.49:8000';
const socket_city_map = new WebSocket(`ws://${ipAddress}/city_map`);
const socket_ws = new WebSocket(`ws://${ipAddress}/ws`);