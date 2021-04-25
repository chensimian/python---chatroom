import random
import socket
import threading
import json  # json.dumps(some)打包   json.loads(some)解包
from tkinter import *
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText  # 导入多行文本框用到的包
import time
from tkinter import filedialog
import pymysql
import pwd
IP = ''
PORT = ''
user = ''
listbox1 = ''  # 用于显示在线用户的列表框
ii = 0  # 用于判断是开还是关闭列表框
users = []  # 在线用户列表
block = ['0']
lack =[]
chat = '【群发】'  # 聊天对象, 默认为群聊

# 登陆窗口
loginRoot = tkinter.Tk()
loginRoot.title('聊天室')
loginRoot['height'] = 300
loginRoot['width'] = 350
loginRoot.resizable(0, 0)  # 限制窗口大小
#loginRoot.overrideredirect(True)
IP1 = tkinter.StringVar()
IP1.set('127.0.0.1:8888')  # 默认显示的ip和端口
User = tkinter.StringVar()
User.set('')

# 服务器标签
labelIP = tkinter.Label(loginRoot, text='地址:端口')
labelIP.place(x=35, y=80, width=80, height=20)

entryIP = tkinter.Entry(loginRoot, width=80, textvariable=IP1)
entryIP.place(x=170, y=80, width=130, height=20)

# 用户名标签
# labelUser = tkinter.Label(loginRoot, text='昵称')
# labelUser.place(x=35, y=80, width=80, height=20)
#
# entryUser = tkinter.Entry(loginRoot, width=80,textvariable=User)
# entryUser.place(x=170, y=80, width=130, height=20)

labelCount = tkinter.Label(loginRoot, text='账号名')
labelCount.place(x=35, y=120, width=80, height=20)

entryCount = tkinter.Entry(loginRoot, width=80)
entryCount.place(x=170, y=120, width=130, height=20)

labelPassword = tkinter.Label(loginRoot, text='密码')
labelPassword.place(x=35, y=160, width=80, height=20)

entryPassword = tkinter.Entry(loginRoot, width=80,show ="*")
entryPassword.place(x=170, y=160, width=130, height=20)

# 登录按钮
def login(*args):
    global IP, PORT, user,key
    IP, PORT = entryIP.get().split(':')  # 获取IP和端口号
    PORT = int(PORT)                     # 端口号需要为int类型
    sign = 0

    count = entryCount.get()
    password = entryPassword.get()
    connection = pymysql.connect(host='localhost', user='root', password='lh123456', db="login")
    cursion = connection.cursor()

    cursion.execute('SELECT * FROM users')
    a = cursion.fetchall()
    for i in range(len(a)):
        user = a[i][0]
        count_l = a[i][1]
        password_l = a[i][2]
        key = a[i][3]
        print(key)
        if  count_l == int(count) and password_l == int(password) :
            sign =1
            break
    if sign == 0 :
        tkinter.messagebox.showerror('温馨提示', message='昵称，密码或者账户错误')
    if sign == 1 :
        if not user:
            tkinter.messagebox.showerror('温馨提示', message='请输入任意的用户名！')
        else:
            loginRoot.destroy()  # 关闭窗口
    connection.close()
    cursion.close()



