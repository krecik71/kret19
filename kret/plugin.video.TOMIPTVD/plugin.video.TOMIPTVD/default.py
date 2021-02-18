 # -*- coding: utf-8 -*- 
 
 #############Imports#############
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,base64,os,re,unicodedata,requests,time,string,sys,urllib,urllib2,json,urlparse,zipfile,shutil
from resources.modules import client,control,tools,user,activate,date_converter
import time
from datetime import datetime
import xml.etree.ElementTree as ElementTree


#################################

#############Defined Strings#############
icon         = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.TOMIPTVD/icon.png'))
fanart       = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.TOMIPTVD/fanart.jpg'))

username     = control.setting('Username')
password     = control.setting('Password')

live_url     = '%s:%s/enigma2.php?username=%s&password=%s&type=get_live_categories'%(user.host,user.port,username,password)
vod_url      = '%s:%s/enigma2.php?username=%s&password=%s&type=get_vod_categories'%(user.host,user.port,username,password)
series_url   = '%s:%s/enigma2.php?username=%s&password=%s&type=get_series_categories'%(user.host,user.port,username,password)
panel_api    = '%s:%s/panel_api.php?username=%s&password=%s'%(user.host,user.port,username,password)
play_url     = '%s:%s/live/%s/%s/'%(user.host,user.port,username,password)
search_play      = '%s:%s/'%(user.host,user.port)
panel_api1      = '%s:%s/enigma2.php?username=%s&password=%s&type=get_series'%(user.host,user.port,username,password)


Guide = xbmc.translatePath(os.path.join('special://home/addons/addons/'+user.id+'/resources/catchup', 'guide.xml'))
GuideLoc = xbmc.translatePath(os.path.join('special://home/addons/addons/'+user.id+'/resources/catchup', 'g'))

advanced_settings           =  xbmc.translatePath('special://home/addons/'+user.id+'/resources/advanced_settings')
advanced_settings_target    =  xbmc.translatePath(os.path.join('special://home/userdata','advancedsettings.xml'))

KODIV        = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
#########################################

def buildcleanurl(url):
	url = str(url).replace('USERNAME',username).replace('PASSWORD',password)
	return url
def start():
    auth = '%s:%s/enigma2.php?username=%s&password=%s'%(user.host,user.port,username,password)
    request = requests.get(auth)
    if not request.status_code == 200:
        yesnowindow = xbmcgui.Dialog().yesno('TOM IPTVD', 'TOM IPTVD Aktivierung: ','','Willst du TOM IPTVD aktivieren?', yeslabel='Ja',nolabel='Nein')
        dialog = xbmcgui.Dialog()
        if yesnowindow == 1:
            usern = userpopup()
            passw= passpopup()
            control.setSetting('Username',usern)
            control.setSetting('Password',passw)
            xbmc.executebuiltin('Container.Refresh')
            auth = '%s:%s/enigma2.php?username=%s&password=%s'%(user.host,user.port,usern,passw)
            request = requests.get(auth) 
            if not request.status_code == 200: 
                line1 = "Falsche Login Daten"
                line2 = "Bitte erneut versuchen" 
                line3 = "" 
                xbmcgui.Dialog().notification(line1, line2)
                
            else:
                line1 = "Anmeldung erfolgreich"
                line2 = "Willkommen zu TOM IPTVD"
                line3 = ('[B][COLOR red]%s[/COLOR][/B]'%usern)
                xbmcgui.Dialog().ok('TOM IPTVD', line1, line2, line3)
                #tvguidesetup()
                xbmc.executebuiltin('Container.Refresh')
                home()
                
                
        else:
	        dialog.ok('TOM IPTVD','Aktivierung abgebrochen.','')
	        
    else:
	    home()
       

    
				
def home():
	tools.addDir('IPTV','live',1,icon,fanart,'')
	tools.addDir('VOD','vod',3,icon,fanart,'')
	tools.addDir('Suche','search',5,icon,fanart,'')
	tools.addDir('Account-Info','url',6,icon,fanart,'')
		
