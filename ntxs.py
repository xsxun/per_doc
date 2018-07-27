import requests
import urllib
import bs4 
from http import cookiejar


class novel:

    def __init__(self,tomename,chaptername,chapterUrl,chapterContent):
        self.tomename = tomename
        self.chaptername = chaptername
        self.chapterUrl = chapterUrl
        self.chapterContent = chapterContent
    def show(self):
        print(self.tomename+" "+self.chaptername+" "+self.chapterUrl+" "+self.chapterContent+"\n")

def getFreeLink():
    link = "https://m.zongheng.com/h5/chapter?bookid=408586&cid=42443131&k=241d9e&v=1532709001028&fr=aladin2_freexx"
    mBaidu = "https://m.baidu.com/s?from=1011440l&word=%E9%80%86%E5%A4%A9%E9%82%AA%E7%A5%9E"
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    req = urllib.request.Request(mBaidu,headers=headers)
    html = urllib.request.urlopen(req)
    soup = bs4.BeautifulSoup(html,"html.parser")
    temp_link = soup.find("ul",attrs={"class":"wa-nvl-flow-chapters"}).li.a.get("href")
    req = urllib.request.Request(temp_link,headers=headers)
    html = urllib.request.urlopen(req)
    soup = bs4.BeautifulSoup(html,"html.parser")
    a = soup.findAll("script")[0]
    b_start = str(a).find("https://")
    b_end = str(a).find("\");\n</script>")
    link = str(a)[b_start:b_end]
    return link

def initCookie():
    filename = 'cookie.txt'    
    cookie = cookiejar.MozillaCookieJar(filename)
    handler= urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    opener.open(getFreeLink())
    cookie.save(ignore_discard=True, ignore_expires=True)

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

def req(start):
    initCookie()
    url = 'http://book.zongheng.com/showchapter/408586.html'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    req = urllib.request.Request(url,headers=headers)
    html = urllib.request.urlopen(req)
    soup = bs4.BeautifulSoup(html,"html.parser")
    tomes = soup.findAll('div',attrs={'class':"booklist tomeBean"})

    num = 0
    for i in tomes:
        tomename = i.get('tomename')
        chapters = i.findAll('td', attrs = {"class" : "chapterBean"})
        for chapter in chapters:
            if num > start:
                chaptername = chapter.get('chaptername')
                chapterUrl = chapter.find('a').get('href')
                chapterContent = getContent(chapterUrl)
                if chapterContent != "None" :
                    print(str(num)+"看起来没有问题。")
                    f = open("第%d代号开始.txt"%start,"a+")
                    f.write(tomename+" "+chaptername+"\n"+chapterContent+"\n\n")
                    f.close()
                else:
                    print("@!@出现问题")
            num+=1

# 不确定数据
# current_max = 1181 代表1172章
req(1179)