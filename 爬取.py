import HttpUtils
import json
from DbUtils import Mysqldb
import time
import random

def comment():
    url="https://api.bilibili.com/x/v2/reply/main?csrf=bbd11ca238f4f1248c17dd4164576573&mode=3&next=0&oid=302679955&plat=1&type=1"

def owner_insert(uid):
    mydb = Mysqldb()
    # 作者信息插入语句
    sql = "replace into authorinfo(uid,name,sex,face,sign,following,follower,num) value (%s,%s,%s,%s,%s,%s,%s,%s)"
    # 粉丝和关注
    url1 = "https://api.bilibili.com/x/relation/stat?vmid="+str(uid)+"&jsonp=jsonp"
    # 主页
    url2 = "https://api.bilibili.com/x/space/acc/info?mid="+str(uid)+"&jsonp=jsonp"
    # 解析网页，解析为json对象
    temp1 = json.loads(HttpUtils.getContent(url1))
    temp2 = json.loads(HttpUtils.getContent(url2))
    # 提取data数据
    data1 = temp1["data"]
    data2 = temp2["data"]
    name = data2["name"]
    sex = data2["sex"]
    face = data2["face"]
    sign = data2["sign"]
    following = data1["following"]
    follower = data1["follower"]
    num = 1
    sql1 = "select * from authorinfo where uid='" + str(uid) + "' "
    data = mydb.select_all(sql1)
    if len(data) > 0:
        num = data[0][7]+1
    val=(uid,name,sex,face,sign,following,follower,num)
    mydb.commit_data(sql,val)

def reptile():
    for j in range(1, 26, 1):
        url = "https://api.bilibili.com/x/web-interface/popular?ps=20&pn="+str(j)
        # 解析为json对象
        temp1 = json.loads(HttpUtils.getContent(url))
        # 提取data数据
        data = temp1["data"]
        # 提取列表
        list = data["list"]
        # 创建mysql工具类对象
        mydb = Mysqldb()
        # 视频信息插入语句
        sql ="insert into videoinfo value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        print(url)
        for i in list:
            # BV号
            # print(i["bvid"])
            # 视频编号
            # print(i["aid"])
            # 标签
            # print(i["tname"])
            # 图片
            # print(i["pic"])
            # 标题
            # print(i["title"])
            # 创建时间的时间戳
            timeArray = time.localtime(i["pubdate"])
            checkpoint = time.strftime("%Y-%m-%d", timeArray)
            # print(checkpoint)
            # 简介
            # print(i["desc"])
            # # List数据内层
            stat = i["stat"]
            # 播放量
            # print(stat["view"])
            # 评论
            # print(stat["danmaku"])
            # 点赞
            # print(stat["like"])
            # 投币
            # print(stat["coin"])
            # 收藏
            # print(stat["favorite"])
            # 转发
            # print(stat["share"])
            # 不喜欢
            # print(stat["dislike"])
            # # 数据内层结束
            # 上传地址
            # print(i["pub_location"])
            # # List作者内层
            # 作者uid
            owner = i["owner"]
            # print(owner["mid"])
            print(i["bvid"])
            val = (i["bvid"],i["aid"],i["tname"],i["pic"],i["title"],checkpoint,i["desc"],stat["view"],stat["danmaku"],stat["like"],stat["coin"],stat["favorite"],stat["share"],stat["dislike"],i["pub_location"],owner["mid"])
            mydb.commit_data(sql, val)
            owner_insert(owner["mid"])
        print(j,"ok")
        time.sleep(random.randint(5, 10))
