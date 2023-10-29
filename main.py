import telebot
from random import choice
import security as s
from time import sleep
from webserver import keep_alive

ready = False
bot = telebot.TeleBot(s.token)


@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.chat.id, 'Мур мяу, кусь')
    #launch bot for chanal


@bot.message_handler(content_types=['text'])
def new_message(message):
    #for a new message in channel
  pass

@bot.channel_post_handler()
def new_channel_message(message):
  if message.chat.id == s.chanal_id:  # если бот в нескольких каналах, можно разделять действия по id
      sleep(5)
      bot.send_message(s.chat_id, 'Мур мяу *кусь за ногу и валить*')
  else:
    bot.send_message(message.chat.id, '*Накоклился в лежаночке и спит*')
    print(message, ready)


keep_alive()
bot.polling(none_stop=True)
