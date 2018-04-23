# 基于flask+requests个人博客系统

## 1.基本环境搭建

```python
    1.本人使用的系统是 Centos7
    2.flask环境系统部署
        2.1 安装python3.6
        2.2 安装pip工具
        2.3 pip install -r requirements.txt # 根据文件进行包安装
    3.安装mysql数据库 使用的是mysql 5.7 charset=utf8
    4.建立相关数据库及表
```

## 2.安装教程(推荐安装环境：Centos7)

    1.git clone https://github.com/longzx-9527/flask_spider.git
    2.cd flask_spider
    3.pip install -r  requirement.txt # 安装依赖

以上，应该安装好了python依赖包。
接下来是初始化数据：
    1.首先你应该创建了一个mysql数据库（utf-8格式）,然后修改config.py里面的user、passwd、db
    2.执行blog.sql创建相关表
    3.初始化数据库：python manage.py db init
    4.生成数据库语句：python manage.py db migrate
    5.创建数据库：python manage.py upgrade

运行：`./start.sh`

## 2.个人博客首页

### 2.1 首页界面

![首页](https://images2018.cnblogs.com/blog/1339195/201804/1339195-20180421191246312-1031301812.png)

![首页](https://images2018.cnblogs.com/blog/1339195/201804/1339195-20180421191428100-352502656.png)

### 2.2 可以发布一些自己写的文章

![写文章](https://images2018.cnblogs.com/blog/1339195/201804/1339195-20180420101341637-1481677605.png)

### 2.3 文章显示

![文章显示](https://images2018.cnblogs.com/blog/1339195/201804/1339195-20180421191528180-222376656.png)

### 2.4 文章管理

![文章显示](https://images2018.cnblogs.com/blog/1339195/201804/1339195-20180421191718709-1351293168.png)

## 3.小说爬取展示

### 最终实现效果如下图：

#### 首页显示

![首页显示](https://images2018.cnblogs.com/blog/1339195/201804/1339195-20180418232426530-100667854.png)

可以输入查询小说，如果小说不存在，就调用后台爬虫程序下载

![章节列表](https://images2018.cnblogs.com/blog/1339195/201804/1339195-20180418232908530-1212209202.png)

点开具体页面显示，小说章节列表，对于每个章节，如果本地没有就直接下载，可以点开具体章节开心的阅读，而没有广告，是的没有广告，纯净的

![章节内容](https://images2018.cnblogs.com/blog/1339195/201804/1339195-20180418233105974-334389035.png)
