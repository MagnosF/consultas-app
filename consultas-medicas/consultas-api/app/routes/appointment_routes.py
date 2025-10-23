from fastapi import APIRouter, Depends, HTTPException, status, Path, Body # Ambos são necessários
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Union, Optional

from app.database.connection import get_db
from app.core.dependencies import get_current_user, require_permission
from app.models.appointment_model import Appointment
from app.models.user import User
from app.schemas.appointment_schema import (
    AppointmentCreate, 
    AppointmentResponse, 
    AppointmentUpdateStatus
)

router = APIRouter(
    prefix="/appointments",
    tags=["Agendamento e Consultas"]
)

# Rota 1: Agendar Consulta (Apenas Paciente)
@router.post(
    "/",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission('paciente'))],
    summary="Agendar uma nova consulta (Requer Paciente)"
)
def create_appointment(
    appointment: AppointmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # O ID do paciente é o ID do usuário logado
    patient_id = current_user.id
    
    # 1. Checagem de Conflito de Horário (Simplificada)
    # Apenas verifica se o médico já tem algo agendado naquele horário
    existing_appointment = db.query(Appointment).filter(
        Appointment.doctor_id == appointment.doctor_id,
        Appointment.appointment_date == appointment.appointment_date,
        Appointment.status == 'agendada'
    ).first()

    if existing_appointment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O médico já tem um agendamento neste horário."
        )

    # 2. Criar a nova consulta
    db_appointment = Appointment(
        patient_id=patient_id,
        doctor_id=appointment.doctor_id,
        appointment_date=appointment.appointment_date,
        reason=appointment.reason,
        status='agendada'
    )
    
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


# Rota 2: Listar Histórico/Próximas Consultas (Paciente, Médico, Admin)
@router.get(
    "/me",
    response_model=List[AppointmentResponse],
    summary="Visualizar histórico e próximas consultas (Paciente e Médico)"
)
def list_my_appointments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Se for paciente, lista as consultas onde ele é o paciente
    if current_user.user_type == 'paciente':
        appointments = db.query(Appointment).filter(
            Appointment.patient_id == current_user.id
        ).all()
    # Se for médico, lista as consultas onde ele é o médico
    elif current_user.user_type == 'medico':
        appointments = db.query(Appointment).filter(
            Appointment.doctor_id == current_user.id
        ).all()
    # Admin pode ver todas as consultas (opcional, aqui estamos limitando para 'me')
    else: # Admin (poderia ser uma rota /admin/appointments separada)
        appointments = db.query(Appointment).all()
        
    return appointments


# Rota 3: Cancelar Consulta (Paciente e Médico)
@router.patch(
    "/{appointment_id}/status", 
    response_model=AppointmentResponse,
    summary="Cancelar/Atualizar status da consulta (Requer Paciente ou Médico/Admin)"
)
def update_appointment_status(
    # 1. Path Parameter (Sintaxe para resolver 422 e SyntaxError)
    appointment_id: int = Path(..., description="O ID da consulta a ser atualizada"),

    # 2. Body Parameter (Sintaxe para resolver SyntaxError)
    status_update: AppointmentUpdateStatus = Body(...), 

    # 3. Dependências
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Busca e 404
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consulta não encontrada.")

    # 2. Definição de Permissões (CORRIGIDO)
    is_owner = (current_user.id == appointment.patient_id) or (current_user.id == appointment.doctor_id)
    is_admin = current_user.user_type == 'admin'

    # 3. Verificação de Permissão
    if not (is_admin or is_owner):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para alterar o status desta consulta."
        )

    # 4. Executa a atualização
    appointment.status = status_update.status
    db.commit()
    db.refresh(appointment)

    return appointment