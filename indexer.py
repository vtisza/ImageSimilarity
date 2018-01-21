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

def parse_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_path', help='path to folder to index', type=str, required=True)
    parser.add_argument('-l', '--limit', help='max number of images', type=int, required=False)
    parser.add_argument('-m', '--model', help='model to use', type=str, required=False)
    args = parser.parse_args()
    input_path=args.input_path
    if (args.limit):
        limit=args.limit
    else:
        limit=1000000
    if (args.model):
            model_type=args.model
    else:
        model_type="VGG16"
    return input_path,limit,model_type

def create_model(type="VGG16"):
    model = keras.applications.VGG16(weights='imagenet', include_top=True)
    feat_extractor = Model(inputs=model.input, outputs=model.get_layer("fc2").output)
    return feat_extractor

def list_images(images_path,max_num_images):
    images = [os.path.join(dp,f) for dp, dn, filenames in os.walk(images_path) for f in filenames if os.path.splitext(f)[1].lower() in ['.jpg','.png','.jpeg']]
    images=[image.replace("\\","/") for image in images]
    if max_num_images < len(images):
        images = [images[i] for i in sorted(random.sample(xrange(len(images)), max_num_images))]
    print("keeping %d images to analyze" % len(images))
    return images

def get_image(path):
    img = image.load_img(path, target_size=[224,224])
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return img, x

def predict_images(images,feat_extractor):
    features = []
    new_images=[]
    for image_path in tqdm(images):
        try:
            img, x = get_image(image_path);
            feat = feat_extractor.predict(x)[0]
            features.append(feat)
            new_images.append(image_path)
        except:
            print("problem with {}".format(image_path))
    return features,new_images

def make_pca(features,n_components=200):
    features = np.array(features)
    pca = PCA(n_components=n_components)
    pca.fit(features)
    pca_features = pca.transform(features)
    return pca_features,pca

def save_variables(features,pca,images):
    pickle.dump( features, open( "features.dat", "wb" ) )
    pickle.dump( pca, open( "pca.model", "wb" ) )
    pickle.dump( images, open( "images.list", "wb" ) )
    print("Files saved")

def main():
    input_path,limit,model_type=parse_arg()
    model=create_model(model_type)
    images=list_images(input_path,limit)
    features,images=predict_images(images,model)
    features, pca=make_pca(features)
    save_variables(features,pca,images)
    print("Indexation completed")

if __name__ == "__main__":
    main()