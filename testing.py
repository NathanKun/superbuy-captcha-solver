import os
import string
import numpy as np
from tqdm import tqdm
from PIL import Image
from keras.utils.np_utils import to_categorical
from keras.models import *

folder     = os.getcwd() + '\\images\\'
characters = string.digits + string.ascii_lowercase
width      = 120
height     = 50
n_len      = 4
n_class    = len(characters)

# generator
def gen(batch_size = 32):
    X = np.zeros((batch_size, height, width, 3), dtype = np.uint8)
    y = [np.zeros((batch_size, n_class), dtype = np.uint8) for i in range(n_len)]
    
    captcha_folder_names = os.listdir(folder)
    
    while True:
        for captcha_text in captcha_folder_names:
            i = 0
            captcha_text = captcha_text.split("_")[0]
            
            for i_image in range(128):
                i = i + 1
                captcha_image_names = str(i_image) + '.png'
                image_path = folder + captcha_text + '\\' + captcha_image_names
                
                img = Image.open(image_path).convert("RGB")
                X[i] = img
                
                for j, ch in enumerate(captcha_text):
                    y[j][i, :] = 0
                    y[j][i, characters.find(ch)] = 1
                
                if i == 31:
                    i = 0
                    yield X, y
        print("Generator restart")

def decode(y):
    y = np.argmax(np.array(y), axis=2)[:,0]
    return ''.join([characters[x] for x in y])

def evaluate(model, batch_num=20):
    batch_acc = 0
    generator = gen()
    for i in tqdm(range(batch_num)):
        X, y = next(generator)
        y_pred = model.predict(X)
        y_pred = np.argmax(y_pred, axis=2).T
        y_true = np.argmax(y, axis=2).T
        batch_acc += np.mean(map(np.array_equal, y_true, y_pred))
    return batch_acc / batch_num


def main():
    # model
    model = load_model('2019-01-11_171854.281505.h5')
    
    generator = gen()
    for i in range(256):
        X, y = next(generator)
        y_pred = model.predict(X)
        print('real: %s\npred:%s'%(decode(y), decode(y_pred)))
    
    evaluate(model)
    

if __name__ == '__main__':
    main()
