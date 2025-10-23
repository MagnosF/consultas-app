// consultas-app/src/rotas/AuthRoutes.js

import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';

import LoginScreen from '../screens/LoginScreen';
// IMPORTANTE: Você precisará criar esta tela de Registro depois
import RegisterScreen from '../screens/RegisterScreen'; 

const AuthStack = createStackNavigator();

// Rotas visíveis quando o usuário NÃO está logado
export default function AuthRoutes() {
  return (
    <AuthStack.Navigator
      screenOptions={{
        headerShown: false, // Oculta o cabeçalho em todas as telas
      }}
    >
      <AuthStack.Screen name="Login" component={LoginScreen} />
      <AuthStack.Screen name="Register" component={RegisterScreen} /> 
    </AuthStack.Navigator>
  );
}