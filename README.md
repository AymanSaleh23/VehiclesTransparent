# Making Vehicles Transparent via V2V Vedio Streaming
Graduation Project 2022-2023 supported by Valeo co. mentorship program

## Intorduction to Project Idea
>- Road traffic injuries have become a global health and development problem of epidemic proportions. According to the World Health Organization Global Burden of Disease Project for 2004 , road traffic crashes caused over 1.27 million deaths that year.
>- In 2004, these crashes constituted the ninth leading cause of death, and it was estimated that they
would rise to the fifth leading cause of death by 2030 . 
>- If we account mortality in terms of years of life lost, then the significance of road crashes is even much more relevant, as they are the second, first, and third leading causes of death in the 5–14, 15–29, and 30–44 age groups, respectively . 
>- One of the most severe types of road crashes occurs when a vehicle shifts into an opposing traffic lane and crashes head-on with an oncoming vehicle. 
>- In the United States alone, there were 3986 fatal head-on crashes in 2003, killing 5063 people.
>- The Fatal Analysis Reporting System indicates that the vast majority of these crashes occur on rural undivided two-lane roads and are the result of an inadvertent action of a driver, causing a run-off-road, or of a deliberate action, i.e., executing a passing maneuver .
>- Focusing on driver-assistance technologies of modern vehicles, it is clear that a lane-keeping system is an efficient approach to mitigate head-on crashes caused by the inadvertent actions of drivers. 
>- Regarding passing maneuvers, however, there are no available systems that help drivers on the decision of whether it is safe to engage on such maneuvers. 
>- Evaluating the safety conditions to initiate a passing maneuver is difficult, particularly when the vehicle in front has no transparent surfaces at a level that allows to see through it and perceive incoming traffic. 
>- This is the case with trucks and buses, whose length constitutes an additional challenge and that typically travel at slower speeds, being the main subjects of overtaking.



### This Project is  a 3-phase project implementation

### under supervision of Prof. Khaled El-Shafie

# System Design and Architecture

![image](https://user-images.githubusercontent.com/58345649/195928204-40d590f2-13e9-4dcd-8814-abf916c0943b.png)

## Our Project architecture mainly divided into subsystems:

### Cameras And Sensors Subsystem:
- To scan and take the live event in front of the vehicle.
- Sensors is to detect the actual distances needed.

### Vision System:
-  To verify the data from Camera and Sensors.

### CPU:
- To apply the logic of transparency using AI and Computer Vision models.
- To do all mathematical calculations for distance.
- Manage All Subsystems.
- Send data to Communication subsystem to be sent to another vehicle.

### Communication Subsystem:
- Communicate and interact with other vehicles via Wifi technology.
Consists of :
- Wifi for Sending.
- Wifi for receiving.
- Gateway/Access point module to connect this vehicle to other vehicles. 

# Project Development Phases

## Phase_1: Establishing all basic features.
- Communication.
- Streaming data in coordinates format.
- Distance Mathematical Operations.
- Computer Vision Model.

## Phase_2:
- Upgrade data Transmission to Video stream.
- Enhance Computer Vision and ML models to increase accuracy.
- Initiate ML model to detect the percentage of successful passing.
- Initiate Triple Modular Redundancy and Voter Module for Verification Inputs.

## Phase_3:
- Additional features:
- Create Server For IOT and Traffic management Features.
- IOT: Find my Vehicle service.
- Traffic management: create a ML model to monitor and suggest better road path.

# System Scenarios
> - This project aims to create a cooperative driver-assistance system for the passing of vision-obstructing vehicles, which combines several technologies to save the passing drivers’ life from unpredictable vehicle moving in the same direction even opposite direction.
> - Once there are a car need to pass a vision-obstructing vehicle but the driver of the rear vehicle doesn’t see what is in front of that vision-obstructing vehicle just enabling this system that scenario will occurred.

- In Vehicle_1 (vision-obstructing):
> - It normally scans objects in vehicle type and detect its coordinates (3 road lines at most: direct front, front right, front left) using Camera and Sensors and Computer Vision model and make some mathematical equations to get the most accurate distances, it will be kept for future propose.

- In Main Vehicle (Normal User):
> - Camera takes a photo of the vehicle_1 (photo contains the vehicle data “No, ID”).
>- Using an encryption method the SSID, Password of the vehicle_1 will be generated (This technique doesn’t Need for internet connection), Then this vehicle will connect to the vehicle_1’s Access point using the receiving Wifi.
> - As soon as connection is stablished the data transfer will be occurred.

- Date consists of:
> - The Front vehicle Data (Length , Height).
> - Coordinates of the vehicle in front of vehicle_1).

# System from Elevation view
![image](https://user-images.githubusercontent.com/58345649/195955464-d5da963c-7e6e-49fb-9048-c520f64e74c8.png)

## Predicted Output in Phase_1
![image](https://user-images.githubusercontent.com/58345649/195955528-8f4fd949-982d-4076-9513-e7f09b1e0c12.png)
(a) Before Activating System
(b) After Activating System

## Predicted Output in Phase_2
![image](https://user-images.githubusercontent.com/58345649/195955583-84f44915-e1aa-4da0-b166-7926fbefa501.png)
(a) Before Activating System
(b) After Activating System

## Predicted Output in Phase_3
![image](https://user-images.githubusercontent.com/58345649/195955598-e4eb0614-c49a-42fd-8cf4-0c9296d331f4.png)
(a) Before Activating System.
(b) After Activating System.
(n%) Successful pass percentage.

