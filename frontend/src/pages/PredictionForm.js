import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../utils/api';
import './PredictionForm.css';

const PredictionForm = () => {
  const navigate = useNavigate();
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [formData, setFormData] = useState({
    startLocationId: '',
    endLocationId: '',
    timePeriod: 'Full_Day',
    occasion: 'Regular',
    season: 'Summer'
  });

  useEffect(() => {
    // Fetch locations from API
    const fetchLocations = async () => {
      try {
        setLoading(true);
        const response = await api.getLocations();
        setLocations(response);
        setLoading(false);
      } catch (err) {
        setError('Failed to load locations. Please try again later.');
        setLoading(false);
        console.error('Error fetching locations:', err);
      }
    };

    fetchLocations();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate form
    if (formData.startLocationId === formData.endLocationId && formData.startLocationId !== '') {
      alert('Start and end locations must be different');
      return;
    }
    
    if (!formData.startLocationId || !formData.endLocationId) {
      alert('Please select both start and end locations');
      return;
    }
    
    try {
      setLoading(true);
      const response = await api.makePrediction(formData);
      
      // Navigate to results page with the prediction data
      navigate('/results', { state: { prediction: response } });
    } catch (err) {
      setError('Failed to make prediction. Please try again later.');
      console.error('Error making prediction:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading && locations.length === 0) {
    return <div className="loading">Loading locations from Texas...</div>;
  }

  return (
    <div className="prediction-form-container">
      <h1>Make a Prediction</h1>
      
      {error && <div className="error-message">{error}</div>}
      
      <form className="prediction-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="startLocationId">Start Location (Texas)</label>
          <select 
            id="startLocationId" 
            name="startLocationId" 
            value={formData.startLocationId} 
            onChange={handleChange}
            required
          >
            <option value="">Select Start Location</option>
            {locations.map(location => (
              <option key={`start-${location.id}`} value={location.id}>
                {location.name}
              </option>
            ))}
          </select>
        </div>
        
        <div className="form-group">
          <label htmlFor="endLocationId">End Location (Texas)</label>
          <select 
            id="endLocationId" 
            name="endLocationId" 
            value={formData.endLocationId} 
            onChange={handleChange}
            required
          >
            <option value="">Select End Location</option>
            {locations.map(location => (
              <option key={`end-${location.id}`} value={location.id}>
                {location.name}
              </option>
            ))}
          </select>
        </div>
        
        <div className="form-group">
          <label htmlFor="timePeriod">Time Period</label>
          <select 
            id="timePeriod" 
            name="timePeriod" 
            value={formData.timePeriod} 
            onChange={handleChange}
          >
            <option value="Morning">Morning</option>
            <option value="Afternoon">Afternoon</option>
            <option value="Evening">Evening</option>
            <option value="Night">Night</option>
            <option value="Full_Day">Full Day</option>
          </select>
        </div>
        
        <div className="form-group">
          <label htmlFor="occasion">Occasion</label>
          <select 
            id="occasion" 
            name="occasion" 
            value={formData.occasion} 
            onChange={handleChange}
          >
            <option value="Regular">Regular</option>
            <option value="Weekend">Weekend</option>
            <option value="Holiday">Holiday</option>
            <option value="Festival">Festival</option>
            <option value="Special Event">Special Event</option>
          </select>
        </div>
        
        <div className="form-group">
          <label htmlFor="season">Season</label>
          <select 
            id="season" 
            name="season" 
            value={formData.season} 
            onChange={handleChange}
          >
            <option value="Spring">Spring</option>
            <option value="Summer">Summer</option>
            <option value="Fall">Fall</option>
            <option value="Winter">Winter</option>
          </select>
        </div>
        
        <button type="submit" className="submit-button" disabled={loading}>
          {loading ? 'Processing...' : 'Predict Demand'}
        </button>
      </form>
    </div>
  );
};

export default PredictionForm;
