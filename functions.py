import telebot
from telebot import types
import json

with open('config.json', 'r', encoding="utf-8") as file:
    config = json.load(file)
    
def questions_func(clients, bot, message, answer, prompt): 
    clients['clients'][f'{message.chat.first_name}-{message.chat.last_name}'].append(answer.split('_')[1][6:])
    with open('clients.json', 'w') as file:
        json.dump(clients, file, indent=4)
    if int(num) <= 6:
        fu.create_question(bot, message, int(num)+1)
    else:
        end_question(bot, message, prompt)

def create_question(bot, message, k):
    markup = types.InlineKeyboardMarkup()
    count = f"q{k}_count"
    
    for i in range(1,config[count]+1):
        markup.add(types.InlineKeyboardButton(config[f"q{k}_answer{i}"], callback_data=f"q{k}_answer{i}_data"))
    if k > 1:
        markup.add(types.InlineKeyboardButton("Попереднє питання", callback_data="back_button"))
    bot.edit_message_text(f"{k}\\. "+config[f"question{k}_text"], message.chat.id, message_id = message.id, reply_markup=markup, parse_mode="MarkdownV2")

def end_question(bot, message, result):
    tariff_number = int(list(filter(str.isdigit, result.splitlines()[-1]))[-1])
    result_form = result.splitlines()
    result_form.pop()
    result = "\n".join(line.strip() for line in result_form)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(config["buy_button_name"], url=config[f"tariff{tariff_number}_url"]))
    markup.add(types.InlineKeyboardButton(config["last_button_name"], callback_data=config["last_button_data"]))
    bot.edit_message_text(result, message.chat.id, message_id = message.id, parse_mode="Markdown", reply_markup=markup)

def tariff_offer(bot, message, result, question_number):
    if question_number == 1:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(config["buy_button_name"], url=config[f"tariff5_url"]))
        markup.add(types.InlineKeyboardButton(config["end_button_name"], callback_data=config["end_button_data"]+f"{question_number}"))
    elif question_number == 2:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Переглянути тарифи", url=config["tariff6_url"]))
        markup.add(types.InlineKeyboardButton(config["end_button_name"], callback_data=config["end_button_data"]+f"{question_number}"))
    bot.edit_message_text(str(result), message.chat.id, message_id = message.id, reply_markup=markup)
    
def create_main_template(bot, message):
    if message.chat.last_name != None:
        msg = f"{message.chat.first_name} {message.chat.last_name}, давай підберемо для тебе тариф\\!\n"
    else:
        msg = f"{message.chat.first_name}, давай підберемо для тебе тариф\\!\n"

    markup = create_main_buttons()
    bot.send_message(message.chat.id, msg +'\n'+ config["main_text"], reply_markup=markup, parse_mode='MarkdownV2')
    
def edit_to_main_template(bot, message):
    if message.chat.last_name != None:
        msg = f"{message.chat.first_name} {message.chat.last_name}, давай підберемо для тебе тариф\\!\n"
    else:
        msg = f"{message.chat.first_name}, давай підберемо для тебе тариф\\!\n"

    markup = create_main_buttons()
    bot.edit_message_text(msg +'\n'+ config["main_text"], message.chat.id, message_id = message.id, reply_markup=markup, parse_mode="MarkdownV2")

def create_main_buttons():
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(config["button1_name"], callback_data=config["button1_data"])
    markup.add(btn1)
    btn2 = types.InlineKeyboardButton(config["button2_name"], callback_data=config["button2_data"])
    btn3 = types.InlineKeyboardButton(config["button3_name"], callback_data=config["button3_data"])
    btn4 = types.InlineKeyboardButton(config["button4_name"], url="https://www.lifecell.ua/uk/mobilnij-zvyazok/taryfy/")
    markup.add(btn2,btn3,btn4)
    return markup

def find_tarif(bot, message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(config["button1_but"], callback_data=config["button1_but_data"]))
    markup.add(types.InlineKeyboardButton(config["button_back_text"], callback_data=config["button_back_data"]))
    bot.edit_message_text(config["button1_text"], message.chat.id, message_id = message.id, reply_markup=markup)
    
def add_client_answer(clients, answer, message):
    clients['clients'][f'{message.chat.first_name}-{message.chat.last_name}'].append(answer.split('_')[1][6:])
    with open('clients.json', 'w') as file:
        json.dump(clients, file, indent=4)

def delete_client_answer(clients, answer, message):
    del clients['clients'][f'{message.chat.first_name}-{message.chat.last_name}'][-1]
    with open('clients.json', 'w') as file:
        json.dump(clients, file, indent=4)