loginRoot.bind('<Return>', login)            # 回车绑定登录功能
but_image = tkinter.PhotoImage(file=r"./img/login.png")
but = tkinter.Button(loginRoot, image=but_image,command=login)
but.place(x=60, y=200, width=236, height=31)
def register():
    root2 =tkinter.Tk()
    root2.title('聊天室')
    root2['height'] = 300
    root2['width'] = 350
    root2.resizable(0, 0)
    labeliP = tkinter.Label(root2, text='用户名')
    labeliP.place(x=35, y=80, width=80, height=20)

    entryiP = tkinter.Entry(root2, width=80, textvariable=IP1)
    entryiP.place(x=170, y=80, width=130, height=20)
    labelcount = tkinter.Label(root2, text='账号名')
    labelcount.place(x=35, y=120, width=80, height=20)

    entrycount = tkinter.Entry(root2, width=80)
    entrycount.place(x=170, y=120, width=130, height=20)

    labelpassword = tkinter.Label(root2, text='密码')
    labelpassword.place(x=35, y=160, width=80, height=20)

    entrypassword = tkinter.Entry(root2, width=80, show="*")
    entrypassword.place(x=170, y=160, width=130, height=20)

    labelkey = tkinter.Label(root2, text='密钥')
    labelkey.place(x=35, y=200, width=80, height=20)

    entrykey = tkinter.Entry(root2, width=80, show="*")
    entrykey.place(x=170, y=200, width=130, height=20)
    def RR():

        connection = pymysql.connect(host='localhost', user='root', password='lh123456', db="login")
        cursion = connection.cursor()
        sql = 'INSERT INTO users VALUES(%s,%s,%s,%s);'
        user = entryiP.get()
        count = entrycount.get()
        password = entrypassword.get()
        key = entrykey.get()
        result = cursion.execute(sql, (user, count, password, key))
        if result:
            tkinter.messagebox.showinfo('温馨提示', message='注册成功')
            root2.destroy()
        connection.commit()
        connection.close()
    Rbut = tkinter.Button(root2, text ="注册", command=RR)
    Rbut.place(x=60, y=230, width=236, height=31)

    root2.mainloop()
rbut = tkinter.Button(loginRoot, text="注册",command=register)
rbut.place(x=60, y=240, width=236, height=31)
loginRoot.mainloop()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))
if user:
    s.send(user.encode())  # 发送用户名

else:
    s.send('no'.encode())  # 没有输入用户名则标记no

# 如果没有用户名则将ip和端口号设置为用户名
addr = s.getsockname()  # 获取客户端ip和端口号
print(addr[1])
addr = addr[0] + ':' + str(addr[1])
if user == '':
    user = addr

# 聊天窗口
# 创建图形界面
root = tkinter.Tk()
root.title(user)  # 窗口命名为用户名
root['height'] = 400
root['width'] = 580
root.resizable(0, 0)  # 限制窗口大小
root.configure(bg="#87CEFA")
# 创建多行文本框
listbox = ScrolledText(root)
listbox.place(x=5, y=0, width=570, height=320)
# 文本框使用的字体颜色
listbox.tag_config('red', foreground='red')
listbox.tag_config('blue', foreground='blue')
listbox.tag_config('green', foreground='green')
listbox.tag_config('pink', foreground='pink')
listbox.insert(tkinter.END, '欢迎加入聊天室 ！', 'blue')


# 表情功能代码部分
# 5个按钮, 使用全局变量, 方便创建和销毁
b1 = ''
b2 = ''
b3 = ''
b4 = ''
b5 = ''
# 将图片打开存入变量中
p1 = tkinter.PhotoImage(file='./emoji/facepalm.png')
p2 = tkinter.PhotoImage(file='./emoji/smirk.png')
p3 = tkinter.PhotoImage(file='./emoji/concerned.png')
p4 = tkinter.PhotoImage(file='./emoji/smart.gif')
p5 = tkinter.PhotoImage(file='./emoji/ss (1).png')
# 用字典将标记与表情图片一一对应, 用于后面接收标记判断表情贴图
dic = {'aa**': p1, 'bb**': p2, 'cc**': p3, 'dd**': p4,'ff**':p5}
ee = 0  # 判断表情面板开关的标志


# 发送表情图标记的函数, 在按钮点击事件中调用


def mark(exp):  # 参数是发的表情图标记, 发送后将按钮销毁
    global ee
    mes = exp + ':;' + user + ':;' + chat
    s.send(mes.encode())
    b1.destroy()
    b2.destroy()
    b3.destroy()
    b4.destroy()
    b5.destroy()
    ee = 0


# 四个对应的函数
def bb1():
    mark('aa**')


def bb2():
    mark('bb**')


