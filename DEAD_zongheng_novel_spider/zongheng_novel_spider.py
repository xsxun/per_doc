import requests
import urllib
import bs4 
from http import cookiejar
import time
import random
from fake_useragent import UserAgent
import sys

## 686515 都市之透视医圣 + 最新章节免费阅读_百度小说
## 408586 逆天邪神 + 最新章节免费阅读_百度小说
## 359388 最强武神 + 最新章节免费阅读_百度小说
def getFakeLink(bookname):
    search_keyword=urllib.parse.quote(bookname + "最新章节免费阅读_百度小说")
    mBaidu = "https://m.baidu.com/s?from=1011440l&word="+ search_keyword
    user_agent = UserAgent().random
    headers = { 'User-Agent' : user_agent }
    req = urllib.request.Request(mBaidu,headers=headers)
    html = urllib.request.urlopen(req)
    soup = bs4.BeautifulSoup(html,"html.parser")
    try:
        temp_link = soup.find("ul",attrs={"class":"wa-nvl-flow-chapters"}).li.a.get("href")
        req = urllib.request.Request(temp_link,headers=headers)
        html = urllib.request.urlopen(req)
        soup = bs4.BeautifulSoup(html,"html.parser")
        a = soup.findAll("script")[0]
        b_start = str(a).find("https://")
        b_end = str(a).find("\");\n</script>")
        link = str(a)[b_start:b_end]
        return link
    except  AttributeError:
        print("仅支持手机百度端可以免费阅读的小说!")
        return None

def initCookie(bookname):
    filename = 'cookie.txt'    
    cookie = cookiejar.MozillaCookieJar(filename)
    handler= urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    if(getFakeLink(bookname)!=None):
        opener.open(getFakeLink(bookname))
        cookie.save(ignore_discard=True, ignore_expires=True)
    else:
        print("无法获取这本小说")
        sys.exit()

def getContent(chapterUrl):
    content = ""
    cookie = cookiejar.MozillaCookieJar()
    cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
    req = opener.open(chapterUrl)
    html = req.read().decode()
    soup = bs4.BeautifulSoup(html,"html.parser")
    test = soup.find('div',attrs={'class':'readtext'})
    content = str(test).replace("<div class=\"readtext\" onselectstart=\"return false;\" style=\"-moz-user-select:none;-webkit-user-select:none;\" unselectable=\"on\">\n","").\
    replace("<div class=\"shade_one\" title=\"大家好我是分割线\">","").replace("<div class=\"\" id=\"readerFt\" itemprop=\"acticleBody\">\n","").\
    replace("<script>document.getElementById(\"readerFt\").className = \"rft_\" + rSetDef()[2];</script>\n","").replace("<!-- 正常输出文章内容 -->\n","").\
    replace("<div class=\"\" id=\"readerFs\">","").replace("<script>document.getElementById(\"readerFs\").className = \"rfs_\" + rSetDef()[3]</script>","").replace("</div>","").replace("<p>","").replace("</p>","\n\n")
    return content

def zh_novel(bookNum,start):
    '''
    bookNum : the number behind URL "http://book.zongheng.com/showchapter/" of showchapter page
    start : a number represents all chapters beginning with 0
    '''
    url = 'http://book.zongheng.com/showchapter/'+str(bookNum)+'.html'
    user_agent = UserAgent().random
    headers = { 'User-Agent' : user_agent }
    req = urllib.request.Request(url,headers=headers)
    html = urllib.request.urlopen(req)
    soup = bs4.BeautifulSoup(html,"html.parser")
    # novel name
    bookname = soup.find("div",attrs={"class":"tc txt"}).h1.text
    # author name
    authorname = soup.find("div",attrs={"class":"tc txt"}).span.a.text
    #init cookie
    initCookie(bookname)
    # write novel name and author name into txt
    f = open(bookname+"start_with_%d.txt"%start,"a+")
    f.write(bookname+"\n"+authorname+"\n\n")
    f.close()
    # tomes
    tomes = soup.findAll('div',attrs={'class':"booklist tomeBean"})
    num = 0
    for i in tomes:
        tomename = i.get('tomename')
        chapters = i.findAll('td', attrs = {"class" : "chapterBean"})
        for chapter in chapters:
            if num >= start: 
                chaptername = chapter.get('chaptername')
                chapterUrl = chapter.find('a').get('href')
                chapterContent = getContent(chapterUrl)
                if chapterContent != "None" :
                    print(str(num)+"看起来没有问题。")
                    f = open(bookname+"start_with_%d.txt"%start,"a+")
                    f.write(tomename+" "+chaptername+"\n"+chapterContent+"\n\n")
                    f.close()
                    time.sleep(random.randrange(0,2)) #add sleep to avoid ip block
                else:
                    print("@!@出现问题")
                    f = open("第%d代号开始.txt"%start,"a+")
                    f.write("\n!!!!!!!!!!!!!!!!!!!!!!!\n代号%d的章节出现问题！\n!!!!!!!!!!!!!!!!!!!!!!!\n"%num)
                    f.close()
                    break
            num+=1

# start 为不确定数据 取决于作品相关的变动与否
## 408586 逆天邪神 + 最新章节免费阅读_百度小说
# current_max = 1182 代表1173章
zh_novel(408586,1182)
