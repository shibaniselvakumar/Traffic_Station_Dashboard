import { useEffect, useState } from "react";
import { io } from "socket.io-client";
import "./App.css"; // Import external stylesheet

export default function Dashboard() {
  const [updates, setUpdates] = useState([]);

  useEffect(() => {
    const socket = io("http://localhost:5000"); // Adjust backend URL if needed

    socket.on("connect", () => {
      console.log("Connected to WebSocket");
      socket.emit("join_room", "dashboard");
    });

    socket.on("ambulance_signal_update", (data) => {
      console.log("New update received:", data);
      setUpdates((prevUpdates) => [data, ...prevUpdates]);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">Ambulance Monitoring Dashboard</h1>
      <div className="updates-container">
        <h2 className="updates-title">Live Updates</h2>
        <ul className="updates-list">
          {updates.map((update, index) => (
            <li key={index} className="update-item">
              🚑 Ambulance {update.order_id} is near signal {update.signal_id} at {update.timestamp}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