def bb3():
    mark('cc**')


def bb4():
    mark('dd**')
def bb5():
    mark('ff**')

def express():
    global b1, b2, b3, b4,b5,ee
    if ee == 0:
        ee = 1
        b1 = tkinter.Button(root, command=bb1, image=p1,
                            relief=tkinter.FLAT, bd=0)
        b2 = tkinter.Button(root, command=bb2, image=p2,
                            relief=tkinter.FLAT, bd=0)
        b3 = tkinter.Button(root, command=bb3, image=p3,
                            relief=tkinter.FLAT, bd=0)
        b4 = tkinter.Button(root, command=bb4, image=p4,
                            relief=tkinter.FLAT, bd=0)
        b5 = tkinter.Button(root, command=bb5, image=p5,
                            relief=tkinter.FLAT, bd=0)
        b1.place(x=5, y=248)
        b2.place(x=75, y=248)
        b3.place(x=145, y=248)
        b4.place(x=215, y=248)
        b5.place(x=285, y=248)
    else:
        ee = 0
        b1.destroy()
        b2.destroy()
        b3.destroy()
        b4.destroy()
        b5.destroy()

# 创建表情按钮
eBut_img = tkinter.PhotoImage(file=r"./img/emoji.png")
eBut = tkinter.Button(root, text='表情', image=eBut_img,command=express)
eBut.place(x=5, y=320, width=32, height=32)
eBut.config(background="darkorange1", foreground="white",activebackground="black", activeforeground="white")
# 图片功能代码部分
# 从图片服务端的缓存文件夹中下载图片到客户端缓存文件夹中
def fileGet(name):
    PORT3 = 8889
    ss2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss2.connect((IP, PORT3))
    message = 'get ' + name
    ss2.send(message.encode())
    fileName = '.\\Client_image_cache\\' + name
    print('Start downloading image!')
    print('Waiting.......')
    with open(fileName, 'wb') as f:
        while True:
            data = ss2.recv(1024)
            if data == 'EOF'.encode():
                print('Download completed!')
                break
            f.write(data)
    time.sleep(0.1)
    ss2.send('quit'.encode())


# 将图片上传到图片服务端的缓存文件夹中
def  filePut(fileName):
    PORT3 = 8889
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.connect((IP, PORT3))
    # 截取文件名
    print(fileName)
    name = fileName.split('/')[-1]
    print(name)
    message = 'put ' + name
    ss.send(message.encode())
    time.sleep(0.1)
    print('Start uploading image!')
    print('Waiting.......')
    with open(fileName, 'rb') as f:
        while True:
            a = f.read(1024)
            if not a:
                break
            ss.send(a)
        time.sleep(0.1)  # 延时确保文件发送完整
        ss.send('EOF'.encode())
        print('Upload completed')
    ss.send('quit'.encode())
    time.sleep(0.1)
    # 上传成功后发一个信息给所有客户端
    mes = '``#' + name + ':;' + user + ':;' + chat
    s.send(mes.encode())


# 文件功能代码部分
# 将在文件功能窗口用到的组件名都列出来, 方便重新打开时会对面板进行更新
list2 = ''  # 列表框
label = ''  # 显示路径的标签
upload = ''  # 上传按钮
close = ''  # 关闭按钮


