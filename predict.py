from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import model_from_json
import numpy as np



def load_model():

    with open("model.json", 'r') as model_file:
        model_json = model_file.read()

    model = model_from_json(model_json)

    model.load_weights('model.h5')
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    print('Loaded model')

    return model


def predict_class(model, image_path):

    print('predicting image')

    image_file = image.load_img(image_path, target_size=(64, 64))
    image_file = image.img_to_array(image_file)
    image_file = np.expand_dims(image_file, axis=0)
    result = model.predict(image_file)[0]
    
    max_pred, max_class = 0, 0

    for i in range(len(result)):
        if result[i] > max_pred:
            max_pred = result[i]
            max_class = i

    if max_class == 0:
        return 'other'
    elif max_class == 1:
        return 'wild_fire'
    else:
        return 'residential_fire'


model = load_model()


def get_model():

    return model



