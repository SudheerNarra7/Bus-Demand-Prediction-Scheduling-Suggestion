import axios from 'axios';

// Backend API URL - change this to match your backend server
const API_BASE_URL = 'http://localhost:8000/api';

const api = {
  // Get all locations
  getLocations: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/locations`);
      return response.data;
    } catch (error) {
      console.error('Error fetching locations:', error);
      throw error;
    }
  },
  
  // Make a prediction
  makePrediction: async (predictionData) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/predict`, {
        start_location_id: parseInt(predictionData.startLocationId),
        end_location_id: parseInt(predictionData.endLocationId),
        time_period: predictionData.timePeriod,
        occasion: predictionData.occasion,
        season: predictionData.season
      });
      return response.data;
    } catch (error) {
      console.error('Error making prediction:', error);
      throw error;
    }
  },
  
  // Get prediction history
  getPredictionHistory: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/predictions/history`);
      return response.data;
    } catch (error) {
      console.error('Error fetching prediction history:', error);
      throw error;
    }
  }
};

export default api;