def fileClient():
    PORT2 = 8889
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT2))

    # 修改root窗口大小显示文件管理的组件
    root['height'] = 390
    root['width'] = 760

    # 创建列表框
    list2 = tkinter.Listbox(root)
    list2.place(x=580, y=25, width=175, height=325)

    # 将接收到的目录文件列表打印出来(dir), 显示在列表框中, 在pwd函数中调用
    def recvList(enter, lu):
        s.send(enter.encode())
        data = s.recv(4096)
        data = json.loads(data.decode())
        list2.delete(0, tkinter.END)  # 清空列表框
        lu = lu.split('\\')
        if len(lu) != 1:
            list2.insert(tkinter.END, '回到上一级目录')
            list2.itemconfig(0, fg='red')
        for i in range(len(data)):
            list2.insert(tkinter.END, ('' + data[i]))
            if '.' not in data[i]:
                list2.itemconfig(tkinter.END, fg='black')
            else:
                list2.itemconfig(tkinter.END, fg='blue')

    # 创建标签显示服务端工作目录
    def lab():
        global label
        data = s.recv(1024)  # 接收目录
        lu = data.decode()
        try:
            label.destroy()
            label = tkinter.Label(root, text=lu)
            label.place(x=580, y=0, )
        except:
            label = tkinter.Label(root, text=lu)
            label.place(x=580, y=0, )
        recvList('dir', lu)


    # 进入指定目录(cd)
    def cd(message):
        s.send(message.encode())

    # 刚连接上服务端时进行一次面板刷新
    cd('cd same')
    lab()

    # 接收下载文件(get)
    def get(message):
        # print(message)
        name = message.split(' ')
        # print(name)
        name = name[1]  # 获取命令的第二个参数(文件名)
        # 选择对话框, 选择文件的保存路径
        fileName = tkinter.filedialog.asksaveasfilename(title='Save file to', initialfile=name)
        # 如果文件名非空才进行下载
        if fileName:
            s.send(message.encode())
            with open(fileName, 'wb') as f:
                while True:
                    data = s.recv(1024)
                    if data == 'EOF'.encode():
                        tkinter.messagebox.showinfo(title='Message',
                                                    message='Download completed!')
                        break
                    f.write(data)

    # 创建用于绑定在列表框上的函数
    def run(*args):
        Droot = tkinter.Tk()

        def flash():
            indexs = list2.curselection()
            index = indexs[0]
            content = list2.get(index)
            print(content)

            # 如果有一个 . 则为文件
            if '.' in content:
                content = 'get ' + content
                get(content)
                cd('cd same')
            elif content == '回到上一级目录':
                content = 'cd ..'
                cd(content)
            else:
                content = 'cd ' + content
                cd(content)
            lab()  # 刷新显示页面
            Droot.destroy()

        def Encryption():
            indexs = list2.curselection()
            index = indexs[0]
            content = list2.get(index)
            text = label["text"]
            path = text+"\\"+content
            print(key)
            pwd.encrypt_oracle(path,key,user)
            lab()  # 刷新显示页面
            Droot.destroy()
        def decrypt():
            indexs = list2.curselection()
            index = indexs[0]
            content = list2.get(index)
            text = label["text"]
            path = text+"\\"+content
            print(path)
            pwd.loop(path,key,user)
            lab()  # 刷新显示页面
            Droot.destroy()



        Button(Droot, text="加密文件", width=12,command = Encryption).grid(row=2, column=0, sticky=W, padx=10, pady=5)
        Button(Droot, text="解密", width=12,command= decrypt ).grid(row=2, column=1, sticky=E, padx=10, pady=5)
        Button(Droot, text="执行", width=12,command = flash).grid(row=2, column=2, sticky=E, padx=10, pady=5)
        Droot.mainloop()
    # 在列表框上设置绑定事件
    list2.bind('<ButtonRelease-1>', run)

    # 上传客户端所在文件夹中指定的文件到服务端, 在函数中获取文件名, 不用传参数
    def put():
        # 选择对话框
        fileName = tkinter.filedialog.askopenfilename(title='Select upload file')
        # 如果有选择文件才继续执行
        if fileName:
            name = fileName.split('/')[-1]
            message = 'put ' + name
            s.send(message.encode())
            with open(fileName, 'rb') as f:
                while True:
                    a = f.read(1024)
                    if not a:
                        break
                    s.send(a)
                time.sleep(0.1)  # 延时确保文件发送完整
                s.send('EOF'.encode())
                tkinter.messagebox.showinfo(title='Message',
                                            message='Upload completed!')
        cd('cd same')
        lab()  # 上传成功后刷新显示页面

    # 创建上传按钮, 并绑定上传文件功能
    upload = tkinter.Button(root, text='Upload file', command=put)
    upload.place(x=600, y=353, height=30, width=80)

    # 关闭文件管理器, 待完善
    def closeFile():
        root['height'] = 390
        root['width'] = 580
        # 关闭连接
        s.send('quit'.encode())
        s.close()

    # 创建关闭按钮
    close = tkinter.Button(root, text='Close', command=closeFile)
    close.place(x=685, y=353, height=30, width=70)


