import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  return (
    <div className="home">
      <div className="hero">
        <h1>Bus Demand Prediction & Scheduling Suggestion</h1>
        <p>Optimize your bus scheduling with machine learning predictions</p>
        <Link to="/predict" className="cta-button">Make a Prediction</Link>
      </div>
      
      <div className="features">
        <div className="feature-card">
          <h2>Predict Passenger Demand</h2>
          <p>Use historical data to predict the number of passengers for specific routes, times, and occasions.</p>
        </div>
        
        <div className="feature-card">
          <h2>Optimize Bus Scheduling</h2>
          <p>Get recommendations on the optimal number of buses needed based on predicted demand.</p>
        </div>
        
        <div className="feature-card">
          <h2>Data Visualization</h2>
          <p>View clear visualizations of predicted demand across different time slots.</p>
        </div>
      </div>
      
      <div className="how-it-works">
        <h2>How It Works</h2>
        <ol>
          <li>Select your route (start and end locations)</li>
          <li>Choose the time period, occasion, and season</li>
          <li>Get instant predictions for passenger demand</li>
          <li>View suggested bus scheduling based on the predictions</li>
        </ol>
      </div>
    </div>
  );
};

export default Home;
