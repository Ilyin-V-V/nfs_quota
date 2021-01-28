#!/usr/bin/env python
import sys
import re
import cfg
import logger
import help
import quota

class Core(object):
        def __init__(self):
                self.name = "Core"
		self.num_param = len(sys.argv)
		self.action = ""
		self.key_f = "-f"
		self.filesystem = ""
		self.key_u = "-u"
		self.user = ""
		self.key_s = "-s"
		self.soft = ""
		self.key_h = "-h"
		self.hard = ""
		self.report = "-r"
		self.help_param = 2
		self.report_param = 3
		self.show_remove_param = 6
		self.add_edit_param = 10
		self.stop = False

	def initialization_param(self,num_param,action,key_f,filesystem,key_u,user,key_s,soft,key_h,hard):
                obj_initialization,obj_log = cfg.Configuration(),logger.Logger()
		if num_param == self.help_param and action == "-h":
		#If number param == help_param => help() method
                	obj_initialization = help.Help(action)
			obj_initialization.view_help()
		elif num_param == self.report_param and action == "--all":
		#If number param == report_param => report() method
			if key_f != "-r":
				obj_log.loglogged('run','initialization_param','not','Not parameter in '+action+' run with the -h key for help')
                                print 'Not parameter in',action,'run with the -h key for help'
			else:
				return	action
		elif num_param == self.show_remove_param:
		#If number param == show_remove_param => remove() or show() method
			if action == "--remove" or action == "--show":
				if key_f != "-f" or\
					not filesystem or\
					key_u != "-u" or\
					not user:
						obj_log.loglogged('run','initialization_param','not','Not parameter in '+action+' run with the -h key for help')
						print 'Not parameter in',action,'run with the -h key for help'
						self.stop=True
						return action,key_f,filesystem,key_u,user,self.stop
				else:
					return action,key_f,filesystem,key_u,user,self.stop
			else:
				obj_log.loglogged('run','initialization_param','not','Not find action '+action+' run with the -h key for help')
				print 'Not find action',action,'run with the -h key for help'
                              	return action,key_f,filesystem,key_u,user,self.stop
		elif num_param == self.add_edit_param:
                #If number param == add_edit_param => add() or edit() method
			if action == "--add" or action == "--edit" or "--change":
                                if key_f != "-f" or\
                                        not filesystem or\
                                        key_u != "-u" or\
                                        not user or\
					key_s != "-s" or\
					not soft or\
					not hard or\
					key_h != "-h" or\
					(soft.isdigit() == False) or\
					(hard.isdigit() == False):
						obj_log.loglogged('run','initialization_param','not','Not parameter in '+action+' run with the -h key for help')
                                                print 'Not parameter in',action,'run with the -h key for help'
						self.stop=True
                                                return action,key_f,filesystem,key_u,user,key_s,soft,key_h,hard,self.stop
                                else:
                                        return action,key_f,filesystem,key_u,user,key_s,soft,key_h,hard,self.stop
                        else:
				obj_log.loglogged('run','initialization_param','not','Not find action '+action+' run with the -h key for help')
                                print 'Not find action',action,'run with the -h key for help'
                                return action,key_f,filesystem,key_u,user,key_s,soft,key_h,hard,self.stop
		else:
			obj_log.loglogged('run','initialization_param','not','Not action '+action+' run with the -h key for help')
			print 'Not action',action,'run with the -h key for help'

	def validate_param_filesystem(self,param_filesystem):
		obj_validate,obj_log = cfg.Configuration(),logger.Logger()
		valid,index,index_max=False,0,len(obj_validate.filesystem)
		while index < index_max:
			if param_filesystem != obj_validate.filesystem[index]:
				obj_log.loglogged('run',validate_param_filesystem,'not',"Not find set quota file system in settings")
				print "Not find set quota file system in settings"
				return valid
			index+=1
		valid=True
		return valid

