#!/usr/bin/env python

class Help():
	def __init__(self,key):
                self.name = "Help"
                self.key = key
		self.message = '========================================================================================== \n'+\
			'Application set,modify,remove block limits (soft hard) file systems. \n'+\
			'========================================================================================== \n'+\
			'1) Add new user quota \n'+\
			'Example syntax (size in kilobytes): scripts --add -f filesystem -u user -s soft -h hard \n'+\
			'scripts --add -f /home -u user -s 768 -h 1024 \n'+\
			"\n"+\
			'2) Edit user quota \n'+\
			'Example syntax (size in kilobytes): scripts --edit -f filesystem -u user -s soft -h hard \n'+\
                        'scripts --edit -f /home -u user -s 768 -h 1024 \n'+\
			"\n"+\
			'3) Remove user quota \n'+\
			'Example syntax (size in kilobytes): scripts --remove -f filesystem -u user \n'+\
                        'scripts --remove -f /home -u user \n'+\
			"\n"+\
			'4) Show user quota \n'+\
			'Example syntax: scripts --show -f filesystem -u user \n'+\
                        'scripts --show -f /home -u user \n'+\
			"\n"+\
			'5) Get user quota report \n'+\
			'Example syntax: scripts --all -r \n'+\
                        'scripts --all -r \n'+\
			"\n"+\
                        '6) Edit user quota no validate \n'+\
                        'Example syntax (size in kilobytes): scripts --change -f filesystem -u user -s soft -h hard \n'+\
                        'scripts --change -f /home -u user -s 768 -h 1024'

        def view_help(self):
                if self.key:
			print self.message
