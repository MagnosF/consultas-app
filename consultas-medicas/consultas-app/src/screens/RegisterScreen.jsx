// consultas-app/src/Telas/RegisterScreen.js

import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ActivityIndicator, Alert, Picker } from 'react-native';
import api from '../services/api'; // Importa a configuração do Axios

export default function RegisterScreen({ navigation }) {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [document, setDocument] = useState(''); // CPF ou CRM
  const [password, setPassword] = useState('');
  const [userType, setUserType] = useState('paciente'); // Padrão: paciente
  const [loading, setLoading] = useState(false);

  const handleRegister = async () => {
    // 1. Validação básica
    if (!fullName || !email || !document || !password) {
      Alert.alert("Erro", "Por favor, preencha todos os campos.");
      return;
    }

    setLoading(true);

    try {
      const userData = {
        full_name: fullName,
        email: email,
        document: document,
        password: password,
        user_type: userType,
      };

      // 2. Chamada à API (POST /users/)
      const response = await api.post('/users/', userData);

      setLoading(false);
      
      // 3. Sucesso: Redireciona para o Login
      Alert.alert(
        "Sucesso", 
        `Usuário "${userType}" cadastrado! Você pode fazer login agora.`,
        [{ text: "OK", onPress: () => navigation.navigate('Login') }]
      );

    } catch (error) {
      setLoading(false);
      const errorMessage = error.response?.data?.detail || "Ocorreu um erro no cadastro. Verifique a conexão.";
      
      Alert.alert("Falha no Cadastro", errorMessage);
      console.error("Erro no cadastro:", error.response || error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Novo Cadastro</Text>

      <TextInput style={styles.input} placeholder="Nome Completo" value={fullName} onChangeText={setFullName} />
      <TextInput style={styles.input} placeholder="E-mail" value={email} onChangeText={setEmail} keyboardType="email-address" autoCapitalize="none" />
      <TextInput style={styles.input} placeholder="CPF / Documento" value={document} onChangeText={setDocument} />
      <TextInput style={styles.input} placeholder="Senha" value={password} onChangeText={setPassword} secureTextEntry />

      <Text style={styles.label}>Tipo de Perfil:</Text>
      <View style={styles.pickerContainer}>
        <Picker
          selectedValue={userType}
          onValueChange={(itemValue) => setUserType(itemValue)}
          style={styles.picker}
        >
          <Picker.Item label="Paciente" value="paciente" />
          <Picker.Item label="Médico" value="medico" />
          {/* O Admin normalmente é criado manualmente ou reservado */}
          <Picker.Item label="Administrador" value="admin" /> 
        </Picker>
      </View>


      <TouchableOpacity 
        style={styles.button} 
        onPress={handleRegister} 
        disabled={loading}
      >
        {loading ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.buttonText}>Cadastrar</Text>
        )}
      </TouchableOpacity>

      <TouchableOpacity onPress={() => navigation.navigate('Login')}>
        <Text style={styles.linkText}>Já tem conta? Voltar ao Login</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 30,
    backgroundColor: '#f0f4f7',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#007AFF',
    marginBottom: 40,
    textAlign: 'center',
  },
  input: {
    height: 50,
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 8,
    paddingHorizontal: 15,
    marginBottom: 15,
    backgroundColor: '#fff',
  },
  label: {
    fontSize: 16,
    color: '#333',
    marginBottom: 5,
  },
  pickerContainer: {
    borderColor: '#ccc',
    borderWidth: 1,
    borderRadius: 8,
    marginBottom: 15,
    overflow: 'hidden',
    backgroundColor: '#fff',
    height: 50,
    justifyContent: 'center',
  },
  picker: {
    height: 50,
  },
  button: {
    backgroundColor: '#28A745', // Cor verde para cadastro
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
    marginBottom: 15,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  linkText: {
    color: '#007AFF',
    textAlign: 'center',
    marginTop: 10,
  }
});