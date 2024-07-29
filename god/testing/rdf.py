
file_path = 'god/testing/txt.c'

c_file = open(file_path,'r+')
c_content = c_file.read()
goal_content = '# if (NEXT_MACG1):\n#  include "god/testing/txt.c"\n# else\n'
if goal_content in c_content:
    index = c_content.find('# if (NEXT_MACG1):\n#  include "god/testing/txt.c"\n# else\n')
    new_content = c_content[:index] +'//# if (NEXT_MACG1):\n#  include "god/testing/txt.c"\n//# else\n' + c_content[len(goal_content)+index:]

    c_file.seek(0)
    c_file.write(new_content)      
else:
    print('goal_content inexistence')  
c_file.close()


