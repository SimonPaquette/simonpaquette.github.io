##########################################################################
#list of function to use
#
#def isSame (image_1,image_2):
#	Return True or False if is the same person
#
#def start (image_path_1, json_file_1, image_path_2, json_file_2):
#	Get result if its the same person are not from the begenning
#		print True or False
#
#def show (image_path_1, json_file_1, image_path_2=None, json_file_2=None)
#	Show the cropped images separate in 4 parts
#		create window
#
#def getHist (image_path, json_file, showMat=False)
#	Get access to the 4 histograms of the image
#		return [hist1,hist2,hist3,hist4]
#
#def compare (image_hist_1, image_hist_2, method):
#	Get the value result from the comparaison between 2 images
#		return [average,p1,p2,p3,p4,val]
#
##########################################################################

import cv2
import json
import os
import numpy


def crop (image_path, json_file):
	"Crop the picture given into the size of the bBox annotation"
	
	with open (json_file,"r") as file:
		file=json.load(file)
	
	name=os.path.basename(image_path)
	picture=cv2.imread(image_path)
	found=False
	
	#Crop to the annotation size
	for filename,data in file.items():
		if name==filename:
			found=True
			image_width=data["width"]
			image_height=data["height"]
			for annot in data["annotations"]:
				if annot["label"].lower()=="person":
					width 	= int(annot["width"])
					height 	= int(annot["height"])
					x		= int(annot["x"])
					y		= int(annot["y"])

	if found==True:	
		#if out of limit
		if y<0:
			y=0
		if x<0:
			x=0
		if y+height>image_height:
			height=image_height-y
		if x+width>image_width:
			width=image_width-x

		#Crop if found
		pic=picture[y:y+height, x:x+width]

	elif found==False:
		print("The json file don't match with the capture folder:")
		print("\t"+json_file)
		print("\t"+image_path+"\n")
		pic=None

	return pic


def creating (hsv_picture):
	"Create a histogram from the hsv_picture given"

	hist = cv2.calcHist([hsv_picture], [0, 1, 2], None, [8,8,8], [0, 180, 0, 256, 0, 256])
	hist = cv2.normalize(hist, hist, norm_type=cv2.NORM_L1)

	return hist


def show (image_path_1, json_file_1, image_path_2=None, json_file_2=None):
	"Show the cropped images separate in 4 parts"
	
	name=os.path.basename(image_path_1)
	im_show=[]	#images to show

	#To access image one by one and crop
	images=[]
	images.append(image_path_1)
	if image_path_2!=None:
		images.append(image_path_2)
	
	for image in images:
		#Took first image
		if image==images[0]:
			pic=crop(image,json_file_1)
		if len(images)==2:
			#Took second image
			if image==images[1]:
				pic=crop(image,json_file_2)

		#Get the size of the cropped image
		new_height,new_width,dim=pic.shape
	
		#Separate 4 parts of the picture
		line1 = cv2.line(pic,(0,int(new_height/4)),(new_width,int(new_height/4)),(0,255,0),1)
		line2 = cv2.line(line1,(0,int(new_height/2)),(new_width,int(new_height/2)),(0,255,0),1)
		line3 = cv2.line(line2,(0,int((3*new_height)/4)),(new_width,int((3*new_height)/4)),(0,255,0),1)

		pic=cv2.resize(line3,(300,400))	#To keep same size for each picture
		im_show.append(pic)
	
	#To show images in same window
	if len(im_show)==2:
		horizontal=numpy.concatenate((im_show[0], im_show[1]),axis=1)
		cv2.imshow(name, horizontal)
		cv2.moveWindow(name, 300,200)	
	if len(im_show)==1:
		cv2.imshow(name, im_show[0])
		cv2.moveWindow(name, 300,200)	
	
	cv2.waitKey(0)
	

