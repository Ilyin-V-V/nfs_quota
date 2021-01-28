#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
import logger
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Email():
        def __init__(self,host,user,password,m_subject,m_from,m_to,m_text,m_email,m_user,m_use,m_soft,m_hard):
                self.name = "Email"
		self.host = host
		self.user = user
		self.password = password
		self.m_email = m_email
		self.m_from = m_from
		self.m_to = m_to
		self.h1 = m_text[0]
		self.h2 = m_text[1]
		self.tr1 = "User: "+m_user
		self.tr2 = "Used: "+str(m_use)+" Gb"
		self.tr3 = "Warning: "+str(m_soft)+" Gb"
		self.tr4 = "Blocking: "+str(m_hard)+" Gb"
		self.m_user = m_user
		self.m_use = m_use
		self.m_soft = m_soft
		self.m_hard = m_hard
		self.msg = MIMEMultipart('alternative')
		self.msg['Subject'] = m_subject
		self.msg['From'] = m_from
		self.msg['To'] = m_to
		self.m_text = "User: "+str(m_user)+'\n'+\
                                "Used: "+str(m_use)+'\n'+\
                                "Limit: "+str(m_soft)
		self.html = """\
		<html>
  		 <head></head>
                  <style>
		   .tr{margin-left: 3em;}
                   .h{margin-left: 1em;}
		  </style>
  		  <body>
                   <p class="h"><font size="4" color="red" face="Arial">
		"""+self.h1+\
			"""</font></p>
                   <p class="tr"><font size="3" color="green" face="Arial">
		"""+self.tr1+\
                	"""</font><br>
		   <font size="3" color="green" face="Arial">
                """+self.tr2+\
                        """</font><br>
                   <font size="3" color="green" face="Arial">
                """+self.tr3+\
                        """</font><br>
                    <font size="3" color="green" face="Arial">
                """+self.tr4+\
                        """</font><br>
		   </p>
		    <p class="h"><font size="3" color="black" face="Arial">
                """+self.h2+\
                        """</font></p>
                 </body>
                </html>
		"""
	def send_email(self,user):
		part1 = MIMEText(self.m_text,'plain','utf-8')
		part2 = MIMEText(self.html,'html','utf-8')
		self.msg.attach(part1)
		self.msg.attach(part2)
                index,index_max,obj_log=0,len(self.m_email),logger.Logger()
                while index < index_max:
			if user == self.m_email[index]:
				obj_log.loglogged(user+' '+'user on the mailing list exclusion list')
				return
			index+=1
		obj_log.loglogged('Send email alert '+' '+self.m_to)
		try:
			server = smtplib.SMTP(self.host)
			try:
				server.sendmail(self.m_from,[self.m_to],self.msg.as_string())
			finally:
				server.quit()
		except (OSError, smtplib.SMTPException) as e:
                	obj_log.loglogged('Error send smtp email '+self.host+' '+user)
