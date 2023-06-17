import telebot
from telebot import types

import json

import functions as fu
import openai
import os

with open('config.json', 'r', encoding="utf-8") as file:
    config = json.load(file)

with open('clients.json', 'r', encoding="utf-8") as file:
    clients = json.load(file)
    
openai.api_key = config["api_key"]

prompt = """Є мобільний оператор lifecell, який має наступні тарифи:

     Перший Тариф.
    Назва: "Вільний Лайф"
    Ціна: 180 грн за 4 тижні якщо номер перенесено, 275 грн за 4 тижні якщо номер зареєстровано/персоніфіковано, стандартна вартість 325 грн за 4 тижні.
    Дзвінки: 1600 хв на всі номери по Україні
    Інтернет: Безлімітний інтернет.
    Додаткові опції: Безліміт на соцмережі, месенджери та освітні платформи.
                     Пакет Вільний ТВ+ включено у тариф
                     Хмарне сховище lifebox: 50 GB
    
     Другий Тариф.
    Назва: "Смарт Лайф"
    Ціна: 120 грн за 4 тижні якщо номер перенесено, 175 грн за 4 тижні якщо номер зареєстровано/персоніфіковано, стандартна вартість 225 грн за 4 тижні.
    Дзвінки: 800 хв на всі номери по Україні
    Інтернет: 25 GB інтернету.
    Додаткові опції: Безліміт на соцмережі, месенджери та освітні платформи.
    
     Третій Тариф.
    Назва: "Просто Лайф"
    Ціна: 90 грн за 4 тижні якщо номер перенесено, 140 грн за 4 тижні якщо номер зареєстровано/персоніфіковано, стандартна вартість 160 грн за 4 тижні.
    Дзвінки: 300 хв на всі номери по Україні
    Інтернет: 8 GB інтернету.
    Додаткові опції: Безліміт на соцмережі, месенджери та освітні платформи.
                     
     Четвертий Тариф.
    Назва: "Platinum Лайф"
    Ціна: 250 грн за 4 тижні якщо номер перенесено, 400 грн за 4 тижні якщо номер зареєстровано/персоніфіковано, стандартна вартість 450 грн за 4 тижні.
    Дзвінки: 3000 хв на всі номери по Україні
    Інтернет: Безлімітний інтернет.
    Додаткові опції: Безліміт на соцмережі, месенджери та освітні платформи.
                     Пакет Платинум ТВ+ включено у тариф
                     Хмарне сховище lifebox: 500 GB
                     
     П'ятий Тариф.
    Назва: "Шкільний Лайф"
    Ціна: Стандартна вартість 150 грн за 4 тижні.
    Дзвінки: Безліміт на lifecell. Безліміт на два "Обрані номери".
    Інтернет: 7 GB інтернету.
    Додаткові опції: Безліміт на соцмережі, месенджери та освітні платформи.
                     
Клієнт проходить опитування, де хоче вибрати найбільш підходящий для нього тариф. Ось питання:

1. Скільки вам років?
    - Меньше 18
    - Більше 18

2. Для кого вам потрібен тариф?
    - Для сім'ї
    - Для себе
    
3. Для чого вам потрібен тариф?
    - Для дзвінків 
    - Для інтернету 
    - Для соц мереж 
    - Для всього 

4. Яка ціна тарифу вас влаштовує?
    - Менше 200
    - Більше 200
    - Мені байдуже

5. Який об'єм інтернету вам потрібен?
    - Безліміт
    - Менше 10
    - Більше 10
    - Мені байдуже
    
6. Як часто ви користуєтесь соц. мережами та мессенджерами?
    - Часто
    - Рідко
    - Мені байдуже
    
7. Скільки хвилин вам потрібно для дзвінків по Україні?\n_Дзвінки у мережі lifecell - безкоштовні._
    - Менше 1200 хвилин
    - Більше 1200 хвилин
    - Мені байдуже
    
    Тобі відішлеться лист виду [1,3,3,2,2,2,1], де кожна цифра це порядковий номер відповіді на кожне завдання.
Тобі потрібно підібрати найбільш підходящий тариф за цим листом. Якщо відповідь на третє питання "Для дзвінків",
то не враховувати відповідь на 5-те питання.


    Починати треба з слів "Ми можемо порекомендувати вам тариф " (можна змінювати слова синонімами або перефразувати), після цього
пропусти один рядок і відправ наступну форму, де заміни значення в <> в залежності від тарифу:
    
\n💵 **Ціна:** <ціна за тариф> грн / 4 тижні
☎️ **Дзвінки:** <кількість хвилин по Україні> хв
🌐 **Інтернет:** <кількість ГБ інтернету, може бути Безліміт> ГБ
🤯 **А ще у пакеті послуг тарифу:** <плюси, які є в тарифі, які можуть зацікавити клієнта>
    Номер тарифу: <Номер тарифу зі списка>
"""

