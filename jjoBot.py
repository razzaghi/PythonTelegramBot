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
    'inews': 'دریافت مهمترین اخبار روز',
    'menu': 'منو'
}

serviceIp = "10.0.9.151"

getLast = "http://" + serviceIp + "/DoCommand.aspx?fn=getLast&Code=@code&top=5&nf=28"
getImportant = "http://"+ serviceIp +"/DoCommand.aspx?fn=getPopular"
search = "http://" + serviceIp + "/DoCommand.aspx?fn=search&Code=@code&top=5&nf=28&query="
inews = "http://" + serviceIp + "/DoCommand.aspx?fn=search&Code=@code&top=5&nf=28"
lnews = "http://" + serviceIp + "/DoCommand.aspx?fn=search&Code=@code&top=5&nf=28"

menuItem = [
    "lnews",
    "inews",
    "serviceTable"
]

menuItemLbl = [
    "آخرین اخبار",
    "مهمترین اخبار",
    "سرویس های برگزیده"
]

servicesCodeTable = [
    "01-04-102",
    "01-02-01-169",
    "01-06-91",
    "01-03-01-119",
    "112",
    "-1"
]

servicesNameTable = [
    "جامعه",
    "سیاسی",
    "حوادث",
    "اقتصادی",
    "ورزشی",
    "بازگشت"
]


hideBoard = types.ReplyKeyboardHide()  # if sent as reply_markup, will hide the keyboard
menuSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)  #create the image selection keyboard
subMenuSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)  #create the image selection keyboard
for name in menuItemLbl:
    menuSelect.add(name)

for name in servicesNameTable:
    subMenuSelect.add(name)

def listener(messages):
    for m in messages:
        cid = m.chat.id
        print(m)
        if m.content_type == 'text':
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


@bot.message_handler(commands=['menu'])
def command_image(m):
    cid = m.chat.id
    bot.send_message(cid, "لطفا گزینه مورد نظر خود را انتخاب نمایید", reply_markup=menuSelect)  #show the keyboard

def getServiceCode(t):
    flag = False
    i = 0
    for name in servicesNameTable:
        if name == t:
            flag = True
            break
        i += 1
    if flag:
        return servicesCodeTable[i]
    else:
        return False

def getMenuCode(t):
    flag = False
    i = 0
    for name in menuItemLbl:
        if name == t:
            flag = True
            break
        i += 1
    if flag:
        return menuItem[i]
    else:
        return False

def getLastFromService(cid,serviceCode):
    url = getLast.replace("@code",serviceCode)
    content = requests.get(url).json()
    for r in content:
        data = r
        url = data['Url'].replace("jamejamonline","jjo")
        url = data['Url'].replace("www.jamejamonline","jjo")
        bot.send_message(cid, "http://JJO.Ir \r\n" + data['Title'] + "\r\n" + url,disable_web_page_preview=True)

def lnews(cid):
    url = getLast.replace("@code","-1")
    content = requests.get(url).json()
    for r in content:
        data = r
        url = data['Url'].replace("jamejamonline","jjo")
        url = data['Url'].replace("www.jamejamonline","jjo")
        bot.send_message(cid, "http://JJO.Ir \r\n" + data['Title'] + "\r\n" + url,disable_web_page_preview=True)

def inews(cid):
    content = requests.get(getImportant).json()
    for r in content:
        data = r
        url = data['Url'].replace("jamejamonline","jjo")
        url = data['Url'].replace("www.jamejamonline","jjo")
        bot.send_message(cid, "http://JJO.Ir \r\n" + data['Title'] + "\r\n" + url,disable_web_page_preview=True)

def showSubmenu(cid):
    bot.send_message(cid, "لطفا سرویس مورد نظر خود را انتخاب نمایید", reply_markup=subMenuSelect)  #show the keyboard

@bot.message_handler(func=lambda message: (message.text in servicesNameTable))
def msg_servicePackageSelect(m):
    cid = m.chat.id
    print("Submenu")
    text = m.text
    bot.send_chat_action(cid,'typing')
    serviceCode =getServiceCode(m.text)
    if serviceCode != False:
        if(serviceCode=="-1"):
             bot.send_message(cid, "لطفا گزینه مورد نظر خود را انتخاب نمایید", reply_markup=menuSelect)
        else:
            getLastFromService(cid,serviceCode)

@bot.message_handler(func=lambda message: (message.text in menuItemLbl))
def msg_menuSelect(m):
    print("Main Menu")
    cid = m.chat.id
    text = m.text
    bot.send_chat_action(cid,'typing')
    menuCode =getMenuCode(m.text)
    print(menuCode)
    if menuCode != False:
        if menuCode=="lnews":
            lnews(cid)
        elif menuCode=="inews":
            inews(cid)
        elif menuCode=="serviceTable":
            showSubmenu(cid)

@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    helpText = "دستورات زیر موجود است : \n"
    for key in commands:
        helpText += "/" + key + ": "
        helpText += commands[key] + "\n"
    bot.send_message(cid, helpText)

@bot.message_handler(commands=['lnews'])
def command_lastNews(m):
    cid = m.chat.id
    bot.send_chat_action(cid, 'typing')
    lnews(cid)


@bot.message_handler(commands=['inews'])
def command_important_news(m):
    cid = m.chat.id
    bot.send_chat_action(cid, 'typing')
    inews(cid)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    bot.send_message(m.chat.id,
                     "Iدستور وارد شده صحیح نمی باشد برای راهنمایی  از این دستور ا ستفاده کنید \r\n /help")


while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break
