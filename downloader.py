import os
import random
import string
import threading
import time
from datetime import datetime
from io import BytesIO

import requests
import tkinter as tk 
from PIL import Image, ImageTk

url = 'https://login.superbuy.com/api/site/captcha'
folder = os.getcwd() + '\\images\\'

class downloadCaptchaThread (threading.Thread):
    def __init__(self, threadID, headers, captchaText, imgsPerThread, targetFolder):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = 'T-' + str(threadID) + '-' + captchaText
        self.headers = headers
        self.captchaText = captchaText
        self.imgsPerThread = imgsPerThread
        self.targetFolder = targetFolder
        
    def run(self):
        print ("Start Thread " + self.name)

        # download images
        print('Downloading ' + str(self.imgsPerThread) + ' images for captcha ' + self.captchaText + '...')
        for i in range(1, self.imgsPerThread):
            with open(self.targetFolder + str(i) + '.png', 'wb') as f:
                f.write(requests.get(url, headers=self.headers).content)
        
        print ("End Thread " + self.name)



def genCookieHeaders():
    phpsessid = 'PHPSESSID=' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=26))
    return {'Cookie': phpsessid}



def main():
    imgsPerThread = 128
    nbOfThreads = 64
    threads = [None] * nbOfThreads

    for threadCount in range(nbOfThreads):
        # generate new PHPSESSID
        headers = genCookieHeaders()

        # send first request
        requestContent = requests.get(url, headers = headers).content

        # convert to image
        #firstImage = Image.open(BytesIO(requestContent))

        # plot
        #root = tk.Tk()
        #tkimage = ImageTk.PhotoImage(firstImage)
        #tk.Label(root, image=tkimage).pack()
        #root.focus_force()
        #root.mainloop()

        # input the captcha text
        #captchaText = input('Enter the captcha:\n')
        
        captchaText = ''.join(random.choices(string.ascii_uppercase, k=10))
        
        # mkdir
        targetFolder = folder + captchaText + '\\'
        os.mkdir(targetFolder)

        # save first image
        with open(targetFolder + '0.png', 'wb') as f:
            f.write(requestContent)

        thread = downloadCaptchaThread(threadCount, headers, captchaText, imgsPerThread, targetFolder)
        thread.start()
        threads[threadCount] = thread
        
        time.sleep(1)

    for t in threads:
        t.join()

    print ("Exit Main Thread")

if __name__ == '__main__':
    main()
