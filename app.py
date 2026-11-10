import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2


class CartoonifyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cartoonify - Image Cartoonizer")
        self.root.geometry("1050x720")
        self.root.minsize(850, 600)
        self.root.configure(bg="#f3f5f9")

        self.original_image = None
        self.cartoon_image = None
        self.current_path = None
        self.original_photo = None
        self.cartoon_photo = None

        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self.root, bg="#172554", height=85)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="Cartoonify Your Image",
            font=("Segoe UI", 24, "bold"), fg="white", bg="#172554"
        ).pack(pady=(13, 2))
        tk.Label(
            header, text="Turn your photos into cartoon-style artwork",
            font=("Segoe UI", 10), fg="#dbeafe", bg="#172554"
        ).pack()

        toolbar = tk.Frame(self.root, bg="#f3f5f9")
        toolbar.pack(fill="x", padx=24, pady=18)

        self.upload_btn = tk.Button(
            toolbar, text="  Upload Image  ", command=self.upload_image,
            font=("Segoe UI", 11, "bold"), bg="#2563eb", fg="white",
            activebackground="#1d4ed8", activeforeground="white",
            relief="flat", padx=12, pady=10, cursor="hand2"
        )
        self.upload_btn.pack(side="left", padx=(0, 10))

        self.cartoon_btn = tk.Button(
            toolbar, text="  Cartoonify  ", command=self.cartoonify,
            font=("Segoe UI", 11, "bold"), bg="#0f766e", fg="white",
            activebackground="#115e59", activeforeground="white",
            relief="flat", padx=12, pady=10, cursor="hand2", state="disabled"
        )
        self.cartoon_btn.pack(side="left", padx=10)

        self.save_btn = tk.Button(
            toolbar, text="  Save Cartoon  ", command=self.save_image,
            font=("Segoe UI", 11, "bold"), bg="#7c3aed", fg="white",
            activebackground="#6d28d9", activeforeground="white",
            relief="flat", padx=12, pady=10, cursor="hand2", state="disabled"
        )
        self.save_btn.pack(side="left", padx=10)

        self.reset_btn = tk.Button(
            toolbar, text="Reset", command=self.reset,
            font=("Segoe UI", 10), bg="#e2e8f0", fg="#1e293b",
            relief="flat", padx=14, pady=10, cursor="hand2"
        )
        self.reset_btn.pack(side="right")

        image_area = tk.Frame(self.root, bg="#f3f5f9")
        image_area.pack(fill="both", expand=True, padx=24, pady=(0, 12))
        image_area.grid_columnconfigure(0, weight=1)
        image_area.grid_columnconfigure(1, weight=1)
        image_area.grid_rowconfigure(1, weight=1)

        tk.Label(
            image_area, text="Original Image", font=("Segoe UI", 13, "bold"),
            bg="#f3f5f9", fg="#1e293b"
        ).grid(row=0, column=0, pady=(0, 9))
        tk.Label(
            image_area, text="Cartoon Result", font=("Segoe UI", 13, "bold"),
            bg="#f3f5f9", fg="#1e293b"
        ).grid(row=0, column=1, pady=(0, 9))

        self.original_panel = tk.Label(
            image_area, text="Upload an image to get started",
            bg="white", fg="#64748b", font=("Segoe UI", 11),
            relief="solid", bd=1, anchor="center"
        )
        self.original_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 8))

        self.cartoon_panel = tk.Label(
            image_area, text="Your cartoon image will appear here",
            bg="white", fg="#64748b", font=("Segoe UI", 11),
            relief="solid", bd=1, anchor="center"
        )
        self.cartoon_panel.grid(row=1, column=1, sticky="nsew", padx=(8, 0))

        self.status = tk.StringVar(value="Ready. Upload an image to begin.")
        tk.Label(
            self.root, textvariable=self.status, anchor="w",
            bg="#e2e8f0", fg="#334155", font=("Segoe UI", 9), padx=16, pady=9
        ).pack(fill="x", side="bottom")

    def _show_image(self, image, panel):
        height, width = image.shape[:2]
        max_width, max_height = 470, 430
        scale = min(max_width / width, max_height / height, 1)
        display_width = max(1, int(width * scale))
        display_height = max(1, int(height * scale))

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb).resize(
            (display_width, display_height), Image.Resampling.LANCZOS
        )
        photo = ImageTk.PhotoImage(pil_image)
        panel.configure(image=photo, text="")
        panel.image = photo
        return photo

    def upload_image(self):
        path = filedialog.askopenfilename(
            title="Choose an image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.webp"),
                ("All files", "*.*")
            ]
        )
        if not path:
            return

        image = cv2.imread(path)
        if image is None:
            messagebox.showerror("Unable to open image", "Please choose a valid image file.")
            return

        self.current_path = path
        self.original_image = image
        self.cartoon_image = None
        self.original_photo = self._show_image(image, self.original_panel)
        self.cartoon_panel.configure(
            image="", text="Click Cartoonify to create your result."
        )
        self.cartoon_panel.image = None
        self.cartoon_photo = None
        self.cartoon_btn.configure(state="normal")
        self.save_btn.configure(state="disabled")
        self.status.set(f"Loaded: {os.path.basename(path)}")

    def cartoonify(self):
        if self.original_image is None:
            messagebox.showwarning("No image", "Please upload an image first.")
            return

        try:
            # Step 1: Convert the image to grayscale.
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)

            # Step 2: Smooth the grayscale image.
            smooth_gray = cv2.medianBlur(gray, 5)

            # Step 3: Detect and highlight edges.
            edges = cv2.adaptiveThreshold(
                smooth_gray, 255,
                cv2.ADAPTIVE_THRESH_MEAN_C,
                cv2.THRESH_BINARY,
                9, 9
            )

            # Step 4: Smooth colours while preserving important edges.
            color = cv2.bilateralFilter(self.original_image, 9, 250, 250)

            # Step 5: Combine the smooth colour image and edge mask.
            self.cartoon_image = cv2.bitwise_and(color, color, mask=edges)

            self.cartoon_photo = self._show_image(
                self.cartoon_image, self.cartoon_panel
            )
            self.save_btn.configure(state="normal")
            self.status.set("Cartoon effect applied successfully.")
        except cv2.error as error:
            messagebox.showerror("Processing error", str(error))

    def save_image(self):
        if self.cartoon_image is None:
            messagebox.showwarning("Nothing to save", "Please cartoonify an image first.")
            return

        default_name = "cartoonified_image.png"
        if self.current_path:
            stem = os.path.splitext(os.path.basename(self.current_path))[0]
            default_name = f"{stem}_cartoon.png"

        path = filedialog.asksaveasfilename(
            title="Save cartoon image",
            initialfile=default_name,
            defaultextension=".png",
            filetypes=[
                ("PNG image", "*.png"),
                ("JPEG image", "*.jpg"),
                ("All files", "*.*")
            ]
        )
        if not path:
            return

        if cv2.imwrite(path, self.cartoon_image):
            self.status.set(f"Saved: {path}")
            messagebox.showinfo("Image saved", f"Your cartoon image was saved to:\n{path}")
        else:
            messagebox.showerror("Save failed", "The image could not be saved.")

    def reset(self):
        self.original_image = None
        self.cartoon_image = None
        self.current_path = None
        self.original_photo = None
        self.cartoon_photo = None
        self.original_panel.configure(image="", text="Upload an image to get started")
        self.cartoon_panel.configure(image="", text="Your cartoon image will appear here")
        self.original_panel.image = None
        self.cartoon_panel.image = None
        self.cartoon_btn.configure(state="disabled")
        self.save_btn.configure(state="disabled")
        self.status.set("Ready. Upload an image to begin.")


def main():
    root = tk.Tk()
    CartoonifyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
