import os
import random
import string
from datetime import datetime
from io import BytesIO

import requests
import matplotlib.pyplot as plt
from PIL import Image

url = 'https://login.superbuy.com/api/site/captcha'
folder = os.getcwd() + '\\images\\'

def genCookieHeaders():
    phpsessid = 'PHPSESSID=' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=26))
    return {'Cookie': phpsessid}

def getCaptcha(batch = 128):
    # generate new PHPSESSID
    headers = genCookieHeaders()

    # send first request
    requestContent = requests.get(url, headers=headers).content

    # convert to image
    firstImage = Image.open(BytesIO(requestContent))

    # plot
    imgplot = plt.imshow(firstImage)
    plt.show()

    # input the captcha text
    captchaText = input("Enter the captcha:\n")

    # mkdir
    targetFolder = folder + captchaText + '\\'
    os.mkdir(targetFolder)

    # save first image
    with open(targetFolder + '0.png', 'wb') as f:
        f.write(requestContent)

    # download more images
    print('Downloading ' + str(batch) + ' images for captcha ' + captchaText + '...')
    for i in range(1, batch):
        with open(targetFolder + str(i) + '.png', 'wb') as f:
            f.write(requests.get(url, headers=headers).content)

def main():
    getCaptcha()

if __name__ == '__main__':
    
    main()
