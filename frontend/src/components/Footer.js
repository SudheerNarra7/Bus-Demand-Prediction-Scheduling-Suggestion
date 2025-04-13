import React from 'react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <p>&copy; {new Date().getFullYear()} Bus Demand Prediction - Devloped by  Sudheer Reddy Narra</p>
      </div>
    </footer>
  );
};

export default Footer;
