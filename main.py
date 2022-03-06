import random
import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup

# Парсинг названия групп и их жанров
resp = requests.get(r'http://www.prostosound.com.ua/spravochniki/gruppy/241/any')
soup = BeautifulSoup(resp.text, features="lxml")

nameList = []
genreList = []

music_list = soup.find_all('div', {'class': 'm-table__table'})
for msc in music_list:
    try:
        name = msc.find('a').text
        genre = msc.find('table', {'class': 'table-small'}).find('span').text
    except:
        name = 'название не найдено'
        genre = 'жанр не найден'
    nameList.append(name)
    genreList.append(genre)
print(nameList)
print(genreList)

bot = telebot.TeleBot('5244491754:AAGuHBdfAqdiWUw5LwAcRA1wfKrlVLC0lyo')

# Приветствие и справка
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
  if message.text == "Привет":
      bot.send_message(message.from_user.id, "Привет, я люблю французскую музыку!")
      keyboard = types.InlineKeyboardMarkup()

      key_yes = types.InlineKeyboardButton(text='Да', callback_data='pressYes')
      keyboard.add(key_yes)

      key_no = types.InlineKeyboardButton(text='Нет', callback_data='pressNo')
      keyboard.add(key_no)
      # Показываем все кнопки сразу и пишем сообщение о выборе
      bot.send_message(message.from_user.id, text='Хочешь открыть для себя новую музыкальную группу из Франции ?', reply_markup=keyboard)
  elif message.text == "/help":
      bot.send_message(message.from_user.id, "Напиши Привет")
  else:
      bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # Если нажали на одну из 2 кнопок — выводим соответствующий результат
    if call.data == "pressYes":
        # Формируем Сообщение со случайной Группой
        rnd = random.randrange(len(nameList))
        msg = 'Группа:' + ' ' + nameList[rnd] + '\nЖанр:' + ' ' + genreList[rnd]
        # Отправляем текст в Телеграм
        bot.send_message(call.message.chat.id, msg)
    elif call.data == "pressNo":
        msg = "Заходи еще!"
        bot.send_message(call.message.chat.id, msg)

# Постоянный опрос бота в Телеграме
bot.polling(none_stop=True, interval=0)
