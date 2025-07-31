import openai

# Configurazione di OpenAI
#openai.api_key = "your-openai-api-key"
client = openai.OpenAI(api_key="xxxxxxxxxxxxxx")

def agent1_task(data):
    # Usa OpenAI per generare una risposta
    response = openai.Completion.create(
        model="text-davinci-003",  # Usa il modello appropriato
        prompt=data,  # Invia i dati (prompt) per la risposta
        max_tokens=150
    )
    result = response.choices[0].text.strip()
    return result
