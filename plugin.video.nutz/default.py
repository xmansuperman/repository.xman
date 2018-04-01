# -*- coding: utf-8 -*-
import xbmcaddon,os,xbmc,xbmcgui,urllib,urllib2,re,xbmcplugin,sys,logging,json,random,requests,uuid,cookielib
from StringIO import StringIO
import gzip
__USERAGENT__ = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'
__addon__ = xbmcaddon.Addon()
__cwd__ = xbmc.translatePath(__addon__.getAddonInfo('path')).decode("utf-8")
Addon = xbmcaddon.Addon()
quality='best'
user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
if not os.path.exists(user_dataDir):
     os.makedirs(user_dataDir)
headers = {
    'Host': 'www.tarefet.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}
deviceID = Addon.getSetting("makoDeviceID")
if deviceID.strip() == '':
	uuidStr = str(uuid.uuid1()).upper()
	deviceID = "W{0}{1}".format(uuidStr[:8], uuidStr[9:])
	Addon.setSetting("makoDeviceID", deviceID)
    
userAgents = [
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12',
	'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
	'Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/7.1.8 Safari/537.85.17',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17',
	'Mozilla/5.0 (X11; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0',
	'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/8.0.6 Safari/600.6.3',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.50 (KHTML, like Gecko) Version/9.0 Safari/601.1.50',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
	'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/8.0.3 Safari/600.3.18',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/43.0.2357.130 Chrome/43.0.2357.130 Safari/537.36',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0;  Trident/5.0)',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;  Trident/5.0)',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
	'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:40.0) Gecko/20100101 Firefox/40.0',
	'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0',
	'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
	'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/6.1.6 Safari/537.78.2',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/7.1.7 Safari/537.85.16',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:38.0) Gecko/20100101 Firefox/38.0',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36'
]
UA = random.choice(userAgents)
def get_params():
        param=[]
        if len(sys.argv)>=2:
          paramstring=sys.argv[2]
          if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param     

def addNolink( name, url,mode,isFolder, iconimage="DefaultFolder.png"):
 

          
          name='[COLOR lightblue][I]'+name+'[/I][/COLOR]'
          u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
          liz = xbmcgui.ListItem( name, iconImage=iconimage, thumbnailImage=iconimage)

          liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote( name)   })

          liz.setProperty("IsPlayable","false")
          liz.setProperty( "Fanart_Image", iconimage )
          xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=isFolder)
###############################################################################################################        

def addDir3(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        art = {}
        art.update({'poster': iconimage})
        liz.setArt(art)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        
        return ok



def addLink( name, url,mode,isFolder, iconimage,fanart,description,data=''):

          u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+(name)+"&data="+str(data)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+(description)
 

          
         
         
          #u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
          liz = xbmcgui.ListItem( name, iconImage=iconimage, thumbnailImage=iconimage)

          liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote( name), "Plot": description   })
          art = {}
          art.update({'poster': iconimage})
          liz.setArt(art)
          liz.setProperty("IsPlayable","true")
          liz.setProperty( "Fanart_Image", fanart )
          xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=isFolder)


def read_site_html(url_link):
    import requests
    '''
    req = urllib2.Request(url_link)
    req.add_header('User-agent',__USERAGENT__)# 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')
    html = urllib2.urlopen(req).read()
    '''
    html=requests.get(url_link,headers=headers).content
    return html

def main_menu():
    html=read_site_html('http://www.tarefet.com/')
    regex='"nav-item">.+?id="(.+?)".+?href="(.+?)".+?<span>(.+?)<.+?<img src="(.+?)"'
    match=re.compile(regex,re.DOTALL).findall(html)
    for id,link,name,image in match:
      addNolink( name, 'www',99,False, iconimage=image)
      regex_pre='aria-labelledby="%s">(.+?)</ul>'%id

      match_pre=re.compile(regex_pre,re.DOTALL).findall(html)

      for items in match_pre:
        regex_in='<a href="(.+?)".+?src="(.+?)".+?p>(.+?)<'
        match_in=re.compile(regex_in).findall(items)
        
        for link,image,name in match_in:
           addDir3(name,link,2,image,image,name)
def GetJson(url):
    import requests

    html = requests.get(url, headers={"User-Agent": UA}).content

    if html == "":
        return None
    resultJSON = json.loads(html)
    if resultJSON is None or len(resultJSON) < 1:
        return None
    if resultJSON.has_key("root"):
        return resultJSON["root"]
    else:
        return resultJSON
