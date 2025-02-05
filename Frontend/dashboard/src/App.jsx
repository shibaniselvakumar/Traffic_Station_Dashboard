import { useEffect, useState } from "react";
import { io } from "socket.io-client";
import "./App.css"; // Import external stylesheet
import logo from './assets/logo.png';  // Adjust the path if necessary


export default function Dashboard() {
  const [updates, setUpdates] = useState([]);

  // Load logs from localStorage when the component mounts
  useEffect(() => {
    // Retrieve logs from localStorage on page load
    const storedUpdates = JSON.parse(localStorage.getItem('logs')) || [];
    setUpdates(storedUpdates);

    const socket = io("http://localhost:5000"); // Adjust backend URL if needed

    socket.on("connect", () => {
      console.log("Connected to WebSocket");
      socket.emit("join_room", "dashboard");
    });

    socket.on("ambulance_signal_update", (data) => {
      console.log("New update received:", data);

      // Store the new update in localStorage
      const updatedLogs = [data, ...updates];
      localStorage.setItem('logs', JSON.stringify(updatedLogs));

      // Update state
      setUpdates(updatedLogs);
    });

    return () => {
      socket.disconnect();
    };
  }, [updates]); // Make sure that updates is part of the dependency array

  // Function to format timestamp as time
  const formatTime = (timestamp) => {
    const date = new Date(timestamp * 1000); // Convert timestamp to milliseconds
    return date.toLocaleTimeString(); // Returns only the time (HH:MM:SS)
  };

  return (
    <>
      {/* Header Section */}
      <div className="header-container">
        <img src={logo} alt="Logo" className="header-logo" />
        <h1 className="header-title">Live Ambulance Tracking</h1>
      </div>

      {/* Main Content Area */}
      <div className="content-container">
        <div className="updates-container">
          <ul className="updates-list">
            {updates.map((update, index) => (
              <li key={index} className="update-item">
                <p>🚑 Ambulance {update.order_id} is near signal {update.signal_id}</p>
                <span>{formatTime(update.timestamp)}</span> {/* Formatted time */}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </>
  );
}
