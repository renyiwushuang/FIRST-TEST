import tkinter as tk


class MainPage:

    def __init__(self, master):

        self.root = master
        self.root.geometry('600x400')
        self.root.title('学生信息管理系统v0.0.1')
        self.create_page()

    def create_page(self):
        self.about_frame = tk.Frame(self.root)
        tk.Label(self.about_frame, text='关于本作品').pack()

        menubar = tk.Menu(self.root)
        menubar.add_command(label='录入')
        menubar.add_command(label='查询')
        menubar.add_command(label='删除')
        menubar.add_command(label='修改')
        menubar.add_command(label='关于', command=self.show_about)
        self.root['menu'] = menubar

    def show_about(self):
        self.about_frame.pack()


if __name__ == '__main__':
    root = tk.Tk()
    MainPage(root)
    root.mainloop()
