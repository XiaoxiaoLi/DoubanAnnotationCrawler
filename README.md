DoubanAnnotationGrabber 豆瓣读书笔记备份导出下载脚本
==================
利用Scrapy 导出用户全部读书笔记到一个xml文件中。

### [心得笔记ThoughtProcess](https://cindyxiaoxiaoli.wordpress.com/2018/08/30/%E8%B1%86%E7%93%A3%E8%AF%BB%E4%B9%A6%E7%AC%94%E8%AE%B0%E4%B8%8B%E8%BD%BD%E5%A4%87%E4%BB%BD%E8%84%9A%E6%9C%AC/)

### To install required packages

`pip install -r requirements.txt`

### To run the script
`scrapy crawl annotation -a username=<douban_username>`

#### To change the output file path

Find your username http://www.douban.com/people/<username>/

By default it outputs to `annotations.xml` in the same folder. The `FEED_URI` can be changed in `settings.py` or by specifying it in the command when running the script.

`scrapy crawl annotation -a username=<douban_username> -o <output_filepath>`

### Known Issues
- 经导出后豆瓣读书笔记的<原文开始>tag变为`&gt; `。就先这么看吧还凑合。
- 开头有个parsing exception，没具体看谁造成的回头再修吧。
