
# -*- coding: utf-8 -*-
import sys
l1ll111i1i11i1_vr_ = sys.version_info [0] == 2
l1l1l1i1i11i1_vr_ = 2048
l1ll1li1i11i1_vr_ = 7
def l1llll1i1i11i1_vr_ (l1i1i11i1_vr_):
	global l1l1ll1i1i11i1_vr_
	l1lll11li1i11i1_vr_ = ord (l1i1i11i1_vr_ [-1])
	l1ll11li1i11i1_vr_ = l1i1i11i1_vr_ [:-1]
	l1l1li1i11i1_vr_ = l1lll11li1i11i1_vr_ % len (l1ll11li1i11i1_vr_)
	l1l11i1i11i1_vr_ = l1ll11li1i11i1_vr_ [:l1l1li1i11i1_vr_] + l1ll11li1i11i1_vr_ [l1l1li1i11i1_vr_:]
	if l1ll111i1i11i1_vr_:
		l11lllli1i11i1_vr_ = unicode () .join ([unichr (ord (char) - l1l1l1i1i11i1_vr_ - (l11111i1i11i1_vr_ + l1lll11li1i11i1_vr_) % l1ll1li1i11i1_vr_) for l11111i1i11i1_vr_, char in enumerate (l1l11i1i11i1_vr_)])
	else:
		l11lllli1i11i1_vr_ = str () .join ([chr (ord (char) - l1l1l1i1i11i1_vr_ - (l11111i1i11i1_vr_ + l1lll11li1i11i1_vr_) % l1ll1li1i11i1_vr_) for l11111i1i11i1_vr_, char in enumerate (l1l11i1i11i1_vr_)])
	return eval (l11lllli1i11i1_vr_)
#'\nCreated on Thu Apr -18 2016\n\n@author: ramicspa\n'
import urllib2,urllib
import re
#import l1l1111l1i1i11i1_vr_
import json as json
UA='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
BASEURL='https://vider.info'
TIMEOUT = 30
def getUrl(url,data=None,headers={},cookies=None):
    if headers:
        my_header=headers
    else:
        my_header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'}
    req = urllib2.Request(url,data,my_header)
    if cookies:
        req.add_header('Cookie', cookies)
    try:
        response = urllib2.urlopen(req,timeout=TIMEOUT)
        link =  response.read()
        response.close()
    except:
        link=''
    return link
def _get_overflowtype(overflow):
    out=[]
    item = overflow[0]
    for item in overflow:
        href = re.compile('<a href="(.*?)"\\s*>').findall(item)
        img = re.compile('<img src="(.*?)">').findall(item)
        title = re.compile('<span class="txt_md">(.*?)</span>').findall(item)
        duration = re.compile('<i class="fa fa-clock-o"></i>(.*?)</span>',).findall(item)
        if href and title:
            one = {'href'   : BASEURL+href[0],
                   'title' : unicodePLchar(title[0]).strip() if title else '',
                   'img' : img[0],
                   'duration': duration[0].strip() if duration else ''
                   }
            out.append(one)
    return out
def _get_clearfixtype(clearfix):
    out=[]
    for item in clearfix:
        href_title = re.compile('<a href="(.+?)"\\s*class=".*"\\s*>(.*?)</a>').findall(item)
        img = re.compile('<img src="(.*?)" ').findall(item)
        meta = re.compile('<p class="meta">(.*?)</p>',re.DOTALL).findall(item)
        duration = re.compile('<div class="duration">(.*?)</div>').findall(item)
        plot = re.compile('<p class="description">(.*?)</p>').findall(item)
        status = re.findall('<div class="float-r badge_new">(.*?)</div>',item)
        if href_title:
            folder =''
            if meta:
                txt = ' '.join(x.strip() for x in re.compile('>(.*?)<',re.DOTALL).findall(meta[0])).strip()
                match1 = re.compile('Katalog\xc3\xb3w: \\d+ / Plik\xc3\xb3w: \\d+').findall(txt)
                match2 = True if 'Filmy:' in txt and 'Rozmiar:' in txt else False
                if match1:
                    folder = match1[0]
                elif match2:
                    folder = status[0] if status else ''
                    plot.append(txt)
            image=''
            if img:
                image = img[0]
                if not 'http' in image:
                   image =  BASEURL + image
            one = {'href'  : BASEURL+href_title[0][0],
                   'title' : unicodePLchar(href_title[0][1]).strip() if href_title else '',
                   'img' : image,
                   'folder': unicodePLchar(folder).strip(),
                   'duration': duration[0] if duration else '',
                   'plot' :unicodePLchar(plot[0]).strip() if plot else '',
                   }
            if one.get('folder'):
                one['title'] = '[COLOR lightblue]%s[/COLOR] - [COLOR lightgreen]%s[/COLOR]' %(one['title'], one.get('folder'))
            out.append(one)
    return out
