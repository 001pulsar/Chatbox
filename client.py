import socket
import threading
from tkinter import *
from tkinter import font
from tkinter import ttk

def get_server_address():
    global SERVER
    SERVER = entry_server.get()
    server_window.destroy()

def get_port():
    global port
    try:
        port = int(entry_port.get())
        window.destroy()
    except ValueError:
        print("Invalid port number. Please enter an integer.")
        return

server_window = Tk()
server_window.title("Enter Server Address")

label_server = Label(server_window, text="Server Address:")
label_server.pack()

entry_server = Entry(server_window)
entry_server.pack()

button_server_submit = Button(server_window, text="Submit", command=get_server_address)
button_server_submit.pack()

SERVER = None
server_window.mainloop()

if SERVER is None:
    exit()

window = Tk()
window.title("Enter Port")

label_port = Label(window, text="Port to connect:")
label_port.pack()

entry_port = Entry(window)
entry_port.pack()

button_submit = Button(window, text="Submit", command=get_port)
button_submit.pack()

port = None
window.mainloop()

if port is None:
    exit()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((SERVER, port))
except ConnectionRefusedError:
    print(f"Connection refused. Please check if the server is running on {SERVER}:{port}.")
    exit()

class GUI:
    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()

        self.login = Toplevel()
        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300)

        self.pls = Label(self.login, text="Please login to continue", justify=CENTER, font="Helvetica 14 bold")
        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

        self.labelName = Label(self.login, text="Name: ", font="Helvetica 12")
        self.labelName.place(relheight=0.2, relx=0.1, rely=0.2)

        self.entryName = Entry(self.login, font="Helvetica 14")
        self.entryName.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.2)
        self.entryName.focus()

        self.go = Button(self.login, text="CONTINUE", font="Helvetica 14 bold", command=lambda: self.goAhead(self.entryName.get()))
        self.go.place(relx=0.4, rely=0.55)
        self.Window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)
        rcv = threading.Thread(target=self.receive)
        rcv.start()

    def layout(self, name):
        self.name = name
        self.Window.deiconify()
        self.Window.title("Chatbox")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=470, height=550, bg="#17202A")

        self.labelHead = Label(self.Window, bg="#17202A", fg="#EAECEE", text=self.name, font="Helvetica 13 bold", pady=5)
        self.labelHead.place(relwidth=1)

        self.line = Label(self.Window, width=450, bg="#ABB2B9")
        self.line.place(relwidth=1, rely=0.07, relheight=0.012)

        self.textCons = Text(self.Window, width=20, height=2, bg="#17202A", fg="#EAECEE", font="Helvetica 14", padx=5, pady=5)
        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)

        self.labelBottom = Label(self.Window, bg="#ABB2B9", height=80)
        self.labelBottom.place(relwidth=1, rely=0.825)

        self.entryMsg = Entry(self.labelBottom, bg="#2C3E50", fg="#EAECEE", font="Helvetica 13")
        self.entryMsg.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.entryMsg.focus()

        self.buttonMsg = Button(self.labelBottom, text="Send", font="Helvetica 10 bold", width=20, bg="#ABB2B9", command=lambda: self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

        self.textCons.config(cursor="arrow")

        scrollbar = Scrollbar(self.textCons)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()

    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message == 'NAME':
                    client.send(self.name.encode('utf-8'))
                else:
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, message + "\n\n")
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
            except Exception as e: #catch any exception to avoid crashing
                print(f"An error occurred: {e}")
                client.close()
                break

    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        message = f"{self.name}: {self.msg}"
        client.send(message.encode('utf-8'))


g = GUI()
