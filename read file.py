fs = open(r"file",'r')  
#con2 = fs.read(4)  
#con1 = fs.read(10)  
con = fs.read()  
print(con)  
fs.close() 
welcome to new file
--------------
import os
current_path = os.getcwd()
print("The current working directory is as follows:")
print(current_path)

relative_path = "AnotherDirectory\\SubDirectory"
new_path = os.path.join(os.getcwd(),relative_path)
print("The new path is as follows:")
print(new_path)
-----------------------
file_object = open(r'file', 'r')
for current_line in file_object:
print(current_line, end='')
file_object.close()
