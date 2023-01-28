#-*- coding: utf-8 -*-  
import filecmp
import difflib
import pprint
import os,sys
import chardet #pip install chardet
import logging
import csv
import time
import re
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


path1="C:\\Users\\admin\\Desktop\\compare\\ntyy\\main\\java\\com\\brs\\battery\\repair\\"
path2="C:\\Users\\admin\\Desktop\\compare\\source\\main\\java\\com\\yx\\battery\\guard\\"


holderlist = []
rightfilelist = []
leftfilelist = []

d = difflib.Differ()

def writecsvdata(line):
    with open(genfilename+".csv", 'a+', newline='') as csvfile:
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
def fetch_word(ipt):
    lst = []
    #   输入小写化
    s = ipt.lower()
    while len(s) > 0:
        #   提取头部的英文匹配
        match = re.match(r'[a-z]+', s)
        if match:
            word = match.group(0)
        else:
            #   若非英文单词，直接获取第一个字符
            word = s[0:1]
        lst.append(word)
        #   从文本中去掉提取的 word，并去除文本收尾的空格字符
        s = s.replace(word, '', 1).strip(' ')
    return lst

def cmpfile(leftfilelist,rightfilelist):
    
    for l in leftfilelist:
        lname=""
        rname=""
        lnametemp=os.path.basename(l)[4:]
        #lnametemp=fetch_word(os.path.basename(l))
        for r in rightfilelist:
            print(r)
            if(r.find(lnametemp)>0):
                lname=l
                rname=r
                print(lname,rname)
                break;
            else:
                continue
        if(rname==""):#右侧无相关匹配文件
            continue
        temp=l
        temp2=rname
        print(temp,temp2)
        logger.info("比对文件：%s   %s",temp,temp2)
        
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
            #print(text1)
            rel=list(d.compare(text1,text2))
            numcommon=GetCommonLine(rel)


            item1 = "%s,%s,%d,%d,%.2f,%s,%d,%d,%.2f" %(temp,temp2,numcommon,num1,numcommon/num1*100,temp2,numcommon,num2,numcommon/num2*100)
 
            writecsvdata(item1)
            logger.info("文件1：%s  文件2：%s 总行数:%d 相同行:%d 差异行：%d 相同率:%.4f",temp,temp2,num1,numcommon,num1-numcommon,numcommon/num1*100)
          
    


   



def compareme(dir1,dir2):  
    print(dir1,dir2)  
    diffsubdir=''
    index=dir1.index(path1)+len(path1)
    if(index>0):
        diffsubdir=dir1[index:]
        print(diffsubdir)

    dircomp = filecmp.dircmp(dir1,dir2)
    left_list = dircomp.left_list

    
    right_list = dircomp.right_list      
    diff_in_one = dircomp.diff_files   
    print(dircomp.common_files)


    dirpath = os.path.abspath(dir1)     
    if(len(diff_in_one)>0):
        for x in diff_in_one:
            if(len(diffsubdir)):
                holderlist.append(diffsubdir+"\\"+x)
            else:
                holderlist.append(x)
        #print(holderlist)  

    if(len(diff_in_one)==0):
        print(type(left_list))
        for l in left_list:
            leftfilename=dir1+l;
            print(leftfilename)
            if(os.path.isfile(leftfilename)):
                leftfilelist.append(leftfilename)
        for r in right_list:
            rightfilename=dir2+r;
            print(rightfilename)
            if(os.path.isfile(rightfilename)):
                rightfilelist.append(rightfilename)
        if(len(leftfilelist)>0):
            cmpfile(leftfilelist,rightfilelist)
        leftfilelist.clear()
        rightfilelist.clear()

    if len(dircomp.common_dirs) > 0:  #判断是否存在相同子目录，以便递归
            for item in dircomp.common_dirs:   #递归子目录
                compareme(os.path.abspath(os.path.join(dir1,item))+"\\",os.path.abspath(os.path.join(dir2,item))+"\\")
    return holderlist

compareme(path1,path2)
#holderlist.sort()



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
    






