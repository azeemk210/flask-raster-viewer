# 🗺️ Flask Raster Viewer

A simple Flask web app to upload, georeference, and visualize raster files (GeoTIFF `.tif`, Sentinel `.jp2`) using Leaflet.

---

## 📦 Features

- Upload `.tif`, `.tiff`, or `.jp2` files
- Automatically:
  - Converts `.jp2` → `.tif` → `.png`
  - Extracts WGS84 bounds with GDAL
  - Displays the raster on a Leaflet map
- Toggle layer visibility on the map

---

## 🚀 Quick Start

### 1. Clone this repo

```bash
git clone https://github.com/azeemk210/flask-raster-viewer.git
cd flask-raster-viewer
```

### 2. Create environment

####  Using `conda` (recommended)

```bash
conda env create -f environment.yml
conda activate geoapp
```
pip install -r requirements.txt
```

### 3. Run the app

```bash
python app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 📁 Upload Format

Supported file types:
- `.tif`, `.tiff` (GeoTIFF with georeference)
- `.jp2` (Sentinel-2 imagery)

After upload:
- The raster is converted to `.png`
- Bounds are extracted and passed to Leaflet
- Map auto-zooms to the raster extent

---

## 📸 Screenshot

> !## 📸 Screenshot

![Map Viewer Screenshot](D:\QGIS\geoapp\image.png)

---

## 🧪 Dev Notes

- Built using:
  - Flask
  - GDAL (Python bindings)
  - Leaflet.js
- GDAL is required and must be installed properly with `conda` or a precompiled wheel (Windows users see: [Gohlke Wheels](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal))

---

## 📝 License

MIT License — feel free to use, modify, and share.