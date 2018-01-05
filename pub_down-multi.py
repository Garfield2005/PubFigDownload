# -*- coding: utf-8 -*-  

# Author: mm.zhang
# Time: 2018-01-04 18:57
# ModifyTime: 2018-01-04 18:57
# File: pub_down-multi.py
# Description: PubFig图片数据集多线程下载：有下载失败的可以重新运行该程序，已经下载的会跳过

import os  
import re  
import time  
import urllib
import urllib.request
import queue
import time
import threading
import sys

data_type = 'eval' #数据类型: dev 或者 eval, 也用来作为图片的存储目录使用
eval_urls = 'eval_urls.txt' #待下载文件信息
failed_urls_file = data_type + '_' + 'failed_urls.txt'

numConsumerThread = 50 # 下载线程数量
numQueueSize = 1000 #待下载队列大小
unProcessUrlQueue = queue.Queue(numQueueSize)

mutex_numsuccess = threading.Lock()
mutex_numfailed = threading.Lock()
mutex_failed_urls = threading.Lock()

numall = 0
numsuccess = 0
numfailed = 0
# 生产者
def produce_thread():
    global numall
    global numsuccess
    global numfailed
    
    fid=open(eval_urls)
    lines=fid.readlines()  
    numall = len(lines)
    for line in lines:
        if line.startswith('#'):
          numall = numall - 1
          continue
        while unProcessUrlQueue.full():
          print("待处理URL队列已满,等待10秒钟")
          time.sleep(10)
        unProcessUrlQueue.put(line)
          
                      
# 消费者    
def consumer_thread():
    global numall
    global numsuccess
    global numfailed
    
    failed_urls = ''
    while True:
      if unProcessUrlQueue.empty():
        print("待处理队列已经处理完成,退出线程")
        
        mutex_failed_urls.acquire()
        file_object = open(failed_urls_file, 'w+')
        file_object.write(failed_urls)
        file_object.close()
        mutex_failed_urls.release()
        
        break
        #time.sleep(60)
        #continue
      image_info = unProcessUrlQueue.get()
      
      line_split=image_info.split('\t')  
      name=line_split[0]  
      imagenum=line_split[1]  
      image_url=line_split[2]  
      rect=line_split[3]  
      md5sum=line_split[4] 

      save_dir = data_type + '/' + name
      if False == os.path.exists(save_dir):
        try:
          os.makedirs(save_dir)
        except OSError:
          print("目录已存在:" + save_dir)
      imagepath = save_dir+'/'+imagenum+'.jpg'
      if os.path.exists(imagepath):
         print("文件已经存在(success=" + str(numsuccess) + ";fail=" + str(numfailed) + "/all=" + str(numall) + ": "+ imagepath) 
         mutex_numsuccess.acquire()
         numsuccess = numsuccess + 1
         mutex_numsuccess.release()
         continue
      try:
         req = urllib.request.Request(image_url)
         req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')
         fp = urllib.request.urlopen(req,timeout=2)
         data = fp.read()  
         fp.close()  
         file=open(imagepath,'w+b')  
         file.write(data)  
         mutex_numsuccess.acquire()
         numsuccess = numsuccess + 1
         mutex_numsuccess.release()
         print("下载成功(success=" + str(numsuccess) + ";fail=" + str(numfailed) + "/all=" + str(numall) + ": "+ image_url) 
         file.close()  
      except Exception:  
         mutex_numfailed.acquire()
         numfailed = numfailed + 1
         mutex_numfailed.release()
         failed_urls = failed_urls + image_info
         #unProcessUrlQueue.put(image_info)
         print("下载失败(success=" + str(numsuccess) + ";fail=" + str(numfailed) + "/all=" + str(numall) + ": "+ image_url) 
          
def run_controller():
    # 生产者线程
    produce_controller = threading.Thread(target=produce_thread)
    produce_controller.start()
    
    time.sleep(5) #等待5秒钟，以使得生产者产生部分数据
    # 消费者线程
    for i in range(0,numConsumerThread):
      consumer_controller = threading.Thread(target=consumer_thread)
      consumer_controller.start()
        
if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ('dev', 'eval'):
       print("参数错误: python pub_down-multi.py dev|eval")
       sys.exit(0)
    data_type = sys.argv[1]
    if 'dev' == data_type:
      eval_urls = 'dev_urls.txt' #待下载文件信息
    else:
      eval_urls = 'eval_urls.txt' #待下载文件信息
    failed_urls_file = data_type + '_' + 'failed_urls.txt'
    
    print("正在处理: " + data_type + "; " + eval_urls)
    run_controller()
