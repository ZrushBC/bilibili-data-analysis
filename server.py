from glob import escape
from flask import Flask, request, jsonify, render_template, redirect, make_response, session
from DbUtils import Mysqldb
import os
import 爬取

from flask_apscheduler import APScheduler, scheduler

scheduler = APScheduler()
scheduler.start()
app = Flask(__name__)

# 使用session必须配置一个key值
app.config['SECRET_KEY'] = os.urandom(24)


# 值可以更改，用随机数可以保证安全性
# app.config['SECRET_KEY'] = "kungong"
# app.config['SECRET_KEY'] = "1324865"

# server.py 同级别
# templates  默认模板页面所在文件夹
# static  默认css和js所在文件夹


# interval example, 间隔执行, 每30秒执行一次 秒（seconds=10，misfire_grace_time=900）
# @scheduler.task('interval', id='do_job_1', seconds=10,misfire_grace_time=900)
# def job():
#     爬取.reptile()
#     print('Job executed')
# 每周
@scheduler.task('cron', id='do_job_3', week='*', day_of_week='sun')
def job3():
    爬取.reptile()
    print('Job  executed')


# 图片映射
@app.route("/img/<fname>")
def showimg(fname):
    # print("显示图片")
    cdir = os.getcwd() + "\\img\\" + fname  # os.getcwd() 获取当前项目路径
    image_data = open(cdir, 'rb').read()
    res = make_response(image_data)
    res.headers['Content-Type'] = 'img/jpg'
    return res


# 默认页面（直接输入ip地址）
@app.route('/')
def default():
    return redirect("/index")


# 跳转到 首页
@app.route('/index')
def index():
    return render_template("index.html")


# 跳转到 登录页面
@app.route("/login")
def login():
    return render_template("login.html")


# 登录验证
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        username = request.form["username"]  # 获得用户名
        password = request.form["password"]  # 获得密码
        # 从数据库验证账号
        sql = "select * from userinfo where username='" + username + "' and password='" + password + "'"
        mydb = Mysqldb()
        data = mydb.select_all(sql)
        if len(data) == 0:  # 登录失败
            print("账号或密码错误")
            msg = "账号或密码错误"
            return render_template("login.html", msg=msg)
        else:
            print("登录成功")
            # 放入session
            session['username'] = username
            session['password'] = password
            session['heading'] = data[0][3]
            session['type'] = data[0][4]
            session['appellation'] = data[0][5]
    return render_template("admin.html")


# 跳转到 注册页面
@app.route("/register")
def register():
    return render_template("register.html")


# 用户注册保存到数据库
@app.route("/regSubmit", methods=["GET", "POST"])
def regSubmit():
    if request.method == "POST":
        appellation = request.form["appellation"]  # 获得称谓
        username = request.form["username"]  # 获得账号
        password1 = request.form["password1"]  # 获得密码1
        password2 = request.form["password2"]  # 获得密码2
        if password1 != password2:
            return render_template("register.html", msg="两次密码不一致")
        sql = "select * from userinfo where username='" + username + "' "
        mydb = Mysqldb()
        # 验证账号是否存在
        if len(mydb.select_all(sql)) > 0:
            return render_template("register.html", msg="账号已存在")
        sql2 = "insert userinfo(username,password,heading,type,appellation) values(%s,%s,%s,%s,%s)"
        val = (username, password1, "/img/head.jpg", 0, appellation)
        mydb.commit_data(sql2, val)
    return render_template("login.html")


# 退出登录
@app.route("/loginOut")
def loginOut():
    # 删除session中信息
    session.pop("username")
    session.pop("heading")
    session.pop("type")
    session.pop("appellation")
    return render_template("login.html")


# 用户列表页面
@app.route("/userlist", methods=["GET", "POST"])
def userlist():
    # 接受参数 get提交  直接输入网址
    # keyword = request.args["keyword"]
    keyword = ""
    mydb = Mysqldb()
    sql = "select * from userinfo"
    if request.method == "POST":
        # post提交 接受参数
        keyword = request.form["keyword"]
        sql = "select * from userinfo where username like'%" + keyword + "%'"
        # sql = sql + "where name like'%"+keyword+"%'"
    data = mydb.select_all(sql)
    return render_template("userlist.html", data=data, keyword=keyword)


