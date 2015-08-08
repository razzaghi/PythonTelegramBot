#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import telebot
import requests
from telebot import types
import time

TOKEN = '93764156:AAFrZoe6Qe7gkX88AV_PqNqETO2NCXkk07Q'

commands = {
              'help': 'راهنمایی در مورد ',
              'lnews': 'دریافت آخرین اخبار',
              'inews': 'دریافت مهمترین اخبار روز'
}

hideBoard = types.ReplyKeyboardHide()  # if sent as reply_markup, will hide the keyboard

def listener(messages):
    for m in messages:
        cid = m.chat.id
        if m.content_type == 'text':
            # print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)
            print("[" + str(m.chat.id) + "]: " + m.text)


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  #register listener
try:
    bot.polling()
except Exception:
    pass


@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    bot.send_message(cid, "سلام خوش اومدی، امیدوارم بتونم بهترین اخبار رو در اختیارت بذارم")


@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    helpText = "دستورات زیر موجود است : \n"
    for key in commands:
        helpText += "/" + key + ": "
        helpText += commands[key] + "\n"
    bot.send_message(cid, helpText)


def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        else:
            item = item.encode('utf-8')
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        key = key.encode('utf-8')
        if isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        else:
            value = value.encode('utf-8')
        rv[key] = value
    return rv

@bot.message_handler(commands=['lnews'])
def command_lastNews(m):
    cid = m.chat.id
    bot.send_chat_action(cid, 'typing')
    content = requests.get('http://10.0.9.31/DoCommand.aspx?fn=getLast&Code=-1&top=5').json()
    for r in content:
        # data = _decode_dict(r)
        data = r
        bot.send_message(cid, "http://JJO.Ir \r\n"+data['Title']+"\r\n"+data['Url'])

@bot.message_handler(commands=['inews'])
def command_important_news(m):
    cid = m.chat.id
    bot.send_chat_action(cid, 'typing')
    content = requests.get('http://10.0.9.31/DoCommand.aspx?fn=getPopular').json()
    i=0
    for r in content:
        if i==3:
            break
        i+=1
        # data = _decode_dict(r)
        data = r
        bot.send_message(cid, "http://JJO.Ir \r\n"+data['Title']+"\r\n"+data['Url'])

@bot.message_handler(func=lambda message: message.text == "hi")
def command_textHi(m):
    bot.send_message(m.chat.id, "سلام به دوست خوبم")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    bot.send_message(m.chat.id,
                     "Iدستور وارد شده صحیح نمی باشد برای راهنمایی  از این دستور ا ستفاده کنید \r\n /help")  #this is the standard reply to a normal message

while True:  # Don't let the main Thread end.
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break
