import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import { Bar, Pie, Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import './PredictionResults.css';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const PredictionResults = () => {
  const location = useLocation();
  const prediction = location.state?.prediction;
  
  // If no prediction data, show error
  if (!prediction) {
    return (
      <div className="no-results">
        <h2>No prediction data available</h2>
        <p>Please make a prediction first.</p>
        <Link to="/predict" className="button">Make a Prediction</Link>
      </div>
    );
  }
  
  // Prepare data for bar chart
  const barChartData = {
    labels: prediction.predictions.map(p => p.time_slot),
    datasets: [
      {
        label: 'Predicted Demand (Tickets)',
        data: prediction.predictions.map(p => p.predicted_demand),
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
      {
        label: 'Buses Needed',
        data: prediction.predictions.map(p => p.buses_needed),
        backgroundColor: 'rgba(153, 102, 255, 0.6)',
        borderColor: 'rgba(153, 102, 255, 1)',
        borderWidth: 1,
      },
    ],
  };
  
  // Prepare data for pie chart
  const pieChartData = {
    labels: prediction.predictions.map(p => p.time_slot),
    datasets: [
      {
        label: 'Demand Distribution',
        data: prediction.predictions.map(p => p.predicted_demand),
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };
  
  // Prepare data for line chart (trend visualization)
  const lineChartData = {
    labels: prediction.predictions.map(p => p.time_slot),
    datasets: [
      {
        label: 'Demand Trend',
        data: prediction.predictions.map(p => p.predicted_demand),
        fill: true,
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        tension: 0.4,
      },
    ],
  };
  
  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Predicted Demand by Time Slot',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  return (
    <div className="prediction-dashboard">
      <div className="dashboard-header">
        <h1>Prediction Dashboard</h1>
        <div className="route-info">
          <span className="route-label">Route:</span>
          <span className="route-value">
            {prediction.route.start.name} (ID: {prediction.route.start.id}) to {prediction.route.end.name} (ID: {prediction.route.end.id})
          </span>
        </div>
      </div>
      
      <div className="dashboard-summary">
        <div className="summary-card">
          <h2>Route Summary</h2>
          <div className="summary-details">
            <div className="summary-row">
              <span className="summary-label">From:</span>
              <span className="summary-value">{prediction.route.start.name} (ID: {prediction.route.start.id})</span>
            </div>
            <div className="summary-row">
              <span className="summary-label">To:</span>
              <span className="summary-value">{prediction.route.end.name} (ID: {prediction.route.end.id})</span>
            </div>
            <div className="summary-row">
              <span className="summary-label">Time Period:</span>
              <span className="summary-value">{prediction.time_period.replace('_', ' ')}</span>
            </div>
            <div className="summary-row">
              <span className="summary-label">Occasion:</span>
              <span className="summary-value">{prediction.occasion}</span>
            </div>
            <div className="summary-row">
              <span className="summary-label">Season:</span>
              <span className="summary-value">{prediction.season}</span>
            </div>
          </div>
          <div className="totals">
            <div className="total-item">
              <span className="total-label">Total Predicted Demand:</span>
              <span className="total-value">{prediction.total_predicted_demand} tickets</span>
            </div>
            <div className="total-item">
              <span className="total-label">Total Buses Needed:</span>
              <span className="total-value">{prediction.total_buses_needed} buses</span>
            </div>
          </div>
        </div>
        
        <div className="kpi-cards">
          <div className="kpi-card">
            <h3>Average Demand</h3>
            <div className="kpi-value">
              {Math.round(prediction.total_predicted_demand / prediction.predictions.length)} tickets
            </div>
            <div className="kpi-label">Per time slot</div>
          </div>
          
          <div className="kpi-card">
            <h3>Peak Demand</h3>
            <div className="kpi-value">
              {Math.max(...prediction.predictions.map(p => p.predicted_demand))} tickets
            </div>
            <div className="kpi-label">Highest demand time slot</div>
          </div>
          
          <div className="kpi-card">
            <h3>Average Buses</h3>
            <div className="kpi-value">
              {Math.round(prediction.total_buses_needed / prediction.predictions.length)} buses
            </div>
            <div className="kpi-label">Per time slot</div>
          </div>
        </div>
      </div>
      
      <div className="dashboard-charts">
        <div className="chart-container">
          <h2>Demand and Buses by Time Slot</h2>
          <Bar data={barChartData} options={chartOptions} />
        </div>
        
        <div className="chart-row">
          <div className="chart-container half-width">
            <h2>Demand Distribution</h2>
            <Pie data={pieChartData} />
          </div>
          
          <div className="chart-container half-width">
            <h2>Demand Trend</h2>
            <Line data={lineChartData} />
          </div>
        </div>
      </div>
      
      <div className="detailed-results">
        <h2>Detailed Predictions</h2>
        <div className="results-table">
          <table>
            <thead>
              <tr>
                <th>Time Slot</th>
                <th>Predicted Demand</th>
                <th>Buses Needed</th>
                <th>Utilization</th>
              </tr>
            </thead>
            <tbody>
              {prediction.predictions.map((pred, index) => {
                const busCapacity = 50; // Assuming each bus can carry 50 passengers
                const utilization = (pred.predicted_demand / (pred.buses_needed * busCapacity) * 100).toFixed(1);
                
                return (
                  <tr key={index}>
                    <td>{pred.time_slot}</td>
                    <td>{pred.predicted_demand} tickets</td>
                    <td>{pred.buses_needed} buses</td>
                    <td>{utilization}%</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
      
      <div className="actions">
        <Link to="/predict" className="button">Make Another Prediction</Link>
        <Link to="/history" className="button secondary">View Prediction History</Link>
      </div>
    </div>
  );
};

export default PredictionResults;