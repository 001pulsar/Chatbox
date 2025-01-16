import socket
import threading
from tkinter import *
from tkinter import font
from tkinter import ttk

def get_port():
  """
  Gets the port number entered by the user and sets the 'port' variable.
  """
  global port
  port = int(entry_port.get())
  window.destroy()  # Close the window after getting the port

# Create the main window for port selection
window = Tk()
window.title("Enter Port")

# Create a label
label_port = Label(window, text="Port to connect:")
label_port.pack()

# Create an entry field for user input
entry_port = Entry(window)
entry_port.pack()

# Create a submit button
button_submit = Button(window, text="Submit", command=get_port)
button_submit.pack()

# Initialize the port variable (optional)
port = None

# Start the GUI event loop for port selection
window.mainloop()

# Now the port is set and the mainloop has finished

# SERVER address (can be replaced with an IP address if needed)
SERVER = "192.168.0.104" 

# Create a new client socket and connect to the server using the selected port
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((SERVER, port))
except ConnectionRefusedError:
    print(f"Connection refused. Please check if the server is running on port {port}.")
    exit()

# Create a GUI class for the chat
class GUI:
  # constructor method
  def __init__(self):
    self.Window = Tk()
    self.Window.withdraw()

    self.login = Toplevel()
    self.login.title("Login")
    self.login.resizable(width=False, height=False)
    self.login.configure(width=400, height=300)

    self.pls = Label(self.login,
                     text="Please login to continue",
                     justify=CENTER,
                     font="Helvetica 14 bold")
    self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

    self.labelName = Label(self.login, text="Name: ", font="Helvetica 12")
    self.labelName.place(relheight=0.2, relx=0.1, rely=0.2)

    self.entryName = Entry(self.login, font="Helvetica 14")
    self.entryName.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.2)

    self.entryName.focus()

    self.go = Button(self.login,
                      text="CONTINUE",
                      font="Helvetica 14 bold",
                      command=lambda: self.goAhead(self.entryName.get()))
    self.go.place(relx=0.4, rely=0.55)
    self.Window.mainloop()

  def goAhead(self, name):
    self.login.destroy()
    self.layout(name)

    # The thread to receive messages
    rcv = threading.Thread(target=self.receive)
    rcv.start()

  # The main layout of the chat
  def layout(self, name):
    self.name = name
    self.Window.deiconify()
    self.Window.title("Chatbox")
    self.Window.resizable(width=False, height=False)
    self.Window.configure(width=470, height=550, bg="#17202A")

    self.labelHead = Label(self.Window, bg="#17202A", fg="#EAECEE",
                           text=self.name, font="Helvetica 13 bold", pady=5)
    self.labelHead.place(relwidth=1)

    self.line = Label(self.Window, width=450, bg="#ABB2B9")
    self.line.place(relwidth=1, rely=0.07, relheight=0.012)

    self.textCons = Text(self.Window, width=20, height=2, bg="#17202A",
                         fg="#EAECEE", font="Helvetica 14", padx=5, pady=5)
    self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)

    self.labelBottom = Label(self.Window, bg="#ABB2B9", height=80)
    self.labelBottom.place(relwidth=1, rely=0.825)

    self.entryMsg = Entry(self.labelBottom, bg="#2C3E50", fg="#EAECEE",
                          font="Helvetica 13")
    self.entryMsg.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
    self.entryMsg.focus()

    self.buttonMsg = Button(self.labelBottom, text="Send",
                            font="Helvetica 10 bold", width=20, bg="#ABB2B9",
                            command=lambda: self.sendButton(self.entryMsg.get()))
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
          self.textCons.insert(END, message+"\n\n")
          self.textCons.config(state=DISABLED)
          self.textCons.see(END)
      except:
        print("An error occurred!")
        client.close()
        break

  def sendMessage(self):
    self.textCons.config(state=DISABLED)
    while True:
      message = (f"{self.name}: {self.msg}")
      client.send(message.encode('utf-8'))
      break

# create a GUI class object
g = GUI()