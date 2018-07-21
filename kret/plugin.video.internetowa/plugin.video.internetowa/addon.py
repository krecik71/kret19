import sys, re, os
import urllib, urllib2
import urlparse
import xbmcgui
import xbmcplugin
import xbmc, xbmcaddon
import json

__myurl__ = 'http://internetowa.ws'
__scriptID__ = 'plugin.video.internetowa'
__addon__ = xbmcaddon.Addon(id='plugin.video.internetowa')

version = 2018070701

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

if mode is None:
    url = 'http://internetowa.ws/?c=kodiVersion'
    headers = { 'User-Agent': 'XBMC', 'ContentType': 'application/x-www-form-urlencoded' }
    post = {}
    data = urllib.urlencode(post)
    reqUrl = urllib2.Request(url, data, headers)
    try:
		red_json = urllib2.urlopen(reqUrl)
    except:
        xbmcgui.Dialog().ok('Brak Polaczenia','Brak polaczenia z Internetem lub blad serwera');	
        obj_data = json.load(red_json)	
	
        versionnet = obj_data
        if (versionnet>version):
	    xbmcgui.Dialog().ok('Nowa Wersja',' Dostepna nowa wersja.\n Pobierz z http://internetowa.ws/kodi ! ')
    else: 
    	icon = os.path.join( __addon__.getAddonInfo('path'), 'images/icon-tv.png' )
    	url = build_url({'mode': 'tv', 'foldername': 'Telewizja Online'})
    	li = xbmcgui.ListItem('Telewizja Online', iconImage=icon)
    	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    	

    	icon = os.path.join( __addon__.getAddonInfo('path'), 'images/icon-opcje.png' )
    	url = build_url({'mode': 'ustawienia', 'foldername': 'Ustawienia'})
    	li = xbmcgui.ListItem('Ustawienia', iconImage=icon)
    	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,listitem=li, isFolder=True)

    	xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'tv':
    url = 'http://internetowa.ws/?c=kodiVersion'
    headers = { 'User-Agent': 'XBMC', 'ContentType': 'application/x-www-form-urlencoded', 'Referer' : 'http://internetowa.ws/'	}
    post = {}
    data = urllib.urlencode(post)
    reqUrl = urllib2.Request(url, data, headers)
    try:
		red_json = urllib2.urlopen(reqUrl)
    except:
        xbmcgui.Dialog().ok('Brak Polaczenia','Brak polaczenia z Internetem lub blad serwera');	
        obj_data = json.load(red_json)	
	
        versionnet = obj_data
        if (versionnet>version):
	    xbmcgui.Dialog().ok('Nowa Wersja',' Dostepna nowa wersja.\n Pobierz z http://internetowa.ws/kodi ! ')
    else: 
    	PASS = __addon__.getSetting('pass')
    	NAME = __addon__.getSetting('name')

    	url = 'http://internetowa.ws/index.php?c=kodi' + '&email=' + NAME + '&password=' + PASS
    	headers = { 'User-Agent': 'XBMC', 'ContentType': 'application/x-www-form-urlencoded', 'Referer' : 'http://internetowa.ws/' }
    	post = {}
    	data = urllib.urlencode(post)
    	reqUrl = urllib2.Request(url, data, headers)
    	red_json = urllib2.urlopen(reqUrl)
    	obj_data = json.load(red_json)

    	foldername = args['foldername'][0]
    	icon = os.path.join( __addon__.getAddonInfo('path'), 'images/icon-tv.png' )
    	if len(obj_data) is 0:
        	dialog = xbmcgui.Dialog()
        	dialog.ok("Brak konta premium", " Brak aktywnego konta premium.\n Wiecej informacji na http://internetowa.ws po zalogowaniu w zakladce moje konto. ")
    	else:
        	for s in range(len(obj_data)):
        	 url = obj_data[s]['stationURL']
        	 li = xbmcgui.ListItem(obj_data[s]['stationName'], thumbnailImage=obj_data[s]['stationLogo'], iconImage=obj_data[s]['stationLogo'])
        	 xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li)
    	xbmcplugin.endOfDirectory(addon_handle)
	


elif mode[0] == 'ustawienia':
    __addon__.openSettings()
