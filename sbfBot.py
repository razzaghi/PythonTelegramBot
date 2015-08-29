#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import telebot
import requests
from telebot import types
import time

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)


TOKEN = '98066991:AAGdW3DZMZukIBy4UxapfYQ4rexYkVmoeHM'

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
    try:
        for m in messages:
            cid = m.chat.id
            if m.content_type == 'text':
                print("[" + str(cid) + "]: " + m.text)
    except Exception as inst:
        print(type(inst))     # the exception instance
        print(inst.args)      # arguments stored in .args
        print(inst)           # __str__ allows args to be printed directly

bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  #register listener
try:
    bot.polling()
except Exception:
    pass


@bot.message_handler(commands=['start'])
def command_start(m):
    try:
        cid = m.chat.id
        bot.send_message(cid, "سلام خوش اومدی، امیدوارم بتونم بهترین اخبار رو در اختیارت بذارم")
    except Exception as inst:
        print(type(inst))     # the exception instance
        print(inst.args)      # arguments stored in .args
        print(inst)           # __str__ allows args to be printed directly


@bot.message_handler(commands=['menu'])
def command_image(m):
    cid = m.chat.id
    sendCommandForMenu(cid, "لطفا گزینه مورد نظر خود را انتخاب نمایید", reply_markup=menuSelect)  #show the keyboard

def callAPi(url):
    s = requests.Session()
    s.mount('https://', MyAdapter())
    return s.get(url).json()


def getServiceCode(t):
    try:
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
    except Exception as inst:
        print(type(inst))     # the exception instance
        print(inst.args)      # arguments stored in .args
        print(inst)           # __str__ allows args to be printed directly

def getMenuCode(t):
    try:
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
    except Exception as inst:
        print(type(inst))     # the exception instance
        print(inst.args)      # arguments stored in .args
        print(inst)           # __str__ allows args to be printed directly


def getLastFromService(cid,serviceCode):
    try:
        print(serviceCode)
        url = getLast.replace("@code",serviceCode)
        print(url);
        content = callAPi(url)
        for r in content:
            data = r
            url = data['Url'].replace("www.jamejamonline","jjo")
            url = url.replace("jamejamonline","jjo")
            sendText(cid, "http://JJO.Ir \r\n" + data['Title'] + "\r\n" + url)
    except Exception as inst:
        print(type(inst))     # the exception instance
        print(inst.args)      # arguments stored in .args
        print(inst)           # __str__ allows args to be printed directly

def sendText(cid,text):
    try:
        bot.send_message(cid, "@jjoBot \r\n"+text,disable_web_page_preview=True)
    except Exception as inst:
        print(type(inst))     # the exception instance
        print(inst.args)      # arguments stored in .args
        print(inst)           # __str__ allows args to be printed directly

def sendCommandForMenu(cid,text,reply_markup):
    try:
        bot.send_message(cid, "@jjoBot \r\n"+text,reply_markup=reply_markup)
    except Exception as inst:
        print(type(inst))     # the exception instance
        print(inst.args)      # arguments stored in .args
        print(inst)           # __str__ allows args to be printed directly


def lnews(cid):
    try:
        url = getLast.replace("@code","-1")
        content = callAPi(url)
        for r in content:
            data = r
            url = data['Url'].replace("www.jamejamonline","jjo")
            url = url.replace("jamejamonline","jjo")
            sendText(cid, "http://JJO.Ir \r\n" + data['Title'] + "\r\n" + url)
    except Exception as inst:
        print(type(inst))     # the exception instance
        print(inst.args)      # arguments stored in .args
        print(inst)           # __str__ allows args to be printed directly

def inews(cid):
    try:
        content = callAPi(getImportant)
        for r in content:
            data = r
            url = data['Url'].replace("www.jamejamonline","jjo")
            url = url.replace("jamejamonline","jjo")
            sendText(cid, "http://JJO.Ir \r\n" + data['Title'] + "\r\n" + url)
    except Exception as inst:
        print(type(inst))     # the exception instance
        print(inst.args)      # arguments stored in .args
        print(inst)           # __str__ allows args to be printed directly

def showSubmenu(cid):
    sendCommandForMenu(cid, "لطفا سرویس مورد نظر خود را انتخاب نمایید", reply_markup=subMenuSelect)  #show the keyboard

@bot.message_handler(func=lambda message: (message.text in servicesNameTable))
def msg_servicePackageSelect(m):
    try:
        cid = m.chat.id
        print("Submenu")
        text = m.text
        bot.send_chat_action(cid,'typing')
        serviceCode =getServiceCode(m.text)
        if serviceCode != False:
            if(serviceCode=="-1"):
                 sendCommandForMenu(cid, "لطفا گزینه مورد نظر خود را انتخاب نمایید", reply_markup=menuSelect)
            else:
                getLastFromService(cid,serviceCode)
    except Exception as inst:
        print(type(inst))     # the exception instance
        print(inst.args)      # arguments stored in .args
        print(inst)           # __str__ allows args to be printed directly

@bot.message_handler(func=lambda message: (message.text in menuItemLbl))
def msg_menuSelect(m):
    try:
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
    except Exception as inst:
        print(type(inst))     # the exception instance
        print(inst.args)      # arguments stored in .args
        print(inst)           # __str__ allows args to be printed directly

@bot.message_handler(commands=['help'])
def command_help(m):
    try:
        cid = m.chat.id
        helpText = "دستورات زیر موجود است : \n"
        for key in commands:
            helpText += "/" + key + ": "
            helpText += commands[key] + "\n"
        sendText(cid, helpText)
    except Exception as inst:
        print(type(inst))     # the exception instance
        print(inst.args)      # arguments stored in .args
        print(inst)           # __str__ allows args to be printed directly

@bot.message_handler(commands=['lnews'])
def command_lastNews(m):
    try:
        cid = m.chat.id
        bot.send_chat_action(cid, 'typing')
        lnews(cid)
    except Exception as inst:
        print(type(inst))     # the exception instance
        print(inst.args)      # arguments stored in .args
        print(inst)           # __str__ allows args to be printed directly


@bot.message_handler(commands=['inews'])
def command_important_news(m):
    try:
        cid = m.chat.id
        bot.send_chat_action(cid, 'typing')
        inews(cid)
    except Exception as inst:
        print(type(inst))     # the exception instance
        print(inst.args)      # arguments stored in .args
        print(inst)           # __str__ allows args to be printed directly

@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    try:
        sendText(m.chat.id,
                     "Iدستور وارد شده صحیح نمی باشد برای راهنمایی  از این دستور ا ستفاده کنید \r\n /help")
    except Exception as inst:
        print(type(inst))     # the exception instance
        print(inst.args)      # arguments stored in .args
        print(inst)           # __str__ allows args to be printed directly



while True:
    try:
        time.sleep(1)
    except Exception as inst:
        print(type(inst))     # the exception instance
        print(inst.args)      # arguments stored in .args
        print(inst)           # __str__ allows args to be printed directly