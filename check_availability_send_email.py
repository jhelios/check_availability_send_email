#/usr/bin/python3
import socket
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendMail(message):
	try:
		#Envio de correo
		sender_address = 'email@gmail.com'
		sender_pass = 'pass_email'
		receiver_address = 'destinatio@mail.com'

		mail_content = "Hola,\n\nSe idenfico lo siguiente: \n"+message+"\n\nEste mensaje fue creado por el script de validación de disponibilidad, por favor no responder.\nThanks!"

		message = MIMEMultipart()
		message['From'] = sender_address
		message['To'] = receiver_address
		message['Subject'] = 'Reporte de disponibilidad - Script python' 
		message.attach(MIMEText(mail_content, 'plain'))
		session = smtplib.SMTP('smtp.gmail.com', 587)
		session.starttls()
		session.login(sender_address, sender_pass)
		text = message.as_string()
		session.sendmail(sender_address, receiver_address, text)
		session.quit()
		return True
	except:
		return False

#Validación de disponibilidad

hosts = {
	'domain1':[80],
	'domain3':[3389],
	'1.1.1.1':[21],
	'3.3.3.3':[23]
}

for host in hosts:
	for port in hosts[host]:
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			result = sock.connect_ex((host,port))
			if result == 0:
				mailSent = sendMail("Puerto abierto: "+host+":"+str(port))
				if mailSent:
					print("Puerto abierto:",host+":"+str(port), "- Correo enviado correctamente")
				else:
					print("Puerto abierto:",host+":"+str(port), "- Error en envio de correo")
			else:
				print("Puerto cerrado")
		except socket.error as error:
			if str(error).find("[Errno 11001] getaddrinfo failed") >= 0:
				print("Host no disponible")
			else:
				sendMail("Se presento un error en la validación de", host, ". Error:", error)
		finally:
			sock.close()
