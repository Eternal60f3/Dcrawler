主要文件是两个：

main_hand_download.py

- 点击https://www.zhipin.com/web/geek/jobs?query=&city=100010000&position=100102
  自行登录，把左边职业信息栏，滑到最底部，然后crtl + s保存为info.html文件
- 能做到一次稳定爬取300条数据，耗时40分钟左右(具体时间待测试)，程序结束


main_online.py

- 直接运行即可，能够一直爬，大概一个小时后会出现，boss反爬标志，此时自行ctrl+c终止程序
- 一次大概200-300条数据，具体数量不稳定


如下载使用，需要进行的操作：

- 修改database.py中的数据库信息
- 下载[chromedriver](https://blog.csdn.net/yuxuan6699/article/details/134644038)
