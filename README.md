# myspider
基于scrapy_redis的百科爬虫，包括百度百科和互动百科

运行环境  python3.6 <br> 

其他
见需求文件，requirements.txt   除了scrapy_redis的环境之外，还有一些机器学习的环境，可以使用conda进行安装和版本管理，方便快捷


默认没有开启redis的配置，并发量过大容易给网站造成严重的负荷，尽量控制下载延时。需要使用redis的朋友，请在setting.py中，讲注释的部分取消注释，同时在spider中更改继承的类；同时远端配置好redis即可。
