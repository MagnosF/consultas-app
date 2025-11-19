import axios from 'axios';


const API_BASE_URL = 'https://consultas-api-244o.onrender.com/';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;