def getHist (image, json_file=None, showMat=False):
	"Get access to the 4 histograms of the image"
	
	pic=image
	if json_file!=None:
		pic=crop(image,json_file)
	pic=cv2.resize(pic,(300,400))	#Get same size
	new_height,new_width,dim=pic.shape

	#Convert BGR to HSV
	hsv = cv2.cvtColor(pic,cv2.COLOR_BGR2HSV)

	#Split image in 4 parts
	hsv1 = hsv [0:int(new_height/4), 0:new_width]
	hsv2 = hsv [int(new_height/4):int(new_height/2), 0:new_width]
	hsv3 = hsv [int(new_height/2):int((3*new_height)/4), 0:new_width]
	hsv4 = hsv [int((3*new_height)/4):new_height, 0:new_width]

	#Create 4 hist, top to bottom of the image
	hist1 = creating(hsv1)
	hist2 = creating(hsv2)
	hist3 = creating(hsv3)
	hist4 = creating(hsv4)

	if showMat==True:
		print([hist1,hist2,hist3,hist4])

	return [hist1,hist2,hist3,hist4]


def compare (image_hist_1, image_hist_2, method):
	"Get the value result from the comparaison between 2 images"

	p1 = cv2.compareHist(image_hist_1[0], image_hist_2[0], method)
	p2 = cv2.compareHist(image_hist_1[1], image_hist_2[1], method)
	p3 = cv2.compareHist(image_hist_1[2], image_hist_2[2], method)
	p4 = cv2.compareHist(image_hist_1[3], image_hist_2[3], method)

	#Value to compare (average of 4 parts)
	average=(p1+p2+p3+p4)/4

	#Other testing value (personalized value)
	val=(p1+p2*3+p3*3)/7

	return [average,p1,p2,p3,p4,val]

#List of method given by cv2.compareHist()
method=[
		None,
		cv2.HISTCMP_CORREL,			#[-1;1]		:	1=perfect match		-1=mismatch
		cv2.HISTCMP_CHISQR,			#[0;inf]	:	0=perfect match		inf=mismatch
		cv2.HISTCMP_INTERSECT,		#[0;1]		:	1=perfect match		0=mismatch		
		cv2.HISTCMP_BHATTACHARYYA	#[0;1]		:	0=perfect match		1=mismatch
	]


def start (image_path_1, json_file_1, image_path_2, json_file_2):
	"Get result if its the same person are not from the begenning"

	same=False

	hist1=getHist(image_path_1,json_file_1)
	hist2=getHist(image_path_2,json_file_2)

	result=compare(hist1,hist2,method[3])
	result=result[5]	#get the personalized value

	if result>=0.425:
		same=True

	print(same)


def isSame (image_1,image_2):
	"Return True or False if is the same person"

	same=False

	hist1=getHist(image_1)
	hist2=getHist(image_2)

	result=compare(hist1,hist2,method[3])
	result=result[5]	#get the personalized value

	if result>=0.425:
		same=True

	return same



if __name__ == "__main__":

	images1="C:/Users/vivalab/Desktop/crop/cap4_cam1/"
	images2="C:/Users/vivalab/Desktop/crop/cap4_cam2/"

	for image1 in os.listdir(images1):
		
		num1, extension1 = os.path.splitext(image1)
		ID1, filename1 = num1.split("-")
		time1=int(filename1)
		
		path1=images1+image1
		picture1=cv2.imread(path1)

		hist1=getHist(picture1)

		best=[]

		for image2 in os.listdir(images2):
		
			num2, extension2 = os.path.splitext(image2)
			ID2, filename2 = num2.split("-")
			time2=int(filename2)

			if (time1-40000<=time2<=time1):
			
				path2=images2+image2
				picture2=cv2.imread(path2)
		
				hist2=getHist(picture2) 

				result=compare(hist1,hist2,method[3])
				value=result[5]

				if value>0.425:
					best.append([value,path2])
					#if len(best)>32:
					best.sort(key=lambda x:x[0])
					#del best[0]

		if len(best)>0:
			person=best[-1]
			person=os.path.basename(person[1])
			person=person.split(".")[0]
			person=person.split("-")[1]
			person=int(person)
		
			for item in best:

				filename=os.path.basename(item[1])
				file=filename.split(".")[0]
				time=file.split("-")[1]
				time=int(time)

	
				if (person-4000<=time<=person+4000):
					
					pic1=cv2.imread(path1)
					pic2=cv2.imread(item[1])

					pic1=cv2.resize(pic1,(300,400))	
					pic2=cv2.resize(pic2,(300,400))	
		
					horizontal=numpy.concatenate((pic1, pic2),axis=1)
					#cv2.imshow(image1+" <<<>>> "+filename, horizontal)
					#cv2.moveWindow(image1+" <<<>>> "+filename, 300,200)
					#cv2.waitKey(0)
