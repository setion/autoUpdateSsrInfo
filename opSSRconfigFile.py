#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import GetSsrInfo
import time
import os

# workPath = "E:\Nutstore\shadowsocks-gui-0.6.2-win-ia32\ShadowsocksR-4.7.0-win\\"
workPath = os.path.abspath('..') + '\\'
# print workPath
ret = os.popen('tasklist|find "ShadowsocksR"')
if ret.read().find('ShadowsocksR') == -1:
    print 'SSR is not running,will run SSR'
    print workPath+'ShadowsocksR-dotnet4.0.exe'
    os.popen('start /b '+ workPath + 'ShadowsocksR-dotnet4.0.exe')
else:
    print 'SSR is running'

def LoopUpdateConfigFile(SSRinfo):
    write=0
    fopen = open(workPath+'gui-config.json')
    configContent =  fopen.read()
    fopen.close()
    configJson = json.loads(configContent)
    
    if SSRinfo[0] == configJson['configs'][-1]['server'] or configJson['configs'][-1]['remarks_base64'] == '5p2l6Ieq5Z-65Y-L55qEQnVmZg' : #if serverAddr or remarks same,then update
        if SSRinfo[1] != str(configJson['configs'][-1]['server_port']) or SSRinfo[5] != str(configJson['configs'][-1]['password']):
            print 'ssr info changed, will update ssr info'
            write = 1
            configJson['configs'][-1]['server_port'] = SSRinfo[1]
            configJson['configs'][-1]['password'] = SSRinfo[5]
            configJson['configs'][-1]['method'] = SSRinfo[3]
            configJson['configs'][-1]['protocol'] = SSRinfo[2]
            configJson['configs'][-1]['obfs'] = SSRinfo[4]
            configJson['configs'][-1]['remarks'] = '来自基友的Buff'
            configJson['configs'][-1]['remarks_base64'] = '5p2l6Ieq5Z-65Y-L55qEQnVmZg'
            configJson['configs'][-1]['group'] = '来自基友的Buff'
        else:
            print 'ssr info not change'
        
    else:
        print 'get new ssr info, will add new info'
        write = 1
        configJson['configs'].append({
                    "remarks" : "来自基友的Buff",
                    "id" : "B8AB81B219FFFE42B1BE2D9B1D97420D",
                    "server" : SSRinfo[0],
                    "server_port" : SSRinfo[1],
                    "server_udp_port" : 0,
                    "password" : SSRinfo[5],
                    "method" : SSRinfo[3],
                    "protocol" : SSRinfo[2],
                    "protocolparam" : "",
                    "obfs" : SSRinfo[4],
                    "obfsparam" : "",
                    "remarks_base64" : "5p2l6Ieq5Z-65Y-L55qEQnVmZg",
                    "group" : "来自基友的Buff",
                    "enable" : True,
                    "udp_over_tcp" : False
                    })
    if write == 1:
        configJson['index']=len(configJson['configs'])-1
        ret = os.popen('taskkill -f -im ShadowsocksR-*')
        print ret.read().decode('GBK').encode('utf-8')+'end'
        fw = open(workPath+'gui-config.json','w')
        fw.write(json.dumps(configJson))
        fw.close()
        fw = open(workPath+'update.log','a')
        print 'write log\n run SSR'
        fw.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n')
        fw.close()
        os.popen('start /b '+ workPath + 'ShadowsocksR-dotnet4.0.exe')
        print 'run SSR success'
    # print configJson['configs'][len(configJson['configs'])-1]
def DetectSsrServer():
    for x in range(3):
        ret =os.popen(workPath + 'curl --socks5 127.0.0.1:1080 https://google.com -k')
        tempStdout = ret.read()
        print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        if tempStdout == '':
            print '[######cannot connect to google[-1]######]'
        elif tempStdout.find('Failed')!= -1:
            print '[######connect to google failed[-2]######]'
        elif tempStdout.find('www.google.com') != -1:
            print '[######connect to google OK!!######]'
            return True
        else:
            print '[######connect to google failed[-3]######]'
    print 'will return false'
    return False
    
def updateSsrInfo():
    pass
def GetSsrInfo():
    SSRinfo = SSR_Detect.GetSSRinfo()
    return SSRinfo
currConfigIndex = 0
preConfigIndex = -1
while True:
    if DetectSsrServer():
        time.sleep(120)
    else:
        SsrInfo = GetSsrInfo()
        if currConfigIndex >= len(SsrInfo):
            currConfigIndex = 0
        for x in range(currConfigIndex,len(SsrInfo)):
            tempInfo = SsrInfo[x]
            print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            print 'currConfigIndex = %d, will use config [%d] %s' % (preConfigIndex , x , str(tempInfo))
            currConfigIndex = x+1
            preConfigIndex = x
            LoopUpdateConfigFile(tempInfo)
            if DetectSsrServer():
#                 time.sleep(60)
                break
