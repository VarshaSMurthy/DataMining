import brainExtraction
import os

def test():
    #print the current working directory. This directory should conatin the dataset directory as subdirectory
    print(os.getcwd())
    
    #set the data set folder path
    dataset_folder_path="./Data/"
    
    #path to folder to save the sliced images
    output_folder="./Slices/"
    
    #loop through all the images present in the dataset
    for files in os.listdir(dataset_folder_path):
        #Only slice and contour the images ending with _thresh.png in dataset folder
        if files.endswith("_prob.png"):
            #function to slice the ICMR images
            brainExtraction.main(os.path.join(dataset_folder_path,files),output_folder)
            
    #function to remove the images without brain data
    #brainExtraction.filterImage()
    
    #path to pass to contouring function. This path/directory should conatins both slice and boundaries directory as sub-directory
    path=os.getcwd()
    
    #function to perform contouring on sliced images
    brainExtraction.conturing(path)

if __name__=="__main__":
    test()