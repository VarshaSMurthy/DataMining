import cv2
from PIL import Image, ImageDraw
import os
import numpy as np

def main(filename,save_folder):
    #read the image
    image=cv2.imread(filename)
    #convert the black area to white for better view
    img=cv2.bitwise_not(image)
    #convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    #Calculate the counter of the image
    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE) 
    #copy the image
    image_copy = img.copy()
    #save th area of counter
    similar=[]
    #save the bouding box the counters
    r_bbox=[]
    #loop throug the counter area
    for c in contours:
        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        similar.append(cv2.contourArea(c))
        r_bbox.append([x,y,x+w,y+h])

    #get all the bounding box near to 0 x axis
    #Now goal is to find the R in the image, OCR is not able to detetct the R due to low resolution
    #So we got the counter rectangle and cordinated present in the r_bbox get the all the first R near to o the poisiton of 
    #x-axis
    
    x_near=[]
    for data in r_bbox:
        if data[0]>=0 and data[0]<=1:
    #         print(data)
            x_near.append(data)
        
    #Now get the all the R presentent in the same line where y is contant and x is increasing
    line=[]
    for i in range(len(x_near)):
        l=[]
        for data in r_bbox:
            if data[1]>=x_near[i][1] and data[1]<=x_near[i][1]+1:
                l.append(data)
        if len(l)>1:
            line.append(l)
        
    #sort the line w.r.t y axis
    lst=sorted(line, key=lambda x: x[1],)
    
    #sort the list with respect to x axis
    for i in range(len(lst)):
        lst[i]=sorted(lst[i], key=lambda x: x[0])
        
    #get all the xy cordiante of alphabet R
    xycordinate=[]
    
    #Open original image to crop the images
    im = Image.open(filename) 
    draw = ImageDraw.Draw(im) 
    for i in range(len(lst)):
        z=[]
        for k in range(len(lst[i])-1):
            
            #draw.line((lst[i][k][0],lst[i][k][1],lst[i][k+1][0],lst[i][k+1][1]), fill="red",width=5)
            z.append([lst[i][k][0],lst[i][k][1]])
        z.append([lst[i][k+1][0],lst[i][k+1][1]])
        x=(lst[i][k+1][0]-lst[i][k][0])
        z.append([x+lst[i][k+1][0],lst[i][k+1][1]])
    
        #draw.line((lst[i][k][0],lst[i][k][1],x+lst[i][k+1][0],lst[i][k+1][1]), fill="red",width=5)
        lst[i].append([x+lst[i][k+1][0],lst[i][k+1][1],0,0])
        xycordinate.append(z)

    #Check folder present or not to save the output
    if os.path.isdir(save_folder):
        pass
    else:
        os.mkdir(save_folder)
        
    #Crop all the images and save it in folder
    img =im
    count=0
    # print(len(xycordinate))
    for k,x_axis in enumerate(xycordinate):
        
        if k==len(xycordinate)-1:
            # print(True)
            break
        for i in range(len(x_axis)-1):
            count=count+1
            #draw.rectangle([(x_axis[i][0],x_axis[i][1]),(xycordinate[k+1][i+1][0],xycordinate[k+1][i+1][1])],fill="blue")
            #top_left_x, top_left_y, bottom_right_x, bottom_right_y
            img2=im.crop((x_axis[i][0],x_axis[i][1]+5.5,xycordinate[k+1][i+1][0],xycordinate[k+1][i+1][1]))
            name=os.path.basename(filename)
            
            if os.path.isdir(os.path.join(save_folder,name.split(".")[0])):
                pass
            else:       
                os.mkdir(os.path.join(save_folder,name.split(".")[0]))
            ###conditon not to save the full black images##########
            w=(xycordinate[k+1][i+1][0])-(x_axis[i][0])
            h=(xycordinate[k+1][i+1][1])-(x_axis[i][1]+6)
            var=len([px for px in list(img2.getdata()) if px[1] < 0.01])
            per=(var/(w*h))*100            
            #print(var, w*h, per)            
            if per < float(100):   
                img2.save(save_folder+name.split(".")[0]+"//"+name.split(".")[0]+"_crop_image_"+str(count)+".png")
    print("Completed slicing images in "+name)


def filterImage():
    #print(os.getcwd())
    os.chdir("./Slices/")
    #print(os.getcwd())
    #loop through the images in slice folder
    for files in os.listdir():
        #print(files)
        os.chdir(files)
        for file in os.listdir():
            #print(file)
            #convert to grey scale
            img=cv2.imread(file,0)
            #print(img.shape)
            count = cv2.countNonZero(img)
            #print(count)
            if count < 14:
                os.remove(file)
        os.chdir('..')
        #print(os.getcwd())
        print("Filetered images in "+files)
    os.chdir('..')
    #print(os.getcwd())
    
def conturing(path):
    
    print(os.getcwd())
    os.chdir(path)
    os.chdir('./Slices/')
    
    
    #Check if Boundaries folder is present or not to save the output
    if os.path.isdir('../Boundaries'):
        pass
    else:
        os.mkdir('../Boundaries')
        
    for files in os.listdir():
        #Check folder present or not to save the output
        if os.path.isdir(path+"\\Boundaries\\"+files):
            pass
        else:
            os.mkdir(path+"\\Boundaries\\"+files)
        #print(files)
        os.chdir(files)
        #print(os.getcwd())
        for file in os.listdir():
            #print(file)
            image=cv2.imread(file)
            # convert the image to grayscale format
            img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # apply binary thresholding
            ret, thresh = cv2.threshold(img_gray, 0, 150, cv2.THRESH_BINARY)
            # visualize the binary image
            contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
            # draw contours on the original image            
            cv2.drawContours(image=image, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=1, lineType=cv2.LINE_AA)
            # see the results
            dest=path+"\\Boundaries\\"+files
            outfile = '%s\%s' % (dest, file)
            #print(outfile)
            cv2.imwrite(outfile,image)
        os.chdir('..')
        print("Completed contouring images in "+files)
        #print(os.getcwd())
    os.chdir('..')
    print(os.getcwd())