Un esempio completo di una web app Python che gestisce 4 agenti, utilizzando LLM (Large Language Model), Celery, Redis e Matrix. L'app è composta da diverse parti: il server Flask, gli agenti Celery, la gestione di Redis per la coda dei task, e l'integrazione con Matrix.

# 1. requirements.txt
Le dipendenze necessarie per il progetto:

- Flask
- Celery
- redis
- matrix-nio
- llama-index
- openai

2. Dockerfile
   
Un esempio di Dockerfile per il progetto:

```Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]


3. docker-compose.yml
Configura i servizi necessari, inclusi Redis e il web server per Flask:

services:
  web:
    build: .
    container_name: flask_app
    ports:
      - "5000:5000"
    depends_on:
      - redis
    environment:
      - CELERY_BROKER_URL=redis://redis:6379/0

  redis:
    image: "redis:latest"
    container_name: redis

  celery:
    build: .
    container_name: celery_worker
    command: celery -A app.tasks worker --loglevel=info
    depends_on:
      - redis

4. config.py
Configura le impostazioni per Flask e Celery:

import os
  class Config:
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    MATRIX_HOMESERVER_URL = 'https://matrix.org'
    MATRIX_USER = 'user@example.com'
    MATRIX_PASSWORD = 'password'

5. app/__init__.py
Inizializza Flask e Celery:

from flask import Flask
from celery import Celery
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

from app import tasks

6. app/tasks.py
Definisce i task Celery per gli agenti:


from app import celery
from app.agent1 import agent1_task
from app.agent2 import agent2_task
from app.agent3 import agent3_task
from app.agent4 import agent4_task

@celery.task
def run_agent1_task(data):
    return agent1_task(data)

@celery.task
def run_agent2_task(data):
    return agent2_task(data)

@celery.task
def run_agent3_task(data):
    return agent3_task(data)

@celery.task
def run_agent4_task(data):
    return agent4_task(data)

7. app/matrix_integration.py
Gestisce l'integrazione con Matrix:


from nio import AsyncClient, LoginResponse

async def send_message(client, room_id, message):
    await client.room_send(room_id, message)

async def matrix_login():
    client = AsyncClient(Config.MATRIX_HOMESERVER_URL, Config.MATRIX_USER)
    response = await client.login(Config.MATRIX_PASSWORD)
    if isinstance(response, LoginResponse):
        return client
    return None

8. app/agent1.py, app/agent2.py, app/agent3.py, app/agent4.py
Ogni file contiene un agente che esegue una funzione specifica:

Esempio per agent1.py
def agent1_task(data):
    # Qui puoi integrare un LLM o altre logiche
    response = f"Agent 1 processed data: {data}"
    return response

9. app.py
File principale che esegue il server Flask e invoca i task Celery:


from app import app
from flask import request, jsonify
from app.tasks import run_agent1_task, run_agent2_task, run_agent3_task, run_agent4_task

@app.route('/run_agent1', methods=['POST'])
def run_agent1():
    data = request.json.get('data')
    task = run_agent1_task.apply_async(args=[data])
    return jsonify({'task_id': task.id})

@app.route('/run_agent2', methods=['POST'])
def run_agent2():
    data = request.json.get('data')
    task = run_agent2_task.apply_async(args=[data])
    return jsonify({'task_id': task.id})

@app.route('/run_agent3', methods=['POST'])
def run_agent3():
    data = request.json.get('data')
    task = run_agent3_task.apply_async(args=[data])
    return jsonify({'task_id': task.id})

@app.route('/run_agent4', methods=['POST'])
def run_agent4():
    data = request.json.get('data')
    task = run_agent4_task.apply_async(args=[data])
    return jsonify({'task_id': task.id})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

10. Avvio del sistema
Crea le immagini Docker con docker-compose build.
Avvia i servizi con docker-compose up.
Le API saranno accessibili su http://localhost:5001.

Ogni agente viene invocato tramite una richiesta POST. Gli agenti possono eseguire compiti separati (come l'elaborazione del linguaggio naturale usando un LLM o qualsiasi altra logica personalizzata) e possono interagire con Matrix tramite i task Celery.

1. Interazione tra Agenti
Gli agenti possono comunicare tra loro utilizzando Redis come un sistema di messaggistica. Quando un agente termina un task, può inviare i risultati agli altri agenti per una seconda fase di elaborazione. In questo caso, possiamo utilizzare Redis Pub/Sub o direttamente le code Celery per inviare messaggi tra gli agenti.

Ad esempio, se Agent1 termina il suo lavoro e vuole inviare i dati a Agent2, possiamo utilizzare Celery per invocare il task di Agent2:

2. Modifiche per l'interazione tra agenti con Redis e Celery
app/tasks.py – Task Celery che invocano gli agenti in sequenza

from app import celery
from app.agent1 import agent1_task
from app.agent2 import agent2_task
from app.agent3 import agent3_task
from app.agent4 import agent4_task

@celery.task
def run_agent1_task(data):
    result = agent1_task(data)
    # Dopo che l'Agent1 ha completato il suo compito, invia i risultati ad Agent2
    run_agent2_task.apply_async(args=[result])
    return result

@celery.task
def run_agent2_task(data):
    result = agent2_task(data)
    # Dopo che l'Agent2 ha completato il suo compito, invia i risultati ad Agent3
    run_agent3_task.apply_async(args=[result])
    return result

@celery.task
def run_agent3_task(data):
    result = agent3_task(data)
    # Dopo che l'Agent3 ha completato il suo compito, invia i risultati ad Agent4
    run_agent4_task.apply_async(args=[result])
    return result

@celery.task
def run_agent4_task(data):
    return agent4_task(data)

3. Integrazione di OpenAI (LLM)
Ora aggiungiamo l'integrazione con OpenAI per un agente che utilizza un LLM per elaborare il testo. Supponiamo che Agent1 utilizzi OpenAI per generare una risposta a una domanda.

Per fare ciò, dovrai aggiungere la libreria openai al tuo file requirements.txt:

-openai

Quindi, nel codice di Agent1, possiamo usare OpenAI per generare una risposta:

app/agent1.py – LLM con OpenAI

import openai

Configurazione di OpenAI
openai.api_key = "your-openai-api-key"

def agent1_task(data):
    # Usa OpenAI per generare una risposta
    response = openai.Completion.create(
        model="text-davinci-003",  # Usa il modello appropriato
        prompt=data,  # Invia i dati (prompt) per la risposta
        max_tokens=150
    )
    result = response.choices[0].text.strip()
    return result

4. Flusso di lavoro completo
Ora, il flusso di lavoro diventa il seguente:

Agent1 prende i dati (come un prompt), li elabora con OpenAI e genera una risposta.
Agent2 prende il risultato di Agent1 e può eseguire un'elaborazione aggiuntiva.
Agent3 prende i dati da Agent2 e li elabora.
Agent4 esegue l'ultimo compito sui dati elaborati.
Ogni agente invia il proprio risultato al successivo agente tramite il task Celery.

5. Flask API con nuovi agenti
Aggiungiamo anche il supporto per chiamare la sequenza di agenti tramite API Flask:

app.py – API Flask per invocare gli agenti

from app import app
from flask import request, jsonify
from app.tasks import run_agent1_task, run_agent2_task, run_agent3_task, run_agent4_task

@app.route('/run_agent1', methods=['POST'])
def run_agent1():
    data = request.json.get('data')
    task = run_agent1_task.apply_async(args=[data])
    return jsonify({'task_id': task.id})

@app.route('/run_agent2', methods=['POST'])
def run_agent2():
    data = request.json.get('data')
    task = run_agent2_task.apply_async(args=[data])
    return jsonify({'task_id': task.id})

@app.route('/run_agent3', methods=['POST'])
def run_agent3():
    data = request.json.get('data')
    task = run_agent3_task.apply_async(args=[data])
    return jsonify({'task_id': task.id})

@app.route('/run_agent4', methods=['POST'])
def run_agent4():
    data = request.json.get('data')
    task = run_agent4_task.apply_async(args=[data])
    return jsonify({'task_id': task.id})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

6. Avvio del sistema
Dopo aver fatto tutte le modifiche, puoi costruire e avviare il sistema con i seguenti comandi:

Costruisci l'immagine Docker: docker-compose build
Avvia i servizi: docker-compose up

7. Test
Puoi testare la tua app inviando una richiesta POST per invocare uno degli agenti. Ad esempio, per invocare Agent1, puoi usare Postman o curl:

Per fare la POST da portainer.io 
http://95.216.187.242:5001/run_agent2

curl
curl -X POST http://localhost:5001/run_agent1 -H "Content-Type: application/json" -d '{"data": "Qual è la capitale della Francia?"}'
Questo avvierà il task di Agent1, che utilizzerà OpenAI per rispondere alla domanda, e invierà i risultati agli altri agenti per l'elaborazione.

 ----Alternativa al curl in powershell----

$body = @{ data = "che giorno è oggi" } | ConvertTo-Json -Compress
Invoke-RestMethod -Uri "http://localhost:5001/run_agent2" -Method Post -Headers @{"Content-Type"="application/json"} -Body $body


Considerazioni finali
Flusso di interazione: Ogni agente invia i suoi risultati al successivo tramite Celery. Puoi estendere questo flusso per includere più agenti o logiche complesse.
Integrazione con Matrix: Gli agenti potrebbero anche inviare i risultati o interagire con utenti attraverso Matrix (ad esempio, inviare risposte o notifiche).

------------------------------------------------------------------------------------------------------

Se Celery non riesce a connettersi a Redis. Ecco alcune possibili cause e soluzioni:

1. Redis non è in esecuzione
Controlla se Redis è attivo con:

redis-cli ping
Se risponde PONG, Redis è attivo. Se no, avvialo con:

sudo systemctl start redis

oppure, se usi Docker:

docker run -d --name redis -p 6379:6379 redis

2. Redis è configurato per accettare solo connessioni locali
Se Redis è in esecuzione ma Celery non riesce a connettersi, controlla la configurazione:

sudo cat /etc/redis/redis.conf | grep bind

Se trovi:
bind 127.0.0.1

e stai cercando di connetterti da un altro container, dovrai modificare il file /etc/redis/redis.conf e commentare quella linea (# bind 127.0.0.1), poi riavviare Redis:

sudo systemctl restart redis

3. Docker e Network Issues
Se stai usando Docker Compose e Redis è in un container separato, verifica il nome del servizio: Nel docker-compose.yml, se hai:

services:
  redis:
    image: redis
    ports:
      - "6379:6379"
Celery deve connettersi usando redis://redis:6379/0 anziché localhost.

4. Firewall o SELinux
Se hai un firewall attivo, prova a disabilitarlo temporaneamente per testare:

sudo ufw allow 6379
sudo systemctl restart redis

-----------------------------------------------
L'aggiunta di una rete (networks) garantisce che tutti i container possano comunicare tra loro.

Per la connessione a Redis da fuori Docker (es. redis-cli -h localhost -p 6379):
Passaggi successivi
Dopo aver aggiornato il file, ricostruisci e riavvia tutto con:

docker-compose down && docker-compose up --build

Se si verificano problemi controllare i log di Redis con:

docker logs redis

Se Celery non parte, controlla anche i log di Celery:

docker logs celery_worker.

------------------------------------
Se con postman si invia una POST e da errore 404

Se Postman restituisce un errore 404 su una richiesta POST, significa che Flask non trova l'endpoint corrispondente. Ecco cosa puoi verificare:

1. Flask sta eseguendo correttamente l'applicazione?
Controlla i log del container Flask:

docker logs flask_app
Se ci sono errori di importazione o avvio, risolvili prima di testare con Postman.

Puoi anche connetterti direttamente al container ed eseguire:

docker exec -it flask_app flask routes
Questo comando elenca tutti gli endpoint disponibili.

2. Controlla il tuo codice Flask
Assicurati che la route per la POST sia definita correttamente, ad esempio:


from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    return jsonify({"message": "Dati ricevuti", "data": data}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
L'host è 0.0.0.0 (necessario per funzionare in Docker).

## Il metodo è POST e l'endpoint /api/data è definito.

Modifica
docker inspect flask_app | grep "IPAddress"

3. Stai inviando i dati corretti?
Se l'endpoint si aspetta un JSON, assicurati di inviare la richiesta POST con:

Header → Content-Type: application/json
Body → JSON valido, es.
json

{
  "nome": "Mario",
  "età": 30
}
4. Controlla i log delle richieste

Nel container Flask, dovresti vedere le richieste in arrivo:

docker logs -f flask_app


