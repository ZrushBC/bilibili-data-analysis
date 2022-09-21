import requests
def getContent(url):
    # 要爬取数据的网址
    target = url
    # target = 'https://www.bilibili.com'
    # 设置请求头  模拟浏览器来操作
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        # 'Cookie':'''buvid3=015498F1-9847-4485-AA29-9AD7E6AD3110155830infoc; LIVE_BUVID=AUTO9015813431802344; rpdid=|(RlRJ~Rk|~0J'ul)uJRYYlR; video_page_version=v_old_home; fingerprint_s=bc16c999949e0d20616e2bb9cdacde94; i-wanna-go-back=-1; buvid4=53B67400-ED3D-7224-5533-CDB81F85FCB567367-022012119-7xVY/oOUZ+mOqLQ8d8HRGg%3D%3D; _uuid=4E810ACB4-941F-A6B9-2AB6-762649E3865D99441infoc; buvid_fp_plain=undefined; CURRENT_BLACKGAP=0; hit-dyn-v2=1; is-2022-channel=1; sid=5bsc2knf; DedeUserID=44889616; DedeUserID__ckMd5=ce73b0320f9eb770; SESSDATA=2336aef4%2C1670771157%2Ceb7e5*61; bili_jct=bbd11ca238f4f1248c17dd4164576573; buvid_fp=cde5ea3076194b19e97ccfc8170fa64c; b_ut=5; blackside_state=0; nostalgia_conf=-1; i-wanna-go-feeds=-1; CURRENT_QUALITY=0; fingerprint3=b32e99dbeb53bf8fe43d8f9f0189bc3e; fingerprint=42e5943bd8ceb661e2e892dd4bac0922; b_nut=100; b_lsid=EA5E635B_18316D48926; innersign=0; CURRENT_FNVAL=16; PVID=8; bp_video_offset_44889616=703094543145238500'''
    }
    # headers={}
    # 使用get请求获取数据
    req = requests.get(url=target, headers=headers)
    # 设置网页编码  Ctrl+/  常见编码 utf-8  gbk  gb2312
    req.encoding = 'utf8'
    # 获取请求到的内容 存放在html变量名中  text文本  文字
    html = req.text
    # 输出html变量的值
    # print(html)
    return html
