import { useEffect, useState } from "react";
import { io } from "socket.io-client";
import "./App.css"; 
import logo from './assets/logo.png'; 
const link="wss://eee4-2409-40f4-a6-adcf-3d94-8f18-5e69-5bb8.ngrok-free.app/"

export default function Dashboard() {
  const [updates, setUpdates] = useState([]);

  const formatTimestamp = (timestamp) => {
    const date = new Date(parseInt(timestamp) * 1000);
    return date.toLocaleTimeString();
  };

  useEffect(() => {
    const storedUpdates = JSON.parse(localStorage.getItem('logs') || "[]");
    setUpdates(storedUpdates);

    const socket = io(`${link}`, { transports: ["websocket"] });

    socket.on("connect", () => {
      console.log("Connected to WebSocket");
      socket.emit("join_room", { "room": "dashboard" });
    });

    socket.on("ambulance_signal_update", (data) => {
      console.log("New update received:", data);
      setUpdates((prevUpdates) => {
        const updatedLogs = [data, ...prevUpdates];
        localStorage.setItem('logs', JSON.stringify(updatedLogs));
        return updatedLogs;
      });

      setTimeout(() => {
        setUpdates((prevUpdates) => {
          const updatedLogs = prevUpdates.filter(
            (update) => !(update.order_id === data.order_id && update.signal_id === data.signal_id)
          );
          localStorage.setItem('logs', JSON.stringify(updatedLogs));
          return updatedLogs;
        });
      }, 13000);
    });

    socket.on("ambulance_signal_crossed", (data) => {
      console.log("Ambulance crossed signal:", data);
      setUpdates((prevUpdates) => {
        const updatedLogs = prevUpdates.filter(
          (update) => !(update.order_id === data.order_id && update.signal_id === data.signal_id)
        );
        localStorage.setItem('logs', JSON.stringify(updatedLogs));
        return updatedLogs;
      });
    });

    return () => {
      //socket.disconnect();
    };
  }, []);

  const handleDone = (index) => {
    setUpdates((prevUpdates) => {
      const updatedLogs = [...prevUpdates];
      const [doneUpdate] = updatedLogs.splice(index, 1); 
      updatedLogs.push({ ...doneUpdate, done: true });
      localStorage.setItem("logs", JSON.stringify(updatedLogs));
      return updatedLogs; 
    });
  };

  return (
    <div className="dashboard-container">
      <div className="header-container">
        <img src={logo} alt="Logo" className="header-logo" />
        <h1 className="header-title">Live Ambulance Tracking</h1>
      </div>

      <div className="content-container">
        <div className="updates-container">
          <ul className="updates-list">
            {updates.map((update, index) => (
              <li key={index} className="update-item">
                🚑 Ambulance {update.order_id} is near signal {update.signal_id} at {formatTimestamp(update.timestamp)}
                {!update.done && (
                  <button className="done-button" onClick={() => handleDone(index)}>Done</button>
                )}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
