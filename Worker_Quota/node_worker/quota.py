#!/usr/bin/env python
from subprocess import check_output, CalledProcessError, STDOUT
import cfg
import logger

class Quota():
	def __init__(self,filesystem,user,soft,hard,cat,sed,grep,edquota,getent,cut,run_sudo,sudo):
                self.name = "Quota"
		self.term = "#!/bin/bash"
		self.edquota = edquota
		self.cat = cat
		self.sed = sed
		self.grep = grep
		self.getent = getent
		self.cut = cut
		self.sudo = sudo
		self.run_sudo = run_sudo
		self.name_file = "$1"
		self.filesystem	= filesystem
		self.user = user
		self.soft = soft
		self.hard = hard
		self.str = self.cat+' '+\
			self.name_file+\
			' '+'|'+' '+\
			self.sed+\
			self.filesystem+\
			'/'+\
			self.filesystem+\
			'	'+'0'+'	'+self.soft+'	'+self.hard+'	'+'0'+'	'+'0'+'	'+'0/\''+\
			' '+self.name_file
		self.show_str =	self.cat+' '+self.name_file
		self.report = self.getent+' | '+self.cut+' -d":" -f1'

        def add_edit_quota(self,action,filesystem,user,soft,hard,cat,sed,grep,edquota,getent,cut,run_sudo,sudo):
		obj_log = logger.Logger()
		if (soft > "0" and hard > "0"):
			if (int(soft) < int(hard)):
				if ((len(soft) >= 3) and (len(hard) >= 3)):
					if action == "--add": obj_log.loglogged(action,filesystem,user,"add_quota")
					if action == "--edit": obj_log.loglogged(action,filesystem,user,"edit_quota")
					if action == "--change": obj_log.loglogged(action,filesystem,user,"change_quota")
					data = self.str
					obj_add_edit = Quota(filesystem,user,soft,hard,cat,sed,grep,edquota,getent,cut,run_sudo,sudo)
					obj_add_edit.file_create(self.term,data)
					if self.run_sudo == "True": command=self.sudo+' '+edquota+' '+user
                			else: command=edquota+' '+user
					success,output = obj_add_edit.command_execude(command)
					if success:
						code=[success,output]
						return success,code
					else:
						success,code='False','Error '+action+' command',output,' '
                        			code=[success,code]
                        			return success,code
				else:
					success,code='False',"Operation failed option Soft or Hard less than three characters"
					obj_log.loglogged(action,filesystem,user,"Operation failed option Soft or Hard less than three characters")
                                        code=[success,code]
                                       	return success,code
			elif (int(soft) > int(hard)):
				success,code='False',"Operation failed option Soft could not be more Hard"
				obj_log.loglogged(action,filesystem,user,"Operation failed option Soft could not be more Hard")
                                code=[success,code]
                               	return success,code
		elif (soft <= "0" or hard <= "0"):
			success,code='False',"Operation failed option Soft or Hard less equal 0"
			obj_log.loglogged(action,filesystem,user,"Operation failed option Soft or Hard less equal 0")
                        code=[success,code]
                        return success,code

	def remove_quota(self,action,filesystem,user,soft,hard,cat,sed,grep,edquota,getent,cut,run_sudo,sudo):
		obj_log = logger.Logger()
                obj_log.loglogged(action,filesystem,user,"remove_quota")
		data = self.str
		obj_remove = Quota(filesystem,user,soft,hard,cat,sed,grep,edquota,getent,cut,run_sudo,sudo)
                obj_remove.file_create(self.term,data)
		if self.run_sudo == "True": command=self.sudo+' '+edquota+' '+user 
                else: command=edquota+' '+user
		success,output = obj_remove.command_execude(command)
                if success:
                	code=[success,output]
                	return success,code
                else:
                	success,code='False','Error '+action+' command',output
               		code=[success,code]
                	return success,code

	def view_quota(self,action,filesystem,user):
		obj_log = logger.Logger()
                obj_log.loglogged(action,filesystem,user,"show_quota")
		obj_param=cfg.Configuration()
		soft=hard=cat=sed=grep=edquota=getent=cut=run_sudo=sudo="0"
		if self.run_sudo == "True": data,command=self.show_str,self.sudo+' '+self.edquota+' '+self.user
		else: data,command=self.show_str,self.edquota+' '+self.user
		obj_view = Quota(filesystem,user,soft,hard,cat,sed,grep,edquota,getent,cut,run_sudo,sudo)
                obj_view.file_create(self.term,data)
		success,output = obj_view.command_execude(command)
		if success:
                        head=output[0]+' '+output[1]+' '+output[2]+' '+output[3]+' '+output[4]+' '+output[5]+' '+output[6]
                        filesystem,user,use,soft,hard=output[14],output[4],output[15],output[16],output[17]
                        code=[success,head,filesystem,user,use,soft,hard]
                        return success,code
                else:
                     	success,code='False',output[1]+' '+output[2]+' '+output[3]+' '+output[4]+' '+output[5]
                        code=[success,code]
                        return success,code

	def report_quota(self,action,cat,edquota,path):
		obj_log = logger.Logger()
                obj_log.loglogged(action,'report_quota','not_user',"report_quota")
		obj_param=cfg.Configuration()
		filesystem=user=soft=hard=sed=grep=getent=cut="0"
		run_sudo,sudo=self.run_sudo,self.sudo
		command=self.report
		obj_report = Quota(filesystem,user,soft,hard,cat,sed,grep,edquota,getent,cut,run_sudo,sudo)
		success,output = obj_report.command_execude(command)
		if success:
			index,file_path=0,path+"/report"
			command="/usr/bin/rm -f "+file_path
			obj_report.command_execude(command)
			while index<len(output):
				obj_report.user=output[index]
				success,code = obj_report.view_quota(action,filesystem,output[index])
				file = open(file_path, 'a')
                		file.write(str(code) +"\n")
                		file.close()
				print code
				index+=1
			code=[success,'[]']
                        return success,code
                else:
                     	success,code='False','Error '+action+' command',output
                        code=[success,code]
                        return success,code

	def file_create(self,head,data):
		obj_log = logger.Logger()
                obj_log.loglogged('file_create','file_create','not_user','apply_file')
                obj_file = cfg.Configuration()
                file_path = obj_file.path_sh+"/edquota.sh"
                file = open(file_path, 'w')
                file.write(head +"\n")
		file.write(data +"\n")
                file.close()

	def command_execude(self,command):
		obj_log = logger.Logger()
                obj_log.loglogged('command_execude','command_execude','not_user',"apply_command")
		try:
			output = check_output(command,stderr=STDOUT,shell=True)
			success = True
		except CalledProcessError as err:
    			output = err.output
    			success = False
		output = output.split()
		return success,output
