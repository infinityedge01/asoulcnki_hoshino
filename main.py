import hoshino
from hoshino.service import Service
from hoshino.typing import HoshinoBot, CQEvent
from hoshino.util import DailyNumberLimiter, FreqLimiter
import requests
import random
from .request import cnki, essay

sv = Service('枝网工具')

_flt = FreqLimiter(30)
Essay = essay()
id_dict = {
    '672346917': ['向晚', '晚晚', 'Ava', 'AVA', 'ava', '顶晚人', '向晚大魔王'],
    '672353429': ['贝拉', '拉姐', 'Bella', 'BELLA', 'bella', '贝极星', '贝拉kira'],
    '351609538': ['珈乐', '王力口乐', 'Carol', 'CAROL', 'carol', '皇珈骑士', '乐', '音乐珈', '珈乐Carol'],
    '672328094': ['嘉然', '然然', 'Diana', 'DIANA', 'diana', '嘉心糖', '圣嘉然', '嘉然今天吃什么'],
    '672342685': ['乃琳', '乃0', 'Eileen', 'EILEEN', 'eileen', '奶淇琳', '乃淇琳', '乃琳Queen'],
    '703007996': ['A-SOUL_Official', 'ASoul', 'asoul', 'ASOUL', 'Asoul', '官号']
}
@sv.on_prefix(('枝江作文', '枝江作文展', '枝江小作文')) 
async def concat_head(bot: HoshinoBot, ev: CQEvent):
    uid = ev.user_id
    if not _flt.check(uid):
        await bot.finish(ev, '你看太多小作文了')
        return
    pass
    timeRangeMode = 1
    ids = ''
    args = ev.raw_message.split(' ')
    for arg in args:
        for (key, value) in id_dict.items():
            if arg in value:
                ids = key
                break
        if arg.startswith('3') :
            timeRangeMode = 2
        elif arg.startswith('all') :
            timeRangeMode = 0
    page = 1
    tmp = ids + str(timeRangeMode)
    if tmp in Essay.pagenum.keys():
        page = max(page, Essay.pagenum[tmp] // 3 * 2 if Essay.pagenum[tmp] < 20 else Essay.pagenum[tmp] // 2)
    page = max(page, 1)
    page = random.randint(1, page)
    print(ids, timeRangeMode, page)
    s = await Essay.Call(timeRangeMode = timeRangeMode, ids = ids, pageNum= page)
    s = Essay.parse(s, timeRangeMode, ids)
    _flt.start_cd(uid, 30)
    await bot.send(ev, s)
    
@sv.on_prefix(('枝网查重 ', '枝江查重 ', '小作文查重 '))
async def concat_head(bot: HoshinoBot, ev: CQEvent):
    uid = ev.user_id
    if not _flt.check(uid):
        await bot.finish(ev, '你查重太多次了')
        return
    pass
    s = ev.raw_message.split(' ', 1)
    if len(s) < 2:
        return
    s = s[1]
    if len(s) < 10:
        await bot.finish(ev, '小作文太短了')
        return
    if len(s) > 1000:
        await bot.finish(ev, '小作文太长了')
        return
    s = await cnki.Call(s)
    s = cnki.parse(s)
    _flt.start_cd(uid, 30)
    await bot.send(ev, s)

@sv.on_prefix(('枝网查重完整 ', '枝江查重完整 ', '小作文查重完整 '))
async def concat_head(bot: HoshinoBot, ev: CQEvent):
    uid = ev.user_id
    if not _flt.check(uid):
        await bot.finish(ev, '你查重太多次了')
        return
    pass
    s = ev.raw_message.split(' ', 1)
    if len(s) < 2:
        return
    s = s[1]
    if len(s) < 10:
        await bot.finish(ev, '小作文太短了')
        return
    if len(s) > 1000:
        await bot.finish(ev, '小作文太长了')
        return
    s = await cnki.Call(s)
    s = cnki.parse(s, verbose=True)
    _flt.start_cd(uid, 30)
    await bot.send(ev, s)
    
@sv.on_prefix(('枝网帮助', '枝江帮助'))
async def concat_head(bot: HoshinoBot, ev: CQEvent):
    help_msg =  '''
    枝网查重 [小作文] 对小作文进行枝网查重，输出简短报告
枝网查重完整 [小作文] 对小作文进行枝网查重，输出完整报告
枝江作文展 [嘉然/向晚/珈乐/贝拉/乃琳/官号] [3/7/all] 随机输出一篇枝江小作文，参数为限定up主范围，限定时间（三日内/七日内/所有）
    '''.strip()
    await bot.finish(ev, help_msg)