#!/usr/bin/env python

class Configuration:
        def __init__(self):
                self.path = "/home/edquota/WorkerQuota"
		self.path_sh = "/home/edquota"
		self.filesystem = ['data-lv_data']
		self.edquota = "/usr/sbin/edquota -u"
		self.cat = "/usr/bin/cat"
		self.sed = "/usr/bin/sed -i \'s/"
		self.grep = "/usr/bin/grep"
		self.getent = "/usr/bin/getent passwd"
		self.cut = "/usr/bin/cut"
		self.run_sudo = "True"
		self.sudo = "/usr/bin/sudo -E"
