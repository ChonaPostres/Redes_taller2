import socket
import mailbox
import email.utils


HOST = "127.0.0.1"
PORT = 25

payload = '''
--------------
'''

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()

    with conn:
        while(conn) :

            #print(f"Conectado a {addr}:")
            while True:
                operacion = conn.recv(1024)
                operacion = operacion.decode('UTF-8')
                if not operacion:
                    break
                if (operacion[0] == "1") :
                    operacion = operacion.split(";")
                    print("Operacion de envio de correo")
                    print(operacion)
                    from_addr = email.utils.formataddr(('Autor',operacion[1]))
                    to_addr = email.utils.formataddr(('Para',operacion[2]))
                    mbox = mailbox.mbox('RegistrosEmail.mbox')
                    mbox.lock()
                    try:
                        msg = mailbox.mboxMessage()
                        msg['From'] = from_addr
                        msg['To'] = to_addr
                        msg['Subject'] = operacion[3]
                        msg.set_payload(payload)
                        mbox.add(msg)   
                        mbox.flush()
                    finally:
                        mbox.unlock()
                    print(open('RegistrosEmail.mbox', 'r').read())
                    conn.send(bytes("Correo Enviado", "utf-8"))
                elif (operacion[0] == "2"):
                    print(open('RegistrosEmail.mbox', 'r').read())
                    conn.send(bytes(open('RegistrosEmail.mbox', 'r').read(), "utf-8"))

        
            
            
