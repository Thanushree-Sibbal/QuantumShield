let socket = null;
let listeners = [];

export function connectWebSocket(onMessage) {
  // Register every component that wants data
  listeners.push(onMessage);

  // If socket already exists, don't create another one
  if (
    socket &&
    (socket.readyState === WebSocket.OPEN ||
      socket.readyState === WebSocket.CONNECTING)
  ) {
    return socket;
  }

  socket = new WebSocket("ws://127.0.0.1:8000/ws/transactions");

  socket.onopen = () => {
    console.log("✅ Connected to FastAPI");
  };

  socket.onmessage = (event) => {
    const tx = JSON.parse(event.data);

    // Send the transaction to ALL listeners
    listeners.forEach((listener) => listener(tx));
  };

  socket.onerror = (err) => {
    console.error("WebSocket Error:", err);
  };

  socket.onclose = () => {
    console.log("Disconnected");
    socket = null;
    listeners = [];
  };

  return socket;
}