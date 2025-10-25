// consultas-app/src/rotas/AppRoutes.js (Versão Atualizada FINAL)

import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import AgendaScreen from '../screens/AgendaScreen';

const AppStack = createStackNavigator();

// Rotas visíveis APÓS o login (telas principais)
export default function AppRoutes() {
    return (
        <AppStack.Navigator>
            {/* 2. Define a AgendaScreen como a primeira tela */}
            <AppStack.Screen 
                name="Agenda" 
                component={AgendaScreen} 
                options={{ 
                    title: 'Minhas Consultas',
                    // Você pode adicionar um cabeçalho customizado ou botões aqui no futuro
                }} 
            />
            
            {/* 3. Se quiser adicionar a rota de Agendamento/Criação, ela entraria aqui: */}
            {/* <AppStack.Screen name="AgendarNovo" component={AppointmentCreateScreen} /> */}

            {/* A tela Placeholder não será mais usada como rota principal */}
        </AppStack.Navigator>
    );
}