def livecategory(url):
	url  = buildcleanurl(url)
	open = tools.OPEN_URL(live_url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
		tools.addDir('%s'%name,url1,2,icon,fanart,'')
		
def Livelist(url):
	url  = buildcleanurl(url)
	open = tools.OPEN_URL(url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		xbmc.log(str(name))
		name = re.sub('\[.*?min ','-',name)
		thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
		url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
		desc = tools.regex_from_to(a,'<description>','</description>')
		tools.addDir(name,url1,4,thumb,fanart,base64.b64decode(desc))
		
		
		
	

				
				

def vod(url):
	if url =="vod":
		open = tools.OPEN_URL(vod_url)
	else:
		url  = buildcleanurl(url)
		open = tools.OPEN_URL(url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		if '<playlist_url>' in open:
			name = tools.regex_from_to(a,'<title>','</title>')
			url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
			tools.addDir(str(base64.b64decode(name)).replace('?',''),url1,33,icon,fanart,'')
		else:
			if xbmcaddon.Addon().getSetting('meta') == 'true':
				try:
					name = tools.regex_from_to(a,'<title>','</title>')
					name = base64.b64decode(name)
					thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
					url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
					desc = tools.regex_from_to(a,'<description>','</description>')
					desc = base64.b64decode(desc)
					plot = tools.regex_from_to(desc,'PLOT:','\n')
					cast = tools.regex_from_to(desc,'CAST:','\n')
					ratin= tools.regex_from_to(desc,'RATING:','\n')
					year = tools.regex_from_to(desc,'RELEASEDATE:','\n').replace(' ','-')
					year = re.compile('-.*?-.*?-(.*?)-',re.DOTALL).findall(year)
					runt = tools.regex_from_to(desc,'DURATION_SECS:','\n')
					genre= tools.regex_from_to(desc,'GENRE:','\n')
					tools.addDirMeta(str(name).replace('[/COLOR][/B].','.[/COLOR][/B]'),url,4,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(cast).split(),ratin,runt,genre)
				except:pass
				xbmcplugin.setContent(int(sys.argv[1]), 'movies')
			else:
				name = tools.regex_from_to(a,'<title>','</title>')
				name = base64.b64decode(name)
				thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
				url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
				desc = tools.regex_from_to(a,'<description>','</description>')
				if not 'All' in name:
				    tools.addDir(name,url,4,thumb,fanart,base64.b64decode(desc))



				    
def series(url):
	if url =="series":
		open = tools.OPEN_URL(series_url)
	else:
		url  = buildcleanurl(url)
		open = tools.OPEN_URL(url)
	all_cats = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_cats:
		if '<playlist_url>' in open:
			name = tools.regex_from_to(a,'<title>','</title>')
			url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
			if not 'QWxs' in name:
			    tools.addDir(str(base64.b64decode(name)).replace('?',''),url1,34,icon,fanart,'')
		else:
			if xbmcaddon.Addon().getSetting('meta') == 'true':
				try:
					name = tools.regex_from_to(a,'<title>','</title>')
					name = base64.b64decode(name)
					thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
					url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
					desc = tools.regex_from_to(a,'<description>','</description>')
					desc = base64.b64decode(desc)
					plot = tools.regex_from_to(desc,'PLOT:','\n')
					cast = tools.regex_from_to(desc,'CAST:','\n')
					ratin= tools.regex_from_to(desc,'RATING:','\n')
					year = tools.regex_from_to(desc,'RELEASEDATE:','\n').replace(' ','-')
					year = re.compile('-.*?-.*?-(.*?)-',re.DOTALL).findall(year)
					runt = tools.regex_from_to(desc,'DURATION_SECS:','\n')
					genre= tools.regex_from_to(desc,'GENRE:','\n')
					tools.addDirMeta(str(name).replace('[/COLOR][/B].','.[/COLOR][/B]'),url,4,thumb,fanart,plot,str(year).replace("['","").replace("']",""),str(cast).split(),ratin,runt,genre)
				except:pass
				xbmcplugin.setContent(int(sys.argv[1]), 'movies')
			else:
				name = tools.regex_from_to(a,'<title>','</title>')
				name = base64.b64decode(name)
				thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
				url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
				desc = tools.regex_from_to(a,'<description>','</description>')
				if not 'All' in name:
				    tools.addDir(name,url,4,thumb,fanart,base64.b64decode(desc))
				
				




		
##############################################
#### RULE NO.1 - DONT WRITE CODE THAT IS  ####
#### ALREADY WRITTEN AND PROVEN TO WORK :)####
##############################################


def catchup():
    listcatchup()

def freetv():
	xbmc.executebuiltin('RunAddon(plugin.video.PsycoTV)')

		
def listcatchup():
	open = tools.OPEN_URL(panel_api)
	all  = tools.regex_get_all(open,'{"num','direct')
	for a in all:
		if '"tv_archive":1' in a:
			name = tools.regex_from_to(a,'"epg_channel_id":"','"').replace('\/','/')
			thumb= tools.regex_from_to(a,'"stream_icon":"','"').replace('\/','/')
			id   = tools.regex_from_to(a,'stream_id":"','"')
			if not name=="":
				tools.addDir(name,'url',13,thumb,fanart,id)
			

def tvarchive(name,description):
    days = 10
	
    now = str(datetime.datetime.now()).replace('-','').replace(':','').replace(' ','')
    date3 = datetime.datetime.now() - datetime.timedelta(days)
    date = str(date3)
    date = str(date).replace('-','').replace(':','').replace(' ','')
    APIv2 = base64.b64decode("JXM6JXMvcGxheWVyX2FwaS5waHA/dXNlcm5hbWU9JXMmcGFzc3dvcmQ9JXMmYWN0aW9uPWdldF9zaW1wbGVfZGF0YV90YWJsZSZzdHJlYW1faWQ9JXM=")%(user.host,user.port,username,password,description)
    link=tools.OPEN_URL(APIv2)
    match = re.compile('"title":"(.+?)".+?"start":"(.+?)","end":"(.+?)","description":"(.+?)"').findall(link)
    for ShowTitle,start,end,DesC in match:
        ShowTitle = base64.b64decode(ShowTitle)
        DesC = base64.b64decode(DesC)
        format = '%Y-%m-%d %H:%M:%S'
        try:
            modend = dtdeep.strptime(end, format)
            modstart = dtdeep.strptime(start, format)
        except:
            modend = datetime.datetime(*(time.strptime(end, format)[0:6]))
            modstart = datetime.datetime(*(time.strptime(start, format)[0:6]))
        StreamDuration = modend - modstart
        modend_ts = time.mktime(modend.timetuple())
        modstart_ts = time.mktime(modstart.timetuple())
        FinalDuration = int(modend_ts-modstart_ts) / 60
        strstart = start
        Realstart = str(strstart).replace('-','').replace(':','').replace(' ','')
        start2 = start[:-3]
        editstart = start2
        start2 = str(start2).replace(' ',' - ')
        start = str(editstart).replace(' ',':')
        Editstart = start[:13] + '-' + start[13:]
        Finalstart = Editstart.replace('-:','-')
        if Realstart > date:
            if Realstart < now:
                catchupURL = base64.b64decode("JXM6JXMvc3RyZWFtaW5nL3RpbWVzaGlmdC5waHA/dXNlcm5hbWU9JXMmcGFzc3dvcmQ9JXMmc3RyZWFtPSVzJnN0YXJ0PQ==")%(user.host,user.port,username,password,description)
                ResultURL = catchupURL + str(Finalstart) + "&duration=%s"%(FinalDuration)
                kanalinimi = "[B][COLOR purple]%s[/COLOR][/B] - %s"%(start2,ShowTitle)
                tools.addDir(kanalinimi,ResultURL,4,icon,fanart,DesC)

	
					
def DownloaderClass(url, dest):
    dp = xbmcgui.DialogProgress()
    dp.create('Fetching latest Catch Up',"Fetching latest Catch Up...",' ', ' ')
    dp.update(0)
    start_time=time.time()
    urllib.urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs, fs, dp, start_time))

def _pbhook(numblocks, blocksize, filesize, dp, start_time):
        try: 
            percent = min(numblocks * blocksize * 100 / filesize, 100) 
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: 
                eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: 
                eta = 0 
            kbps_speed = kbps_speed / 1024 
            mbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '[B][COLOR purple]%.02f MB of less than 5MB[/COLOR][/B]' % (currently_downloaded)
            e = '[B][COLOR purple]Speed:  %.02f Mb/s ' % mbps_speed  + '[/COLOR][/B]'
            dp.update(percent, mbs, e)
        except: 
            percent = 100 
            dp.update(percent) 
        if dp.iscanceled():
            dialog = xbmcgui.Dialog()
            dialog.ok(user.name, 'The download was cancelled.')
				
            sys.exit()
            dp.close()
#####################################################################

def tvguide():
		xbmc.executebuiltin('ActivateWindow(TVGuide)')
def stream_video(url):
	url = buildcleanurl(url)
	url = str(url).replace('USERNAME',username).replace('PASSWORD',password)
	liz = xbmcgui.ListItem('', iconImage='DefaultVideo.png', thumbnailImage=icon)
	liz.setInfo(type='Video', infoLabels={'Title': '', 'Plot': ''})
	liz.setProperty('IsPlayable','true')
	liz.setPath(str(url))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
	
def searchdialog():
	search = control.inputDialog(heading='Search ' +':')
	if search=="":
		return
	else:
		return search

	
def search():
	if mode==3:
		return False
	text = searchdialog()
	if not text:
		xbmc.executebuiltin("XBMC.Notification(Suchfeld ist leer,Suche abgebrochen,4000,"+icon+")")
		return
	xbmc.log(str(text))
	open = tools.OPEN_URL(panel_api)
	all_chans = tools.regex_get_all(open,'{"num":','tv_arch')
	for a in all_chans:
		name = tools.regex_from_to(a,'name":"','"').replace('\/','/')
		url  = tools.regex_from_to(a,'"stream_id":"','"')
		comp  = tools.regex_from_to(a,'"container_extension":"','"')
		lms  = tools.regex_from_to(a,'"stream_type":"','"')
		thumb= tools.regex_from_to(a,'stream_icon":"','"').replace('\/','/')
		if lms == 'live':
		    if text in name.lower():
		        tools.addDir(name,search_play+'live/'+username+'/'+password+'/'+url+'.ts',4,thumb,fanart,'')
		    elif text not in name.lower() and text in name:
			    tools.addDir(name,search_play+'live/'+username+'/'+password+'/'+url+'.ts',4,thumb,fanart,'')
		else:
		    if text in name.lower():
			    tools.addDir(name,search_play+lms+'/'+username+'/'+password+'/'+url+'.'+comp,4,thumb,fanart,'')
		    elif text not in name.lower() and text in name:
			    tools.addDir(name,search_play+lms+'/'+username+'/'+password+'/'+url+'.'+comp,4,thumb,fanart,'')
				
	xbmc.log(str(base64.b64encode(text)))
	open = tools.OPEN_URL(panel_api1)
	all_chans = tools.regex_get_all(open,'<channel>','</channel>')
	for a in all_chans:
		name = tools.regex_from_to(a,'<title>','</title>')
		name = base64.b64decode(name)
		url  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
		lms  = tools.regex_from_to(a,'"stream_type":"','"')
		thumb= tools.regex_from_to(a,'stream_icon":"','"').replace('\/','/')
		if text in name.lower():
		    tools.addDir(name,url,34,thumb,fanart,'')
		elif text not in name.lower() and text in name:
			tools.addDir(name,url,34,thumb,fanart,'')
	
def settingsmenu():
	tools.addDir('Account Information','url',6,icon,fanart,'')
	if xbmcaddon.Addon().getSetting('hidexxx')=='true':
		XXX = '[B][COLOR lime]AN[/COLOR][/B]'
	else:
		XXX = '[B][COLOR red]AUS[/COLOR][/B]'
	tools.addDir('Erwachsenenkanäle sind %s'%XXX,'XXX',10,icon,fanart,XXX)
	
	

def addonsettings(url,description):
	url  = buildcleanurl(url)
	if url =="XXX":
		if 'AN' in description:
			xbmcaddon.Addon().setSetting('hidexxx','false')
			xbmc.executebuiltin('Container.Refresh')
		else:
			xbmcaddon.Addon().setSetting('hidexxx','true')
			xbmc.executebuiltin('Container.Refresh')
		xbmc.executebuiltin('Container.Refresh')
	
		
def advancedsettings(device):
	if device == 'stick':
		file = open(os.path.join(advanced_settings, 'stick.xml'))
	elif device == 'firetv':
		file = open(os.path.join(advanced_settings, 'firetv.xml'))
	elif device == 'lessthan':
		file = open(os.path.join(advanced_settings, 'lessthan1GB.xml'))
	elif device == 'morethan':
		file = open(os.path.join(advanced_settings, 'morethan1GB.xml'))
	elif device == 'shield':
		file = open(os.path.join(advanced_settings, 'shield.xml'))
	elif device == 'remove':
		os.remove(advanced_settings_target)
	
	try:
		read = file.read()
		f = open(advanced_settings_target, mode='w+')
		f.write(read)
		f.close()
	except:
		pass
		
	
def pvrsetup():
	correctPVR()
	return
		
		
def asettings():
	choice = xbmcgui.Dialog().yesno(user.name, 'Please Select The RAM Size of Your Device', yeslabel='Less than 1GB RAM', nolabel='More than 1GB RAM')
	if choice:
		lessthan()
	else:
		morethan()
	

def morethan():
		file = open(os.path.join(advanced_settings, 'morethan.xml'))
		a = file.read()
		f = open(advanced_settings_target, mode='w+')
		f.write(a)
		f.close()

		
def lessthan():
		file = open(os.path.join(advanced_settings, 'lessthan.xml'))
		a = file.read()
		f = open(advanced_settings_target, mode='w+')
		f.write(a)
		f.close()
		
		
def userpopup():
	kb =xbmc.Keyboard ('', 'heading', True)
	kb.setHeading('Benutzername eingeben')
	kb.setHiddenInput(False)
	kb.doModal()
	if (kb.isConfirmed()):
		text = kb.getText()
		return text
	else:
		return False

		
def passpopup():
	kb =xbmc.Keyboard ('', 'heading', True)
	kb.setHeading('Passwort eingeben')
	kb.setHiddenInput(False)
	kb.doModal()
	if (kb.isConfirmed()):
		text = kb.getText()
		return text
	else:
		return False
		
		
def accountinfo():
	open = tools.OPEN_URL(panel_api)
	username   = tools.regex_from_to(open,'"username":"','"')
	password   = tools.regex_from_to(open,'"password":"','"')
	status     = tools.regex_from_to(open,'"status":"','"')
	connects   = tools.regex_from_to(open,'"max_connections":"','"')
	active     = tools.regex_from_to(open,'"active_cons":"','"')
	expiry     = tools.regex_from_to(open,'"exp_date":"','"')
	expiry     = datetime.fromtimestamp(int(expiry)).strftime('%d/%m/%Y - %H:%M')
	expreg     = re.compile('^(.*?)/(.*?)/(.*?)$',re.DOTALL).findall(expiry)
	for day,month,year in expreg:
	    month     = tools.MonthNumToName(month)
	    year      = re.sub(' -.*?$','',year)
	    expiry    = day+'. '+month+'  '+year
	ip        = tools.getlocalip()
	extip     = tools.getexternalip()
	tools.addDir('[B][COLOR red]Benutzername :[/COLOR][/B] '+username,'','',icon,fanart,'')
	tools.addDir('[B][COLOR red]Passwort :[/COLOR][/B] '+password,'','',icon,fanart,'')
	tools.addDir('[B][COLOR red]Ablaufdatum:[/COLOR][/B] '+expiry,'','',icon,fanart,'')
	tools.addDir('[B][COLOR red]Status :[/COLOR][/B] %s'%status,'','',icon,fanart,'')
	tools.addDir('[B][COLOR red]Aktuelle Verbindungen:[/COLOR][/B] '+active,'','',icon,fanart,'')
	tools.addDir('[B][COLOR red]Erlaubte Verbindungen:[/COLOR][/B] '+connects,'','',icon,fanart,'')
	tools.addDir('[B][COLOR red]Lokale IP-Addresse:[/COLOR][/B] '+ip,'','',icon,fanart,'')
	tools.addDir('[B][COLOR red]Externe IP-Address-e:[/COLOR][/B] '+extip,'','',icon,fanart,'')
	tools.addDir('[B][COLOR red]Kodi Version:[/COLOR][/B] '+str(KODIV),'','',icon,fanart,'')
		

		
	
def correctPVR():
    addon = xbmcaddon.Addon(user.id)
    username_text = addon.getSetting(id='Username')
    password_text = addon.getSetting(id='Password')
    PVR = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/pvr.iptvsimple/settings.xml'))
    PVRVOR = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.TOMIPTV/settingsvor.xml'))
    PVRShot = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/pvr.iptvsimple/settings1.xml'))
    M3U = xbmc.translatePath(os.path.join('special://home/userdata/fav.m3u'))
    M3UNEW = xbmc.translatePath(os.path.join('special://home/userdata/favnew.m3u'))
    shutil.move(PVR,PVRShot)
    shutil.rmtree(PVRShot, ignore_errors=True)
    #hier PVR Einstellungen Text Ändern und M3u Text Ändnern
    f1 = open(PVRVOR, 'r')
    f2 = open(PVR, 'w')
    for line in f1:
        f2.write(line.replace('var2',password_text).replace('var1',username_text))
    f1.close()
    f2.close()
    f3 = open(M3U, 'r')
    f4 = open(M3UNEW, 'w')
    for line in f3:
        f4.write(line.replace('password',password_text).replace('username',username_text))
    f3.close()
    f4.close()
    activate.get_packages()
    

	

	
def tvguidesetup():
		pvrsetup()
		
def num2day(num):
	if num =="0":
		day = 'monday'
	elif num=="1":
		day = 'tuesday'
	elif num=="2":
		day = 'wednesday'
	elif num=="3":
		day = 'thursday'
	elif num=="4":
		day = 'friday'
	elif num=="5":
		day = 'saturday'
	elif num=="6":
		day = 'sunday'
	return day
	
def extras():
	tools.addDir('Create a Short M3U & EPG Url','url',17,icon,fanart,'')
	tools.addDir('Run a Speed Test','ST',10,icon,fanart,'')
	tools.addDir('Setup PVR Guide','tv',10,icon,fanart,'')
	tools.addDir('Clear Cache','CC',10,icon,fanart,'')
	

params=tools.get_params()
url=None
name=None
mode=None
iconimage=None
description=None
query=None
type=None

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
	description=urllib.unquote_plus(params["description"])
except:
	pass
try:
	query=urllib.unquote_plus(params["query"])
except:
	pass
try:
	type=urllib.unquote_plus(params["type"])
except:
	pass

if mode==None or url==None or len(url)<1:
	start()

elif mode==1:
	livecategory(url)
	
elif mode==2:
	Livelist(url)
	
elif mode==3:
    tools.addDir('Filme','vod',33,icon,fanart,'')
    tools.addDir('Serien','series',34,icon,fanart,'')
    
	
elif mode==33:
    vod(url)
    
elif mode==34:
    series(url)
	
elif mode==4:
	stream_video(url)
	
elif mode==5:
	search()
	
elif mode==6:
	accountinfo()
	
elif mode==7:
	tvguide()
	
elif mode==8:
	settingsmenu()
	
elif mode==9:
	xbmc.executebuiltin('ActivateWindow(busydialog)')
	tools.Trailer().play(url) 
	xbmc.executebuiltin('Dialog.Close(busydialog)')
	
elif mode==10:
	addonsettings(url,description)
	
elif mode==11:
	pvrsetup()
	
elif mode==12:
	catchup()

elif mode==13:
	tvarchive(name,description)
	
elif mode==14:
	listcatchup2()
	
elif mode==15:
	ivueint()
	
elif mode==16:
	extras()
	
elif mode==17:
	from resources.modules import shortlinks
	shortlinks.showlinks()
    
elif mode==18:
	freetv()

elif mode==9999:
	xbmcgui.Dialog().ok('[B][COLOR skyblue]Zinitv Player[/COLOR][/B]','This Category Will Be Available Soon!')
	livecategory('url')

xbmcplugin.endOfDirectory(int(sys.argv[1]))