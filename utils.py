from Tkinter import *
from PIL import ImageTk, Image
import pickle
import csv

def load_labels():
    import pickle
    return pickle.load(open("new_labels.p","rb"))

def assign_indices():
    index_dict = {}
    with open("image_filename.csv","rb") as csvfile:
        csvreader = csv.reader(csvfile)
        for example in csvreader:
            filename = example[1][51:]
            index_dict[filename] = example[0]

    location_dict = {}
    with open("flood_gps.csv","rb") as csvfile:
        csvreader = csv.reader(csvfile)
        for example in csvreader:
            location_dict[example[0]] = (example[2],example[3])

    labels = load_labels()
    label_dict = {}
    for obj in labels.keys():
        file_list_w_object = labels[obj]
        index_list = []
        for image_tuple in file_list_w_object:
            try:
                filename = image_tuple[0]
                index = index_dict[filename]
                location = location_dict[index]
                index_list.append([index, location])
            except:
                print(filename)
        label_dict[obj] = index_list
    pickle.dump(label_dict, open("labeled_indices.p","wb"), protocol = 2)
    return label_dict

def validate_labels():
    label_list = load_labels()
    keys = label_list.keys()
    approved = {}
    denied = {}
    for key in keys:
        for filename in label_list[key]:
            filename = filename[0] #Labeled filenames are saved as tuples with filenames and Inception model labels
            try:
                large_image = Image.open("images/" + filename)
            except:
                print("No Image {}".format(filename))
                break

            root = Tk()
            root.title("Validation GUI")
            root.geometry("750x750")
            app = Validate_Labels_GUI(root,filename,key,approved,denied)
            root.mainloop()
            root.destroy()
            pickle.dump((approved,denied), open("validated_labels.p","wb"),protocol = 2)

class Validate_Labels_GUI(Frame):
    """Object to create Graphical User Interface to validate the labels given by the Inception model"""
    def __init__(self, master, filename, label, approved, denied):
        Frame.__init__(self,master)
        self.filename = filename
        self.label = label
        self.approved = approved
        self.denied = denied
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.instruction = Label(self, text = "Is there a {} in this picture?".format(self.label),font = ("Helvetica", 20))
        self.instruction.grid(row = 0, column = 0, columnspan = 4)

        large_image = Image.open("images/" + self.filename)
        
        scale = min((1.,600./max(large_image.size)))
        image = large_image.resize( [int(scale * dim) for dim in large_image.size] )
        
        TKImage = ImageTk.PhotoImage(image)
        
        self.picture = Label(self, image=TKImage)
        self.picture.image = TKImage
        self.picture.grid(row = 1, column = 1, columnspan = 10, sticky = W)
        
        self.yes_button = Button(self, text = "Yes", command = self.approve,font= ("Helvetica", 14))
        self.yes_button.grid(row = 2,column = 8, sticky = W)

        self.yes_button.bind("<Return>",self.approve)
        self.yes_button.focus()

        self.no_button = Button(self, text = "No", command = self.deny, font= ("Helvetica", 14))
        self.no_button.grid(row = 2,column = 2,sticky = W)

        self.no_button.bind("<Return>",self.deny)
        self.no_button.focus()

    def approve(self, *args):
        if self.label in self.approved:
            if self.filename in self.approved[self.label]:
                self.quit()
                return
            self.approved[self.label].append(self.filename)
        else:
            self.approved[self.label] = [self.filename]
        self.quit()
   
    def deny(self, *args):
        if self.label in self.denied:
            if self.filename in self.denied[self.label]:
                self.quit()
                return
            self.denied[self.label].append(self.filename)
        else:
            self.denied[self.label] = [self.filename]
        self.quit()
