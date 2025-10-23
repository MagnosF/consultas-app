// consultas-app/src/services/api.js

import axios from 'axios';

// ⚠️ ATENÇÃO: O Endereço IP deve ser ajustado
// - Se estiver usando um EMULADOR ANDROID: use 'http://10.0.2.2:8000'
// - Se estiver usando um CELULAR FÍSICO (com Expo Go): use o IP LOCAL da sua máquina (Ex: 'http://192.168.1.XX:8000')
const API_BASE_URL = 'http://10.0.2.2:8000'; 

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;