# 如何使用爬虫分析 Python 岗位招聘情况

#### Life is short, you need Python。

Python 是一门很优雅的编程语言，用着很舒服。闲来学学。但是病不清楚现在的市场需要pythoner具备什么样的能力，
公司需要什么样的人才，市场对相应人才的需求量怎么样？

所以呢，就想爬去网站上的招聘信息看看

### 开发环境

安装selenium

    sudo pip install selenium

selenium2.x 调用高版本浏览器会出现不兼容问题，调用低版本浏览器正常
selenium3.x 调用浏览器必须下载一个类似不定的文件，比如firefox的geckodriver，chrome的chromedriver
各个浏览器的补丁[下载地址:](http://www.seleniumhq.org/download/)

安装 BeautifulSoup

    sudo pip install BeautifulSoup

安装 jieba 中文分词库

    全自动安装：
    easy_install jieba 或者pip install jieba / pip3 install jieba
    半自动安装：
    先下载 http://pypi.python.org/pypi/jieba/ ，解压后运行 python setup.py install
    手动安装：将 jieba 目录放置于当前目录或者 site-packages 目录
    通过 import jieba 来引用

