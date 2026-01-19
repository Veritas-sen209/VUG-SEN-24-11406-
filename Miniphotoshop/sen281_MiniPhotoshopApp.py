import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class MiniPhotoshop:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Image Filter App - Mini Photoshop")
        self.root.geometry("900x600")

        self.original_image = None
        self.processed_image = None

        # Buttons Frame
        btn_frame = tk.Frame(root)
        btn_frame.pack(side=tk.TOP, pady=10)

        tk.Button(btn_frame, text="Open Image", command=self.open_image).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Grayscale", command=self.grayscale).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Blur", command=self.blur).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Sharpen", command=self.sharpen).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Edge Detection", command=self.edge_detection).grid(row=0, column=4, padx=5)
        tk.Button(btn_frame, text="Increase Brightness", command=self.brightness).grid(row=0, column=5, padx=5)
        tk.Button(btn_frame, text="Reset", command=self.reset_image).grid(row=0, column=6, padx=5)
        tk.Button(btn_frame, text="Save Image", command=self.save_image).grid(row=0, column=7, padx=5)

        # Image Display
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

    def open_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.png *.jpeg")]
        )
        if path:
            self.original_image = cv2.imread(path)
            self.processed_image = self.original_image.copy()
            self.display_image(self.original_image)

    def display_image(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_pil = img_pil.resize((600, 400))
        img_tk = ImageTk.PhotoImage(img_pil)
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk

    def grayscale(self):
        if self.processed_image is not None:
            gray = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
            self.processed_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            self.display_image(self.processed_image)

    def blur(self):
        if self.processed_image is not None:
            self.processed_image = cv2.GaussianBlur(self.processed_image, (15, 15), 0)
            self.display_image(self.processed_image)

    def sharpen(self):
        if self.processed_image is not None:
            kernel = np.array([[0, -1, 0],
                               [-1, 5, -1],
                               [0, -1, 0]])
            self.processed_image = cv2.filter2D(self.processed_image, -1, kernel)
            self.display_image(self.processed_image)

    def edge_detection(self):
        if self.processed_image is not None:
            gray = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            self.processed_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            self.display_image(self.processed_image)

    def brightness(self):
        if self.processed_image is not None:
            self.processed_image = cv2.convertScaleAbs(
                self.processed_image, alpha=1, beta=50
            )
            self.display_image(self.processed_image)

    def reset_image(self):
        if self.original_image is not None:
            self.processed_image = self.original_image.copy()
            self.display_image(self.processed_image)

    def save_image(self):
        if self.processed_image is not None:
            path = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")]
            )
            if path:
                cv2.imwrite(path, self.processed_image)
                messagebox.showinfo("Saved", "Image saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MiniPhotoshop(root)
    root.mainloop()