bot = telebot.TeleBot(config["token"])

@bot.message_handler(commands=['start'])
def main(message):
    clients['clients'][f'{message.chat.first_name}-{message.chat.last_name}'] = []
    fu.create_main_template(bot, message)
    with open('clients.json', 'w') as file:
        json.dump(clients, file, indent=4) 

@bot.callback_query_handler(func = lambda call: True)
def answer(call):
    message = call.message
    answer = call.data
    if answer.split('_')[0][:1] == "b":
        if answer == config["button1_data"]:
            fu.find_tarif(bot, message)
        elif answer == config["button2_data"]:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(config["button_back_text"], callback_data=config["button_back_data"]))
            bot.edit_message_text(config["button2_text"], message.chat.id, message_id = message.id, reply_markup=markup, parse_mode='MarkdownV2')
        elif answer == config["button3_data"]:
            markup_another = types.InlineKeyboardMarkup()
            markup_another.add(types.InlineKeyboardButton(config["zsu_but1_name"], url=config["zsu_but1_url"]))
            markup_another.add(types.InlineKeyboardButton(config["zsu_but2_name"], url=config["zsu_but2_url"]))
            markup_another.add(types.InlineKeyboardButton(config["zsu_but3_name"], url=config["zsu_but3_url"]))
            markup_another.add(types.InlineKeyboardButton(config["button_back_text"], callback_data=config["button_back_data"]))
            msg_text = config["button3_text"]
            bot.edit_message_text(msg_text, message.chat.id, message_id = message.id, reply_markup=markup_another)
        elif answer == config["button_back_data"]:
            fu.edit_to_main_template(bot, message)
        elif answer == config["button1_but_data"]:
            fu.create_question(bot, message, 1)
        elif answer == "back_button":
            question_number = str(message.text).split(".")[0][:1]
            fu.create_question(bot, message, int(question_number)-1)
            fu.delete_client_answer(clients, answer, message)
    elif answer.split('_')[0][:1] == "q":
        num = answer.split('_')[0][1:2]
        if num == "1" and answer.split('_')[1][6:] == "1":
            result = """Спробуйте "Шкільний Лайф"
            
💵 Ціна: 150 грн / 4 тижні
☎️ Дзвінки: Безліміт
🌐 Інтернет: 7 ГБ
🤯 А ще у пакеті послуг тарифу: Безліміт на соцмережі, месенджери, освітні платформи."""
            fu.tariff_offer(bot, message, result, 1)
        elif num == "2" and answer.split('_')[1][6:] == "1":
            result = """Рекомендуємо вам тариф "Смарт сім'я S/M/L"

💵 Ціна: 375 - 425 - 500 грн / 4 тижні
☎️ Дзвінки: 500 - 750 - 1500 хв
🌐 Інтернет: 20 - 30 - 50 ГБ
🤯 А ще у пакеті послуг тарифу: Змінюються в залежності від вибранного тарифу"""
            fu.tariff_offer(bot, message, result, 2)
        else:    
            fu.add_client_answer(clients, answer, message)
            if int(num) <= 6:
                fu.create_question(bot, message, int(num)+1)
            else:
                bot.edit_message_text("Ви пройшли тестування\\!\nПочекайте *декілька секунд*, поки наш бот з ШІ обробить ваші відповіді\\.", message.chat.id, message_id = message.id, parse_mode="MarkdownV2")
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": str(clients['clients'][f'{message.chat.first_name}-{message.chat.last_name}'])}
                    ],
                    temperature=0.4
                )
                fu.end_question(bot,message, completion.choices[0].message['content'])
    elif answer.split('_')[0][:1] == "e":
        if answer == "end_button1":
            fu.add_client_answer(clients, answer, message)
            fu.create_question(bot, message, 2)
        elif answer == "end_button2":
            fu.add_client_answer(clients, answer, message)
            fu.create_question(bot, message, 2)
    elif answer.split('_')[0][:1] == "l":
        if answer == config["last_button_data"]:
            clients['clients'][f'{message.chat.first_name}-{message.chat.last_name}'] = []
            fu.create_main_template(bot, message)
            with open('clients.json', 'w') as file:
                json.dump(clients, file, indent=4) 
    bot.answer_callback_query(callback_query_id=call.id)

bot.polling(none_stop = True, interval = 0)