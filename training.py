'''
TF: https://www.tensorflow.org/install/pip
CPU
pip3 install --user --upgrade https://storage.googleapis.com/tensorflow/windows/cpu/tensorflow-1.12.0-cp36-cp36m-win_amd64.whl
pip install keras
pip install matplotlib
pip install pillow
pip install pydot
Graphzy: https://graphviz.gitlab.io/_pages/Download/Download_windows.html
'''
import os
import string
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from PIL import Image
from keras.utils.np_utils import to_categorical
from keras.models import *
from keras.layers import *

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

def main():
    # model
    input_tensor = Input((height, width, 3))
    x = input_tensor

    for i in range(4):
        x = Conv2D(filters = 32 * 2 ** i, kernel_size = (3, 3), activation = 'relu')(x)
        x = Conv2D(filters = 32 * 2 ** i, kernel_size = (3, 3), activation = 'relu')(x)
        x = BatchNormalization()(x)
        x = MaxPooling2D(pool_size=(2, 2), data_format="channels_first")(x)

    x = Flatten()(x)
    x = Dropout(0.25)(x)
    x = [Dense(n_class, activation='softmax', name='c%d'%(i+1))(x) for i in range(4)]
    model = Model(inputs=input_tensor, outputs=x)

    model.compile(loss='categorical_crossentropy',
                  optimizer='adadelta',
                  metrics=['accuracy'])

    # model visualization                  
    from keras.utils.vis_utils import plot_model
    plot_model(model, to_file="model.png", show_shapes=True)

    # training
    model.fit_generator(gen(), validation_data=gen(), epochs=20,
                        steps_per_epoch=1024, validation_steps=256,
                        workers=1, use_multiprocessing=False)

    # save
    model.save(str(datetime.now()).replace(':', '').replace(' ', '_') + '.h5')
    

if __name__ == '__main__':
    main()
