// consultas-app/src/rotas/AppRoutes.js

import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';

const PlaceholderScreen = () => {
    // 3. O Hook useAuth DEVE ser chamado dentro do corpo da função
    const { signOut } = useAuth(); 

    return (
        <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
            <Text style={{ fontSize: 20, marginBottom: 20 }}>
                Bem-vindo(a)! Você está logado(a).
            </Text>
            {/* 4. O onPress agora chama a função signOut corretamente */}
            <Button title="SAIR (Logout)" onPress={signOut} color="#DC3545" />
        </View>
    );
};

const AppStack = createStackNavigator();

// Rotas visíveis APÓS o login (telas principais)
export default function AppRoutes() {
    return (
        <AppStack.Navigator>
            <AppStack.Screen name="Dashboard" component={PlaceholderScreen} />
        </AppStack.Navigator>
    );
}