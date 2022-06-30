from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2 as cv
import numpy as np

# Load Yolo
net = cv.dnn.readNet("yolov3_training_last.weights", "yolov3_testing.cfg")

# Name custom object
classes = ["Rust"]

root= Tk()
file=()

final=[]
size=(1000,600)


def open():
    global img
    file= filedialog.askopenfilenames(parent=root, title="Select A File", filetypes=(("jpg files", ".jpg"), ("all files", ".")))

    print(root.splitlist(file))
    
    file_found(file) #Returns a list of images in Tk format

    my_Label= Label(image=final[0]).grid(row=0,column=0, columnspan=3)  

    status= Label(root, text=f"Image 1 of "+ str(len(final)), bd=1, relief=SUNKEN, anchor=E)
    status.grid(row=2, column=0, columnspan=3, sticky=W+E)

open_btn= Button(root, text="Open file", command=open).grid(row=0, column=1)    #starts executing program on clicking open file

def next(n):                        #next button function
    global my_Label
    global button_next
    global button_back

    my_Label= Label(image=final[n-1])
    button_next = Button(root, text=">>", command= lambda: next(n+1))
    button_back=Button(root, text="<<", command= lambda: back(n-1))

    if n == len(final):
        button_next=Button(root, text=">>", state=DISABLED)

    my_Label.grid(row=0,column=0, columnspan=3)

    button_back.grid(row=1, column=0)
    button_next.grid(row=1, column=2)

    Label(root, text=f"Image "+ str(n) +" of "+ str(len(final)), bd=1, relief=SUNKEN, anchor=E).grid(row=2, column=0, columnspan=3, sticky=W+E)


def back(n):
    global my_Label
    global button_next
    global button_back

    my_Label= Label(image=final[n-1])
    button_next = Button(root, text=">>", command= lambda: next(n+1))
    button_back=Button(root, text="<<", command= lambda: back(n-1))

    if n==1:
        button_back=Button(root, text="<<", state=DISABLED)

    my_Label.grid(row=0,column=0, columnspan=3)

    button_back.grid(row=1, column=0)
    button_next.grid(row=1, column=2)

    Label(root, text=f"Image "+ str(n) +" of "+ str(len(final)), bd=1, relief=SUNKEN, anchor=E).grid(row=2, column=0, columnspan=3, sticky=W+E)
    

button_back= Button(root, text="<<", command=back, state=DISABLED).grid(row=1, column=0)
button_exit= Button(root, text="EXIT", command=root.quit).grid(row=1, column=1)
button_next= Button(root, text=">>", command= lambda: next(2)).grid(row=1, column=2, pady=10)


layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
colors = (150,200,75)

def file_found(file):
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
                confidence = scores[class_id]       #always between 0 to 1
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
        font = cv.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv.putText(img, label, (x, y + 30), font, 3, color, 2)

        temp0 = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        temp1 = Image.fromarray(temp0)
        re=temp1.resize(size)
        temp2 = ImageTk.PhotoImage(re)
        final.append(temp2)

root.mainloop()