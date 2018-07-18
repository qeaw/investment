import tkinter,time
import requests
import os
# from tkinter import Tk,Button,mainloop
import numpy as np
import pandas as pd
import smtplib
from email.mime.text import MIMEText

from pandas import DataFrame, Series
from tkinter import *
from tkinter import messagebox
from datetime import datetime, timedelta
import itchat


itchat.auto_login(hotReload= True)

print(str(itchat.search_friends(name="蔚")[0]).split(","))

print(dir(itchat))

print(itchat.get_chatrooms())