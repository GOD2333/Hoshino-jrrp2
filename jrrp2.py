'''
Descripttion: 
version: 1.0
Author: Rene8028
Date: 2022-07-20 21:58:25
LastEditors: Rene8028
LastEditTime: 2022-07-20 22:54:46
由Rinco304修改适配到HoshinoBot
'''


import datetime
from pathlib import Path
import sqlite3
from hoshino import Service, util, aiorequests, priv
from hoshino.typing import CQEvent
from nonebot.log import logger
import random
from datetime import date

data_dir = Path("data/jrrp2").absolute()
data_dir.mkdir(parents=True, exist_ok=True)

# '''数据库初始化'''
jdb = sqlite3.connect("data/jrrp2/jrrpdata.db")
cursor = jdb.cursor()

# '''表初始化'''
try:
    create_tb_cmd='''
    CREATE TABLE IF NOT EXISTS jdata
    (QQID int,
    Value int,
    Date text);
    '''
    cursor.execute(create_tb_cmd)
except:
    logger.error("jrrp2 Create data table failed")

#自定义数值对应回复
def luck_simple(num):
    if num == 100:
        return '超吉','100！100诶！！你就是欧皇？'
    elif num == 0:
        return '超凶(大寄)','？？？反向欧皇？'
    elif num > 75:
        return '大吉','好耶！今天运气真不错呢'
    elif num > 65:
        return '吉','哦豁，今天运气还顺利哦'
    elif num > 62:
        return '半吉','emm，今天运气一般般呢'
    elif num > 58:
        return '小吉','还……还行吧，今天运气稍差一点点呢'
    elif num > 53:
        return '末小吉','唔……今天运气有点差哦'
    elif num > 18:
        return '末吉','呜哇，今天运气应该不太好'
    elif num > 9:
        return '凶','啊这……(没错……是百分制)，今天还是吃点好的吧'
    else:
        return '大凶','啊这……(个位数可还行)，今天还是吃点好的吧'
    
#新增数据
def insert_tb(qqid,value,date):
    insert_tb_cmd = f'insert into jdata(QQID, Value, Date) values("{qqid}","{value}","{date}")'
    cursor.execute(insert_tb_cmd)
    jdb.commit()
#查询历史数据
def select_tb_all(qqid):
    select_tb_cmd = f'select *from jdata where QQID = {qqid}'
    cursor.execute(select_tb_cmd)
    return cursor.fetchall()
#查询今日是否存在数据
def select_tb_today(qqid,date):
    select_tb_cmd = f'select *from jdata where QQID = {qqid} and Date = {date}'
    cursor.execute(select_tb_cmd)
    results = cursor.fetchall()
    if results:
        return True
    return False
#判断是否本周
def same_week(dateString):
    d1 = datetime.datetime.strptime(dateString,'%y%m%d')
    d2 = datetime.datetime.today()
    return d1.isocalendar()[1] == d2.isocalendar()[1] \
              and d1.year == d2.year
#判断是否本月
def same_month(dateString):
    d1 = datetime.datetime.strptime(dateString,'%y%m%d')
    d2 = datetime.datetime.today()
    return d1.month == d2.month \
              and d1.year == d2.year

sv_help = '''
[.jrrp] [今日人品] [今日运势]   获取你的今日人品
[本周人品] [本周运势] [周运势]  获取你的本周平均人品
[本月人品] [本月运势] [月运势]  获取你的本月平均人品
[总人品] [平均人品] [平均运势]  获取你的历史平均人品
'''.strip()

sv = Service(
    name = '今日人品',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #可见性
    enable_on_default = True, #默认启用
    bundle = '娱乐', #分组归类
    help_ = sv_help #帮助说明
    )


@sv.on_fullmatch(('.jrrp','今日人品','今日运势'))
async def jrrp_handle(bot: Bot, event: CQEvent):
    rnd = random.Random()
    rnd.seed(int(date.today().strftime("%y%m%d")) + int(event.user_id()))
    lucknum = rnd.randint(1,100)
    if not select_tb_today(event.user_id(),date.today().strftime("%y%m%d")):
        insert_tb(event.user_id(),lucknum,date.today().strftime("%y%m%d"))
    await bot.send(event, f"您今日的幸运指数是{lucknum}，为{luck_simple(lucknum)[0]}，{luck_simple(lucknum)[1]}", at_sender=True)


@sv.on_fullmatch(('总人品','平均人品','平均运势'))
async def alljrrp_handle(bot: Bot, event: CQEvent):
    alldata = select_tb_all(event.user_id())
    if alldata == None:
        await bot.send(event, "您还没有过历史人品记录！", at_sender=True)
    times = len(alldata)
    allnum = 0
    for i in alldata:
        allnum = allnum + int(i[1])
    await bot.send(event, f"您一共使用了{times}天今日人品，您历史平均的幸运指数是{round(allnum / times,1)}", at_sender=True)


@sv.on_fullmatch(('本月人品','本月运势','月运势'))
async def monthjrrp_handle(bot: Bot, event: CQEvent):
    alldata = select_tb_all(event.user_id())
    times = 0
    allnum = 0
    for i in alldata:
        if same_month(i[2]):
            times = times + 1
            allnum = allnum + int(i[1])
    if times == 0:
        await bot.send(event, "您本月还没有过人品记录！", at_sender=True)
    await bot.send(event, f"您本月共使用了{times}天今日人品，平均的幸运指数是{round(allnum / times,1)}", at_sender=True)


@sv.on_fullmatch(('本周人品','本周运势','周运势'))
async def weekjrrp_handle(bot: Bot, event: CQEvent):
    alldata = select_tb_all(event.user_id())
    if alldata == None:
        await jrrp.finish(Message(f'[CQ:at,qq={event.user_id()}]您还没有过历史人品记录！'))
    times = 0
    allnum = 0
    for i in alldata:
        if same_week(i[2]):
            times = times + 1
            allnum = allnum + int(i[1])
    if times == 0:
        await bot.send(event, "您本周还没有过人品记录！", at_sender=True)
    await bot.send(event, f"您本周共使用了{times}次jrrp，平均的幸运指数是{round(allnum / times,1)}", at_sender=True)
