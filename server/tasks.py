from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@app.task
def process_jdm_question(question):
    # Simula procesamiento de datos complejos
    if "piezas" in question:
        return "Las piezas populares incluyen turbocompresores HKS y suspensiones coilover Tein."
    return "Consulta procesada."