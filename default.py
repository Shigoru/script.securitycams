'''

This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) License.



To view a copy of this license, visit

German version:  http://creativecommons.org/licenses/by-nc-sa/4.0/deed.de

English version: http://creativecommons.org/licenses/by-nc-sa/4.0/



or send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California, 94105, USA.

'''


import xbmc
import xbmcgui
import xbmcvfs
import xbmcaddon
import os.path
from urllib import urlretrieve
from PIL import Image
from threading import Thread


addon   = xbmcaddon.Addon()
addonid = addon.getAddonInfo('id')
addonname = addon.getAddonInfo('name')


ACTION_PREVIOUS_MENU = 10
ACTION_STOP = 13
ACTION_NAV_BACK = 92
ACTION_BACKSPACE = 110



class CamWindow(xbmcgui.WindowDialog):
    def __init__(self):
        path = xbmc.translatePath('special://profile/addon_data/%s' %addonid )
        loader = xbmc.translatePath('special://home/addons/%s/resources/loader.gif' %addonid )
        

        if not xbmcvfs.exists(path):
            xbmcvfs.mkdir(path)


        urls = [
        addon.getSetting('URL1'),
        addon.getSetting('URL2'),
        addon.getSetting('URL3'),
        addon.getSetting('URL4'),
        addon.getSetting('URL5'),
        addon.getSetting('URL6')

        # Test URLs with Webcams
        #'http://webcams.passau.de/cam-rathaus-huge-aktuell.jpg',
        #'http://www.mediac2.de/projekte/webcam/wallstrasse/aktuell/aktuell.jpg',
        #'http://www.cityscope.de/bmw/current_pano.jpg',
        #'http://www.goldbeck.de/uploads/webcam/df0691/current.jpg',
        #'http://62.157.185.131/record/current.jpg',
        #'http://webcams.passau.de/cam-rathaus-huge-aktuell.jpg'
        ]


        files = [
        os.path.join(path, '1.0.jpg'),
        os.path.join(path, '2.0.jpg'),
        os.path.join(path, '3.0.jpg'),
        os.path.join(path, '4.0.jpg'),
        os.path.join(path, '5.0.jpg'),
        os.path.join(path, '6.0.jpg')
        ]


        coords = (
            (12, 360, 205, 160),
            (222, 360, 205, 160),
            (432, 360, 205, 160),
            (642, 360, 205, 160),
            (852, 360, 205, 160),
            (1062, 360, 205, 160),
        )


        imgs = []
        for c, f in zip(coords, files):
            # aspectRatio: integer - (values 0 = stretch (default), 1 = scale up (crops), 2 = scale down (black bars)
            img = xbmcgui.ControlImage(*c, filename=loader, aspectRatio = 0)
            self.addControl(img)            
            imgs.append(img)


        # workaround - superimposed image controls to prevent flicker
        imgs2 = []
        for c, f in zip(coords, files):
            img = xbmcgui.ControlImage(*c, filename='', aspectRatio = 0)
            self.addControl(img)            
            imgs2.append(img)
        

        cams = [list(l) for l in zip(urls, files, imgs, imgs2)]


        self.show()        
        self.isRunning = True


        for i, c in enumerate(cams):
            t = Thread(target=self.getImages, args=(i, c, path))
            t.start()


        while (not xbmc.abortRequested) and (self.isRunning):       
            xbmc.sleep(1000)   


        for i in xbmcvfs.listdir(path)[1]:
            if i <> "settings.xml":
                xbmcvfs.delete(os.path.join(path, i))



    def getImages(self, i, c, path):
        x=0
        while (not xbmc.abortRequested) and (self.isRunning):
            try:
                x+=1
                c[1] = os.path.join(path, '%d.%d.jpg') %(i, x)
                urlretrieve(c[0], c[1])
                c[2].setColorDiffuse('0xFFFFFFFF')
                c[3].setColorDiffuse('0xFFFFFFFF')
                c[2].setImage(c[1], useCache=False)                
                xbmcvfs.delete(os.path.join(path, '%d.%d.jpg') %(i, x-1))
                c[3].setImage(c[1], useCache=False)               
            except Exception, e:
                xbmc.log(str(e))
                #error = xbmc.translatePath('special://home/addons/%s/resources/error.png' %addonid )
                #c[2].setImage(error, useCache=False)
                c[2].setColorDiffuse('0xC0FF0000')
                c[3].setColorDiffuse('0xC0FF0000')


    def onAction(self, action):
        if action in (ACTION_PREVIOUS_MENU, ACTION_STOP, ACTION_NAV_BACK, ACTION_BACKSPACE):
            self.isRunning = False
            self.close()

            

CW = CamWindow()
del CW

