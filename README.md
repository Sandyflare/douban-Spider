# douban-Spider
豆瓣爬虫爬取设计 运用正则表达式


# -豆瓣反爬虫机制
1、在没有携带 cookie 的情况下，如果某个 IP 短时间高并发请求网站，该 IP 会立马被封。当 IP 被封，登录豆瓣网站会解封。

2、在携带 cookie 的情况下，某个 IP 请求网站过于频繁。豆瓣的反爬虫机制变为只封 cookie 不封 IP。也就说退出登录或者换个账号还能继续访问网站。

有两种解决思路：第一种可以增加等待时间降低并发数，但是这样就会导致爬取效率降低；第二种就是使用代理IP轮换进行爬取，这样既不影响效率也不会导致IP被封。

可以看出，豆瓣是一个十分体谅爬虫新手的网站。人家主人都那么人性化了，客人就要适可而止。我们只要在代码中登录账号，同时降低并发数，再随机延迟等待一段时间。我们的爬虫程序就不会被封杀了。


# -API分析
# (1)电影分类API
接口：https://movie.douban.com/j/search_tags

返回豆瓣电影的所有分类，JSON格式

{"tags":["热门","最新","经典","可播放","豆瓣高分","冷门佳片","华语","欧美","韩国","日本","动作","喜剧","爱情","科幻","悬疑","恐怖","文艺"]}

# (2)获取各分类电影的ID名称图片等信息

接口：https://movie.douban.com/j/search_subjects?type=movie请求参数：
![image](https://user-images.githubusercontent.com/78190034/123568021-058d3900-d7f6-11eb-9d5e-73d2f0b2d1a6.png)

请求示例：

获取豆瓣高分电影分类按热度排序20部电影

https://movie.douban.com/j/search_subjects?type=movie&tag=豆瓣高分&sort=recommend&page_limit=20&page_start=0
# (3)获取每部电影详情
抓包未发现返回数据的接口，网页源码发现了JSON数据，可以使用正则匹配的方式获取

地址：https://movie.douban.com/subject/{电影id}

正则：application/ld\+json">([\s\S]*?)</script

