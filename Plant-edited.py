from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2 as cv
import numpy as np
from ctypes import alignment
from glob import glob
from os import popen


# Load Yolo
net = cv.dnn.readNet("yolov3_training_last.weights", "yolov3_testing.cfg")
#dnn means deep neural network

# Name custom object
classes = ["Rust"]

root= Tk()
root.title("Plant Disease Detector")
root.geometry("1006x572")

file=()             #Stores all the file locations of all images selected
final=[]            #Stores all the image processed images in Tk format
size=(1000,500)     #Size of the main window and the size images are resized to


intro = ImageTk.PhotoImage(Image.open("intro.png"))     #PRrints the intro design
Label(root,image=intro).grid(row=0,column=0)


def clear():
    for widgets in root.winfo_children():
        widgets.destroy()

def open():                 #When user clicks on open file on tk window
    
    file= filedialog.askopenfilenames(parent=root, title="Select Files", filetypes=(("jpg files", ".jpg"), ("all files", ".")))

    root.splitlist(file)
    clear()
    ml(file) #Returns a list of images in Tk format

    button_back= Button(root, text="<<", command=back, state=DISABLED).grid(row=1, column=0)
    button_exit= Button(root, text="EXIT", command=root.quit).grid(row=1, column=1)
    button_next= Button(root, text=">>", command= lambda: next(2)).grid(row=1, column=4, pady=10)
    button_new= Button(root, text="Next", command= disease).grid(row=1, column=3)

    my_Label= Label(image=final[0]).grid(row=0,column=0, columnspan=5)

    if detect[0]==0:        # 1 in detect list means rust present
        Label(root,text="Healthy Plant", font='Helvetica 10 bold', fg="#284737").grid(row=1, column=0, columnspan=5)
    else:  
        Label(root,text="Rust Disease", font='Helvetica 10 bold', fg="#621D1D").grid(row=1, column=0, columnspan=5)

    status= Label(root, text=f"Image 1 of "+ str(len(final)), bd=1, relief=SUNKEN, anchor=E)    #displaying numberth of image on tk window on left bottom
    status.grid(row=2, column=0, columnspan=5, sticky=W+E)

def next(n):      #next button function
    global my_Label
    global button_next
    global button_back

    my_Label= Label(image=final[n-1])
    button_next = Button(root, text=">>", command= lambda: next(n+1))
    button_back=Button(root, text="<<", command= lambda: back(n-1))

    if n == len(final):
        button_next=Button(root, text=">>", state=DISABLED)

    my_Label.grid(row=0,column=0, columnspan=5)

    button_back.grid(row=1, column=0)
    button_next.grid(row=1, column=4)

    Label(root, text=f"Image "+ str(n) +" of "+ str(len(final)), bd=1, relief=SUNKEN, anchor=E).grid(row=2, column=0, columnspan=5, sticky=W+E)

    if detect[n-1]==1:
        Label(root,text="Rust Disease", font='Helvetica 10 bold', fg="#621D1D").grid(row=1, column=0, columnspan=5)
    else:
        Label(root,text="Healthy Plant", font='Helvetica 10 bold', fg="#284737").grid(row=1, column=0, columnspan=5)

def back(n):        # Back Button
    global my_Label
    global button_next
    global button_back

    my_Label= Label(image=final[n-1])
    button_next = Button(root, text=">>", command= lambda: next(n+1))
    button_back=Button(root, text="<<", command= lambda: back(n-1))

    if n==1:
        button_back=Button(root, text="<<", state=DISABLED)

    my_Label.grid(row=0,column=0, columnspan=5)

    button_back.grid(row=1, column=0)
    button_next.grid(row=1, column=4)

    Label(root, text=f"Image "+ str(n) +" of "+ str(len(final)), bd=1, relief=SUNKEN, anchor=E).grid(row=2, column=0, columnspan=5, sticky=W+E)

    if detect[n-1]==1:
        Label(root,text="Rust Disease", font='Helvetica 10 bold', fg="#621D1D").grid(row=1, column=0, columnspan=5)
    else:
        Label(root,text="Healthy Plant", font='Helvetica 10 bold', fg="#284737").grid(row=1, column=0, columnspan=5)

