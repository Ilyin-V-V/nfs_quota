#!/usr/bin/env python
from datetime import datetime
import cfg

class Logger():
        def __init__(self):
                self.name = "Logger"
		self.date = datetime.strftime(datetime.now(), "%d:%m:%Y-%H:%M:%S")

	def loglogged(self,action,filesystem,user,code):
		obj_log = cfg.Configuration()
		file_path = obj_log.path+"/log.log"
		file = open(file_path, 'a')
		data = self.date+" "+user+" "+action+" "+filesystem+" "+str(code)
		file.write(data +"\n")
		file.close()
