
import random
import re
from netflav.dbs.db import sqldb
from scrapy.exceptions import IgnoreRequest
import aiohttp
import base64


class RandomUserAgentMiddleware(object):
    def __init__(self):
        self.user_agent = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.1021.400 QQBrowser/9.0.2524.400",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        ]

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(self.user_agent)
        request.headers['Cookie'] = 'i18next=zh'


class UrlFilterMiddleware(object):
    def __init__(self):
        self.db = sqldb()

    def process_request(self, request, spider):
        # 先取出url中的id
        url = request.url
        if 'id=' in url:
            id = re.findall(r'video\?id=(.*)', url)[0]
        # 判断是否下载过
            if self.db.isExit(id) is False:
                print("id:{}已经下载过".format(id))
                raise IgnoreRequest("该内容已经下载过")
        return None


class ProxyMiddleware(object):

    async def process_request(self, request, spider):
        url = request.url
        if 'streamtape.to' in url:
            return None
        # request.meta['max_retry_times'] = 10
        # async with aiohttp.ClientSession() as client:
        #     resp = await client.get(self.proxy_url)
        #     if not resp.status == 200:
        #         return
        #     print(await resp.text())
            # proxy = 'https://' + await resp.text()
            request.meta['proxy'] = "http://customer-7894ab:bec5cc43@proxy.ipipgo.com:31212"
            # auths = base64.b64encode(bytes('7894ab:bec5cc43', 'utf-8'))
            # request.headers['Proxy-Authorization'] = b'Basic ' + auths
            request.header['Connection'] = "Close"