# 创建文件按钮
fBut_img = tkinter.PhotoImage(file = r"./img/file.png")
fBut = tkinter.Button(root, text='File',image=fBut_img, command=fileClient)
fBut.place(x=37, y=320, width=32, height=32)
def Game():
    a.set("game start\n请输入1-100之间的整数值")
    mes = entry.get() + ':;' + user + ':;' + chat  # 添加聊天对象标记
    s.send(mes.encode())
    a.set('')  # 发送后清空文本框
    number = random.randint(1, 100)
    f = open("game.txt","w+",encoding="utf-8")
    f.write(str(number))
    f.close()

gBut_img = tkinter.PhotoImage(file=r"./img/boom.png")
gBut = tkinter.Button(root, text='game',image=gBut_img,command=Game)
gBut.place(x=69, y=320, width=32, height=32)
date = []
def Search():
    SearchRoot = Tk()
    SearchRoot['height'] = 275
    SearchRoot['width'] = 290
    Searchlog = Entry(SearchRoot, width=40)
    Searchlog.place(x=5, y=5, width=280, height=20)
    Slistbox = ScrolledText(SearchRoot)
    Slistbox.place(x=5, y=30, width=280, height=195)
    def search_l():
        if Searchlog.get() == '':
            tkinter.messagebox.showerror('温馨提示', message='请输入查找内容')
        if Searchlog.get() != '':
            Search_n = Searchlog.get()
            print(Search_n)
            f = open("./log/u4.txt", "r+", encoding="utf-8")
            List = f.readlines()
            sign = 0
            List = [line.strip('\n') for line in List]
            for i in range(len(List)):
                # a = List[i].split(">")
                #
                # l = List[i].split(">")[1:]
                if Search_n in List[i]:
                    data = List[i]+"\n"
                    Slistbox.insert(tkinter.END, data, 'black')
                    sign = 1
            if sign == 0:
                tkinter.messagebox.showinfo('温馨提示', message='查无此记录')


    def returnn():
        SearchRoot.destroy()
    sbut_1 = Button(SearchRoot, text="按内容查找", width=12,command = search_l )
    sbut_1.place(x=5,y = 230,width=95, height=30)
    sbut_2 = Button(SearchRoot, text="退出", width=12, command= returnn)
    sbut_2.place(x=150,y = 230,width=95, height=30)
    SearchRoot.mainloop()


sBut_img = tkinter.PhotoImage(file=r'./img/search.png')
sBut = tkinter.Button(root, image = sBut_img,command = Search)
sBut.place(x=101, y=320, width=32, height=32)
# 创建多行文本框, 显示在线用户
listbox1 = tkinter.Listbox(root)
listbox1.place(x=445, y=0, width=130, height=320)


def showUsers():
    global listbox1, ii
    if ii == 1:
        listbox1.place(x=445, y=0, width=130, height=320)
        ii = 0
    else:
        listbox1.place_forget()  # 隐藏控件
        ii = 1


# 查看在线用户按钮
button1 = tkinter.Button(root, text='用户列表', command=showUsers)
button1.place(x=485, y=320, width=90, height=30)

# 创建输入文本框和关联变量
a = tkinter.StringVar()
a.set('')
entry = tkinter.Entry(root, width=120, textvariable=a)
entry.place(x=5, y=350, width=570, height=40)


