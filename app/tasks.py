from app import celery
from app.agent1 import agent1_task
from app.agent2 import agent2_task
from app.agent3 import agent3_task
from app.agent4 import agent4_task
from app.matrix_integration import send_matrix_message

@celery.task
def run_agent1_task(data):
    result = agent1_task(data)
    send_matrix_message(f"Agent1 ha completato il task: {result}")
    run_agent2_task.apply_async(args=[result])
    return result

@celery.task
def run_agent2_task(data):
    result = agent2_task(data)
    send_matrix_message(f"Agent2 ha completato il task: {result}")
    run_agent3_task.apply_async(args=[result])
    return result

@celery.task
def run_agent3_task(data):
    result = agent3_task(data)
    send_matrix_message(f"Agent3 ha completato il task: {result}")
    run_agent4_task.apply_async(args=[result])
    return result

@celery.task
def run_agent4_task(data):
    result = agent4_task(data)
    send_matrix_message(f"Agent4 ha completato il task: {result}")
    return agent4_task(data)

