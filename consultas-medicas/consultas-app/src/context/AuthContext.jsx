
import React, { createContext, useState, useEffect, useContext } from 'react';
import api from '../services/api'; // Importa a configuração do Axios
import AsyncStorage from '@react-native-async-storage/async-storage'; // Para persistir o token

const AuthContext = createContext();

// ---------------------------------------------
// 1. O Provedor de Contexto (Guarda o estado e a função de login)
// ---------------------------------------------

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null); // Dados do usuário logado (opcional)
  const [token, setToken] = useState(null); // O token JWT
  const [loading, setLoading] = useState(true); // Para checar se o token já foi carregado do storage

  // 1.1. Efeito para carregar o token salvo ao iniciar o app
  useEffect(() => {
    async function loadStorageData() {
      // Tenta recuperar o token do armazenamento assíncrono
      const storedToken = await AsyncStorage.getItem('@MyApp:token');
      // Adicionaria aqui a lógica para carregar os dados do usuário se necessário

      if (storedToken) {
        // Define o token no estado
        setToken(storedToken);
        // Define o token padrão para todas as requisições futuras do Axios
        api.defaults.headers.Authorization = `Bearer ${storedToken}`;
      }
      setLoading(false);
    }

    loadStorageData();
  }, []);

  // 1.2. Função de Login
  const signIn = async (email, password) => {
    try {
      // Fazendo POST /token para o backend FastAPI
      // FastAPI espera x-www-form-urlencoded. Usaremos FormData para simular isso.
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);
      
      const response = await api.post('/token', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      const { access_token, token_type } = response.data;
      const fullToken = `${token_type} ${access_token}`;

      // 1. Salva o token no estado
      setToken(fullToken);
      
      // 2. Salva o token no armazenamento assíncrono para persistência
      await AsyncStorage.setItem('@MyApp:token', fullToken);

      // 3. Define o token padrão para o Axios
      api.defaults.headers.Authorization = fullToken;

      return { success: true };

    } catch (error) {
      console.error("Erro no login:", error.response || error);
      return { success: false, message: "Falha na autenticação. Verifique as credenciais." };
    }
  };

  // 1.3. Função de Logout
  const signOut = async () => {
    await AsyncStorage.clear();
    setToken(null);
    setUser(null);
    api.defaults.headers.Authorization = undefined;
  };

  return (
    <AuthContext.Provider
      value={{ signed: !!token, token, user, loading, signIn, signOut }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// ---------------------------------------------
// 2. Hook Customizado para usar o Contexto
// ---------------------------------------------
export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  }

  return context;
}