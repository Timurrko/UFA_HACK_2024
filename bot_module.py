import telebot
from telebot import types
from config import token
import asyncio
import json
import requests

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    keyb = types.InlineKeyboardMarkup(row_width=2)
    ent_butn = types.InlineKeyboardButton(text='Войти', callback_data='ent')
    reg_butn = types.InlineKeyboardButton(text='Зарегестрироваться', callback_data='reg')
    keyb.add(ent_butn, reg_butn)
    bot.send_message(message.chat.id, "Приветствую!", reply_markup=keyb)


@bot.callback_query_handler(func=lambda callback: callback.data == 'reg')
def check_for_callback(callback):
    message = callback.message
    bot.send_message(message.chat.id, 'Придумайте логин')
    bot.register_next_step_handler(message, new_login)


def new_login(message):
    global user_login
    user_login = message.text
    if user_login != 'ben':
        print(user_login)
        bot.send_message(message.chat.id, 'Придумайте пароль')
        bot.register_next_step_handler(message, new_pass)
    else:
        bot.send_message(message.chat.id, 'Этот логин занят. Придумайте другой логин.')
        bot.register_next_step_handler(message, new_login)


def new_pass(message):
    global user_pass
    user_pass = message.text
    print(user_pass)
    bot.send_message(message.chat.id,
                     'Пользователь создан!' + '\n' + 'Логин: ' + user_login + '\t' + 'Пароль: ' + user_pass)
    authorised_session(user_login, user_pass)


def authorised_session(log, passw):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    new_proj_butn = types.InlineKeyboardButton(text='Создать новый проект', callback_data='/createproj')
    exist_proj_butn = types.InlineKeyboardButton(text='Посмотреть существующие проекты', callback_data='/seeprojs')


bot.polling()