def OpenURL(url, headers={}, user_data=None, CookieJar=None, retries=1):
	link = ""
	handlers = [
		urllib2.HTTPHandler(),
		urllib2.HTTPSHandler(),
		urllib2.HTTPCookieProcessor(CookieJar)
	]

	opener = urllib2.build_opener(*handlers)
	req = urllib2.Request(url)
	req.add_header('Accept-encoding', 'gzip')
	for k, v in headers.items():
		req.add_header(k, v)
	if req.headers.get('User-Agent', '') == '':
		req.add_header('User-Agent', UA)
	for i in range(retries):
		if 1:#try:

			response = opener.open(req, user_data, timeout=100)

			if response.info().get('Content-Encoding') == 'gzip':
				buf = StringIO( response.read())
				f = gzip.GzipFile(fileobj=buf)
				link = f.read()
			else:
				link = response.read()
			response.close()
			break
		#except Exception as ex:
		#	xbmc.log(str(ex), 3)
		#	return None
	return link
def DelCookies():
	tempDir = xbmc.translatePath('special://temp/').decode("utf-8")
	for the_file in os.listdir(tempDir):
		if not '.fi' in the_file and the_file != 'cookies.dat':
			continue
		file_path = os.path.join(tempDir, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as ex:
			xbmc.log(str(ex), 3)
def GetStreams(url, headers={}, user_data=None, CookieJar=None, retries=1, quality='best'):
        import urlparse
        base = urlparse.urlparse(url)
        baseUrl = '{0}://{1}{2}'.format(base.scheme, base.netloc, base.path)

        text = OpenURL(url, headers=headers, user_data=user_data, CookieJar=CookieJar, retries=retries)
        
        resolutions =  [x for x in re.compile('^#EXT-X-STREAM-INF:.*?BANDWIDTH=(\d+).*?\n(.*?)$', re.M).findall(text)]
        link = url
        if quality == 'best':
            link = max(resolutions, key=lambda item:int(item[0]))[1]
        elif quality == 'choose':
            [item[0] for item in resolutions]
            qualityInd = xbmcgui.Dialog().select(GetLocaleString(30005), [item[0] for item in resolutions])
            if qualityInd > -1:
                link = resolutions[qualityInd][1]
        else:
            quality = int(quality)
            res = 0
            for resolution in resolutions:
                _res = int(resolution[0])
                if _res >=  res and _res <=  quality:
                    res = _res
                    link = resolution[1]
        if not link.startswith('http'): 
            link = urlparse.urljoin(baseUrl, link)
        return link
def get_keshet():
        baseUrl = 'https://www.mako.co.il'
        endings = 'type=service&device=desktop&strto=desktop'
        headers={"User-Agent": UA}
        url='http://www.mako.co.il/mako-vod-live-tv/VOD-6540b8dcb64fd31006.htm'
        url = "{0}&{1}".format(url, endings) if "?" in url else "{0}?{1}".format(url, endings)
        prms = GetJson(url)
        if prms is None or not prms.has_key("video"):
            xbmc.log("Cannot get item", 2)
            return
        #iconimage = GetImage(prms["video"], 'pic_I', iconimage)
        videoChannelId=prms["channelId"]
        vcmid = prms["video"]["guid"]
        url = "{0}/VodPlaylist?vcmid={0}&videoChannelId={1}".format(vcmid,videoChannelId)
  
        DelCookies()
        g = url[url.find('vcmid=')+6: url.find('&videoChannelId=')]
        h = url[url.find('&videoChannelId=')+16:]
        temp_url='{0}/AjaxPage?jspName=playlist.jsp&vcmid={1}&videoChannelId={2}&consumer=web&encryption=no'.format(baseUrl, g, h)
        text = OpenURL(temp_url, headers=headers)
      
        result = json.loads(text)['media']
        u = ""
        for item in result:
            if item['format'] == 'AKAMAI_HLS':
                u = item['url']
                if '512035/CH2LIVE_LOW' in u:
                    u = u.replace('512035/CH2LIVE_LOW', '512033/CH2LIVE_HIGH')
                u2 = u[u.find('/', 7):]
                break
       
        l = 'http://mass.mako.co.il/ClicksStatistics/entitlementsServicesV2.jsp?et=gt&rv=akamai&lp={0}'.format(u2)
  
        text = OpenURL(l, headers=headers)
        result = json.loads(text)
        if result['caseId'] == '4':
            result = Login()
            text = OpenURL(l, headers=headers)
            result = json.loads(text)
            if result['caseId'] != '1':
                xbmc.executebuiltin("XBMC.Notification({0}, You need to pay if you want to watch this video., {1}, {2})".format(AddonName, 5000 ,icon))
                return
        elif result['caseId'] != '1':
            xbmc.executebuiltin("XBMC.Notification({0}, Cannot get access for this video., {1}, {2})".format(AddonName, 5000 ,icon))
            return
        t = urllib.unquote_plus(result['tickets'][0]['ticket'])
 
        if u.startswith('//'):
            u = 'http:{0}'.format(u)
        cookie_jar = cookielib.LWPCookieJar()
  
        link = GetStreams('{0}?{1}'.format(u, t), headers=headers, CookieJar=cookie_jar, quality=quality)
        cookies = ";".join(['{0}'.format(urllib.quote('{0}={1}'.format(_cookie.name, _cookie.value))) for _cookie in cookie_jar])
        final = '{0}|User-Agent={1}&Cookie={2}'.format(link, UA, cookies)

        return final
def next_level(name,url,image):
   if 'http://www.tarefet.com' not in url:
     url='http://www.tarefet.com'+url
   x=read_site_html(url)
   regex="file: '(.+?)'"
   match=re.compile(regex).findall(x)
   regex_p='<p>(.+?)</p>'
   match_p=re.compile(regex_p).findall(x)
   for link in match:
     addLink( name, link,3,False, image,image,match_p[0])
   regex_p='<iframe(.+?)</iframe>'
   match_p=re.compile(regex_p,re.I).findall(x)
   playingUrlsList = []
   for item in match_p:

     regex_in='src="(.+?)"'
     match_in=re.compile(regex_in,re.I).findall(item)

     playingUrlsList.append(match_in[0])
     
   if len (playingUrlsList)>0:
     addLink( name, json.dumps(playingUrlsList),3,False, image,image,match_p[0])
   regex_pre='<article id="(.+?)</article>'
   match_pre=re.compile(regex_pre,re.DOTALL).findall(x)
   for item in match_pre:
      regex_in='img.+?src="(.+?)".+?<a href="(.+?)">(.+?)<'
      match_in=re.compile(regex_in,re.DOTALL).findall(item)
      for image,link,name in match_in:
        addDir3(name,link,2,image,image,name)
def GetPyVer():
	return '{0}.{1}.{2}'.format(sys.version_info[0], sys.version_info[1], sys.version_info[2])
def get_reshet():
	referer = 'http://reshet.tv/live/'
	if GetPyVer() >= '2.7.9':
		headers={"Accept": "application/json;pk=BCpkADawqM30eqkItS5d08jYUtMkbTKu99oEBllbfUaFKeknXu4iYsh75cRm2huJ_b1-pXEPuvItI-733TqJN1zENi-DcHlt7b4Dv6gCT8T3BS-ampD0XMnORQLoLvjvxD14AseHxvk0esW3", "User-Agent": userAgent}
		result = OpenURL('https://edge.api.brightcove.com/playback/v1/accounts/1551111274001/videos/ref:stream_reshet_live1', headers=headers)
		headers={"User-Agent": UA, 'Referer': referer}
		link = GetStreams(json.loads(result)['sources'][0]['src'], headers=headers, quality=quality)
	else:
		link = 'https://besttv1.aoslive.it.best-tv.com/reshet/studio/index.m3u8'
	final = '{0}|User-Agent={1}&Referer={2}'.format(link, UA, referer)
	return final
def play(name,url,plot,image):
     import resolveurl
     if 'www.mako.co.il' in url:
       url=get_keshet()
     if 'reshet.tv' in url:
       url=get_reshet()
     try:
       all_links=json.loads(url)
       names=[]
       links=[]
       for link in all_links:
         if 'http' not in link:
           link='http:'+link
         regex='//(.+?)/'
         match=re.compile(regex).findall(link)
         names.append(match[0])
         links.append(link)
       if len(names)==1:
         url=links[0]
       else:
           ret=xbmcgui.Dialog().select("בחר מקור", names)
           if ret!=-1:
             resolvable=resolveurl.HostedMediaFile(links[ret]).valid_url()
             if resolvable:
                url=resolveurl.resolve(links[ret])
             else:
               url=links[ret]
           else:
             sys.exit()
     except:
      pass
     video_data={}
     video_data['title']=name
     video_data['plot']=plot
     video_data['poster']=image
     video_data[u'mpaa']=unicode('heb')

     listItem = xbmcgui.ListItem(video_data['title'], path=url) 
     listItem.setInfo(type='Video', infoLabels=video_data)


     listItem.setProperty('IsPlayable', 'true')

     xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
params=get_params()

url=None
name=None
mode=None
iconimage=None
fanart=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
   


if mode==None or url==None or len(url)<1:
        main_menu()
elif mode==2:
       next_level(name,url,iconimage)
elif mode==3:
      play(name,url,description,iconimage)
xbmcplugin.setContent(int(sys.argv[1]), 'movies')


xbmcplugin.endOfDirectory(int(sys.argv[1]))

