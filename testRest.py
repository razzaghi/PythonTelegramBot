#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import telebot
import requests
from telebot import types
import time



serviceIp = "10.0.9.151"

getLast = "http://" + serviceIp + "/DoCommand.aspx?fn=getLast&Code=@code&top=5&nf=28"
getImportant = "http://"+ serviceIp +"/DoCommand.aspx?fn=getPopular"
search = "http://" + serviceIp + "/DoCommand.aspx?fn=search&Code=@code&top=5&nf=28&query="
inews = "http://" + serviceIp + "/DoCommand.aspx?fn=search&Code=@code&top=5&nf=28"
lnews = "http://" + serviceIp + "/DoCommand.aspx?fn=search&Code=@code&top=5&nf=28"

while True:
    try:
        content = requests.get(getImportant).json()
        for r in content:
            data = r
            url = data['Url'].replace("www.jamejamonline","jjo")
            url = url.replace("jamejamonline","jjo")
            print(data['Title'] + "\r\n" + url)
    except Exception as inst:
        print(type(inst))     # the exception instance
        print(inst.args)      # arguments stored in .args
        print(inst)           # __str__ allows args to be printed directly