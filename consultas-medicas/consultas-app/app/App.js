// consultas-app/App.js

import 'react-native-gesture-handler'; // Importação essencial para react-navigation
import React from 'react';
import { ActivityIndicator, View, StyleSheet } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { AuthProvider, useAuth } from '../src/context/AuthContext'; // 1. O Provedor de Contexto

import AuthRoutes from '../src/routes/AuthRoutes'; // 2. Rotas para Deslogados
import AppRoutes from '../src/routes/AppRoutes'; // 3. Rotas para Logados

// ---------------------------------------------
// Componente que decide as rotas (condicional)
// ---------------------------------------------
function Routes() {
  const { signed, loading } = useAuth();

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }

  // Se o usuário estiver logado, mostra as rotas principais (AppRoutes)
  // Caso contrário, mostra as rotas de autenticação (AuthRoutes)
  return signed ? <AppRoutes /> : <AuthRoutes />;
}

// ---------------------------------------------
// Componente principal que aplica o contexto
// ---------------------------------------------
export default function App() {
  return (
    <AuthProvider>
        <Routes />
    </AuthProvider>
  );
}

const styles = StyleSheet.create({
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});