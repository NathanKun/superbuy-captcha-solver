import os
import random
import string
import threading
from datetime import datetime
from io import BytesIO

import requests
import matplotlib.pyplot as plt
from PIL import Image

url = 'https://login.superbuy.com/api/site/captcha'
folder = os.getcwd() + '\\images\\'

class downloadCaptchaThread (threading.Thread):
    def __init__(self, threadID, headers, captchaText, imgsPerThread, targetFolder):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = 'Thread-' + str(threadID) + '-' + captchaText
        self.headers = headers
        self.captchaText = captchaText
        self.imgsPerThread = imgsPerThread
        self.targetFolder = targetFolder
        
    def run(self):
        print ("开始线程：" + self.name)

        # download images
        print('Downloading ' + str(self.imgsPerThread) + ' images for captcha ' + self.captchaText + '...')
        for i in range(1, self.imgsPerThread):
            with open(self.targetFolder + str(i) + '.png', 'wb') as f:
                f.write(requests.get(url, headers=self.headers).content)
        
        print ("退出线程：" + self.name)



def genCookieHeaders():
    phpsessid = 'PHPSESSID=' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=26))
    return {'Cookie': phpsessid}



def main():
    imgsPerThread = 128
    nbOfThreads = 5
    threads = [None] * nbOfThreads

    for threadCount in range(nbOfThreads):
        # generate new PHPSESSID
        headers = genCookieHeaders()

        # send first request
        requestContent = requests.get(url, headers = headers).content

        # convert to image
        firstImage = Image.open(BytesIO(requestContent))

        # plot
        imgplot = plt.imshow(firstImage)
        plt.show()

        # input the captcha text
        captchaText = input('Enter the captcha:\n')
        
        # mkdir
        targetFolder = folder + captchaText + '\\'
        os.mkdir(targetFolder)

        # save first image
        with open(targetFolder + '0.png', 'wb') as f:
            f.write(requestContent)

        thread = downloadCaptchaThread(threadCount, headers, captchaText, imgsPerThread, targetFolder)
        thread.start()
        threads[threadCount] = thread

    for t in threads:
        t.join()

    print ("退出主线程")

if __name__ == '__main__':
    main()
