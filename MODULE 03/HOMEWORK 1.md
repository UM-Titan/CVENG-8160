# Creating Customize Data Loaders
In this assignment you will be using python to create customized data loaders that will be able to accept and process training datasets in diverse formats. 

## Assignment Details
You are provided with two datasets: [localization](https://drive.google.com/file/d/1rMabUduN4_fFN9THlxG4_IJ1Mli1e657/view?usp=drive_link) and classification. 
Localization: provides images and a csv file describing the location of objects in each image. 
Classification: provides images collated in folders which describe the type of vehicle classes the images belong to. 
To complete this assignment:
* Download and extract both datasets
* Use object oriented programming to write a custom data loader to read and transform both datasets. Note that localization will need labels to be transformed also. 
* The transforms to use should include: resizing of images, horizontal, vertical flip, tensor and normalization of data.
* Include custom plotting functions to help visualize data. 

## Rules
* Feel free to use online resources. However, if you use any function or technique not discussed in class, demonstrate your understanding of the technique with at least 2 examples of how to use the function. You will lose points if this is not done
* Use google collab only
* While you may discuss this homework with your colleagues, your solution should not look too similar to others. You will be penalized for that. 
