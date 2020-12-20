# Smart and Sustainable Irrigation
The objective of the system is to implement a smart irrigation system in azure cloud which switches on water systems based on current and future weather conditions thus saving water (Sustainability). The system also helps to monitor agricultural methane (Greenhouse gas) emissions and crop fires which are harmful for both crop and environment and this system also gives severe weather alerts one day prior to farmers so that they can save their dried produce and crops from rain.
# Circuit Diagram
![alt text](https://github.com/YaswantSaiKrishna/Smart-and-Sustainable-Irrigation/blob/main/Images/Circuit.png?raw=true)
# Azure Cloud Architecture
![alt text](https://github.com/YaswantSaiKrishna/Smart-and-Sustainable-Irrigation/blob/main/Images/Azure.jpeg?raw=true)
# How to guide ?
Step 1: Clone the repository using git clone.

Step 2: Copy the NodeMCUBoard project folder to your arduino project folder.

Step 3: Open the NodeMCUBoard.ino file in your arduino ide .

Step 4: Create Azure resources (IoT Hub, Stream Analytics, Maps) .

Step 5: Update the mqtt and azure credentials .

Step 6: Upload the code to your arduino board .

Step 7: Create an azure timer function using any python ide (I used visual studio codespaces) .

Step 8: Copy the __init__.py file from Azure_Timer_Function folder and update the maps credentials .

Step 9: Deploy the azure function using docker .

Step 10: Start the azure function and plug-in your NodeMCU to powersupply .
