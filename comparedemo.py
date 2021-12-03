import filecmp
import difflib
import pprint
import os,sys
import chardet
import logging
import csv
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("result4.log")
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
 
console = logging.StreamHandler()
console.setLevel(logging.INFO)
 
logger.addHandler(handler)
logger.addHandler(console)


path1="D:\\1\\V3.8-2021-01\\"
path2="D:\\4\\20210129\\"

def writecsvdata(line):
    with open('result4.csv', 'a+', newline='') as csvfile:
        spamriter = csv.writer(csvfile, dialect='excel')
        line_list = line.strip('\n').split(',') 
        spamriter.writerow(line_list)
    csvfile.close()
def GetCommonLine(rel):
    numcommon=0
    for str in rel:
        print (str[0])
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
    print (count)
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
        print(holderlist)
        if len(dircomp.common_dirs) > 0:  #判断是否存在相同子目录，以便递归
            for item in dircomp.common_dirs:   #递归子目录
                compareme(os.path.abspath(os.path.join(dir1,item)),os.path.abspath(os.path.join(dir2,item)))
        return holderlist

compareme(path1,path2)
#holderlist.sort()
d = difflib.Differ()


#print(holderlist)

logger.info("两个文件夹 一共有%d个不同文件",len(holderlist))
current=0
for name in holderlist:
    current+=1
    temp=path1+name
    temp2=path2+name
    print(temp,temp2)
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
        print('文件错误')
        logger.error("文件1读取错误")
    finally:
        f1.close()

    try:
       f2= open(temp2, 'r', encoding=cur_encoding2)
       text2 = f2.readlines()
       num2=len(text2)
    except:
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
   
        item1 = "%s,%d,%d,%.2f,%s,%d,%d,%.2f" %(temp,numcommon,num1,numcommon/num1*100,temp2,numcommon,num2,numcommon/num2*100)
 
        writecsvdata(item1)
        logger.info("文件1：%s  总行数:%d 相同行:%d 差异行：%d 相同率:%.4f",temp,num1,numcommon,num1-numcommon,numcommon/num1*100)
        logger.info("文件2：%s  总行数:%d 相同行:%d 差异行：%d 相同率:%.4f",temp2,num2,numcommon,num2-numcommon,numcommon/num2*100)
    






