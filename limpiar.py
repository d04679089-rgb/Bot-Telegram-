import telebot
TOKEN = 'TU_TOKEN_AQUI' # Pon aquí tu token real
bot = telebot.TeleBot(TOKEN)
bot.delete_webhook()
print("Webhook eliminado con éxito")
