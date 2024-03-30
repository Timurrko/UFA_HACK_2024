import sqlite3

import telebot
from telebot import types

from DataBase import DataBase
from config import token
from db_config import db_path

bot = telebot.TeleBot(token)

dbase = DataBase(db_path)
curr_log = ''


@bot.message_handler(commands=['start'])
def start(message):
    keyb = types.InlineKeyboardMarkup(row_width=1)
    ent_butn = types.InlineKeyboardButton(text='Войти', callback_data='ent')
    reg_butn = types.InlineKeyboardButton(text='Зарегестрироваться', callback_data='reg')
    keyb.add(ent_butn, reg_butn)
    bot.send_message(message.chat.id, "Приветствую!", reply_markup=keyb)


@bot.callback_query_handler(func=lambda callback: callback.data == 'ent')
def authorization(callback):
    message = callback.message
    bot.send_message(message.chat.id, 'Введите логин')
    bot.register_next_step_handler(message, check_for_login)


def check_for_login(message):
    global curr_log
    curr_log = message.text
    if dbase.check_login(message.text):
        bot.send_message(message.chat.id, 'Введите пароль')
        bot.register_next_step_handler(message, check_for_pass)
    else:
        bot.send_message(message.chat.id, 'Этот логин не существует.')
        bot.register_next_step_handler(message, check_for_login)


def check_for_pass(message):
    print(curr_log)
    print(hash(message.text))

    if not dbase.check_login_data(curr_log, hash(message.text)):
        bot.send_message(message.chat.id, 'Авторизация успешна.')
        bot.register_next_step_handler(message, authorised_session(message.chat.id))
    else:
        bot.send_message(message.chat.id, 'Пароль неверный.')
        bot.register_next_step_handler(message, check_for_pass)
    print(dbase.check_login_data(curr_log, hash(message.text)))


@bot.callback_query_handler(func=lambda callback: callback.data == 'reg')
def check_for_callback(callback):
    message = callback.message
    bot.send_message(message.chat.id, 'Придумайте логин')
    bot.register_next_step_handler(message, new_login)


def new_login(message):
    if dbase.check_login(message.text):
        bot.send_message(message.chat.id, 'Этот логин занят. Придумайте другой логин.')
        bot.register_next_step_handler(message, new_login)
    else:
        print(message.text)
        global curr_log
        curr_log = message.text
        bot.send_message(message.chat.id, 'Придумайте пароль')
        bot.register_next_step_handler(message, new_pass)


def new_pass(message):
    global curr_log
    user_pass = message.text
    print(hash(user_pass))
    dbase.add_user(curr_log, hash(user_pass), 0)
    print(message.chat.id)
    print(curr_log)
    dbase.add_tg_user(curr_log, message.chat.id)
    bot.send_message(message.chat.id,
                     'Пользователь создан!' + '\n' + 'Логин: ' + curr_log + '\t' + 'Пароль: ' + user_pass)

    authorised_session(message.chat.id)


def authorised_session(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    proj_manag_butn = types.InlineKeyboardButton(text='Управление проектами', callback_data='proj_manag')
    exit_butn = types.InlineKeyboardButton(text='Выход', callback_data='exit')
    keyboard.add(proj_manag_butn, exit_butn)
    bot.send_message(message, "Приветствую!", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda callback: callback.data == 'proj_manag')
def proj_managment(callback):
    message = callback.message
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    create_proj_butn = types.InlineKeyboardButton(text='Создание проекта', callback_data='proj_create')
    mod_butn = types.InlineKeyboardButton(text='Редактирование', callback_data='mod_proj')
    keyboard.add(create_proj_butn, mod_butn)
    bot.send_message(message.chat.id, "Режим управления проектами!", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda callback: callback.data == 'proj_create')
def proj_create(callback):
    message = callback.message
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    bot.send_message(message.chat.id, "Введите название пректа")
    bot.register_next_step_handler(message, proj_name)


def proj_name(message):
    project_name = message.text
    dbase.add_project(project_name, " ")
    project_exits = dbase.check_if_project_exist(project_name)
    if project_exits:
        bot.send_message(message.chat.id, "Проект успешно создан")
    else:
        bot.send_message(message.chat.id, "Не удалось создать проект")

@bot.callback_query_handler(func=lambda callback: callback.data == 'mod_proj')
def proj_mod(callback):
    message = callback.message
    data = dbase.select_project()
    bot.send_message(message.chat.id, "Выберете проект",  data)
    bot.register_next_step_handler(message, change_proj)

def change_proj(message):
    global project_name
    project_name = message.text
    if dbase.check_if_project_exist(project_name):
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        add_user_butn = types.InlineKeyboardButton(text='Добавить пользователя', callback_data='proj_add_user')
        add_comp_butn = types.InlineKeyboardButton(text='Добавить компонент', callback_data='proj_add_comp')
        del_butn = types.InlineKeyboardButton(text='Удалить проект', callback_data='proj_del')
        keyboard.add(add_user_butn, add_comp_butn, del_butn)
        bot.send_message(message.chat.id, "Управление проектом!", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Прект не найден, поробуйте еще раз")
        bot.register_next_step_handler(message, change_proj)

@bot.callback_query_handler(func=lambda callback: callback.data == 'proj_add_comp')
def add_component(callback):
    message = callback.message
    bot.send_message(message.chat.id, "Выберете компонент, введите списком")
    bot.register_next_step_handler(message, component_name)

def component_name(message):
    component = message.text
    dbase.add_components_to_project(project_name, component )
@bot.callback_query_handler(func=lambda callback: callback.data == 'exit')
def exit(callback):
    message = callback.message
    dbase.delete_tg_user(curr_log, message.chat.id)


bot.polling()
