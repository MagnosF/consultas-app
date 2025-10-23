from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base
from app.models.user import User # Importa o modelo User

# Status possíveis de uma consulta
APPOINTMENT_STATUS = ('agendada', 'cancelada', 'concluida')

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    
    # Relação com o Paciente (o usuário que agendou)
    patient_id = Column(Integer, ForeignKey('users.id'))
    
    # Relação com o Médico (o usuário que irá atender)
    doctor_id = Column(Integer, ForeignKey('users.id'))
    
    appointment_date = Column(DateTime)
    reason = Column(String(255)) # Motivo da consulta
    status = Column(Enum(*APPOINTMENT_STATUS), default='agendada')
    
    created_at = Column(DateTime, default=func.now())
    
    # Definição dos relacionamentos para facilitar consultas
    patient = relationship("User", foreign_keys=[patient_id], backref="patient_appointments")
    doctor = relationship("User", foreign_keys=[doctor_id], backref="doctor_appointments")
    
    def __repr__(self):
        return f"<Appointment(id={self.id}, date='{self.appointment_date}', status='{self.status}')>"