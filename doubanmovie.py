import json
import requests,re
import csv
import time,random

def get_user_agent():
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36'
    ]
    return random.choice(user_agent_list)


headers={
    "User-Agent": get_user_agent()
}


def get_url(url):
    time.sleep(2)
    res = requests.get(url, headers=headers,timeout=3)
    json_data = json.loads(res.text)
    subjects = json_data['subjects']
    print(subjects)
    for i in subjects:
        urllist.append(i['url'])
    return urllist

def get_urlist(urllist):
    for url in urllist:
        time.sleep(random.uniform(5,10))
        r = requests.get(url=url, headers=headers)
        r.encoding='utf-8'
        name=re.findall('<span property="v:itemreviewed">(.*?)</span>',r.text)[0]
        year=re.findall('<span class="year">\((.*?)\)</span>',r.text)[0]
        genre=re.findall('<span property="v:genre">(.*?)</span>',r.text)
        country=re.findall('<span class="pl">制片国家/地区:</span> (.*?)<br/>',r.text)[0]
        runtime=re.findall('<span property="v:runtime" content=".*?">(.*?)分钟</span>',r.text)
        runtime=runtime[0] if runtime else "/"
        rate=re.findall('<strong class="ll rating_num" property="v:average">(.*?)</strong>',r.text)[0]
        votes=re.findall('<span property="v:votes">(.*?)</span>',r.text)[0]
        comments=re.findall('<a href=".*?comments\?status=P">全部 (.*?) 条</a>',r.text)[0]
        kanguo=re.findall('<a href=".*?comments\?status=P">(.*?)人看过</a>',r.text)[0]
        xiangkan=re.findall('<a href=".*?comments\?status=F">(.*?)人想看</a>',r.text)[0]
        print(name,year,"|".join(genre),country,runtime,rate,votes,comments,kanguo,xiangkan)
        list2.append([name,year,"|".join(genre),country,runtime,rate,votes,comments,kanguo,xiangkan])
    return list2

def get_list2(list2):
    with open('douban.csv','w',encoding="utf-8",newline="") as f:
        csv_writer=csv.writer(f)
        csv_writer.writerow(("电影名字","上映年份","类型","地区","时长","评分","评价人数","短评数","看过","想看"))
        csv_writer.writerows(list2)

if __name__ == '__main__':
    urls = ['https://movie.douban.com/j/search_subjects?type=movie&tag=豆瓣高分&sort=recommend&page_limit=20&page_start={}'.format(str(i)) for i in range(0,200,20)]
    urllist = []
    for url in urls:
        get_url(url)
    print(urllist)
    list2=[]
    a=get_urlist(urllist)
    print(a)
    get_list2(a)