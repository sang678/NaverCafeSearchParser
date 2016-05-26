# -*- coding: cp949 -*-

import urllib
import urllib2
import sys

from bs4 import BeautifulSoup
from naverlogin import NaverSession

class NaverCafeSearchParser :
    nsession = NaverSession()
    isLoginSuccess = False
    boardList = None;
    processedMaxArticleNumber = None;
    
    def searchCafe(self,clubId, searchWord):
        request = urllib2.Request("http://cafe.naver.com/ArticleSearchList.nhn?search.clubid="+clubId+"&search.searchBy=0&search.query="+urllib.quote(searchWord))
        request.add_header('cookie',self.nsession.cookies)
        request.add_header("Content-Type","application/x-www-form-urlencoded;charset=euc-kr")
        socket =  urllib2.urlopen(request)
        
        return socket.read()

    def parseBoardList(self,siteUrl,searchWord):

        if self.isLoginSuccess:
            
           # print nsession.cookies

            #siteUrl = "http://cafe.naver.com/joonggonara"
            request = urllib2.Request(siteUrl)
            request.add_header('cookie',self.nsession.cookies)
            
            socket = urllib2.urlopen(request)
            html = socket.read()
            
            #Cafe(Club) ID value extract.  
            clubIdIdx = html.find("g_sClubId")
            g_sClubId = html[clubIdIdx+13 :html.find('\n',clubIdIdx)-3]
            soup = BeautifulSoup(self.searchCafe(g_sClubId, searchWord), "lxml", from_encoding="EUC-KR")
            self.boardList = soup
            return soup

            #print soup
               
            
            #nsession.logout()
        
    def parseBoardListContent(self) :
        i=0
        for link in self.boardList.select(".article-board")[1].select('a[href^="/ArticleRead.nhn?"]') :

            href = link.get("href");
            articleIdx = href.find("articleid=")
            articleNumber = href[articleIdx+10:href.find("&",articleIdx)]

            if self.processedMaxArticleNumber > articleNumber :
                break
            
            
                        
            
            request = urllib2.Request("http://cafe.naver.com/"+href)
            socket = urllib2.urlopen(request)
            html = socket.read()       
            soup = BeautifulSoup(html,"lxml", from_encoding="EUC-KR")
            #print soup
            price_info = soup.select(".price_line")
               
            if len(price_info) > 0 :
                #print "size : " + str(len(price_info))
                print soup.select(".tit-box > div > table > tr > td")[0].get_text()
                print price_info[0].span.get_text()

            if self.processedMaxArticleNumber < articleNumber:
                self.processedMaxArticleNumber = articleNumber
           
    def naverLogin(self,naverId, naverPw):
        if self.nsession.login(naverId, naverPw,False):
            self.isLoginSuccess = True
            print 'login finished.'
        else:
            print 'login failed! check id and password.'

    def naverLogout(self) :
        self.nsession.logout()
        

a = NaverCafeSearchParser()
a.naverLogin("myloginid","tkdrmsdl1!")
a.parseBoardList("http://cafe.naver.com/joonggonara","27인치")
a.parseBoardListContent();
