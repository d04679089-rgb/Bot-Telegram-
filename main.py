import os
import json
import random
import telebot
from telebot.types import Message
from flask import Flask
from threading import Thread

# --- CONFIGURACIÓN ---
# Pegamos tu token directamente aquí para que sea más sencillo
TOKEN = "8607152482:AAGt_KNNUiBJIJ4F6mYmM2GTHjuKNXST8W0"
LIBRARY_FILE = os.path.join(os.path.dirname(__file__), "biblioteca.json")

bot = telebot.TeleBot(TOKEN)

# --- SERVIDOR WEB (Para que Render no lo apague) ---
server = Flask('')

@server.route('/')
def home():
    return "Bot de Biblioteca está en línea ✅"

def run():
    server.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- LÓGICA DEL BOT ---
def load_library() -> dict:
    if os.path.exists(LIBRARY_FILE):
        try:
            with open(LIBRARY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

biblioteca = load_library()

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "📚 ¡Hola! Soy tu Bot de Biblioteca. Escribe el nombre de un libro para buscarlo.")

@bot.message_handler(func=lambda m: True)
def auto_buscador(message):
    if len(message.text) < 3: return
    
    query = message.text.lower()
    encontrado = False
    
    for nombre_archivo, f_id in biblioteca.items():
        if query in nombre_archivo.lower():
            bot.send_document(
                message.chat.id, 
                f_id, 
                caption=f"📖 Aquí tienes: {nombre_archivo.upper()}",
                reply_to_message_id=message.message_id
            )
            encontrado = True
            break # Te manda el primero que encuentra

# --- INICIO ---
if __name__ == "__main__":
    keep_alive() # Arranca el servidor web
    print("Bot encendido...")
    bot.polling(none_stop=True)
  
