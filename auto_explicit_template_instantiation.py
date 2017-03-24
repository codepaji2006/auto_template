#Distributed under GPLv3.0 license.
#Author: codepaji2006@github
#Repo: https://github.com/codepaji2006
#You may copy and distribute verbatim copies of the Program's source code as you
#receive it, in any medium, provided that you conspicuously and appropriately publish 
#on each copy an appropriate copyright notice and disclaimer of warranty; keep intact all
#the notices that refer to this License and to the absence of any warranty; and give any other recipients
#of the Program a copy of this License along with the Program.
#you must preserve the author and Repo notice when distributing or using this code.
#Disclaimer:Absolutely no warranty and your use is at your own risk.

import os


def list_all_matched_pattern_files(directory, fileExtList):
	fileList = []
	nfileList= []
	#for f in os.listdir(directory):
	#	fileList.append(os.path.normcase(f))

	for root, dirs, files in os.walk(".", topdown=False):
		for name in files:
			fileList.append(os.path.join(root, name))
	for f in fileList:
		if f.endswith(fileExtList):
			nfileList.append(f)
	return nfileList

def remove_non_class_def(files):
	nf=[]
	class_names=[]
	_unc=[]
	for f in files:
		if os.path.split(f)[1].startswith("class_") and os.path.split(f)[1].find("_def")<0:
			classn=f.split("_")[1].split(".")[0]
			#print("name=%s"%(classn))
			if classn not in _unc:
				_unc.append(classn)
			if class_names.count(classn)<2:
					class_names.append(classn)
					nf.append(f)
	for c in _unc:
		class_names.remove(c)
	#print("Detected classes:%s"%(class_names))
	return [nf,class_names]

def find_pattern_in_file(fname,pattern):
	bfound=False
	type_list=[]
	n=0
	with open(fname,"r") as f:
		b=f.readlines()
		for s in b:
			bfound==False
			if s.find(pattern)>=0 and s.find("template class ")<0:
			  start_pat = s.find("<",s.find(pattern))
			  end_pat = s.find(">",start_pat)
			  s_type = s[start_pat+1:end_pat]
			  if "class " not in s_type:
				#print(s_type)
				type_list.append(s_type)
				bfound=True
				n=n+1
	if n>0:
		bfound=True
	else:
		bfound=False
	return [bfound,type_list,fname]

def find_usage_of_this_class(classname,excFiles):
	all_files = list_all_matched_pattern_files(".",".cpp")
	pattern = "%s<"%(classname)
	f_list=[]

	all_used_files= [f for f in all_files if f not in excFiles]
	d=dict()
	for f in all_used_files:
		[bfound,type_list,f]=find_pattern_in_file(f,pattern)
		if bfound==True:
			d[f]=type_list
			f_list.append(f)
	#print(all_used_files)
	#print(d)

	return [d,f_list]


def create_auto_def_files(f_list,d_list):
	return

def create_def_file(fname,content):
	with open(fname,"w") as ff:
		ff.write(content)
	return

h_files=list_all_matched_pattern_files(".",".h")
cpp_files=list_all_matched_pattern_files(".",".cpp")
#print("h_files:{0}\ncpp_files:{1}".format(h_files,cpp_files))
[final_files,classes] = remove_non_class_def(h_files+cpp_files)
print("Definition files:%s"%(final_files))

root_dir_class = dict()
for x in classes:

	for f in final_files:
		patt = "class_%s."%(x)
		if patt in f:
			root_dir_class[x]=os.path.split(f)[0]
			break

	[d,f]=find_usage_of_this_class(x,final_files)
	print("for class:%s {"%(x))
	print("		defined in directory:%s\n"%(root_dir_class[x]))
	print("		referred in files:%s\n"%(f))
	print("		instances:%s\n}"%(d))
	for ff in f:
		def_name = "%s/class_%s_def.cpp"%(root_dir_class[x],x)
		print("def file name:%s" %(def_name))
		inc_directive = "#include \"class_%s.cpp\""%(x)
		print(inc_directive)
		str=""
		for g in d[ff]:
			str = str + "template class %s<%s>;\n"%(x,g)
			print(str)

		f_content = "%s\n%s"%(inc_directive,str)
		create_def_file(def_name,f_content)

