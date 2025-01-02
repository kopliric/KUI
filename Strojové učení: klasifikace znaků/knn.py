'''
Machine Learning: k-Neirest Neighbours classifier

author: Richard Koeplinger
contact: kopliric@fel.cvut.cz
date: 28/05/2023
'''

import os
import csv
import string
import argparse
from PIL import Image
import numpy as np


def setup_arg_parser():
    parser = argparse.ArgumentParser(description='Learn and classify image data.')
    parser.add_argument('train_path', type=str, help='path to the training data directory')
    parser.add_argument('test_path', type=str, help='path to the testing data directory')
    parser.add_argument('-k', type=int, default=4, 
                        help='run k-NN classifier (if k is 0 the code may decide about proper K by itself')
    parser.add_argument("-o", metavar='filepath', 
                        default='classification.dsv',
                        help="path (including the filename) of the output .dsv file with the results")
    return parser

def load_train_dataset(directory):
    images = []
    labels = []

    with open(os.path.join(directory, 'truth.dsv'), 'r') as file:
        reader = csv.reader(file, delimiter=':')
        for row in reader:
            filename = row[0]
            label = row[1]

            image_path = os.path.join(directory, filename)
            image = np.array(Image.open(image_path)).astype(int).flatten()

            images.append(image)
            labels.append(label)

    images = np.array(images)
    labels = np.array(labels)

    if all(label.isdigit() for label in labels):
        label_map = {str(digit): digit for digit in range(10)}
        reverse_label_map = {digit: str(digit) for digit in range(10)}
    else:
        label_map = {**{str(digit): digit for digit in range(10)},
                     **{letter: idx for idx, letter in enumerate(string.ascii_uppercase)}}
        reverse_label_map = {value: key for key, value in label_map.items()}

    labels = np.array([label_map[label] for label in labels])
    return images, labels, reverse_label_map

def load_test_dataset(directory):
    images = []
    filenames = []

    for filename in os.listdir(directory):
        image_path = os.path.join(directory, filename)
        image = np.array(Image.open(image_path)).astype(int).flatten()

        images.append(image)
        filenames.append(filename)

    images = np.array(images)
    filenames = np.array(filenames)

    return images, filenames

def calculate_distance(image1, image2):
    diff = image1 - image2
    distance = np.sqrt(np.sum(np.square(diff)))
    return distance

def knn_classifier(images_train, labels_train, k, test_sample):
    distances = [calculate_distance(test_sample, train_sample) for train_sample in images_train]
    nearest_indices = np.argsort(distances)[:k]
    nearest_labels = labels_train[nearest_indices]
    predicted_label = np.argmax(np.bincount(nearest_labels))
    return predicted_label

def recognize_character(train_directory, test_directory, k, output_file):
    images_train, labels_train, reverse_label_map = load_train_dataset(train_directory)
    images_test, test_filenames = load_test_dataset(test_directory)

    with open(output_file, 'w') as file:
        writer = csv.writer(file, delimiter=':')
        for i in range(len(images_test)):
            test_image = images_test[i]
            test_filename = test_filenames[i]
            predicted_label = knn_classifier(images_train, labels_train, k, test_image)
            predicted_label = reverse_label_map[predicted_label]
            writer.writerow([test_filename, predicted_label]) 

def main():
    parser = setup_arg_parser()
    args = parser.parse_args()
    train_directory = args.train_path
    test_directory = args.test_path
    k = args.k
    if k == 0:
        k = 4
    output_file = args.o
    
    recognize_character(train_directory, test_directory, k, output_file)    

        
if __name__ == "__main__":
    main()
    
