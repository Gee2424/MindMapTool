from tkinter import *
from tkinter import simpledialog, colorchooser
from tkinter import messagebox
from PIL import ImageGrab

class Node:
    def __init__(self, canvas, x, y, text, radius=20, color="blue"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.radius = radius

        self.node_id = self.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius, fill=self.color
        )
        self.text_id = self.canvas.create_text(x, y, text=self.text, fill='white')

    def move_to(self, x, y):
        self.x = x
        self.y = y

        self.canvas.move(self.node_id, x - self.x, y - self.y)
        self.canvas.move(self.text_id, x - self.x, y - self.y)

class MindMap:
    def __init__(self, master):
        self.master = master
        self.master.title("Mind Map Maker")

        self.title_label = Label(self.master, text="Mind Map Maker", font=("Arial", 24))
        self.title_label.pack(side=TOP, pady=10)

        self.canvas = Canvas(self.master, width=800, height=600, bg='white')
        self.canvas.pack(expand=YES, fill=BOTH)

        self.node_color = "blue"
        self.edge_color = "black"

        self.nodes = []
        self.previous_node = None

        self.canvas.bind("<Button-1>", self.create_node)
        self.canvas.bind("<Button-3>", self.delete_node)  # right click to delete node
        self.canvas.bind("<B>", self.save_image)

        # UI improvements
        self.control_frame = Frame(self.master)
        self.control_frame.pack(side=BOTTOM, pady=10)

        self.save_button = Button(self.control_frame, text="Save Image", command=self.save_image)
        self.save_button.pack(side=LEFT, padx=10)

        self.color_button = Button(self.control_frame, text="Choose Node Color", command=self.choose_color)
        self.color_button.pack(side=LEFT)

    def create_node(self, event):
        x, y = event.x, event.y
        text = simpledialog.askstring("Input", "Enter node text:")
        if text is None:
            return
        node = Node(self.canvas, x, y, text, color=self.node_color)
        self.nodes.append(node)

        if self.previous_node:
            self.canvas.create_line(self.previous_node.x, self.previous_node.y, x, y, fill=self.edge_color)

        self.previous_node = node

    def delete_node(self, event):
        x, y = event.x, event.y
        item = self.canvas.find_closest(x, y)
        for node in self.nodes:
            if node.node_id == item[0] or node.text_id == item[0]:
                self.canvas.delete(node.node_id)
                self.canvas.delete(node.text_id)
                self.nodes.remove(node)
                break
        else:
            messagebox.showinfo("No Node Found", "No node found at this location.")

    def save_image(self):
        x = self.master.winfo_rootx() + self.canvas.winfo_x()
        y = self.master.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        img_path = simpledialog.askstring("Input", "Enter image path (include .jpg, .png, .bmp):")
        if img_path is None:
            return
        # Check that img_path ends with a valid image file extension
        if not (img_path.endswith('.jpg') or img_path.endswith('.png') or img_path.endswith('.bmp')):
            messagebox.showerror("Error", "Invalid file extension. Please use .jpg, .png, or .bmp")
            return
        ImageGrab.grab().crop((x, y, x1, y1)).save(img_path)

    def choose_color(self):
        # Open color chooser dialog
        color_code = colorchooser.askcolor(title="Choose color")
        if color_code:
            self.node_color = color_code[1]

root = Tk()
my_gui = MindMap(root)
root.mainloop()
