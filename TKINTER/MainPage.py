import tkinter as tk
from tkinter import messagebox
from db import db

class MainPage:
    def __init__(self, master):

        self.root = master
        self.root.geometry('600x400')
        self.root.title('学生信息管理系统v0.0.1')

        self.username = tk.StringVar()
        self.password = tk.StringVar()


        self.page = tk.Frame(root)
        self.page.pack()

        tk.Label(self.page).grid(row=0, column=0)

        tk.Label(self.page, text='账户').grid(row=1, column=1, pady=10)
        tk.Entry(self.page, textvariable=self.username).grid(row=1, column=2)

        tk.Label(self.page, text='密码').grid(row=2, column=1, pady=10)
        tk.Entry(self.page, textvariable=self.password).grid(row=2, column=2)

        tk.Button(self.page, text='登录', command=self.login).grid(row=3, column=1, pady=10)
        tk.Button(self.page, text='退出', command=self.page.quit).grid(row=3, column=2)

    def login(self):
                name = self.username.get()
                pwd = self.password.get()
                flag, message = db.check_login(name, pwd)
                if flag:
                    print('登陆成功')
                else:
                    messagebox.showwarning(title='警告', message=message)
        

if __name__ == '__main__':
    root = tk.Tk()
    LoginPage(root)
    root.mainloop()
