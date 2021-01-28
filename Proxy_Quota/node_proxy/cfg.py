#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Configuration:
        def __init__(self):
                self.path = "/usr/src/ProxyQuota"
		self.ssh_host = ["ip_node1","ip_node2","ip_node3"]
		self.ssh_port = "22"
		self.ssh_user = "edquota"
		self.ssh_root = "root"
		self.command_worker = "./WorkerQuota/worker_quota"
		self.command_quotacheck = "/usr/bin/nohup /home/edquota/WorkerQuota/quotacheck"
		self.command_backup = "/usr/bin/nohup /home/edquota/WorkerQuota/backup"
		#Email alert
		self.host = "mail.domain.ru"
		self.user = "user"
		self.password = "pass"
		self.domain = "domain.ru"
		self.m_subject = "Profile quota exceeded"
		self.m_from = "quota@domain.ru"
		self.m_text = ["Your profile's current quota exceeds the warning value!",
				"Please delete the data to prevent blocking."]
		self.m_email = ['root']
		#Problem show ldap if email report
		self.sys_user = "40"
		self.retry_fail = "5"
