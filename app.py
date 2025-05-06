import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, PositiveFloat
from typing import List

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API de Controle de Salário para Professores",
    description=(
        "Calcula os salários semanais e mensais por campus com base na taxa de hora-aula "
        "e nas horas semanais trabalhadas. Ideal para consultas rápidas sem persistência de dados."
    ),
    version="1.1.0"
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restrinja para os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de Dados
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
    overall_weekly_salary: float = Field(..., description="Salário semanal total considerando todos os campi.")
    overall_monthly_salary: float = Field(..., description="Salário mensal total considerando todos os campi.")

# Endpoint da API para cálculo de salário
@app.post("/calcular-salario", response_model=SalaryBreakdownOutput, tags=["Salário"])
def calcular_salario(data: SalaryInput) -> SalaryBreakdownOutput:
    """
    Calcula o salário semanal e mensal para cada campus e o total geral,
    com base no valor da hora-aula e nas horas semanais informadas.
    Retorna o detalhamento por campus e os totais gerais de salário semanal e mensal.
    """
    try:
        details = []
        overall_weekly_salary = 0.0
        overall_monthly_salary = 0.0

        for campus_data in data.campuses:
            weekly_hours = campus_data.hours
            weekly_salary = data.hourly_rate * weekly_hours
            monthly_hours = weekly_hours * 5.25
            monthly_salary = data.hourly_rate * monthly_hours
            # ou: monthly_salary = weekly_salary * 5.25

            overall_weekly_salary += weekly_salary
            overall_monthly_salary += monthly_salary

            details.append(CampusSalaryBreakdown(
                campus=campus_data.campus,
                weekly_hours=weekly_hours,
                weekly_salary=weekly_salary,
                monthly_hours=monthly_hours,
                monthly_salary=monthly_salary
            ))

        logger.info("Cálculo realizado com sucesso para %d campus(es).", len(data.campuses))
        return SalaryBreakdownOutput(
            details=details,
            overall_weekly_salary=overall_weekly_salary,
            overall_monthly_salary=overall_monthly_salary
        )
    except Exception as e:
        logger.error("Erro durante o cálculo do salário: %s", str(e))
        raise HTTPException(status_code=500, detail="Erro interno ao calcular o salário.")

# Monta a pasta 'static' para servir os arquivos estáticos em "/static"
app.mount("/static", StaticFiles(directory="static"), name="static")

# Rota para servir a página inicial (index.html)
@app.get("/", tags=["Home"])
def root():
    """
    Retorna a página inicial da aplicação.
    """
    return FileResponse("static/index.html")
