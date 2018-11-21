# coding=utf-8
"""
@author: congying
@email: wangcongyinga@gmail.com 
@time: 2018/11/19
"""
import requests
import json
import re


class MusicDownloader(object):
    def __init__(self, play_url):
        self.play_url = play_url

    def crawl_download_url(self):
        raise NotImplementedError


class Zingmp3AudioDownloader(MusicDownloader):
    download_url = 'https://mp3.zing.vn/xhr/media/get-url-download?type=audio&sig={}&code={}'

    def crawl_download_url(self):
        sig, code = self.gen_token()
        url = self.download_url.format(sig, code)
        download_prefix = "https://mp3.zing.vn"
        data = requests.get(url)
        j_data = json.loads(data.text)
        data_info = j_data.get('data', '')
        sources = data_info.get('sources')
        if '128' in sources:
            url_info = sources.get('128', '')
            download_url_128 = download_prefix + url_info.get('link', '') if url_info else ''
        else:
            download_url_128 = ''
        if '320' in sources:
            url_info = sources.get('320', '')
            download_url_320 = download_prefix + url_info.get('link', '') if url_info else ''
        else:
            download_url_320 = ''
        if 'lossless' in sources:
            url_info = sources.get('lossless', '')
            download_url_lossless = download_prefix + url_info.get('link', '') if url_info else ''
        else:
            download_url_lossless = ''
        player = download_url_128
        title = data_info.get('title', '')
        thumbnail = data_info.get('thumb', '')
        artist = data_info.get('artist', '')
        return player, title, artist, thumbnail, download_url_128, download_url_320, download_url_lossless

    def gen_token(self):
        req = requests.get(self.play_url)
        sig_pattern = "data-sig=\"([a-zA-Z0-9]*)\""
        code_pattern = "data-code=\"([a-zA-Z0-9]*)\""
        sig = re.findall(sig_pattern, req.text)
        code = re.findall(code_pattern, req.text)
        return sig[0], code[0]


class Zingmp3VideoDownloader(MusicDownloader):
    download_url = 'https://mp3.zing.vn/xhr/media/get-url-download?type=video&sig={}&code={}'

    def crawl_download_url(self):
        sig, code = self.gen_token()
        url = self.download_url.format(sig, code)
        download_prefix = "https://mp3.zing.vn"
        data = requests.get(url)
        j_data = json.loads(data.text)
        data_info = j_data.get('data', '')
        sources = data_info.get('sources')
        if '360' in sources:
            url_info = sources.get('360', '')
            download_url_360 = download_prefix + url_info.get('link', '') if url_info else ''
        else:
            download_url_360 = ''
        if '480' in sources:
            url_info = sources.get('480', '')
            download_url_480 = download_prefix + url_info.get('link', '') if url_info else ''
        else:
            download_url_480 = ''
        if '720' in sources:
            url_info = sources.get('720', '')
            download_url_720 = download_prefix + url_info.get('link', '') if url_info else ''
        else:
            download_url_720 = ''
        if '1080' in sources:
            url_info = sources.get('1080', '')
            download_url_1080 = download_prefix + url_info.get('link', '') if url_info else ''
        else:
            download_url_1080 = ''

        title = data_info.get('title', '')
        thumbnail = data_info.get('thumb', '')
        artist = data_info.get('artist', '')
        player = download_url_360
        return player, title, thumbnail, artist, download_url_360, download_url_480, download_url_720, download_url_1080

    def gen_token(self):
        req = requests.get(self.play_url)
        sig_pattern = "data-sig=\"([a-zA-Z0-9]*)\""
        code_pattern = "data-code=\"([a-zA-Z0-9]*)\""
        sig = re.findall(sig_pattern, req.text)
        code = re.findall(code_pattern, req.text)
        return sig[0], code[0]


class NhaccuatuiDownloader(MusicDownloader):
    def crawl_download_url(self):
        token = self.gen_token()
        music_id = self.play_url.split('.')[3]
        real_music_url = 'https://graph.nhaccuatui.com/v1/songs/' + music_id + '?access_token=' + token
        req = requests.get(real_music_url)
        result = json.loads(req.text)

        link128 = result['data']['11']
        link320 = result['data']['12']
        lossless = result['data']['19']
        title = result['data']['2']
        artist = result['data']['3']
        thumbnail = result['data']['8']
        return title, artist, thumbnail, link128, link320, lossless

    def gen_token(self):
        url = 'https://graph.nhaccuatui.com/v1/commons/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Host': 'graph.nhaccuatui.com',
                   'Connection': 'Keep-Alive'}
        payload = {'deviceinfo': '{"DeviceID":"dd03852ada21ec149103d02f76eb0a04","DeviceName":"AppTroLyBeDieu", \
        "OsName":"WINDOWS","OsVersion":"8.0","AppName":"NCTTablet","AppTroLyBeDieu":"1.3.0", \
        "UserName":"0","QualityPlay":"128","QualityDownload":"128","QualityCloud":"128","Network":"WIFI","Provider":"NCTCorp"}', \
                   'md5': 'ebd547335f855f3e4f7136f92ccc6955', 'timestamp': '1499177482892'}
        r = requests.post(url, data=payload, headers=headers)
        decoded = json.loads(r.text)
        token = decoded['data']['accessToken']
        return token


if __name__ == "__main__":
    link = 'https://mp3.zing.vn/bai-hat/Vo-Tinh-Xesi-Hoaprox/ZW9DC99A.html'
    player, title, artist, thumbnail, download_url_128, download_url_320, download_url_lossless = Zingmp3AudioDownloader(link).crawl_download_url()
    req = requests.get(player)
