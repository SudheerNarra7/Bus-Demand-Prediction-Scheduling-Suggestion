import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../utils/api';
import './History.css';

const History = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        setLoading(true);
        const response = await api.getPredictionHistory();
        setHistory(response);
        setLoading(false);
      } catch (err) {
        setError('Failed to load prediction history. Please try again later.');
        setLoading(false);
        console.error('Error fetching history:', err);
      }
    };

    fetchHistory();
  }, []);

  if (loading) {
    return <div className="loading">Loading history...</div>;
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="error-message">{error}</div>
        <Link to="/predict" className="button">Make a New Prediction</Link>
      </div>
    );
  }

  if (history.length === 0) {
    return (
      <div className="no-history">
        <h2>No prediction history available</h2>
        <p>Make some predictions to see them here.</p>
        <Link to="/predict" className="button">Make a Prediction</Link>
      </div>
    );
  }

  return (
    <div className="history-container">
      <h1>Prediction History</h1>
      
      <div className="history-list">
        <table className="history-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Route</th>
              <th>Time Period</th>
              <th>Occasion</th>
              <th>Season</th>
              <th>Total Demand</th>
              <th>Buses Needed</th>
            </tr>
          </thead>
          <tbody>
            {history.map((item) => (
              <tr key={item.id}>
                <td>{new Date(item.timestamp).toLocaleString()}</td>
                <td>{item.start_location_name} to {item.end_location_name}</td>
                <td>{item.time_period.replace('_', ' ')}</td>
                <td>{item.occasion}</td>
                <td>{item.season}</td>
                <td>{item.total_predicted_demand}</td>
                <td>{item.total_buses_needed}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      <div className="actions">
        <Link to="/predict" className="button">Make a New Prediction</Link>
      </div>
    </div>
  );
};

export default History;
