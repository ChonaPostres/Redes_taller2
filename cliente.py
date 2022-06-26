from datetime import datetime
import socket
from tkinter import *
from tkinter import ttk

HOST = "127.0.0.1"
PORT = 25



#Main Screen Init
master       = Tk()
master.title('Inicio de sesion')
master.geometry('300x200')


#Storage
temp_username = StringVar()
temp_password = StringVar()
temp_receiver = StringVar()
temp_subject  = StringVar()
temp_body     = StringVar()

class Buzon :
    def __init__(self) :
        self.username = ""
        self.to = ""
        self.subject = ""
        self.body = ""
        self.time = datetime.now()
    def add(self, username, to, subject, body):
        self.username = username
        self.to = to
        self.subject = subject
        self.body = body
        self.time = datetime.now()


#Functions
#def addBuzon(username, to, subject, body) :
 #   print("emailAdd()")
  #  buzon[cont].append(Buzon().add(0, username, to, subject, body))
   # cont+= 1
    #buzonEmail()
def verEmail(email_from, email_to, email_subject) :
    print("verEmail()")
    print(email_from)
    print(email_to)
    print(email_subject)


def buzonEmail() :
    print("buzonEmail()")
    if (validar_email()) :
        # Table
        master.withdraw()
        ventana_buzonDeCorreos = Toplevel()
        ventana_buzonDeCorreos.title("Buzón de Correo")
        ventana_buzonDeCorreos.geometry("300x200")
        Label(ventana_buzonDeCorreos, text="Buzón", font=('Calibri',11)).grid(row=0, sticky=N)
        Button(ventana_buzonDeCorreos, text='Redactar email', command=sendEmail).grid(row=1, column=2,sticky=W+E)
        # Botones de correos 
        try:
            # Pedir correos adjuntos al usuario
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                operacion = "2"
                s.send(bytes(operacion+".", "utf-8"))
                data = s.recv(1024)
            print("Recibido", repr(data))
            data = data.decode('UTF-8')
            data = data.split("\n\n\n--------------\n\n")
            email = []
            print(data)
            for i in range(len(data) - 1):
                split = data[i].split("\n")
                print("\n")
                print(split)
                from_izquierda = (split[1]).find("<") + 1
                from_derecha = (split[1]).find(">")
                to_izquierda = (split[2]).find("<") + 1
                to_derecha = (split[2]).find(">")
                subject = ((split[3]).split(": "))[1] + "        " + split[4]
                email.append([(split[1])[from_izquierda : from_derecha], (split[2])[to_izquierda : to_derecha], subject])
            print(email)
            username = temp_username.get()
            row = 2
            for i in range(len(email)):
                if (username == email[i][0] or username == email[i][1]) :
                    Button(ventana_buzonDeCorreos, text=f"{email[i][2]}", command=lambda:verEmail(email[i][0], email[i][1], email[i][2])).grid(row=row, column=2, sticky=W+E)
                    row+=1
            
        except Exception as e:
            print(e)

    else: 
        print("No se encuentra registrado")
    
    


def validar_email() :
    return True
def sendEmail() :
    if (validar_email()) :
        master.withdraw()
        ventana_envioDeCorreos = Toplevel()
        ventana_envioDeCorreos.title('Crear correo')
        ventana_envioDeCorreos.geometry('300x200')
        frameSendEmail = LabelFrame(ventana_envioDeCorreos, text="Crear Correo")
        frameSendEmail.grid(row=0, column=0, columnspan=3, pady=20)
        Label(frameSendEmail, text="To", font=('Calibri', 11)).grid(row=1,sticky=W, padx=5)
        receiverEntry  = Entry(frameSendEmail, textvariable = temp_receiver)
        receiverEntry.grid(row=1,column=1)
        Label(frameSendEmail, text="Subject", font=('Calibri', 11)).grid(row=2,sticky=W, padx=5)
        subjectEntry  = Entry(frameSendEmail, textvariable = temp_subject)
        subjectEntry.grid(row=2,column=1)
        Label(frameSendEmail, text="Body", font=('Calibri', 11)).grid(row=3,sticky=W, padx=5)
        bodyEntry     = Entry(frameSendEmail, textvariable = temp_body)
        bodyEntry.grid(row=3,column=1)
        Button(ventana_envioDeCorreos, text = "Send", command = send).grid(row=4,  sticky=W,  padx=45, pady=40)
    else :
        print("No se encuentra registrado")
    
def send():
    try:
        username = temp_username.get()
        to       = temp_receiver.get()
        subject  = temp_subject.get()
        body     = temp_body.get()
        if username=="" or to=="" or subject=="" or body=="":
            return
        else:
            finalMessage = '{}\n{}'.format(subject, body)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                operacion = "1"
                s.send(bytes(operacion+";", "utf-8"))
                s.send(bytes(username+";", "utf-8"))
                s.send(bytes(to+";", "utf-8"))
                s.send(bytes(finalMessage+";", "utf-8"))
                
                data = s.recv(1024)
                #addBuzon(username, to, subject, body)
            print("Recibido", repr(data))
    except Exception as e:
        print(e)


def reset():
  usernameEntry.delete(0,'end')
  passwordEntry.delete(0,'end')
  #receiverEntry.delete(0,'end')
  #subjectEntry.delete(0,'end')
  #bodyEntry.delete(0,'end')

#Frame Iniciar Sesion
frameIS = LabelFrame(master, text = "Iniciar Sesion")
frameIS.grid(row=1, column=0, columnspan=3, pady=20)

#Labels
Label(master, text="Custom Email App", font=('Calibri',15)).grid(row=0, sticky=N)
#Label(master, text="Iniciar Sesion", font=('Calibri',11)).grid(row=1, sticky=W, padx=5 ,pady=10)
Label(frameIS, text="Email", font=('Calibri', 11)).grid(row=2,sticky=W, padx=5)
usernameEntry = Entry(frameIS, textvariable = temp_username)
usernameEntry.grid(row=2,column=1)
Label(frameIS, text="Password", font=('Calibri', 11)).grid(row=3,sticky=W, padx=5)
passwordEntry = Entry(frameIS, show="*", textvariable = temp_password)
passwordEntry.grid(row=3,column=1)



#Buttons
Button(master, text = "Login", command = buzonEmail).grid(row=7,   sticky=W,  pady=40, padx=45)

#Mainloop
master.mainloop()






