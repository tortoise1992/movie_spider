# -*- coding: UTF-8 -*-  
import requests
import pymysql
from pyquery import PyQuery as pq
# from concurrent.futures import ThreadPoolExecutor
# 多线程爬取下载资源
# threadPool=ThreadPoolExecutor(max_workers=5)
conn =pymysql.connect(host='127.0.0.1',user='root',password='zss131313',db='movie',port=3306,charset="utf8")
cur = conn.cursor()
headers={
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
}
host='http://www.15yc.com'
baseUrl='http://www.15yc.com/type/1/%d.html'
def get_page(url):
    try:
        response=requests.get(url,headers=headers)
        response.encoding = 'utf-8'
        return pq(response.text)
    except:
        print('呀，竟然无法解析...')

#         threadPool.submit(download_page,url+item.attr('href'), item.text())

def get_real_video(url,name):
    has_save=find_same(name)
    if not has_save:
        print('-----我发现了最新的电影：' + name + '，正在尝试爬取...')
        video_page = get_page(url)
        video_page_url = host+video_page('.online-button a').attr('href')
        # 同时拿到其他信息
        movie={
            "title":name,
            "poster":video_page('.img-thumbnail').attr('src'),
            "content":video_page('.summary').text(),
            "visit":0,
            "star":0
        }

        video_page_two=get_page(video_page_url)
        if video_page_two and video_page_two('iframe'):
            video_page_hide=video_page_two('iframe').attr('src')
            video_page_real=get_page(video_page_hide)
            if video_page_real and video_page_real('iframe'):
                video_real_address=video_page_real('iframe').attr('src')
                movie['address']=video_real_address
                # print(movie)
                insert_into(movie['title'],movie['poster'],video_real_address,movie['content'])
                # return video_real_address
                # 此处可以开始保存进入数据库
                print('>>>电影：' +name + '已经爬取入库')
            else:
                print('资源无效')
        else:
            print('资源无效')
    else:
        print('已存在')

def insert_into(title,poster,addr,content):
    sqla = '''
            insert into movie_info(title,poster,address,content)
            values(%s,%s,%s,%s);
           '''
    try:
        cur.execute(sqla , (title, poster,addr,content))
        conn.commit()
        # print('保存成功')
    except Exception as e:
        # 错误回滚
        conn.rollback()
        print('存入数据库的时候出了点错误')

def find_same(name):
    sql='''
        SELECT title FROM movie_info WHERE title=%s
        '''
    cur.execute(sql,(name))
    result=cur.fetchone()
    # print(result)
    if result:
        return True
    else:
        return False
def get_page_enter(url):
    page=get_page(url)
    enters=page('.movie-item>a')
    for item in enters.items():
        # threadPool.submit(get_real_video,host+item.attr('href'),item.attr('title'))
        get_real_video(host+item.attr('href'),item.attr('title'))
def start():
    for i in range(1,4):
        page_url=baseUrl % i
        get_page_enter(page_url)
    conn.commit()
    cur.close()
    conn.close()
    print('全部电影保存完毕！！！')
start()
# a=find_same('芒刺')
# print(a)
# res=get_page(host+'/play/3881.html')
# if not res('iframe')  :
#     print('you get it')
