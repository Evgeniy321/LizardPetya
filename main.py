import telebot
from random import choice, randint
import security as s
from time import sleep
from webserver import keep_alive

ready = False
actionCount = 0
bot = telebot.TeleBot(s.token)

attacks_action = ['Мур мяу *кусь за ногу и валить*',
                  'Кусь за ногe',
                  'Кусь за палец',
                  'Кусь за живот',
                  'Реззко подбигает и просит кушать',
                  "*Скря-Скряб-Скряб побдегает к тебе варан и ждет пока ты дашь вкусняшку"]

sleep_actions = ['Спит',
                 'Спит',
                 'Спит',
                 'Спит',
                 'Спит',
                 'Спит']

sleep_actions_finaly = ['*Ушел в другую комнату спать, вы ему мешайте своими переговорами*']

hi_steackers = ['CAACAgIAAxkBAAEBqWVlPvUNAfcDUGbqWhfruEkJnSk8kAACYAADDnr7CkGRLQbGGfu6MAQ',
                'CAACAgIAAxkBAAEBqWdlPvUl3DdNUK6SajXC_YyeCairJAACjgADl_TGFGxjxuaUUOw3MAQ',
                'CAACAgIAAxkBAAEBqWllPvUzAAHRkOa_N0A0CTIFZHG_RO0AAjoUAAKH28lLt4S2aCX5a1QwBA',
                'CAACAgIAAxkBAAEBqWtlPvVOQds5ho-t9rw47KUTQZEpWgACXgcAAlwCZQNV1K4CElTj3zAE',
                'CAACAgQAAxkBAAEBqW1lPvVl0WqdGTSwMPMJVsmVTQEMCQACpQADzjkIDUnINzIR1FDaMAQ']

eat_steackers = ['CAACAgIAAxkBAAEBqVtlPvRAYu5ROO-LgCZW5JjhJtkBgQACgg4AAmdfgEl1YzlcXGcPTTAE',
                 'CAACAgIAAxkBAAEBqV1lPvRjw6aqotx_GG-bymvrkoBhjgACjBAAArrqMEkWokxDvj3lGTAE',
                 'CAACAgIAAxkBAAEBqV9lPvR1dWi83-hudXReiavKkISmCAACOg0AAir8MUonISBQnYVdfTAE',
                 'CAACAgIAAxkBAAEBqWFlPvSXwIsrc06sPPNLgxf3Xw1u3gACTQADv2adGE2tU0P-VNGzMAQ',
                 'CAACAgIAAxkBAAEBqWNlPvSprKe1vnXgUMOq3rgp6wY3BQACPwAD3U7yFffJ8Ga23MjqMAQ']

sleepy_stickers = ['CAACAgQAAxkBAAEBrThlQE5PQWoz5XjfBEJRwbb6Y-mRRgACgAADzjkIDaLUfeB_ZKmUMAQ',
                   'CAACAgQAAxkBAAEBrTplQE5VzF7ymrRYngjxGyLUF0aZuAACyQADzjkIDdrMNTXcY2sNMAQ',
                   'CAACAgQAAxkBAAEBrTxlQE5cD9bND48h_yolzb0OOYwaPgAChgADzjkIDdgatd1t69jyMAQ',
                   'CAACAgIAAxkBAAEBrT5lQE5012L08aDtAhQgWC57CqvflwACsAcAAlwCZQO_ytpL6_o6uzAE',
                   'CAACAgIAAxkBAAEBrUBlQE6Q_EEDsZ3ERAT1__5-LREopQACmgADl_TGFGSHNRpyufmaMAQ']


def action(bot, message,action_frase, sticker):
  try:
    bot.send_sticker(message.chat.id, choice(sticker), reply_to_message_id=message.message_id)
  except Exception as e:
    bot.send_message(s.host_id, f'error {e}')
  bot.reply_to(message, choice(action_frase))

@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.chat.id, '*Вы входите в комнату Пети, он крепко спит*')
  bot.send_message(message.chat.id, choice(sleep_actions_finaly))
    #launch bot for chanal


@bot.message_handler(content_types=['text', 'photo'])
def new_message(message):
  global actionCount
  if actionCount == 0:
    if message.chat.id != s.chat_id and message.chat.id != s.chanal_id:#личное сообщение
      bot.send_message(message.chat.id, '*Тебя же дурака предупреждали, не будить...*')
      bot.send_sticker(message.chat.id, choice(eat_steackers))
    elif message.chat.id != s.chanal_id:#первый комментарий к посту
      action(bot,message, attacks_action, hi_steackers)
      actionCount += 2
      bot.send_message(s.host_id, f'*Ты дурак, я тебя же предупреждаю* angry: {actionCount}')
    else:
      actionCount+=1
  elif actionCount == -100:
    bot.send_message(s.host_id, f'*Ты дурак, я тебя же предупреждаю* angry: {actionCount}')
  else:#если он поздаровался, но в коментариях идет бесседа 
    if message.chat.id != s.chanal_id:
      if randint(0,actionCount+3) == 0:
        action(bot,message, sleep_actions, sleepy_stickers)
        bot.send_message(s.host_id, f'*Ты дурак, я тебя же предупреждаю* angry: {actionCount}')
      elif actionCount > 5:
        action(bot,message, sleep_actions_finaly, sleepy_stickers)
        actionCount = -100
      else:
        actionCount += 1
    


@bot.channel_post_handler()
def new_channel_message(message):
  global actionCount
  actionCount = 0
  bot.send_message(s.host_id, actionCount)
  if message.chat.id != s.chanal_id:  # если бот в нескольких каналах, можно разделять действия по id
    bot.send_message(message.chat.id, '*Накоклился в лежаночке и спит*')
    print(message, ready)



keep_alive()
bot.polling(none_stop=True)
