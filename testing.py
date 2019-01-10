import os
import string
import numpy as np
from PIL import Image
from keras.utils.np_utils import to_categorical
from keras.models import *

folder     = os.getcwd() + '\\images\\128\\'
characters = string.digits + string.ascii_lowercase
width      = 120
height     = 50
n_len      = 4
n_class    = len(characters)

# generator
def gen(batch_size = 128):
    X = np.zeros((batch_size, height, width, 3), dtype = np.uint8)
    y = [np.zeros((batch_size, n_class), dtype = np.uint8) for i in range(n_len)]
    
    captcha_folder_names = os.listdir(folder)
    
    for captcha_text in captcha_folder_names:
    
        for i_image in range(batch_size):
            captcha_image_names = str(i_image) + '.png'
            image_path = folder + captcha_text + '\\' + captcha_image_names
            
            img = Image.open(image_path).convert("RGB")
            X[i_image] = img
            
            for j, ch in enumerate(captcha_text):
                y[j][i_image, :] = 0
                y[j][i_image, characters.find(ch)] = 1
        
        yield X, y

def decode(y):
    y = np.argmax(np.array(y), axis=2)[:,0]
    return ''.join([characters[x] for x in y])

def main():
    # model
    model = load_model('2019-01-10_154336.842906.h5')
    generator = gen(1)
    for i in range(128):
        X, y = next(generator)
        y_pred = model.predict(X)
        print('real: %s\npred:%s'%(decode(y), decode(y_pred)))
    

if __name__ == '__main__':
    main()
