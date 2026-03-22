import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
import json
import os
import shutil

# --- CONFIGURATION ---
BASE_DIR = "public/Floor"
SPRITE_DIR = "SpriteLibrary" # New Default Logo Folder
CONFIG_FILE = os.path.join(BASE_DIR, "floors.json")
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
PIN_RADIUS = 8

class MapperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Floor Plan Admin Tool - Local Staging")
        self.root.geometry("1300x750")

        self.active_floor_folder = None
        self.stores = []
        self.floor_config = []
        self.pending_coords = None
        self.selected_store_id = None 

        # Ensure staging directories exist
        if not os.path.exists(BASE_DIR):
            os.makedirs(BASE_DIR)
        if not os.path.exists(SPRITE_DIR):
            os.makedirs(SPRITE_DIR)

        self.setup_ui()
        self.load_master_config()

    def setup_ui(self):
        # 1. LEFT SIDEBAR (Floor Management & Export)
        self.left_sidebar = tk.Frame(self.root, width=200, bg="#1e293b", padx=10, pady=10)
        self.left_sidebar.pack(side="left", fill="y")

        tk.Label(self.left_sidebar, text="LOCAL FLOORS", fg="white", bg="#1e293b", font=("Arial", 10, "bold")).pack(pady=5)
        self.btn_new_floor = tk.Button(self.left_sidebar, text="+ Add Floor", command=self.add_floor_wizard)
        self.btn_new_floor.pack(fill="x", pady=5)

        self.floor_listbox = tk.Listbox(self.left_sidebar, bg="#334155", fg="white", bd=0, highlightthickness=0)
        self.floor_listbox.pack(fill="both", expand=True, pady=10)
        self.floor_listbox.bind('<<ListboxSelect>>', self.on_floor_select)

        # SPRITE ASSETS SECTION
        tk.Label(self.left_sidebar, text="ASSETS", fg="white", bg="#1e293b", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        
        self.btn_upload_logo = tk.Button(self.left_sidebar, text="+ Upload Store Logo", bg="#475569", fg="white", 
                                    font=("Arial", 9), command=self.upload_logo)
        self.btn_upload_logo.pack(fill="x", pady=2)

        self.btn_sprite = tk.Button(self.left_sidebar, text="GENERATE SPRITES", bg="#f59e0b", fg="white", 
                                    font=("Arial", 10, "bold"), command=self.generate_sprite_sheet)
        self.btn_sprite.pack(fill="x", pady=(2, 10))

        # EXPORT SECTION
        tk.Label(self.left_sidebar, text="PRODUCTION", fg="white", bg="#1e293b", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        self.btn_export = tk.Button(self.left_sidebar, text="EXPORT TO WEB", bg="#8b5cf6", fg="white", 
                                    font=("Arial", 10, "bold"), command=self.export_project)
        self.btn_export.pack(fill="x", pady=5)

        # 2. CENTER CANVAS (The Map)
        self.center_frame = tk.Frame(self.root, bg="#f1f5f9")
        self.center_frame.pack(side="left", fill="both", expand=True)
        
        self.canvas_label = tk.Label(self.center_frame, text="Select a floor from the left menu", font=("Arial", 14), bg="#f1f5f9", fg="#64748b")
        self.canvas_label.place(relx=0.5, rely=0.5, anchor="center")

        self.canvas = tk.Canvas(self.center_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white", highlightthickness=1, highlightbackground="#cbd5e1")
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # 3. RIGHT SIDEBAR (The Editor)
        self.right_sidebar = tk.Frame(self.root, width=300, bg="#f8fafc", padx=20, pady=20, bd=1, relief="sunken")
        self.right_sidebar.pack(side="right", fill="y")

        self.lbl_mode = tk.Label(self.right_sidebar, text="MODE: IDLE", font=("Arial", 10, "bold"), fg="#64748b", bg="#f8fafc")
        self.lbl_mode.pack(pady=(0, 10))
        
        tk.Label(self.right_sidebar, text="Store Name:", bg="#f8fafc").pack(anchor="w")
        self.ent_name = tk.Entry(self.right_sidebar)
        self.ent_name.pack(fill="x", pady=(0, 15))

        tk.Label(self.right_sidebar, text="Lot Number:", bg="#f8fafc").pack(anchor="w")
        self.ent_lot = tk.Entry(self.right_sidebar)
        self.ent_lot.pack(fill="x", pady=(0, 15))

        tk.Label(self.right_sidebar, text="Description:", bg="#f8fafc").pack(anchor="w")
        self.txt_desc = tk.Text(self.right_sidebar, height=4)
        self.txt_desc.pack(fill="x", pady=(0, 20))

        self.btn_action = tk.Button(self.right_sidebar, text="CONFIRM & ADD PIN", bg="#3b82f6", fg="white", 
                                     font=("Arial", 10, "bold"), command=self.handle_action, state="disabled")
        self.btn_action.pack(fill="x")

        self.btn_delete = tk.Button(self.right_sidebar, text="DELETE STORE", bg="#ef4444", fg="white", 
                                     font=("Arial", 10, "bold"), command=self.delete_store, state="disabled")
        self.btn_delete.pack(fill="x", pady=10)

        tk.Label(self.right_sidebar, text="---", bg="#f8fafc").pack(pady=20)

        self.btn_save_json = tk.Button(self.right_sidebar, text="SAVE PINS", bg="#22c55e", fg="white", 
                                       font=("Arial", 10, "bold"), command=self.save_data)
        self.btn_save_json.pack(side="bottom", fill="x")

    # --- ASSET LOGIC ---
    def upload_logo(self):
        source_path = filedialog.askopenfilename(title="Select Logo Image", filetypes=[("Images", "*.png *.jpg *.jpeg")], parent=self.root)
        if not source_path: return
        
        # Force the UI to update and settle before launching the next popup
        self.root.update()
        
        store_name = simpledialog.askstring("Store Name", "Which store is this logo for?\n(Type it exactly as it appears on the map)", parent=self.root)
        if not store_name: return
        
        ext = os.path.splitext(source_path)[1]
        dest_path = os.path.join(SPRITE_DIR, f"{store_name}{ext}")
        
        try:
            shutil.copy(source_path, dest_path)
            messagebox.showinfo("Success", f"Logo added to Library as '{store_name}{ext}'!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy image: {e}", parent=self.root)

    def generate_sprite_sheet(self):
        ICON_SIZE = 120
        COLUMNS = 10
        
        valid_exts = {'.png', '.jpg', '.jpeg'}
        images = [f for f in os.listdir(SPRITE_DIR) if os.path.splitext(f)[1].lower() in valid_exts]
                
        if not images:
            messagebox.showwarning("No Images", "The Sprite Library is empty. Upload some logos first!")
            return

        rows = (len(images) + COLUMNS - 1) // COLUMNS
        sprite_w = COLUMNS * ICON_SIZE
        sprite_h = rows * ICON_SIZE

        master_img = Image.new("RGBA", (sprite_w, sprite_h), (255, 255, 255, 0))
        logo_mapping = {}

        for idx, filename in enumerate(images):
            filepath = os.path.join(SPRITE_DIR, filename)
            try:
                img = Image.open(filepath).convert("RGBA")
                img = img.resize((ICON_SIZE, ICON_SIZE), Image.Resampling.LANCZOS)
                
                col = idx % COLUMNS
                row = idx // COLUMNS
                x = col * ICON_SIZE
                y = row * ICON_SIZE
                
                master_img.paste(img, (x, y))
                
                name_without_ext = os.path.splitext(filename)[0].lower().strip()
                logo_mapping[name_without_ext] = {"x": x, "y": y}
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

        # Save to public folder so React can see it
        sprite_path = os.path.join("public", "icons-sprite.png")
        master_img.save(sprite_path)

        updated_count = 0
        for floor in self.floor_config:
            data_path = os.path.join(BASE_DIR, floor['folder'], "data.json")
            if os.path.exists(data_path):
                with open(data_path, "r") as f:
                    floor_stores = json.load(f)
                
                changed = False
                for s in floor_stores:
                    store_name_lower = s['name'].lower().strip()
                    if store_name_lower in logo_mapping:
                        s['spriteX'] = logo_mapping[store_name_lower]['x']
                        s['spriteY'] = logo_mapping[store_name_lower]['y']
                        changed = True
                        updated_count += 1
                
                if changed:
                    with open(data_path, "w") as f:
                        json.dump(floor_stores, f, indent=2)

        if self.active_floor_folder:
            
            self.load_floor_map()

        messagebox.showinfo("Success", f"Sprite Sheet generated!\n\nLinked {updated_count} logos to stores on the map.")

    # --- WIZARD & EXPORT LOGIC ---
    def add_floor_wizard(self):
        folder_name = simpledialog.askstring("New Floor", "Enter Folder Number/ID (e.g., 0, 1, B1):", parent=self.root)
        if not folder_name: return
        
        self.root.update() # Take a breath
        
        display_name = simpledialog.askstring("New Floor", f"Enter Display Name for '{folder_name}':", parent=self.root)
        if not display_name: return
        
        self.root.update() # Take a breath
        
        messagebox.showinfo("Map Image", "Please select the Map Image (.png or .jpg) for this floor.", parent=self.root)
        image_source = filedialog.askopenfilename(title="Select Map Image", filetypes=[("Images", "*.png *.jpg")], parent=self.root)
        if not image_source: return

        target_dir = os.path.join(BASE_DIR, folder_name)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        shutil.copy(image_source, os.path.join(target_dir, "map.png"))
        
        if not any(f['folder'] == folder_name for f in self.floor_config):
            self.floor_config.append({"folder": folder_name, "name": display_name})
            with open(CONFIG_FILE, "w") as f:
                json.dump(self.floor_config, f, indent=2)
            self.refresh_floor_list()
            messagebox.showinfo("Success", f"Floor '{display_name}' added to local staging!", parent=self.root)

    def export_project(self):
        self.save_data() 
        messagebox.showinfo("Export", "Select the 'public' folder of your React website project.\n\n(e.g., interactive-floor-plan/public)")
        target_web_dir = filedialog.askdirectory(title="Select React 'public' Folder")
        if not target_web_dir: return
        
        dest_floor_path = os.path.join(target_web_dir, "Floor")
        dest_sprite_img = os.path.join(target_web_dir, "icons-sprite.png")
        
        try:
            # Copy Floor Folders
            shutil.copytree(BASE_DIR, dest_floor_path, dirs_exist_ok=True)
            
            # Copy the generated sprite sheet if it exists
            local_sprite_img = os.path.join("public", "icons-sprite.png")
            if os.path.exists(local_sprite_img):
                shutil.copy(local_sprite_img, dest_sprite_img)
                
            messagebox.showinfo("Export Successful", "All map data and sprites exported!\nRefresh your website to see changes.")
        except Exception as e:
            messagebox.showerror("Export Failed", f"An error occurred:\n{str(e)}")

    def load_master_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                self.floor_config = json.load(f)
            self.refresh_floor_list()

    def refresh_floor_list(self):
        self.floor_listbox.delete(0, tk.END)
        for floor in self.floor_config:
            self.floor_listbox.insert(tk.END, floor['name'])

    def on_floor_select(self, event):
        selection = self.floor_listbox.curselection()
        if not selection: return
        idx = selection[0]
        self.active_floor_folder = self.floor_config[idx]['folder']
        self.load_floor_map()

    def load_floor_map(self):
        map_path = os.path.join(BASE_DIR, self.active_floor_folder, "map.png")
        if not os.path.exists(map_path):
            messagebox.showerror("Error", f"No 'map.png' found in {map_path}")
            return

        img = Image.open(map_path).resize((CANVAS_WIDTH, CANVAS_HEIGHT))
        self.tk_img = ImageTk.PhotoImage(img)
        
        self.canvas_label.place_forget()
        self.canvas.pack(padx=20, pady=20)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

        data_path = os.path.join(BASE_DIR, self.active_floor_folder, "data.json")
        if os.path.exists(data_path):
            with open(data_path, "r") as f:
                self.stores = json.load(f)
            self.draw_existing_pins()
        else:
            self.stores = []
        
        self.reset_editor()

    # --- PINNING & EDITING LOGIC ---
    def on_canvas_click(self, event):
        if not self.active_floor_folder: return
        
        clicked_store = None
        for s in self.stores:
            if abs(s['x'] - event.x) < PIN_RADIUS and abs(s['y'] - event.y) < PIN_RADIUS:
                clicked_store = s
                break
        
        if clicked_store:
            self.selected_store_id = clicked_store['id']
            self.lbl_mode.config(text=f"MODE: EDITING", fg="#3b82f6")
            
            self.ent_name.delete(0, tk.END)
            self.ent_name.insert(0, clicked_store['name'])
            self.ent_lot.delete(0, tk.END)
            self.ent_lot.insert(0, clicked_store.get('lot', ''))
            self.txt_desc.delete("1.0", tk.END)
            self.txt_desc.insert("1.0", clicked_store.get('description', ''))
            
            self.btn_action.config(text="UPDATE STORE", state="normal", bg="#f59e0b")
            self.btn_delete.config(state="normal")
            self.canvas.delete("temp_pin")
        else:
            self.selected_store_id = None
            self.lbl_mode.config(text="MODE: ADDING NEW", fg="#22c55e")
            self.pending_coords = (event.x, event.y)
            
            self.ent_name.delete(0, tk.END)
            self.ent_lot.delete(0, tk.END)
            self.txt_desc.delete("1.0", tk.END)
            
            self.canvas.delete("temp_pin")
            self.canvas.create_oval(event.x-6, event.y-6, event.x+6, event.y+6, fill="yellow", tags="temp_pin")
            
            self.btn_action.config(text="CONFIRM & ADD PIN", state="normal", bg="#3b82f6")
            self.btn_delete.config(state="disabled")
            self.ent_name.focus()

    def handle_action(self):
        name = self.ent_name.get()
        lot = self.ent_lot.get()
        desc = self.txt_desc.get("1.0", tk.END).strip()

        if not name:
            messagebox.showwarning("Error", "Store Name is required.")
            return

        if self.selected_store_id:
            for s in self.stores:
                if s['id'] == self.selected_store_id:
                    s['name'] = name
                    s['lot'] = lot
                    s['description'] = desc
                    break
        else:
            x, y = self.pending_coords
            new_store = {
                "id": f"S{len(self.stores) + 101}",
                "name": name,
                "lot": lot or "N/A",
                "description": desc,
                "category": "Retail",
                "status": "Open",
                "x": x,
                "y": y,
                "spriteX": 0, "spriteY": 0
            }
            self.stores.append(new_store)

        self.redraw_canvas()
        self.reset_editor()

    def delete_store(self):
        if not self.selected_store_id: return
        if messagebox.askyesno("Delete", "Are you sure you want to remove this store?"):
            self.stores = [s for s in self.stores if s['id'] != self.selected_store_id]
            self.redraw_canvas()
            self.reset_editor()

    def redraw_canvas(self):
        map_path = os.path.join(BASE_DIR, self.active_floor_folder, "map.png")
        img = Image.open(map_path).resize((CANVAS_WIDTH, CANVAS_HEIGHT))
        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
        self.draw_existing_pins()

    def draw_existing_pins(self):
        for s in self.stores:
            self.draw_pin(s['x'], s['y'], s['name'])

    def draw_pin(self, x, y, name):
        self.canvas.create_oval(x-6, y-6, x+6, y+6, fill="#3b82f6", outline="white", width=2)
        self.canvas.create_text(x, y-18, text=name, fill="#1e293b", font=("Arial", 8, "bold"))

    def reset_editor(self):
        self.selected_store_id = None
        self.lbl_mode.config(text="MODE: IDLE", fg="#64748b")
        self.ent_name.delete(0, tk.END)
        self.ent_lot.delete(0, tk.END)
        self.txt_desc.delete("1.0", tk.END)
        self.btn_action.config(state="disabled", text="CONFIRM & ADD PIN", bg="#3b82f6")
        self.btn_delete.config(state="disabled")
        self.canvas.delete("temp_pin")

    def save_data(self):
        if not self.active_floor_folder: return
        path = os.path.join(BASE_DIR, self.active_floor_folder, "data.json")
        with open(path, "w") as f:
            json.dump(self.stores, f, indent=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = MapperApp(root)
    root.mainloop()