from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, PositiveFloat
from typing import List

app = FastAPI(
    title="API de Controle de Salário para Professores",
    description="Calcula os salários semanais e mensais por campus com base na taxa de hora-aula e nas horas semanais trabalhadas.",
    version="1.0.0"
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, defina os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CampusHours(BaseModel):
    campus: str = Field(..., description="Nome do campus.")
    hours: PositiveFloat = Field(..., description="Número de horas semanais trabalhadas no campus.")

class SalaryInput(BaseModel):
    hourly_rate: PositiveFloat = Field(..., description="Valor da hora-aula.")
    campuses: List[CampusHours] = Field(..., description="Lista com as horas semanais por campus.")

class CampusSalaryBreakdown(BaseModel):
    campus: str = Field(..., description="Nome do campus.")
    weekly_hours: float = Field(..., description="Horas trabalhadas na semana.")
    weekly_salary: float = Field(..., description="Salário semanal calculado para o campus.")
    monthly_hours: float = Field(..., description="Horas trabalhadas no mês (aproximado considerando 4 semanas).")
    monthly_salary: float = Field(..., description="Salário mensal calculado para o campus.")

class SalaryBreakdownOutput(BaseModel):
    details: List[CampusSalaryBreakdown] = Field(..., description="Detalhamento do salário por campus.")
    overall_weekly_salary: float = Field(..., description="Salário semanal total considerando todos os campus.")
    overall_monthly_salary: float = Field(..., description="Salário mensal total considerando todos os campus.")

@app.post("/calcular-salario", response_model=SalaryBreakdownOutput)
def calcular_salario(data: SalaryInput) -> SalaryBreakdownOutput:
    """
    Calcula o salário semanal e mensal para cada campus e o total geral,
    com base no valor da hora-aula e nas horas semanais informadas.
    """
    details = []
    overall_weekly_salary = 0.0
    overall_monthly_salary = 0.0

    for campus_data in data.campuses:
        weekly_hours = campus_data.hours
        weekly_salary = data.hourly_rate * weekly_hours
        monthly_hours = weekly_hours * 4  # Considerando 4 semanas por mês
        monthly_salary = weekly_salary * 4

        overall_weekly_salary += weekly_salary
        overall_monthly_salary += monthly_salary

        details.append(CampusSalaryBreakdown(
            campus=campus_data.campus,
            weekly_hours=weekly_hours,
            weekly_salary=weekly_salary,
            monthly_hours=monthly_hours,
            monthly_salary=monthly_salary
        ))

    return SalaryBreakdownOutput(
        details=details,
        overall_weekly_salary=overall_weekly_salary,
        overall_monthly_salary=overall_monthly_salary
    )
