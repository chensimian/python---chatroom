# -*- coding: utf-8 -*-
#AES-demo #采用AES对称加密算法
import os
import time
import psutil
import base64
from Cryptodome.Cipher import AES
from tkinter import *
import tkinter.messagebox
#import struct
def add_to_16(value):# str不是16的倍数那就补足为16的倍数
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  # 返回bytes
def encrypt_oracle(path,kei,user):#加密方法
    users = user
    key = kei
    file_path = path
    filepath,tempfilename = os.path.split(file_path)#filepath源文件所在路径,tempfilename源文件名称包含后缀
    filename,extension = os.path.splitext(tempfilename)#filename源文件名称不包含后缀,extension源文件后缀
    savefile = users+'_'+filename+'已加密'+extension#加密后文件名称
    try:
        text = open(file_path, 'rb').read()# 待加密文本
        open(file_path, 'rb').close()
    except:
        tkinter.messagebox.showerror('温馨提示', message='\n输入有误，请重新输入')
        encrypt_oracle()
    text = str(text)
    aes = AES.new(add_to_16(key), AES.MODE_ECB)# 初始化加密器
    encrypt_aes = aes.encrypt(add_to_16(text))#先进行aes加密
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='cp936') #用base64转成字符串形式 # 执行加密并转码返回bytes
    if filepath == "":
        logbat = open(savefile, 'w')
        logbat.write(encrypted_text)
        logbat.close()
        tkinter.messagebox.showinfo('温馨提示', message='\n文件加密成功 文件以保存为 '+savefile)
    else:
        logbat = open(filepath+'\\'+savefile, 'w')
        logbat.write(encrypted_text)
        logbat.close()
        tkinter.messagebox.showinfo('温馨提示', message='\n文件加密成功 文件保存在 '+filepath+'中 \n\n文件名为 '+savefile)
def loop(path,kei,user):
    root = tkinter.Tk()
    root['height'] = 80
    root['width'] = 250
    root.title("请输入解密后的文件名字")
    labelkey = tkinter.Label(root, text='文件名')
    labelkey.place(x=5, y=10, width=80, height=20)

    entrykey = tkinter.Entry(root, width=80)
    entrykey.place(x=90, y=10, width=130, height=20)


    def commit():

        name = entrykey.get()
        print(name)
        decrypt_oralce(path,name,kei,user)
        root.destroy()

    but = tkinter.Button(root, text="确认", command=commit)
    but.place(x=90, y=40, width=100, height=30)
    root.mainloop()
def decrypt_oralce(path,name,kei,user):#解密方法
    key = kei
    users = user

    file_path = path
    filepath, tempfilename = os.path.split(file_path)
    filename, extension = os.path.splitext(tempfilename)
    try:
        text = open(file_path, 'rb').read()  # 待加密文本
        open(file_path, 'rb').close()
    except:
        print('\n输入有误，请重新输入')
        decrypt_oralce(path)
    savefile = users+'_'+name
    text = str(open(file_path, 'r').read())  # 密文文件
    open(file_path, 'r').close()
    aes = AES.new(add_to_16(key), AES.MODE_ECB)  # 初始化加密器
    base64_decrypted = base64.decodebytes(text.encode(encoding='cp936'))  # 优先逆向解密base64成bytes
    decrypted_text = str(aes.decrypt(base64_decrypted), encoding='gbk').replace('\0', '')  # 执行解密密并转码返回str
    decrypted_text2 = eval(decrypted_text)
    if filepath == "":
        logbat = open(savefile, 'wb')
        logbat.write(decrypted_text2)
        logbat.close()
        tkinter.messagebox.showinfo('温馨提示', message='\n文件解密成功 文件以保存为 ' + savefile)
    else:
        logbat = open(filepath + '\\' + savefile, 'wb')
        logbat.write(decrypted_text2)
        logbat.close()
        tkinter.messagebox.showinfo('温馨提示', message='\n文件解密成功 文件保存在 ' + filepath + '中 \n\n文件名为 ' + savefile)

