import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const Header = () => {
  return (
    <header className="header">
      <div className="container">
        <h1 className="logo">Bus Demand Prediction</h1>
        <nav className="nav">
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/predict">Make Prediction</Link></li>
            <li><Link to="/history">History</Link></li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;
