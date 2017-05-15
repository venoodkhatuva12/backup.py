#!/usr/bin/python
#Author: Vinod.N K
#Distro : Linux -Centos, Rhel, and any fedora
import os

###Changes made from here

from datetime import date, timedelta
date = date.today()
day1 = date.strftime('%d-%m-%Y')
date = date.today() - timedelta(1)
day2 = date.strftime('%d-%m-%Y')
date = date.today() - timedelta(2)
day3 = date.strftime('%d-%m-%Y')
date = date.today() - timedelta(3)
day4 = date.strftime('%d-%m-%Y')
date = date.today() - timedelta(4)
day5 = date.strftime('%d-%m-%Y')

def check_mysql_backup(command):
	print "\n\n#############\nInside check_mysql_backup function\n\n#############\n"
	os.system("%s" %command)
	print command
	f = open('/tmp/root_objects','r')
	backup_file_list = []
       for line in f:
               check = line.find(".gz")
		if(check > 0) :
			line_list = line.split()
			backup_file_list.append("%s"%line_list[3])
               else:
			print "in else"
			print line
	prefix_current = ""
	prefix_previous = ""
	prefix_list = []

	for lista in backup_file_list:
		prefix_current = lista[0:(len(lista) - 13)]
		if(prefix_current != prefix_previous):
			prefix_list.append(prefix_current)
			prefix_previous = prefix_current

	list_to_be_present=[]
	for prefix in prefix_list:
		list_to_be_present.append("%s%s.gz"%(prefix,day1))
		list_to_be_present.append("%s%s.gz"%(prefix,day2))
		list_to_be_present.append("%s%s.gz"%(prefix,day3))
		list_to_be_present.append("%s%s.gz"%(prefix,day4))
		list_to_be_present.append("%s%s.gz"%(prefix,day5))

	f1 = open('/tmp/test_backup.txt','a')
	backup_not_present=set(list_to_be_present) - set(backup_file_list)
	backup_not_present=list(backup_not_present)
	if(len(backup_not_present) != 0):
               f1.write("\n\n################################\n#############################\n")
               f1.write("\n\nBackup for last five days NOT  present for %s\n\n"%command)
               f1.write("###############################\n#############################\n")
		for backup_np in backup_not_present:
			f1.write(backup_np)
			f1.write("\n")
	else:
		f1.write("################################\n#############################\n")
		f1.write("Backup for last five days present for %s\n"%command)
		f1.write("###############################\n#############################\n")
	f1.flush()
	f1.close()
	f.close()

####Changes made uptill here


def find_leaf(lastpart):
	print "lastpart is %s" %lastpart

	if((lastpart == "Scripts/") or (lastpart == "dir-logo/") or (lastpart == "svn_month/") or (lastpart == "svn/") or (lastpart == "git/") or (lastpart == "Jira/") or (lastpart == "Upload/") or (lastpart == "new folder/")):
		print "skiping path s3://dir_backup/%s" %lastpart
		return

	command = "sudo s3cmd ls s3://dir_backup/%s > /tmp/root_objects" %lastpart
	print command
	func_end = 0
	all_objects = os.system("%s" %command)
	child_objects = []
	f = open('/tmp/root_objects','r')
	for line in f:
		check = line.find(".gz")
		if(check < 0) :
			line_list = line.split('/')
			child_objects.append(line_list[-2])
		else:	
			if(lastpart.endswith("mysql/")):
				print"checking mysql backup for %s"%command
				check_mysql_backup(command)
				print "done checkig mysql backup for %s"%command
				return
			return	
	if(len(child_objects) == 0):
		print "No backup found in s3://dir_backup/%s" %lastpart
		return
	elif(len(child_objects) == 1):
		if (lastpart.endswith("%s/"%child_objects[0])):
			print "No backup found in s3://dir_backup/%s"%lastpart
			return
	print child_objects
	f.close
	for last in child_objects:
		newpath = "%s%s/"%(lastpart,last)
		find_leaf(newpath)
find_leaf("")
