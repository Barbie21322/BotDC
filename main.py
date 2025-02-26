import discord
import asyncio
from discord.ext import commands

# Define your Discord bot token here
TOKEN = 'MTM0MzA3MDM5MTExOTExODM2Ng.G6Gogl.MWAMegZbK2B4LdQiJd7mL6vQz1UODgBSvyCEio'

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

canal_periodico = None  # Variable to store the channel for periodic messages

async def enviar_mensaje_periodico():
    """Función para enviar un mensaje cada 10 segundos a un canal disponible."""
    global canal_periodico

    if canal_periodico: # Check if a channel is already selected
        while not bot.is_closed():
            try:
                await canal_periodico.send("¡Mensaje periódico a un canal disponible cada 10 segundos!")
                await asyncio.sleep(10)  # Esperar 10 segundos
            except discord.errors.NotFound:
                print(f"Canal {canal_periodico.name} no encontrado. Deteniendo tarea periódica.")
                break # Stop the loop if the channel is not found
            except Exception as e:
                print(f"Error al enviar mensaje periódico: {e}")
                await asyncio.sleep(10) # Wait and retry in case of temporary errors
    else:
        print("No se pudo encontrar un canal disponible para mensajes periódicos. Asegúrate de que el bot esté en un servidor y tenga permiso para enviar mensajes en al menos un canal de texto.")


@bot.event
async def on_ready():
    global canal_periodico
    print(f'Bot conectado como {bot.user}')

    # Find the first available text channel
    for guild in bot.guilds:
        for channel in guild.text_channels:
            permissions = channel.permissions_for(guild.me)
            if permissions.send_messages:
                canal_periodico = channel
                print(f"Canal seleccionado para mensajes periódicos: {canal_periodico.name} en el servidor: {guild.name}")
                break # Stop searching in channels if we found one
        if canal_periodico: # Stop searching in guilds if we found a channel
            break

    if not canal_periodico:
        print("No se encontró ningún canal de texto disponible donde el bot pueda enviar mensajes.")

    # Start the periodic message task in the background when the bot is ready
    bot.loop.create_task(enviar_mensaje_periodico())

@bot.command()
async def test(ctx):
    """Comando de prueba simple para verificar que el bot responde a comandos."""
    await ctx.send("¡Bot responde!")


if __name__ == "__main__":
    bot.run(TOKEN)