if __name__ == "__main__":
	obj_scripts,obj_log = Core(),logger.Logger()
	if (obj_scripts.num_param == obj_scripts.help_param):
        	help_show = Core()
		help_show.action=str(sys.argv[1])
		key_f=filesystem=key_u=user=key_s=soft=key_h=hard=None
		load_param = help_show.initialization_param(obj_scripts.num_param,
				help_show.action,
				key_f,filesystem,
				key_u,user,
				key_s,soft,
				key_h,hard)

	elif (obj_scripts.num_param == obj_scripts.report_param):
		report_show = Core()
		report_show.action=str(sys.argv[1])
		report_show.key_f=str(sys.argv[2])
		filesystem=key_u=user=key_s=soft=key_h=hard=None
		action = report_show.initialization_param(obj_scripts.num_param,
                                report_show.action,
                                report_show.key_f,filesystem,
                                key_u,user,
                                key_s,soft,
                                key_h,hard)
		if action == "--all":
				obj_param,filesystem,user,soft,hard=cfg.Configuration(),'All','All','0','0'
                                obj_report = quota.Quota(filesystem,user,soft,hard,obj_param.cat,
                                        obj_param.sed,obj_param.grep,obj_param.edquota,obj_param.getent,
					obj_param.cut,obj_param.run_sudo,obj_param.sudo)
                                success,code = obj_report.report_quota(action,obj_param.cat,obj_param.edquota,obj_param.path)
				if success: print code
				else: print code

	elif (obj_scripts.num_param == obj_scripts.show_remove_param):
                quota_show_rm = Core()
		quota_show_rm.action=str(sys.argv[1])
		quota_show_rm.key_f=str(sys.argv[2])
		quota_show_rm.filesystem=str(sys.argv[3])
		quota_show_rm.key_u=str(sys.argv[4])
		quota_show_rm.user=str(sys.argv[5])
		key_s,soft,key_h,hard=quota_show_rm.key_s,quota_show_rm.soft,quota_show_rm.key_h,quota_show_rm.hard
                action,key_f,filesystem,key_u,user,stop = quota_show_rm.initialization_param(obj_scripts.num_param,
				quota_show_rm.action,
				quota_show_rm.key_f,
				quota_show_rm.filesystem,
				quota_show_rm.key_u,
				quota_show_rm.user,
				key_s,soft,key_h,hard)
		if stop: exit()
		validate = quota_show_rm.validate_param_filesystem(filesystem)
		if validate:
			soft=hard="0"
			obj_param,obj_log = cfg.Configuration(),logger.Logger()
			if action == "--show":
				obj_show = quota.Quota(filesystem,user,soft,hard,obj_param.cat,
					obj_param.sed,obj_param.grep,obj_param.edquota,obj_param.getent,
					obj_param.cut,obj_param.run_sudo,obj_param.sudo)
				success,code = obj_show.view_quota(action,filesystem,user)
				obj_log.loglogged(action,filesystem,user,code)
				print code
			elif action == "--remove":
				obj_remove = quota.Quota(filesystem,user,soft,hard,obj_param.cat,
					obj_param.sed,obj_param.grep,obj_param.edquota,obj_param.getent,
					obj_param.cut,obj_param.run_sudo,obj_param.sudo)
                                success,code = obj_remove.view_quota(action,filesystem,user)
                                if success == True:
                                        if (code[5] != '0' and code[6] != '0'):
                                                success,code = obj_remove.remove_quota(action,filesystem,user,soft,hard,
							obj_param.cat,obj_param.sed,obj_param.grep,obj_param.edquota,
							obj_param.getent,obj_param.cut,obj_param.run_sudo,obj_param.sudo)
						code_remove=code
						# Check remove
						success,code = obj_remove.view_quota(action,filesystem,user)
						if success == True:
                                			if (code[5] == '0' and code[6] == '0'):
								obj_log.loglogged(action,filesystem,user,code)
                                        			print code_remove
                                			else:
                                        			code=['False','Check: operation not executed']
								obj_log.loglogged(action,filesystem,user,code)
                                        			print code
                        			else:
							obj_log.loglogged(action,filesystem,user,code)
                                			print code
						# Check remove
                                        else:
                                                code=['False','User quota previously cleared']
						obj_log.loglogged(action,filesystem,user,code)
                                                print code
                                else:
					obj_log.loglogged(action,filesystem,user,code)
                                        print code

	elif (obj_scripts.num_param == obj_scripts.add_edit_param):
		quota_add_edit = Core()
                quota_add_edit.action=str(sys.argv[1])
                quota_add_edit.key_f=str(sys.argv[2])
                quota_add_edit.filesystem=str(sys.argv[3])
                quota_add_edit.key_u=str(sys.argv[4])
                quota_add_edit.user=str(sys.argv[5])
                quota_add_edit.key_s=str(sys.argv[6])
		quota_add_edit.soft=str(sys.argv[7])
		quota_add_edit.key_h=str(sys.argv[8])
		quota_add_edit.hard=str(sys.argv[9])
                action,key_f,filesystem,key_u,user,key_s,soft,key_h,hard,stop = quota_add_edit.initialization_param(obj_scripts.num_param,
				quota_add_edit.action,
				quota_add_edit.key_f,
				quota_add_edit.filesystem,
				quota_add_edit.key_u,
				quota_add_edit.user,
				quota_add_edit.key_s,
				quota_add_edit.soft,
				quota_add_edit.key_h,
				quota_add_edit.hard)
		if stop: exit()
		validate = quota_add_edit.validate_param_filesystem(filesystem)
                if validate:
			obj_param,obj_log = cfg.Configuration(),logger.Logger()
                        if action == "--add":
                                obj_add = quota.Quota(filesystem,user,soft,hard,obj_param.cat,
					obj_param.sed,obj_param.grep,obj_param.edquota,
					obj_param.getent,obj_param.cut,obj_param.run_sudo,obj_param.sudo)
				success,code = obj_add.view_quota(action,filesystem,user)
                                if success == True:
					if (code[5] == '0' and code[6] == '0'):
                                		success,code = obj_add.add_edit_quota(action,filesystem,user,soft,hard,
							obj_param.cat,obj_param.sed,obj_param.grep,obj_param.edquota,
							obj_param.getent,obj_param.cut,obj_param.run_sudo,obj_param.sudo)
						code_add=code
                                                # Check add
						success,code = obj_add.view_quota(action,filesystem,user)
                                                if success == True:
                                                        if (code[5] > '0' and code[6] > '0'):
								obj_log.loglogged(action,filesystem,user,code)
                                                                print code
                                                        else:
                                                                code=['False','Check: operation not executed']
								obj_log.loglogged(action,filesystem,user,code)
                                                                print code
                                                else:
							obj_log.loglogged(action,filesystem,user,code)
                                                     	print code
						# Check add
					else:
						code=['False','A quota has already been set for the user, use the --edit or --remove key to change']
						obj_log.loglogged(action,filesystem,user,code)
						print code
				else:
					obj_log.loglogged(action,filesystem,user,code)
					print code
                        elif action == "--edit":
                                obj_edit = quota.Quota(filesystem,user,soft,hard,obj_param.cat,
					obj_param.sed,obj_param.grep,obj_param.edquota,obj_param.getent,
					obj_param.cut,obj_param.run_sudo,obj_param.sudo)
				success,code = obj_edit.view_quota(action,filesystem,user)
				if success == True:
					old_soft,old_hard=code[5],code[6]
                                        if (code[5] != '0' and code[6] != '0'):
						success,code = obj_edit.add_edit_quota(action,filesystem,user,soft,hard,
							obj_param.cat,obj_param.sed,obj_param.grep,obj_param.edquota,
							obj_param.getent,obj_param.cut,obj_param.run_sudo,obj_param.sudo)
						code_edit=code
						# Check edit
                                                success,code = obj_edit.view_quota(action,filesystem,user)
                                                if success == True:
                                                        if (code[5] != old_soft or code[6] != old_hard):
								obj_log.loglogged(action,filesystem,user,code)
                                                                print code
                                                        else:
                                                                code=['False','Check: operation not executed']
								obj_log.loglogged(action,filesystem,user,code)
                                                                print code
                                                else:
							obj_log.loglogged(action,filesystem,user,code)
                                                        print code
                                                # Check edit
					else:
                                             	code=['False','User quota is 0 use the --add key']
						obj_log.loglogged(action,filesystem,user,code)
                                                print code
                                else:
					obj_log.loglogged(action,filesystem,user,code)
                                     	print code
			elif action == "--change":
				obj_change = quota.Quota(filesystem,user,soft,hard,obj_param.cat,
                                        obj_param.sed,obj_param.grep,obj_param.edquota,obj_param.getent,
                                        obj_param.cut,obj_param.run_sudo,obj_param.sudo)
                                success,code = obj_change.view_quota(action,filesystem,user)
				if success == True:
                                        old_soft,old_hard=code[5],code[6]
                                        success,code = obj_change.add_edit_quota(action,filesystem,user,soft,hard,
                                        	obj_param.cat,obj_param.sed,obj_param.grep,obj_param.edquota,
                                        	obj_param.getent,obj_param.cut,obj_param.run_sudo,obj_param.sudo)
                                       	code_change=code
                                        # Check change
                                        success,code = obj_change.view_quota(action,filesystem,user)
					#print code
                                       	if success == True:
                                        	if (code[5] != old_soft or code[6] != old_hard):
                                                	obj_log.loglogged(action,filesystem,user,code)
                                                	print code
                                        	else:
                                                	code=['False','Check: operation not executed']
                                                	obj_log.loglogged(action,filesystem,user,code)
                                                        print code
                                       	else:
                                        	obj_log.loglogged(action,filesystem,user,code)
                                       		print code
                                        # Check change
                                else:
                                     	obj_log.loglogged(action,filesystem,user,code)
                                        print code
	else:
		obj_log.loglogged('run','main','not','Not parameters run with the -h key for help')
		print 'Not parameters run with the -h key for help'

