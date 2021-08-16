import asyncio
import functools
import requests
import json
import time
import datetime
import random

async def get_asyncio(url):
    future = asyncio.get_event_loop().run_in_executor(None, functools.partial(requests.get, url = url))
    response = await future
    return response
async def post_asyncio(url, json):
    future = asyncio.get_event_loop().run_in_executor(None, functools.partial(requests.post, url = url, json = json))
    response = await future
    return response

class cnki:
    async def Call(s : str):
        data = {
            "text" : s
        }
        r = await post_asyncio(url = 'https://asoulcnki.asia/v1/api/check', json = data)
        response = r.json()
        return response
    
    def parse(data : dict, verbose = False):
        err = "查重失败，请稍后再试"
        if 'code' not in data:
            return err
        if data['code'] != 0:
            return err
        data = data['data']
        now = datetime.datetime.now()
        timestr = now.strftime("%Y/%m/%d %H:%M:%S")
        s = "枝网文本复制检测报告(简洁)\n"
        if verbose:
            s = "枝网文本复制检测报告\n"
        s = s + "查重时间: " + timestr + "\n"
        s = s + "总文字复制比: %.2f%%\n" % (data['rate'] * 100)
        related = data['related']
        if len(related) == 0:
            s = s + "查重结果仅作参考，请注意辨别是否为原创\n"
            return s
        sample = related[0]
        s = s + "相似小作文: " + sample['reply_url'] + "\n"
        reply = sample['reply']
        s = s + "作者: " + reply['m_name'] + "\n"
        s = s + "发表时间: " + datetime.datetime.fromtimestamp(reply['ctime']).strftime("%Y/%m/%d %H:%M:%S") + "\n"
        if verbose :
            s = s + "内容: \n" + reply['content'] + '\n'
        s + "查重结果仅作参考，请注意辨别是否为原创"
        return s
    
class essay:
    def __init__(self):
        self.pagenum = {}
    async def Call(self, timeRangeMode = 1, ids = '', pageNum = 1):
        url = 'https://asoulcnki.asia/v1/api/ranking/?pageSize=10&pageNum={}&timeRangeMode={}&sortMode=0&ids={}&keywords='.format(pageNum, timeRangeMode, ids)
        r = await get_asyncio(url = url)
        response = r.json()
        return response
    
    def parse(self, data : dict, timeRangeMode, ids):
        err = "查找失败，请稍后再试"
        if 'code' not in data:
            return err
        if data['code'] != 0:
            return err
        data = data['data']
        related = data['replies']
        self.pagenum[ids + str(timeRangeMode)] = (data['all_count'] - 1) // 10 + 1
        if len(related) == 0:
            s = "未查找到小作文\n"
            return s
        reply = random.choice(related)
        s = "枝江作文展 作品#{}\n".format(reply['rpid'])
        url = "https://www.bilibili.com/video/av"
        if reply['type_id'] == 11 or reply['type_id'] == 17:
            url = "https://t.bilibili.com/"
        elif reply['type_id'] == 12:
            url = "https://www.bilibili.com/read/cv"
        if reply['type_id'] == 11 or reply['type_id'] == 17:
            url = url + reply['dynamic_id']
        else:
            url = url + reply['oid']
        url = url + "/#reply" + reply['rpid'] 
        s = s + "链接: " + url + "\n"
        s = s + "作者: " + reply['m_name'] + "\n"
        s = s + "发表时间: " + datetime.datetime.fromtimestamp(reply['ctime']).strftime("%Y/%m/%d %H:%M:%S") + "\n"
        s = s + "总赞: " + str(reply['similar_like_sum']) + " "
        s = s + "引用: " + str(reply['similar_count']) + "\n"
        s = s + "内容: \n" + reply['content']
        return s
    