def send(*args):

    sign = 0

    def ssend():
        users.append('【群发】')
        print(chat)
        if chat not in users:
            tkinter.messagebox.showerror('温馨提示', message='没有聊天对象!')
            return
        if chat == user:
            tkinter.messagebox.showerror('温馨提示', message='自己不能和自己进行对话!')
            return
        mes = entry.get() + ':;' + user + ':;' + chat  # 添加聊天对象标记
        s.send(mes.encode())
        a.set('')  # 发送后清空文本框
    if a.get() == '' and sign == 0:
        List = Listbox(root, setgrid=True)
        List.pack()
        lt = ["哦。", "好了，好了，我知道了", "是吗？", "不会是真的吧？", "我这里有好康的"]
        for item in lt:
            List.insert(END, item)
        def quick(self):
            a.set(List.get(List.curselection()))
            ssend()
            List.destroy()
            # 没有添加的话发送信息时会提示没有聊天对象

        List.bind("<Double-Button-1>",quick)
        List.place(x=445, y=253, width=130, height=100)
    if a.get() != '':
        ssend()


# 创建发送按钮
button_send_img = tkinter.PhotoImage(file=r"./img/send.png")
button = tkinter.Button(root,image=button_send_img,command=send)
button.place(x=515, y=353, width=60, height=30)
root.bind('<Return>', send)  # 绑定回车发送信息


# 私聊功能
def private(*args):
    global chat
    # 获取点击的索引然后得到内容(用户名)
    indexs = listbox1.curselection()
    index = indexs[0]
    root2 = Tk()

    Label(root2, text="清选择操作").grid(row=0)
    def chat():
        root2.destroy()
    def kick():
        uuser = listbox1.get(listbox1.curselection())
        sign = 0
        if user == uuser:
            tkinter.messagebox.showerror('温馨提示', message='无法屏蔽自己')
        if user != uuser:
            if uuser not in block:
                sign=1
        if sign == 1:
            block.append(uuser)
            sign = 0
        root2.destroy()
    def lock():
        sign2 = 0
        uuser = listbox1.get(listbox1.curselection())
        if user == uuser:
            tkinter.messagebox.showerror('温馨提示', message="无法踢出自己")

        if user != uuser:
            if uuser not in block:
                sign2 = 1
        if sign2 == 1:
            lack.append(uuser)
            sign = 0
        f = open("lockuser.txt","w",encoding="utf-8")
        for line in lack:
            f.write(line)
            f.write('\n')  # 显示写入换行

        f.close()
        root2.destroy()
    Button(root2, text="私聊", width=12, command=chat).grid(row=4, column=0, sticky=W, padx=10, pady=5)
    Button(root2, text="屏蔽", width=12, command=kick).grid(row=4, column=1, sticky=E, padx=10, pady=5)
    Button(root2, text="踢人", width=12,command = lock ).grid(row=4, column=2, sticky=E, padx=10, pady=5)




    if index > 0:
        chat = listbox1.get(index)
        # 修改客户端名称
        if chat == '【群发】':
            root.title(user)
            return
        ti = '私聊： '+user + ' 发送给  ' + chat
        root.title(ti)


# 在显示用户列表框上设置绑定事件
listbox1.bind('<ButtonRelease-1>', private)

def send2(m):
    a.set(m)
    mes = entry.get() + ':;' + user + ':;' + chat  # 添加聊天对象标记
    s.send(mes.encode())
    a.set('')  # 发送后清空文本框
min = "1"
max = '100'
count = 0
#游戏猜大小功能
def Gamn(markk):
    #定义全局变量，用于标记范围
    global min,max,count
    #读取文件中的随机数，并将其赋值给L
    f = open("game.txt", "r+", encoding="utf-8")
    L = int(f.read())
    if markk.isdigit():#判定输入的是否是数字
        #记录猜测次数
        count+=1
        print("你输入的数值是：" + markk)
        mad = int(markk)
        #判定输入的数字是否在范围内
        if mad < int(min) or mad > int(max):
            send2("超出范围，请重新发送数字")
        # 判定大小，根据比较结果发送不同的信息
        if not mad < int(min) or mad > int(max):
            if mad > L:
                send2("猜大了，在"+min+"~"+markk+"之间")
                max = markk
            if mad < L:
                send2("猜小了，在"+markk+"~"+max+"之间")
                min = markk
            if mad == L:
                send2("boom，你猜中所花费的次数为"+str(count))
                send2("game over")
