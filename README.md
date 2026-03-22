# 🗺️ Interactive Floor Plan Management System

A full-stack solution for managing and displaying interactive, multi-level floor plans. This project consists of a **React/Vite Frontend** for the public-facing map, and a custom **Python Admin Dashboard** that acts as a local Content Management System (CMS) to seamlessly update the map without touching code.

## ✨ Features

### The React Frontend (Web App)
* **Dynamic Floor Navigation:** Switch between floors (e.g., B1, Ground, Level 1) with instant, lazy-loaded data fetching.
* **Interactive Map Pins:** Clickable locations that pull up a detailed sidebar with store names, lot numbers, descriptions, and logos.
* **Automated Asset Handling:** Reads directly from a single master Sprite Sheet for highly optimized, 120x120px high-definition logos.
* **Modern "Eye-Friendly" UI:** Designed with a soothing sky-blue and ocean palette to reduce eye strain, complete with soft shadows and pill-shaped navigation.

### The Python Admin Dashboard (mapper.py)
* **Visual Map Editor:** Click anywhere on the floor plan to drop a pin, fill out the store details in the sidebar, and save it permanently to JSON.
* **Automated Sprite Sheet Generator:** Drop individual .png logos into a folder, click "Generate", and the tool will automatically stitch them into a master sprite sheet and inject the precise CSS coordinates into your map data.
* **Floor Creation Wizard:** Easily add new floors and blueprint images through a step-by-step UI.
* **1-Click Export:** A dedicated staging environment allows you to edit safely, then push all data and images directly to the React public folder with one click.

---

## 🛠️ Tech Stack

* **Frontend:** React, Vite, standard CSS
* **Backend / Admin Tool:** Python 3, Tkinter (GUI), Pillow (Image Processing)
* **Database:** Local JSON files (No external database required)
* **Hosting:** GitHub Pages

---

## 🚀 Getting Started

### 1. Prerequisites
You will need both Node.js and Python installed on your machine.

* Install Node dependencies:
    cd interactive-floor-plan
    npm install

* Install Python dependencies:
    pip install Pillow

### 2. Running the Admin Dashboard (CMS)
This is where you manage your mall data, upload images, and draw pins.
```bash
cd floor-manager
python mapper.py
```

### 3. Running the React Website
This is the live preview of what your visitors will see.
```bash
cd interactive-floor-plan
npm run dev
```

---

## 📝 The Admin Workflow (How to update the map)

This project uses a "Local Staging" architecture. You make changes in the Python tool, then push them to the website.

1. **Add a Floor:** Open the Python tool, click `+ Add Floor`, and select a blueprint image.
2. **Upload Logos:** Click `+ Upload Store Logo` to add a store's branding to the SpriteLibrary.
3. **Generate Sprites:** Click `Generate Sprites`. The tool will stitch your logos together and sync the coordinates to your map data.
4. **Map Stores:** Select a floor, click on the map to place a yellow "Ghost Pin", enter the store details in the right sidebar, and click `Confirm & Add`.
5. **Publish:** Click `EXPORT TO WEB` and select the interactive-floor-plan/public folder. All your hard work will instantly sync to the React app!

---

## 🌐 Deployment
This project is configured to deploy easily to GitHub pages using the gh-pages package.

1. Ensure your vite.config.js has the correct base: '/your-repo-name/' path set.
2. Run the deployment script:
```bash
cd interactive-floor-plan
npm run deploy
```

3. Enable GitHub Pages in your repository settings (deploying from the gh-pages branch).