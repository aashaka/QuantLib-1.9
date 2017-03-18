from subprocess import call
import time
import os.path

s1 = "fatal error: "
s2 = "No rule to make target '"
s3 = "recipe for target 'all-recursive' failed"
call(["rm","make_output_error"])
call(["rm","make_output_main"])

def existsFile(file):
	return os.path.isfile(file)

num=10 # Number of times to run make
while num:
	call(["make 2> make_output_error"], shell=True);
	has_fatal_error=False
	with open('./make_output_error','r') as f:
		b = f.read()
		print "OUTPUT IS: ", b
		fatal_error_in_line = b.find(s1)
		no_rule_target = b.find(s2)
		if fatal_error_in_line != -1:
			print "THE ERROR IS ", fatal_error_in_line
			has_fatal_error=True
			file_included_includes=b[fatal_error_in_line + len(s1):]
			file_included=file_included_includes.split(' ')[0]
			file_included=file_included[:-1]
		elif no_rule_target != -1:
			print "THE ERROR IS NO RULE TO MAKE TARGET"
			has_no_rule=True
			call(["make > make_output_main"], shell=True);
			with open('./make_output_main','r') as mom:
				c=mom.read()
				temp = c.split(s3)[0].split('Entering directory \'')
				dir_path=temp[len(temp)-1].split('\'')[0]
				print "DIRECTORY IS: " + dir_path
			file_included=b[no_rule_target+len(s2):].split(',')[0]
			file_included=file_included[:-1]
			print "FILE TO BE INCLUDED: " + file_included
			file_path=dir_path+'/'+file_included
			#call(["touch",file_path])
	if has_fatal_error:
		with open('./script_log','a') as out:
			file='/home/aashaka/QuantLib-1.9/' + file_included
			source_file='/home/aashaka/Documents/original/QuantLib-1.9/' + file_included
			to_write = 'cp ' + file + '\n'
			out.write(to_write)
		if '.hpp' in file_included:
			print file + " is being included"
			call(["cp",source_file,file])
			cpp_file = file_included[:-4] + '.cpp'
			cpp_dest_file='/home/aashaka/QuantLib-1.9/' + cpp_file
			cpp_source_file='/home/aashaka/Documents/original/QuantLib-1.9/' + cpp_file
			if existsFile(cpp_source_file):
				call(["cp",cpp_source_file,cpp_dest_file])
		else:
			print "No .hpp file. Check script_log for last file which was there"
	elif not has_no_rule:
		print "fatal error or no rule string not found in make output. See the make_output to see what the error is"
		break
	num=num-1;
f.close()