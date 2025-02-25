import asyncio
from nio import AsyncClient, LoginResponse
from config import Config

class MatrixBot:
    def __init__(self):
        self.client = AsyncClient(Config.MATRIX_HOMESERVER_URL, Config.MATRIX_USER)

    async def login(self):
        response = await self.client.login(Config.MATRIX_PASSWORD)
        if isinstance(response, LoginResponse)and response.user_id:
            print(f"Accesso a Matrix riuscito! User ID: {response.user_id}")
        else:
            print(f"Errore di accesso: {response}")
            raise RuntimeError("Login a Matrix fallito: manca user_id")
            
        
    async def send_message(self, message):
        await self.client.room_send(
            room_id=Config.MATRIX_ROOM_ID,
            message_type="m.room.message",
            content={"msgtype": "m.text", "body": message},
        )

    async def logout(self):
        await self.client.close()  #.logout()

def send_matrix_message(message):
    bot = MatrixBot()
    loop = asyncio.get_event_loop()

    if loop.is_running():
        # Se c'è già un event loop attivo, eseguiamo la coroutine in modo sicuro
        asyncio.ensure_future(bot.login())
        asyncio.ensure_future(bot.send_message(message))
        asyncio.ensure_future(bot.logout())
    else:
        # Se non c'è un event loop attivo, ne creiamo uno nuovo
        loop.run_until_complete(bot.login())
        loop.run_until_complete(bot.send_message(message))
        loop.run_until_complete(bot.logout())
