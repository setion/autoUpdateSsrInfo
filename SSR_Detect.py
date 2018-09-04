#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import re
import base64

def CatchSSRinfo():
    url='https://us.ishadowx.net/'
    header ={'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'}
    request = urllib2.Request(url,headers=header)
    response = urllib2.urlopen(request)
    
    responseText = response.read() 
    startPos =  responseText.find('<div class="col-sm-6 col-md-4 col-lg-4 ssr">')
    endPos = responseText.find('<div class="row text-center center">')
    serverInfo = responseText[startPos:endPos]
    # print serverInfo
    addrRe = re.compile('<span id="ipssr.">([\w|\.]*)</span>')
    addrGroups = addrRe.findall(serverInfo)
    
    portRe = re.compile('<h4>Port:<span id="portssr.">(\d*)')
    portGroups = portRe.findall(serverInfo)
    
    pwdRe = re.compile('<h4>Password:<span id="pwssr.">(.*)')
    pwdGroups = pwdRe.findall(serverInfo)
    
    methodRe = re.compile('<h4>Method:(.*)</h4>')
    methodGroups = methodRe.findall(serverInfo)
    
    protocolRe = re.compile('<h4>(.{,16}) .{,22}</h4>')
    protocolGroups = protocolRe.findall(serverInfo)
    
    obfsRe = re.compile('<h4>.{,16} (.{,22})</h4>')
    obfsGroups = obfsRe.findall(serverInfo)
    
    
#     print addrGroups
#     print portGroups
#     print pwdGroups
#     print methodGroups
#     print protocolGroups
#     print obfsGroups
    if addrGroups:
        params_r=[]

        for x in range(len(addrGroups)):
            
            if addrGroups[x] and portGroups[x] and pwdGroups[x] and methodGroups[x] and protocolGroups[x] and obfsGroups[x]:
                pwdBase64 = base64.b64encode(pwdGroups[x])
                params = [addrGroups[x],portGroups[x],protocolGroups[x],methodGroups[x],obfsGroups[x],pwdBase64]#
                params_r.append([addrGroups[x],portGroups[x],protocolGroups[x],methodGroups[x],obfsGroups[x],pwdGroups[x]])
                ssrURL = base64.b64encode(':'.join(params)+'/?obfsparam=')
                ssrURL = ssrURL.replace('=','')
                ssrURL = ssrURL.replace('+','-')
                ssrURL = 'ssr://' + ssrURL.replace('/','_')
                print params_r[-1]
                print ssrURL
        return params_r
# CatchSSRinfo()