def disease():          #Information about the diseases found
    global pop
    global rusty
    pop= Toplevel(root)
    pop.title("Treatments and Prevention")
    pop.geometry("700x500")
    
    Label(pop, text="What is Rust Disease?", font='Helvetica 12 bold').pack(anchor=W)
    Label(pop, text="Rust disease is an obligate fungal parasite that grows on a wide variety of plants useful to humans. These fungi").pack(anchor=W)
    Label(pop, text="are obligate parasites, which means they can only grow on a living host.").pack(anchor=W)
    Label(pop, text="\nHow to identify leaf rust?", font='Helvetica 12 bold').pack(anchor=W)
    Label(pop, text="As the name suggests, many rust diseases present as orange rust on plants in the form of spots, patches or raised").pack(anchor=W) 
    Label(pop, text="blisters. Rust spots on leaves can also come in a variety of shades from bright yellow to dark brown.").pack(anchor=W) 
    Label(pop, text="Rust can be one of the most difficult plant diseases to control once established, but there are some things you ").pack(anchor=W)
    Label(pop, text="can do to both control and prevent rust on plants.").pack(anchor=W)
    Label(pop, text="").pack()
    
    rusty = ImageTk.PhotoImage(Image.open("rusty.png"))
    Label(pop,image=rusty).pack()

    Label(pop, text="\n\nClick Below for Treatment & Prevention ", font='Helvetica 8 bold').pack()
    Button(pop,text="CURE",command=display_cure).pack()

def display_cure():         #To display cure on the last tk window
    for widgets in pop.winfo_children():
        widgets.destroy()
    
    Label(pop, text="Rust treatment and control", font='Helvetica 12 bold').pack(anchor=W)
    Label(pop, text="~Remove and destroy all leaves and plant parts affected by rust.").pack(anchor=W)
    Label(pop, text="~You might have to destroy badly infected plants completely to prevent them infecting other plants of the same").pack(anchor=W)
    Label(pop, text="species.").pack(anchor=W)
    Label(pop, text="~Spray with a suitable rust control product containing fungicide, repeating as recommended. There are no ").pack(anchor=W)
    Label(pop, text="chemicals approved for control of diseases on edible plants.").pack(anchor=W)
    Label(pop, text="~Lawn rust treatment: Mow regularly to reduce the number of affected leaves, remove the clippings and improve ").pack(anchor=W)
    Label(pop, text="air circulation by pruning overhanging trees and shrubs.").pack(anchor=W)
    Label(pop, text="~Pear rust treatment includes removing any juniper bushes in your garden, as they can host the fungus which ").pack(anchor=W)
    Label(pop, text="causes rust on pear trees.").pack(anchor=W)
    Label(pop, text="\nHow to prevent rust disease?", font='Helvetica 12 bold').pack(anchor=W)
    Label(pop, text="~Clear debris away from underneath plants likely to be affected by rust, particularly before the winter, ").pack(anchor=W)
    Label(pop, text="because the fungus overwinters on plant debris.").pack(anchor=W)
    Label(pop, text="~Grow leeks and other members of the onion family on a fresh site each year.").pack(anchor=W)
    Label(pop, text="~Keep plants growing as strongly as possible, without any stress and avoid using high nitrogen fertilisers on ").pack(anchor=W)
    Label(pop, text="susceptible plants because this encourages soft growth which can be more easily infected. High potash feeds ").pack(anchor=W)
    Label(pop, text="help to strengthen plants and prevent rust disease from taking hold.").pack(anchor=W)
    Label(pop, text="~Allow enough space around plants to improve air circulation as rust thrives in damp conditions.").pack(anchor=W)
    Label(pop, text="~Remove weeds which might harbour rust. For example, willow herb is known to host fuchsia rust, while ").pack(anchor=W)
    Label(pop, text="hollyhock rust can spend some of its life on wild mallow.").pack(anchor=W)
    Label(pop, text="  ").pack()
    Button(pop, text="EXIT", command=root.quit).pack()

    
open_btn= Button(root,text="Open file",command=open).place(x=485,y=525)    #starts executing program on clicking open file

# Machine Learning
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
colors = (150,200,75)
detect=[]           #store 0 for healthy, 1 for rust || we defined

def ml(file):
    for img_path in file:
        # Loading image
        img = cv.imread(img_path)
        img = cv.resize(img, None, fx=0.4, fy=0.4)
        height, width, channels = img.shape

        # Detecting objects
        blob = cv.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.3:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        print(indexes)

        if len(indexes)>0:
            detect.append(1)
        else:
            detect.append(0)
            
        font = cv.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv.putText(img, label, (x, y + 30), font, 3, color, 2)

        color_change = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        format_change = Image.fromarray(color_change)
        size_change=format_change.resize(size)
        tk_image = ImageTk.PhotoImage(size_change)
        final.append(tk_image)

root.mainloop()