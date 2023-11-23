#-*- coding: utf-8 -*-  
import filecmp
import difflib
import pprint
import os,sys
import chardet #pip install chardet
import logging
import csv
import time

import fnmatch  
seconds = time.time()

genfilename=time.strftime("result_%Y-%m-%d_%H_%M_%S", time.localtime(seconds))

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler(genfilename+".log")
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
 
console = logging.StreamHandler()
console.setLevel(logging.INFO)
 
logger.addHandler(handler)
logger.addHandler(console)

#path1 检材  path2 样本
path1="C:\\Users\\Administrator\\Desktop\\比对\\222\\unpackerdex\\sources\\"
path2="C:\\Users\\Administrator\\Desktop\\比对\\222\\996_240\\app\\src\\main\\java\\"

#表头
header = ['检材一', '相同行', '总行数', '相同行比例' ,'样本', '相同行', '总行数', '相同行比例'] 
isheader=False
def count_java_files(directory):  
    java_files = []  
    for root, dirs, files in os.walk(directory):  
        for file in fnmatch.filter(files, '*.java'):  
            java_files.append(os.path.join(root, file))  
    return len(java_files)  

def writecsvdata(line,isHead):
    with open(genfilename+".csv", 'a+', newline='') as csvfile:
        spamriter = csv.writer(csvfile, dialect='excel')
        if(isHead==False):
            spamriter.writerow(header)
            isHead=True
        line_list = line.strip('\n').split(',') 
        spamriter.writerow(line_list)
    csvfile.close()
def GetCommonLine(rel):
    numcommon=0
    for str in rel:
        #print (str[0])
        if(str[0]=="-"):
            print (str[0])
        elif(str[0]==" "):
            numcommon=numcommon+1
    return numcommon

def GetNum(filepath):
    count = 0
    thefile = open(filepath,'rb')
    while True:
        buffer = thefile.read(1024 * 8192)
        if not buffer:
            break
        #print(type(buffer.count(b'\n')))
        count+=buffer.count(b'\n')
    thefile.close()
    #print (count)
    return count


holderlist = []

def compareme(dir1,dir2):  
    print(dir1,dir2)  
    diffsubdir=''
    index=dir1.index(path1)+len(path1)
    if(index>0):
        diffsubdir=dir1[index:]
        print(diffsubdir)

    dircomp = filecmp.dircmp(dir1,dir2)
    only_in_one = dircomp.left_only      
    diff_in_one = dircomp.diff_files   

    dirpath = os.path.abspath(dir1)     
    if(len(diff_in_one)>0):
        for x in diff_in_one:
            if(len(diffsubdir)):
                holderlist.append(diffsubdir+"\\"+x)
            else:
                holderlist.append(x)
        #print(holderlist)  
    if len(dircomp.common_dirs) > 0:  #判断是否存在相同子目录，以便递归
            for item in dircomp.common_dirs:   #递归子目录
                compareme(os.path.abspath(os.path.join(dir1,item)),os.path.abspath(os.path.join(dir2,item)))
    return holderlist


#------------------------------------------------------开始执行代码
num_java_files_file1 = count_java_files(path1)  
num_java_files_file2 = count_java_files(path2)  
  
#print(f'在文件 {path1} 中有 {num_java_files_file1} 个以.java为后缀的文件')  
#print(f'在文件 {path2} 中有 {num_java_files_file2} 个以.java为后缀的文件')
logger.info('在文件%s 中有 %d 个以.java为后缀的文件',path1,num_java_files_file1)
logger.info('在文件%s 中有 %d 个以.java为后缀的文件',path2,num_java_files_file2)

compareme(path1,path2)
#holderlist.sort()
d = difflib.Differ()


#print(holderlist)
commfilelen=len(holderlist)
if(num_java_files_file1>commfilelen):
    logger.info("两个文件夹 一共有%d个文件 检材一差异文件 %d个",commfilelen,num_java_files_file1-commfilelen)
else:
    logger.info("两个文件夹 一共有%d个文件 样本差异文件%d个",commfilelen,num_java_files_file2-commfilelen)

#统计
greater_than_70 = 0  
greater_than_80 = 0  
greater_than_90 = 0  
greater_than2_70 = 0  
greater_than2_80 = 0  
greater_than2_90 = 0 


