import time
import sys
import os
import argparse
import random
import pickle
import numpy as np
import keras
from keras.preprocessing import image
from keras.applications.imagenet_utils import decode_predictions, preprocess_input
from keras.models import Model
from sklearn.decomposition import PCA
from scipy.spatial import distance
from tqdm import tqdm

def create_model(type="VGG16"):
    model = keras.applications.VGG16(weights='imagenet', include_top=True)
    feat_extractor = Model(inputs=model.input, outputs=model.get_layer("fc2").output)
    return feat_extractor

def get_image(path):
    img = image.load_img(path, target_size=[224,224])
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return img, x

def get_closest_images(feature, pca_features, images,num_results=10):
    distances = [ distance.euclidean(feature, feat) for feat in pca_features ]
    idx_closest = sorted(range(len(distances)), key=lambda k: distances[k])[1:num_results+1]
    distances = list(np.array(distances)[idx_closest])
    images=list(np.array(images)[idx_closest])
    return images, distances

def get_concatenated_images(indexes, thumb_height):
    thumbs = []
    for idx in indexes:
        img = image.load_img(new_images[idx])
        img = img.resize((int(img.width * thumb_height / img.height), thumb_height))
        thumbs.append(img)
    concat_image = np.concatenate([np.asarray(t) for t in thumbs], axis=1)
    return concat_image

def load_files():
    features=pickle.load( open( "./data/features.dat", "rb" ) )
    pca=pickle.load( open( "./data/pca.model", "rb" ) )
    images=pickle.load( open( "./data/images.list", "rb" ) )
    return features,pca,images

def predict_picture(picture_path,model,pca):
    img, x = get_image(picture_path);
    feat = model.predict(x)[0]
    feat=pca.transform(feat.reshape(1,-1))
    return feat

def closest(picture_path):
    features,pca,images=load_files()
    model=create_model()
    feat=predict_picture(picture_path,model,pca)
    sim_images, distances=get_closest_images(feat, features, images)
    return sim_images, distances

if __name__ == "__main__":
    closest()