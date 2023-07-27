# Rucoy-Vision-Bot
Built with the power of Python's OpenCV and PyAutoGUI, Rucoy Vision bot captures screen images, identifies targets, and automates actions to improve a user's experience in the game Rucoy Online.
![image](https://github.com/Mimsqueeze/Rucoy-Vision-Bot/assets/101283845/f20139c0-8a73-4044-a259-5dbc12bc32cf)

## Getting Started
To get started using this program, you will need to clone the repository. Then, simply run the main.py file in the src folder in your secondary screen while having your game running in your main screen, and everything should be working. 

## Instructions of Use
When you start running the program, everything should be working immediately. You will see lines in the console telling you what the program is doing, as shown below. 
![image](https://github.com/Mimsqueeze/Sorting-Simulator/assets/101283845/e13ffca4-f703-4748-ac4f-16280fb4f43c)

The program can detect whether you are currently attacking in the game: if you are, then the program will simply print "Attacking..."" in the console. If you are not attacking, the program will proceed to locate a target, and click on the target's position after printing information in the console. Finally, to exit the program, simply input Ctrl+C in the console.

## Algorithm
The program uses OpenCV's image processing capabilities to locate targets in the game. Specifically, the program uses OpenCV's template matching to match template images of the target to a screenshot of the game, while PyAutoGUI performs actions such as clicking on the target.

## Extra Notes and Disclaimer
This is actually a very old project I intially made a few years ago, but I recently refactored it and cleaned everything up. It was a super fun and enlightening project and helped to get me into the world of programming!

Also a disclaimer: This program is only meant to be a proof of concept/prototype application. As such, it has limited features and I would not recommend you to actually use it. The program is only tested for 1920x1080 screens, and works for the archer class and drow ranger monster in the game.