current=0
for name in holderlist:
    current+=1
    temp=path1+name
    temp2=path2+name
    print(temp,temp2)
    if (os.path.exists(temp)==False):   
        logger.info("文件1%s不存在",temp)
    if (os.path.exists(temp2)==False):  
        logger.info("文件2%s不存在",temp2)
    logger.info("当前序号:%d 比对文件：%s   %s",current,temp,temp2)
    '''
    num1=GetNum(temp)
    num2=GetNum(temp2)
    pprint.pprint("--------------------")
    pprint.pprint(num1)
    pprint.pprint(num2)
    '''
    fra=open(temp, 'rb')
    cur_encoding1 = chardet.detect(fra.read())['encoding']
    print(cur_encoding1)
    frb=open(temp2, 'rb')
    cur_encoding2 = chardet.detect(frb.read())['encoding']
    print(cur_encoding2)
    isread=False
    try:
        f1= open(temp, 'r', encoding=cur_encoding1) 
        text1 = f1.readlines()
        num1=len(text1)
        isread=True
    except :
        print('文件首次错误')
        logger.error("转换再次尝试")
        try:
            f1= open (temp, 'r', encoding='utf-8') 
            text1 = f1.readlines()
            num1=len(text1)
            isread=True
        except : 
              print('文件错误')
              logger.error("文件1读取错误") 
    finally:
        f1.close()

    try:
       f2= open(temp2, 'r', encoding=cur_encoding2)
       text2 = f2.readlines()
       num2=len(text2)
    except:
        print('文件2首次错误')
        logger.error("转换再次尝试")
        try:
            f2= open (temp2, 'r', encoding='utf-8') 
            text2 = f2.readlines()
            num2=len(text2)
        except : 
              print('文件错误')
              logger.error("文件2读取错误") 
    finally:
        f2.close()
    
    if isread==True:
        rel=list(d.compare(text1,text2))
        numcommon=GetCommonLine(rel)
        #print("文件1 相同行：",numcommon)
        #print("文件1 总行：",num1)
        #print("文件1 相同率：",numcommon/num1)
        #print("文件2 相同行：",numcommon)
        #print("文件2 总行：",num2)
        #print("文件2 相同率：",numcommon/num2)
        #保留2位小数，四舍五入
        result1=round(numcommon/num1*100,2)
        result2=round(numcommon/num2*100,2)
        item1 = "%s,%d,%d,%.2f,%s,%d,%d,%.2f" %(temp,numcommon,num1,result1,temp2,numcommon,num2,result2)
 
        writecsvdata(item1,isheader)
        isheader=True


        if(result1>=70.0):
            greater_than_70 += 1  
        if(result1>=80.0):
            greater_than_80 += 1 
        if(result1>=90.0):
            greater_than_90 += 1 
        if(result2>=70.0):
            greater_than2_70 += 1  
        if(result2>=80.0):
            greater_than2_80 += 1 
        if(result2>=90.0):
            greater_than2_90 += 1 
        
    logger.info("文件1：%s  总行数:%d 相同行:%d 差异行：%d 相同行比例:%.2f",temp,num1,numcommon,num1-numcommon,result1)
    logger.info("文件2：%s  总行数:%d 相同行:%d 差异行：%d 相同行比例:%.2f",temp2,num2,numcommon,num2-numcommon,result2)
        
logger.info("检材 大于且等于70个数:%d 占总文件比:%.2f",greater_than_70,greater_than_70/num_java_files_file1*100)
logger.info("检材 大于且等于80个数:%d 占总文件比:%.2f",greater_than_80,greater_than_80/num_java_files_file1*100)
logger.info("检材 大于且等于90个数:%d 占总文件比:%.2f",greater_than_90,greater_than_90/num_java_files_file1*100)
       
logger.info("样本 大于且等于70个数:%d 占总文件比:%.2f",greater_than2_70,greater_than2_70/num_java_files_file2*100)
logger.info("样本 大于且等于80个数:%d 占总文件比:%.2f",greater_than2_80,greater_than2_80/num_java_files_file2*100)
logger.info("样本 大于且等于90个数:%d 占总文件比:%.2f",greater_than2_90,greater_than2_90/num_java_files_file2*100)
       
     

    






