from pathlib import Path
from typing import Tuple, List

from PIL import Image

from pdf2image import convert_from_path

from src.imageprocessing.pixelcluster import PixelCluster


def load_images_from_path(path:Path)->List:
    result = []

    #the partial loading is for speed while debugging
    for file_el in sorted(list(path.iterdir()))[0:2]:

        result.append(Image.open(file_el))


    return result




def split_image_into_clusters(image:Image)->List[PixelCluster]:

    result = []
    coordinates = extract_coordinates(image, (255, 0, 127))

    indexes = interpret_coordinates(coordinates)
    for i in range(0,len(indexes)-1):
        cluster = PixelCluster(coordinates[indexes[i]:indexes[i+1]])
        result.append(cluster)
    return result

def convert_to_image():


    # Store Pdf with convert_from_path function
    images = convert_from_path('data.pdf')

    for i,img in enumerate(images):
        img.save("./data/output"+ str(i).zfill(2)+".jpg", 'JPEG')


def test_image():
    cluster_list = []
    images = load_images_from_path(Path("./data/").resolve())
    for el in images:
        clusters = split_image_into_clusters(el)
        cluster_list.append(clusters)

    print(cluster_list)
    pass
    exit(-1)




def interpret_coordinates(coordinates: List[Tuple]) -> List[int]:
    indexes = [0]
    for i, tuple_el in enumerate(coordinates[0 : len(coordinates) - 1]):
        x_i = int(coordinates[i][0])
        x_i_plus_one = int(coordinates[i + 1][0])
        print(abs(x_i - x_i_plus_one))
        if abs(x_i - x_i_plus_one) > 25:
            indexes.append(i)
    indexes.append(len(coordinates)-1)
    return indexes




def extract_coordinates(img, rbg_tuple: tuple) -> List[Tuple]:
    result = []
    rbg_list = []
    pix = img.load()
    for x in range(200, img.size[0]):
        for y in range(1300, 1500):

            if pix[x, y] not in rbg_list:
                rbg_list.append(pix[x, y])

            actual_tuple = pix[x,y]
            diff = 0
            for i in range(0,3):
                diff = diff + abs(actual_tuple[i]-rbg_tuple[i])
            if diff < 20:
                print((x,y))
                result.append((x, y))


    return result
