from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Importa o schema de resposta do usuário para poder aninhar o paciente/médico
from app.schemas.user import UserResponse 

# --- Schema de ENTRADA (Input) para Agendar ---
class AppointmentCreate(BaseModel):
    # O patient_id será obtido do token JWT, então não precisa estar no input
    doctor_id: int
    appointment_date: datetime = Field(..., description="Formato: YYYY-MM-DDTHH:MM:SS")
    reason: str = Field(..., max_length=255)

# --- Schema para CANCELAR (apenas um campo de status) ---
class AppointmentUpdateStatus(BaseModel):
    status: str = Field(..., description="Novo status: 'agendada', 'cancelada', 'concluida'")

# --- Schema de SAÍDA (Output) ---
class AppointmentResponse(BaseModel):
    id: int
    appointment_date: datetime
    reason: str
    status: str
    created_at: datetime
    
    # Inclui informações detalhadas do paciente e do médico
    patient: UserResponse # Retorna o objeto UserResponse aninhado
    doctor: UserResponse # Retorna o objeto UserResponse aninhado

    class Config:
        from_attributes = True