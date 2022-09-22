# DataMining Project1:- Extracting Brain boundaries from rs-fMRI data

Python libraries required are as follows:
1. os
2. numpy
3. opencv
4. PIL

Purpose  
In this project you will extract the brain boundaries from the resting state functional magnetic resonance 
imaging (rs-fMRI) scans 

Objectives  
Students will be able to:  
● Extract brain slices from the data set.  
● Extract the brain boundary (periphery) from those slices.  
  
Technology Requirements  
Python 3.6 to 3.9  


  
Figure 1  
Directions  
Dataset:  
You will be given one patient’s dataset which will contain approximately 100 spatial ICs images of that patient’s 
rs-fMRI scan. All the scans will look like figure 1 (except the blood activation (red/blue clusters) part).  
  
Analysis Procedure:  
Given the spatial images of patients, your task will be divided into two parts:  
a) Brain  slice  extraction:  Given  a  spatial  IC,  automate the brain  slices  extraction  process.  For  example, the  IC  in 
figure 1 will have brain slice images like figure 2. So, if a patient has N such images, your task is to automate the 
slice extraction for all the N images.  
  
![image](https://user-images.githubusercontent.com/73743263/191850870-ca8e297b-308f-464f-aba7-15348d6b2ac7.png)
  
  
Figure 2  
b) Brain boundary extraction: Once you have extracted the brain slices, the next task is to extract the boundary of 
the brain in every extracted slice. 

Submit two python files,  
a) brainExtraction.py 
b) test.py 
The brainExtraction.py reads all the images (images those end with word “thresh”) from the given data and 
perform the brain slice extraction and brain boundary extraction. The test.py reads a folder named ‘testPatient’ 
and outputs two folders. One folder named “Slices” and another folder named ‘’Boundaries’. ‘Slices’ folder will 
further have ‘N’ number of folders where N is number of images that ends with “thresh”. for example, in the given 
data we have N=112 (‘testPatient’ will have different ‘N’). Every image folder  should  contain  the  brain  slices 
images of that IC_thresh image. Similarly, another folder “Boundaries” will also have N number of folders and 
every folder will have boundary highlighted images of that IC_thresh image. 
