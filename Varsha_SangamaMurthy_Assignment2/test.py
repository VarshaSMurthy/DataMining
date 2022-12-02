import os
from clustering import brain_extraction, filterImage, clusters

cur_dir = os.getcwd()

source_path = './testData'

if not os.path.exists(cur_dir + '/Slices/'):
    os.mkdir(cur_dir + '/Slices/')

if not os.path.exists(cur_dir + '/Clusters/'):
    os.mkdir(cur_dir + '/Clusters/')

if __name__ == '__main__':
    image_list = os.listdir(source_path)
    for image in image_list:
        if "thresh" in image:
            split_text = os.path.splitext(image)
            sliced_images_path = cur_dir + '/Slices/' + split_text[0]
            cluster_path = cur_dir + '/Clusters/' + split_text[0]
            brain_extraction(image, cluster_path, sliced_images_path)

    # function to remove the images without brain data
    filterImage()
    # path to pass to contouring function. This path/directory should contain both slice and boundaries directory as
    # subdirectory
    path = os.getcwd()
    # function to perform contouring on sliced images
    clusters(path)
