from subprocess import call
import time
import os.path

include_hpp_list=[]
include_list_1=[]
include_cpp_list=['Examples/Bonds/Bonds.cpp']
s3="Include dependency graph"
s4='<table class="memberdecls">'
s1 = 'File Reference'

def hasSlash(name):
	return '/' in name

def findInSubdirectory(filename, subdirectory=''):
	if subdirectory:
		path = subdirectory
	else:
		path = os.getcwd()
	for root, dirs, names in os.walk(path):
		if 'test-suite' not in root:
			if filename in names:
				return os.path.join(root, filename)
	return 'Filenotfound' + filename

def getHppIncludeNames(text):
	include_list=[]
	b=text[text.find(s3):text.find(s4)]
	parts=b.split('href="')
	j=len(parts)
	for i in range (1,j):
		header=parts[i].split('"')[0].split('.html')[0]
		header = header.replace("_2","/")
		header = header.replace("_8",".")
		if header not in include_list_1 and 'all' not in header:
			include_list.append(header)
			include_list_1.append(header)
			getIncludesForCppFile(header)
	c=text[text.find(s1):text.find(s3)]
	parts=c.split('href="')
	j=len(parts)
	for i in range (1,j):
		header=parts[i].split('"')[0].split('.html')[0]
		header = header.replace("_2","/")
		header = header.replace("_8",".")
		header = header.replace("_source","")
		if header not in include_list_1 and 'all' not in header:
			include_list.append(header)
			include_list_1.append(header)
			getIncludesForCppFile(header)
	return include_list

def getPartialHppPath(include_list):
	include_list_temp=[]
	for name in include_list:		
		if not hasSlash(name):
			subdir = '/home/aashaka/Documents/original/QuantLib-1.9/'
			doc_pathname=findInSubdirectory(name,subdir)
			partial_name = doc_pathname[doc_pathname.find(subdir)+len(subdir):]
			include_list_temp.append(partial_name)
	return include_list_temp

def existsCppFile(name):
	subdir = '/home/aashaka/Documents/original/QuantLib-1.9/'
	name = name[:-4] + '.cpp'
	path = subdir+name
	return os.path.isfile(path)

def addCorresCppFiles(name):
	if existsCppFile(name):
		name = name[:-4] + '.cpp'
		include_cpp_list.append(name)

def addToGlobalHppList(to_add_list):
	for name in to_add_list:
		if name not in include_hpp_list:
			print 'FILE IS HERE' + name
			include_hpp_list.append(name)
			addCorresCppFiles(name)
			
def getIncludesForCppFile(file):
	print 'FILE IS' + file
	file = file.replace(".","_8").split('/')
	file = file[len(file)-1]
	url = '/home/aashaka/doxygen/html/' + file + '.html'
	with open(url) as f:
		b=f.read()
		include_list=getHppIncludeNames(b)
		include_list=getPartialHppPath(include_list)
		addToGlobalHppList(include_list)

def doCopy(file):
	main_name = "/home/aashaka/Documents/original/QuantLib-1.9/" + file
	dest_name="/home/aashaka/QuantLib-1.9/" + file
	print "doing cp " + main_name + ' ' + dest_name
	call(["cp",main_name,dest_name])

def getDeps():
	for cpp_file in include_cpp_list:
		with open('./cpp_includes_log','a') as cpp_out:
			cpp_out.write(cpp_file + '\n')
		doCopy(cpp_file)
		getIncludesForCppFile(cpp_file)

	for hpp_file in include_hpp_list:
		with open('./hpp_includes_log','a') as hpp_out:
			hpp_out.write(hpp_file + '\n')
		doCopy(hpp_file)

if __name__=="__main__":
   getDeps()

