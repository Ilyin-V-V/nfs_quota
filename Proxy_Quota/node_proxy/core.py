#!/usr/bin/env python
from time import sleep
import sys
import paramiko
import re
import cfg
import logger
import mail

class Core(object):
        def __init__(self):
                self.name = "Core"
		self.help = "proxy connector example: command string parameters"

	def packing_parameters(self,param):
                str_param,index,index_max='',0,len(param)
                while index < index_max:
			if index != 0:
				str_param = str_param +" "+param[index]
                        index+=1
		return str_param

	def ssh_connect_command(self,host,port,user,command,param):
		obj_log = logger.Logger()
		index,index_max=0,len(host)
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                while index < index_max:
			try:
				client.connect(hostname=host[index], username=user, port=port, timeout=4, banner_timeout=3, auth_timeout=3)
				stdin, stdout, stderr = client.exec_command(command+" "+param)
                		data = stdout.read() + stderr.read()
				index = index_max
				obj_log.loglogged('Return data '+data)
                		return data
			except (paramiko.AuthenticationException,
					paramiko.ssh_exception.NoValidConnectionsError) as e:
					obj_log.loglogged('Timeout connect host '+host[index])
			except paramiko.SSHException as e:
					obj_log.loglogged('Logical error ssh connect host '+host[index])
			except (paramiko.ssh_exception.BadHostKeyException,
					paramiko.ssh_exception.BadAuthenticationType) as e:
					obj_log.loglogged('Bad key error ssh connect host '+host[index])
			finally:
            			client.close()
			index+=1

if __name__ == "__main__":
	obj_scripts,obj_conf,obj_log = Core(),cfg.Configuration(),logger.Logger()
	if len(sys.argv) >= 2:
		#Show help
		if sys.argv[1] == "-h":
			print obj_scripts.help
			exit()
		#Email alert
		if sys.argv[1] == "--all":
			str_param = obj_scripts.packing_parameters(sys.argv)
                	command_out = obj_scripts.ssh_connect_command(obj_conf.ssh_host,obj_conf.ssh_port,obj_conf.ssh_user,
                        	obj_conf.command_worker,str_param)
                	if command_out:
				obj_log.loglogged('Receive quota usage report')
				obj_log.loglogged(command_out)
				quota_arr = command_out.split('\n')
				index,index_max,sys_user=0,len(quota_arr),int(obj_conf.sys_user)
				index_off = index_max - 2
				if (len(quota_arr) < sys_user):
				#Problem ldap show user
					i,max=0,int(obj_conf.retry_fail)
					sleep(2)
					while i < max:
						command_out = obj_scripts.ssh_connect_command(obj_conf.ssh_host,obj_conf.ssh_port,obj_conf.ssh_user,
                                			obj_conf.command_worker,str_param)
						obj_log.loglogged('Receive quota usage report problem ldap show')
                                		obj_log.loglogged(command_out)
						quota_arr = command_out.split('\n')
						if (len(quota_arr) > sys_user):
							index_max=len(quota_arr)
							index_off = index_max - 2
							i=max
						i+=1
				while index < index_max:
					if index < index_off:
						quota = quota_arr[index].split(', ')
						user,use,soft,hard = quota[3],quota[4],quota[5],quota[6]
						u_use,u_soft = re.findall(r"'(.*)'",use),re.findall(r"'(.*)'",soft)
						u_use,u_soft = u_use[0],u_soft[0]
						if (long(u_use) > long(u_soft)):
							if soft != "'0'":
								obj_log.loglogged("Warning usage quota exceeded"+' '+user+' '+use+' '+soft+' '+hard)
								user_login = re.findall(r"'(.*)'",user)
								use_user = re.findall(r"'(.*)'",use)
								use_soft = re.findall(r"'(.*)'",soft)
								use_hard = re.findall(r"'(.*)'",hard)
								to_user = user_login[0]+'@'+obj_conf.domain
								obj_mail = mail.Email(obj_conf.host,obj_conf.user,obj_conf.password,
                							obj_conf.m_subject,obj_conf.m_from,to_user,obj_conf.m_text,obj_conf.m_email,
									user_login[0],float(use_user[0])/1000000,float(use_soft[0])/1000000,
									float(use_hard[0])/1000000)
								obj_mail.send_email(user_login[0])
								sleep(5)
					index+=1
                	else:
                        	obj_log.loglogged('SSH workers not available')
                        	success,code='False','SSH workers not available'
                        	code=[success,code]
                        	print code
			exit()
		#QuotaCheck
                if sys.argv[1] == "--check":
                        str_param = ' >> /home/edquota/WorkerQuota/log.log &'
			command_out = obj_scripts.ssh_connect_command(obj_conf.ssh_host,obj_conf.ssh_port,obj_conf.ssh_root,
                        obj_conf.command_quotacheck,str_param)
                	if command_out:
				obj_log.loglogged(command_out)
                	else:
                        	obj_log.loglogged('Run QuotaCheck background mode')
                        	success,code='True','Run QuotaCheck background mode'
                        	code=[success,code]
                        print code
			exit()
		#BackupStorage
                if sys.argv[1] == "--backup":
                        str_param = ' >> /home/edquota/WorkerQuota/log.log &'
                        command_out = obj_scripts.ssh_connect_command(obj_conf.ssh_host,obj_conf.ssh_port,obj_conf.ssh_root,
                        obj_conf.command_backup,str_param)
                        if command_out:
                                obj_log.loglogged(command_out)
                        else:
                                obj_log.loglogged('Run BackupStorage background mode')
                                success,code='True','Run BackupStorage background mode'
                                code=[success,code]
                        print code
                        exit()
		#Any method
		str_param = obj_scripts.packing_parameters(sys.argv)
		command_out = obj_scripts.ssh_connect_command(obj_conf.ssh_host,obj_conf.ssh_port,obj_conf.ssh_user,
			obj_conf.command_worker,str_param)
		if command_out:
			print command_out
		else:
			obj_log.loglogged('SSH workers not available')
			success,code='False','SSH workers not available'
                        code=[success,code]
			print code

	else:
		print obj_scripts.help
