# Air Canvas

## Objective
To develop an application that utilises computer
vision techniques to detect the motion of a colored tracker
and draw it on a virtual canvas in real time.

The project uses OpenCv and Python to achieve the desired results.

## Workflow
* Initialises video capture and obtains the camera feed as individual frames.

![image](https://user-images.githubusercontent.com/109210914/224982644-90405ab2-0586-4323-be79-9574f4985813.png)

* Inverts the camera feed to obtain a non-inverted frame.

![image](https://user-images.githubusercontent.com/109210914/224982662-1d194029-5d2c-460f-b86f-0a1a1c00ea3b.png)

* Converts the frame from RGB to HSV.

![image](https://user-images.githubusercontent.com/109210914/224982717-fba90ebb-1b9a-44ed-a095-f3b7b87086aa.png)

* Applies a mask on the frame to extract a binary image of the tracker.
* Applies morphological transformations on the mask to remove noise and fill-in any erros within the tracker.

![image](https://user-images.githubusercontent.com/109210914/224982735-e075a711-a7ed-4ed7-8ca6-1e516f78fce3.png)

* Finds the coordinates of the center of the tracker by applying moments.
* Connects the current set of coordinates and the previous set of coordinates by drawing a line between the two.

Other functionalities such as the ability to change colors, draw shapes, change the color of the tracker etc were added later to better mimic an actual drawing application.

## Results

The desired outcomes were accomplished as we were able to draw on the virtual canvas with accuracy.

![image](https://user-images.githubusercontent.com/109210914/224986697-16e4b9ba-df96-406a-a4ed-1b31a292c9b4.png)  
![image](https://user-images.githubusercontent.com/109210914/224986713-8f867919-5f21-4748-abcc-3832a6bb7ee5.png)  
![image](https://user-images.githubusercontent.com/109210914/224986737-2b8e3f12-c953-4159-b7d3-c2687670e0ea.png)



