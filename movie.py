import requests
from pyquery import PyQuery as pq

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
}
baseurl='http://www.66ys.tv/'
testurl='http://www.66ys.tv/xijupian/'
def get_index_page(url):
    response=requests.get(url,headers=headers)
    response.encoding = 'gb2312'
    return response.text

index_page=get_index_page(baseurl)
menu=pq(index_page)('.menutv li a')

def get_list_page(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'gb2312'
    return pq(response.text)

def get_detail_entry(obj):
    item=obj('.listimg').find('a')
    for k in item.items():
        detailurl=k.attr('href')
        get_info(detailurl)

def handle_page(url):
    entry = get_list_page(url)
    pageNum = int(entry('.pagebox a').eq(0).find('b').text())
    get_detail_entry(entry)
    # for i in range(1, pageNum):
    #     if not i == 1:
    #         page_url = url+'/index_%s.html' % str(i)
    #         page=get_list_page(page_url)

def get_info(url):
    detail=get_list_page(url)
    title=detail('h1').text()
    print(title.)

get_index_page(baseurl)
for k in menu.items():
    if not k.text() == '首页':
        category=k.text()
        listUrl=k.attr('href')
        handle_page(listUrl)



