# Hoshino-jrrp2
一个适用于HoshinoBot的带数据库可查询历史平均人品的jrrp插件

此插件移植自nb2插件 [nonebot_plugin_jrrp2](https://github.com/Rene8028/nonebot_plugin_jrrp2)

功能代码没有改动，只做了触发适配与发送和使用帮助

## 如何安装

1. 在HoshinoBot的插件目录modules下clone本项目

   `git clone https://github.com/Rinco304/Hoshino-jrrp2`

2. 在 `config/__bot__.py`的模块列表里加入 `Hoshino-jrrp2`

3. 重启HoshinoBot

## 怎么使用

```
[.jrrp] [今日人品] [今日运势]   获取你的今日人品
[本周人品] [本周运势] [周运势]  获取你的本周平均人品
[本月人品] [本月运势] [月运势]  获取你的本月平均人品
[总人品] [平均人品] [平均运势]  获取你的历史平均人品
```

## 数据库

本插件使用sqlite作为数据库来保存历史查询数据，保存位置为`/HoshinoBot/data/jrrp2/jrrpdata.db`

## 参考致谢

| [nonebot_plugin_jrrp2](https://github.com/Rene8028/nonebot_plugin_jrrp2) | [@Rene8028](https://github.com/Rene8028) |