switch = 0
# 用于时刻接收服务端发送的信息并打印
def recv():

    global users, switch

    while True:
        data = s.recv(1024)
        data = data.decode()
        # 没有捕获到异常则表示接收到的是在线用户列表
        try:
            data = json.loads(data)
            users = data

            listbox1.delete(0, tkinter.END)  # 清空列表框
            number = ('   在线用户数: ' + str(len(data)))
            listbox1.insert(tkinter.END, number)
            listbox1.itemconfig(tkinter.END, fg='black', bg="#f0f0ff")
            listbox1.insert(tkinter.END, '【群发】')
            listbox1.itemconfig(tkinter.END, fg='black')
            for i in range(len(data)):
                listbox1.insert(tkinter.END, (data[i]))
                listbox1.itemconfig(tkinter.END, fg='black')
        except:

            data = data.split(':;')

            data1 = data[0].strip()  # 消息

            data5 = "\n" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 接受到信息的时间

            data2 = data[1]  # 发送信息的用户名
            data3 = data[2]  # 聊天对象
            markk = data1.split('：')[1]

            f = open("./log/u4.txt", "a", encoding="utf-8")
            chat_new = data2+":"+markk + "-------->" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n"
            f.write(chat_new)
            f.close()
            print(data2)
            print(user)

            if data2 not in block:
                if  data2 == user:
                    if markk == "game start\n请输入1-100之间的整数值" :#检测游戏是否开始
                        switch = 1#标志位
                if markk == "game over" and switch == 1:#检测游戏是否结束
                    switch = 0
                if switch == 1:#运行游戏
                    Gamn(markk)


                # 判断是不是图片
                pic = markk.split('#')
                # 判断是不是表情
                # 如果字典里有则贴图
                if (markk in dic) or pic[0] == '``':
                    data4 = '\n' + data2 + '：'  # 例:名字-> \n名字：
                    if data3 == '【群发】':
                        if data2 == user:  # 如果是自己则将则字体变为蓝色
                            listbox.insert(tkinter.END, data5, 'black')#将时间同信息一起输出到listbox中
                            listbox.insert(tkinter.END, data4, 'blue')

                        else:
                            listbox.insert(tkinter.END, data5, 'black')
                            listbox.insert(tkinter.END, data4, 'green')  # END将信息加在最后一行

                    elif data2 == user or data3 == user:  # 显示私聊
                        listbox.insert(tkinter.END, data5, 'black')
                        listbox.insert(tkinter.END, data4, 'red')  # END将信息加在最后一行

                    listbox.image_create(tkinter.END, image=dic[markk])
                else:
                    data1 = '\n' + data1
                    if data3 == '【群发】':
                        if data2 == user:  # 如果是自己则将则字体变为蓝色
                            listbox.insert(tkinter.END, data5, 'black')
                            listbox.insert(tkinter.END, data1, 'blue')

                        else:
                            listbox.insert(tkinter.END, data5, 'black')
                            listbox.insert(tkinter.END, data1, 'green')  # END将信息加在最后一行

                        if len(data) == 4:
                            listbox.insert(tkinter.END, data5, 'black')
                            listbox.insert(tkinter.END, '\n' + data[3], 'pink')

                    elif data2 == user or data3 == user:  # 显示私聊
                        listbox.insert(tkinter.END, data5, 'black')
                        listbox.insert(tkinter.END, data1, 'red')  # END将信息加在最后一行

                listbox.see(tkinter.END)  # 显示在最后


r = threading.Thread(target=recv)
r.start()  # 开始线程接收信息

root.mainloop()
s.close()  # 关闭图形界面后关闭TCP连接