def scanUser(url):
    out=[]
    my={}
    content=getUrl(url)
    overflow = re.compile('<div class="overflow">(.*?)</div>',re.DOTALL).findall(content)
    clearfix = re.compile('<li class="clearfix w-100-p">(.*?)</li>',re.DOTALL).findall(content)
    if overflow:
        out = _get_overflowtype(overflow)
        fileTreeLink = re.compile('<div class="CssTreeValue CssTreeValueMain"><a href="(.*?)"\\s*title="(.*?)"\\s*class="fileTreeLink">').findall(content)
        if fileTreeLink:
            img = re.findall('src="(https://img.vider.info/avatar/.*?)"',content)
            img = img[0] if img else ''
            my = {'href':BASEURL+fileTreeLink[0][0],'title':'[COLOR blue][Kolekcje video][/COLOR]','img':img,'folder':'yes'}
            out.insert(0,my)
    elif clearfix:
        out = _get_clearfixtype(clearfix)
    return out
def search(txt='tangled ever after'):
    out=[]
    url='https://vider.info/search/get'
    payload = {'search_phrase':txt,'search_type':'all','search_saved':0,'pages':1,'limit':150}
    headers= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest'}
    content=getUrl(url,data=json.dumps(payload),headers=headers)
    if content:
        data=json.loads(content)
        print data.keys()
        resp_data_data = data.get('response',{}).get('data_files',{}).get('data',[])
        for item in resp_data_data:
            one = {'href'  : 'http://vider.info/embed/video/'+item.get('id_url',''),
                   'title' : unicodePLchar(item.get('name','')).replace('',''),
                   'img' : '',
                   'folder': '',
                   'duration': item.get('duration',''),
                   'plot' : '',
                   }
            if one.get('folder'):
                one['title'] = '[COLOR blue]%s[/COLOR] - [COLOR green]%s[/COLOR]' %(one['title'], one.get('folder'))
            out.append(one)
    return out
import cookielib
url='https://vider.info/vid/+fn18xnn'
def getVideoUrls(url):
   # '    \n    returns \n        - ulr http://....\n    '
    if '/vid/' in url:
        url=url.replace('/vid/','/embed/video/')
    video_link=''
    if not '/embed/' in url:
        content = getUrl(url)
        embed = re.compile('<div class="video-frame ">[\\s\n]*<iframe src="(/embed/video/.*?)"').findall(content)
        if not embed:
            embed = re.compile('<iframe src="https://vider.info(/embed/video/.*?)"').findall(content)
        if embed:
            url = BASEURL+embed[0]
    content = getUrl(url)
    data = re.compile('data-video-url="(.*?)"').findall(content)
    if data:
        video_link=data[0]+'|Referer={}&User-Agent={}'.format(url,UA)
    return video_link
def unicodePLchar(txt):
    if type(txt) is not str:
        txt=txt.encode('utf-8')
    s='JiNcZCs7'
    txt = re.sub(s.decode('base64'),'',txt)
    txt = txt.replace('&lt;h5&gt;','')
    txt = txt.replace('&lt;/h5&gt;','')
    txt = txt.replace('&nbsp;','')
    txt = txt.replace('&lt;br/&gt;',' ')
    txt = txt.replace('&quot;','"').replace('&amp;quot;','"')
    txt = txt.replace('&oacute;','\xc3\xb3').replace('&Oacute;','\xc3\x93')
    txt = txt.replace('&amp;oacute;','\xc3\xb3').replace('&amp;Oacute;','\xc3\x93')
    txt = txt.replace('\\u0105','\xc4\x85').replace('\\u0104','\xc4\x84')
    txt = txt.replace('\\u0107','\xc4\x87').replace('\\u0106','\xc4\x86')
    txt = txt.replace('\\u0119','\xc4\x99').replace('\\u0118','\xc4\x98')
    txt = txt.replace('\\u0142','\xc5\x82').replace('\\u0141','\xc5\x81')
    txt = txt.replace('\\u0144','\xc5\x84').replace('\\u0144','\xc5\x83')
    txt = txt.replace('\\u00f3','\xc3\xb3').replace('\\u00d3','\xc3\x93')
    txt = txt.replace('\\u015b','\xc5\x9b').replace('\\u015a','\xc5\x9a')
    txt = txt.replace('\\u017a','\xc5\xba').replace('\\u0179','\xc5\xb9')
    txt = txt.replace('\\u017c','\xc5\xbc').replace('\\u017b','\xc5\xbb')
    return txt


