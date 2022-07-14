import os
import datetime
"""
一个自动add . ->commit 'date'-> push的小工具
"""
os.system('git status')
os.system('git add .')

curr_time = datetime.datetime.now() # 2022-07-06 14:55:56.873893 <class 'datetime.datetime'>
curr_time.year          #  <class 'int'>
curr_time.month
curr_time.day
str =  "{}-{}-{}".format(curr_time.year,curr_time.month,curr_time.day)
# print( 'git commit -m' + "'{}'".format(str))
os.system('git commit -m ' + "'{}'".format(str))
os.system('git status')
os.system('git push')