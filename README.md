# PubFigDownload

## PubFig: Public Figures Face Database
1. The PubFig database is a large, real-world face dataset consisting of 58,797 images of 200 people collected from the internet
2. Due to copyright issues, we cannot distribute image files in any format to anyone. Instead, we have made available a list of image URLs where you can download the images yourself
3. HomePage: http://www.cs.columbia.edu/CAVE/databases/pubfig/

## 说明
1. 该脚本是一个简单的多线程程序，用来下载PubFig提供的图片
2. 下载失败的图片信息会放入文件 dev_failed_urls.txt、eval_failed_urls.txt

## 使用方法
1. 从PubFig[下载页面](http://www.cs.columbia.edu/CAVE/databases/pubfig/download/)下载图片url列表文件dev_urls.txt和eval_urls.txt
2. 执行 python pub_down-multi.py dev 或者 python pub_down-multi.py eval 即可下载对应类型数据集
3. 线程数量：默认下载线程数量为50个，可以打开pub_down-multi.py修改参数numConsumerThread