# 用户资料页面
@app.route("/userinfo")
def userinfo():
    return render_template("userinfo.html")

# 删除
@app.route('/Delete',methods=["GET", "POST"])
def Delete():
    id = request.args["id"]
    print(id)
    mydb = Mysqldb()
    sql = "delete from userinfo where id=%s"
    mydb.commit_data(sql, id)
    return redirect("/userlist")


# 视频列表页面
@app.route("/videolist", methods=["GET", "POST"])
def videolist():
    # 接受参数 get提交  直接输入网址
    # keyword = request.args["keyword"]
    keyword = ""
    mydb = Mysqldb()
    sql = "select * from videoinfo"
    if request.method == "POST":
        # post提交 接受参数
        keyword = request.form["keyword"]
        sql = "select * from videoinfo where title like'%" + keyword + "%'"
        # sql = sql + "where name like'%"+keyword+"%'"
    data = mydb.select_all(sql)
    return render_template("videolist.html", data=data, keyword=keyword)


# 视频数据分析
@app.route('/videopic1')
def videopic1():
    mydb = Mysqldb()
    sql = "select * from videoinfo"
    data = mydb.select_all(sql)
    val = []
    val.append(["product","播放量","评论","点赞","投币","收藏","转发","点踩"])
    for w in data:
        t = [w[4],w[7],w[8],w[9],w[10],w[11],w[12],w[13]]
        val.append(t)
    # print(val)
    return render_template("videopic1.html",val=val)

# 视频数据分析
@app.route('/videopic2')
def videopic2():
    mydb = Mysqldb()
    num1 = 0
    num2 = 0
    sql1 = "select *  from videoinfo "
    data1 = mydb.select_all(sql1)
    sql2 = "select tname,count(*) as nums from videoinfo GROUP BY tname"
    data2 = mydb.select_all(sql2)
    val1 = []
    val2 = []
    for w in data1:
        if w[7]/4 <= w[8]+w[9]+w[10]+w[11]+w[12]:
            num1 = num1+1
    for w in data2:
        num2 = num2+w[1]
        val2.append({"value":w[1],"name":w[0]})
    val1.append({"value": len(data1)-num1, "name": "大体上被白嫖的视频"})
    val1.append({"value":num1,"name":"大体上三连的视频"})
    return render_template("videopic2.html",val1=val1,num1=len(data1),val2=val2)

# 作者列表页面
@app.route("/authorlist", methods=["GET", "POST"])
def authorlist():
    # 接受参数 get提交  直接输入网址
    # keyword = request.args["keyword"]
    keyword = ""
    mydb = Mysqldb()
    sql = "select * from authorinfo"
    if request.method == "POST":
        # post提交 接受参数
        keyword = request.form["keyword"]
        sql = "select * from authorinfo where name like'%" + keyword + "%'"
        # sql = sql + "where name like'%"+keyword+"%'"
    data = mydb.select_all(sql)
    return render_template("authorlist.html", data=data, keyword=keyword)

# 作者数据分析
@app.route('/authorpic1')
def authorpic1():
    mydb = Mysqldb()
    sql = "select * from authorinfo"
    data = mydb.select_all(sql)
    val = []
    val.append(["product","粉丝数","关注数"])
    for w in data:
        t = [w[1],w[6],w[5]]
        val.append(t)
    # print(val)
    return render_template("authorpic1.html",val=val)

# 作者数据分析
@app.route('/authorpic2')
def authorpic2():
    mydb = Mysqldb()
    num1 = 0
    num2 = 0
    sql1 = "select *  from authorinfo "
    data1 = mydb.select_all(sql1)
    sql2 = "select sex,count(*) as nums from authorinfo GROUP BY sex"
    data2 = mydb.select_all(sql2)
    val1 = []
    val2 = []
    for w in data1:
        if int(w[6]) <= 1000000:
            num1 = num1+1
    for w in data2:
        num2 = num2+w[1]
        val2.append({"value": w[1], "name": w[0]})
    val1.append({"value": len(data1)-num1, "name": "资深UP主"})
    val1.append({"value": num1, "name": "新人UP主"})
    return render_template("authorpic2.html",val1=val1,num1 = len(data1),val2=val2)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
