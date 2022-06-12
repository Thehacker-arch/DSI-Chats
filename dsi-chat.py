import os
import sys
import time
import socket
import numpy as np
from tkinter import messagebox
from tkinter import font
from threading import *
from tkinter import *

class client_chat_ui():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def connect(self):
        self.for_ip = str(self.ip.get())
        self.for_port = int(self.port.get())
        try:
            self.s.connect((self.for_ip, self.for_port))
            self.close.place(x=15, y=410)
        except:
            messagebox.showerror("Connection Error", "Can't connect to the server.\nPlease try again...")
        self.t = Thread(target=self.write,)
        self.t.start()

    def disconnect(self):
        self.s.close()
        sys.exit(0)

    def logging(self):
        self.ip_log = self.ip.get()
        self.port_log = self.port.get()
        self.nickname_log = self.nickname.get()
        self.home = os.path.expanduser('~')
        self.path = f"{self.home}\\Desktop\\log.txt"
        if os.path.exists(self.path):
            with open(self.path) as a:
                leng = a.read()
            if len(leng) > 0:
                with open(self.path, "a") as f:
                    f.write(self.ip_log+"\n")
                    f.write(self.port_log+"\n")
                    f.write(self.nickname_log+"\n")
                    f.close()
            else:
                with open(self.path, "w") as f:
                    f.write(self.ip_log+"\n")
                    f.write(self.port_log+"\n")
                    f.write(self.nickname_log+"\n")
                    f.close()
        else:
            messagebox.showwarning('File Not Found', 'The File does not exists.\nWe will make a new one for You.')
            open(self.path, "w")
    def write_log(self):
        path = f"{os.path.expanduser('~')}\\Desktop\\log.txt"
        if os.path.exists(path):
            with open(path) as f:
                try:
                    wr = [next(f) for x in range(3)]
                    splits = np.array_split(wr, 1)
                    for array in splits:
                        ip = array[0]
                        port = array[1]
                        nick = array[2] 
                        self.ip.insert(END, ip)
                        self.port.insert(END, port)
                        self.nickname.insert(END, nick)
                except:
                    messagebox.showinfo("No Data", "The Log is Clear.\nNo data to log...")
        else:
            messagebox.showwarning('File Not Found', 'The File does not exists.\nWe will make a new one for You.')
            open(path, "w")

    def clear_logging(self):
        path = f"{os.path.expanduser('~')}\\Desktop\\log.txt"
        with open(path, 'a') as f:
            f.seek(0)
            f.truncate()

    def write(self):
        self.name = self.s.getsockname()
        while True:
            self.message = self.s.recv(4096).decode()
            self.name = self.s.getsockname()
            if not self.message == "":
                time.sleep(1)
                self.listbox.insert(END, f"{self.name}==> {self.message}")

    def send_message(self):
        self.to_send = self.entry.get()
        self.listbox.insert(END, f"You ==> {self.to_send}")
        self.name = str(self.nickname.get())
        msg = self.name+" ==> "+self.to_send+"\n"
        try:
            self.s.send(msg.encode())
            time.sleep(0.1)
            self.entry.delete(0, END)
        except:
            messagebox.showerror("Server Offline", "It seems that the server you are trying to reach is offline.")

    def main(self):
        root = Tk()
        self.entry = Entry(root, font=('Fira Code',12),border=1,width=30)
        self.nickname = Entry(root, font=('Roboto Mono', 10), border=1, width=14)
        label = Label(root, text="DARK-SOUL-IRC", fg="white",bg="black", font=("Roboto Mono", 18))   
        self.listbox=Listbox(root,height=18,width=50, font=("Roboto Mono",10))
        clicked = StringVar()
        clicked.set("Client")
        drop = OptionMenu(root, clicked, "Client", "Server")
        send = Button(root, text="SEND",fg="white",bg="black", command=self.send_message)
        chats = Label(root, text="CHATS", fg="white", bg="black", font=("Fira Code Light", 15))

        def set():
            self.get = Label(root, text=f"IP: {self.ip.get()}", bg="black", fg="blue", font=("Fira Code",11))
            self.get.place(x=15, y=153)
        def set_port():
            self.get = Label(root, text=f"PORT: {self.port.get()}", bg="black", fg="blue", font=("Fira Code",11))
            self.get.place(x=15, y=232)
        def get_name():
            self.name = str(self.nickname.get())
            nick_pr = Label(root, text=f"NICKNAME: {self.name}", bg="black", fg="blue", font=("Fira Code", 11))
            nick_pr.place(x=13, y=329)
            
        self.ip = Entry(root, text="Enter IP address: ", width=16) 
        self.port = Entry(root, text="Enter the Port: ", width=16)
        self.ip_but = Button(root, text="SET IP",fg="white",bg="black", command=set)
        self.con = Button(root, text="CONNECT !!",fg="white",bg="black",font=("Fira Code",10), command=self.connect)
        self.port_set = Button(root, text="SET PORT",fg="white",bg="black", command=set_port)
        self.clear_logging = Button(root, text=" CLEAR LOG ",fg="white",bg="black",font=("Roboto Mono",10),command=self.clear_logging)
        self.enter_1 = Label(root, text="Enter IP", bg="black", fg="white", font=("Roboto Mono",10))
        self.enter_2 = Label(root, text="Enter PORT", bg="black", fg="white", font=("Roboto Mono",10))
        self.close = Button(root, text=" CLOSE CONNECTION ",fg="white",bg="red",font=("Fira Code",10), command=self.disconnect)
        enter_nick = Label(root, text="Enter NICKNAME ", bg="black", fg="white", font=("Roboto Mono",10))
        self.get_nick = Button(root, text=" SET ",fg="white",bg="black",font=("Roboto Mono",9), command=get_name)
        self.log = Button(root, text=" LOG DATA ",fg="white",bg="black",font=("Roboto Mono",10),command=self.logging)
        self.write_logging = Button(root, text=" WRITE LOG ",fg="white",bg="black",font=("Roboto Mono",10),command=self.write_log)
        
        self.write_logging.config(width=9)
        self.write_logging.place(x=115, y=60)
        self.clear_logging.config(width=9)
        self.clear_logging.place(x=105, y=10)
        self.log.config(width=9)
        self.log.place(x=385, y=10)
        chats.place(x=340, y=54)
        self.get_nick.config(height=0)
        self.get_nick.place(x=139, y=294)
        enter_nick.place(x=15, y=267)
        self.enter_2.place(x=15, y=178)
        self.port_set.place(x=125, y=205)
        self.enter_1.place(x=15,y=98)
        self.port.place(x=15, y=207)
        self.con.config(width=18)
        self.con.config(height=1)
        self.con.place(x=15, y=360)
        self.ip_but.config(width=7)
        self.ip_but.place(x=125, y=125)
        self.ip.place(x=15, y=127)
        send.config(height=1)
        send.config(width=11)
        send.place(x=500, y=447)
        drop.config(bg="black", fg="white")
        drop["menu"].config(bg="black", fg="white")
        drop.config(width=6)
        drop.config(height=1)
        drop.place(x=15, y=60)
        label.place(x=193, y=5)
        self.nickname.place(x=15, y=297)
        self.listbox.place(x=190,y=95)
        self.entry.place(x=190, y=445)
        root.title("DSI Chats")
        root.geometry("599x480")
        root.resizable(0,0)
        root.configure(bg="black")
        root.mainloop()


a = client_chat_ui()
a.main()
