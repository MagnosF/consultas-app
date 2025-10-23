// consultas-app/src/Telas/AgendaScreen.js

import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList, ActivityIndicator, Alert, Button } from 'react-native';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';

// Componente principal da Agenda
export default function AgendaScreen() {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const { signOut } = useAuth(); // Usado para logout se a sessão expirar

  // Função para buscar as consultas na API
  const fetchAppointments = async () => {
    setLoading(true);
    try {
      // Chamada à API: GET /appointments/me
      const response = await api.get('/appointments/me');
      
      // Assume-se que o backend retorna uma lista de consultas
      setAppointments(response.data); 
    } catch (error) {
      console.error("Erro ao carregar a agenda:", error.response?.data || error);
      Alert.alert("Erro de Carga", "Não foi possível carregar suas consultas.");
      
      // Se for erro 401/403 (Token Inválido), força o logout
      if (error.response?.status === 401 || error.response?.status === 403) {
        Alert.alert("Sessão Expirada", "Sua sessão expirou. Faça login novamente.");
        signOut();
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Busca os dados assim que a tela é carregada
    fetchAppointments();
  }, []);

  // Exibição de Carregamento
  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
        <Text>Carregando Agenda...</Text>
      </View>
    );
  }

  // Template para renderizar cada item da consulta na lista
  const renderItem = ({ item }) => (
    <View style={styles.appointmentCard}>
      <Text style={styles.dateText}>Data: {new Date(item.appointment_date).toLocaleString('pt-BR')}</Text>
      <Text style={styles.detailText}>Status: {item.status.toUpperCase()}</Text>
      <Text style={styles.detailText}>Motivo: {item.reason}</Text>
      <Text style={styles.doctorText}>Médico: {item.doctor.full_name}</Text>
      {/* Aqui você adicionaria botões de CANCELAR (com PATCH) */}
    </View>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Minha Agenda de Consultas</Text>

      {appointments.length === 0 ? (
        <Text style={styles.emptyText}>Você não tem consultas agendadas.</Text>
      ) : (
        <FlatList
          data={appointments}
          keyExtractor={item => item.id.toString()}
          renderItem={renderItem}
          contentContainerStyle={{ paddingBottom: 20 }}
        />
      )}
      
      <View style={styles.buttonGroup}>
        <Button title="Atualizar Agenda" onPress={fetchAppointments} color="#28A745" />
        <Button title="Sair" onPress={signOut} color="#DC3545" />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f0f4f7',
    padding: 20,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  header: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#007AFF',
    marginBottom: 20,
    textAlign: 'center',
  },
  appointmentCard: {
    backgroundColor: '#fff',
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
    borderLeftWidth: 5,
    borderLeftColor: '#007AFF',
    elevation: 2,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 5,
  },
  dateText: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  detailText: {
    fontSize: 14,
    color: '#555',
  },
  doctorText: {
    fontSize: 14,
    color: '#333',
    marginTop: 5,
    fontWeight: '500',
  },
  emptyText: {
    textAlign: 'center',
    marginTop: 50,
    fontSize: 16,
    color: '#777',
  },
  buttonGroup: {
    marginTop: 10,
    borderTopWidth: 1,
    borderTopColor: '#ccc',
    paddingTop: 10,
  }
});