import { useEffect, useState } from "react";
import "./CarStatus.css"; // import CSS

export default function CarStatus() {
  const [status, setStatus] = useState({});

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/status");
        const data = await res.json();
        setStatus(data.status);
      } catch (err) {
        console.error(err);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 100);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="car-status-container">
      <h2 className="title">Car Status</h2>

      <div className="status-list">
        {Object.entries(status).map(([key, value]) => (
          <div key={key} className="status-item">
            <span className="status-label">{key}</span>
            <span className={`status-badge ${value.toLowerCase()}`}>
              {value}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
