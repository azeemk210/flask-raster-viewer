# flask_geotiff_uploader.py
from flask import Flask, request, render_template, send_from_directory, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from osgeo import gdal
from pyproj import Transformer
import os

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"tif", "tiff", "jp2"}  # Now accepts .jp2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_bounds_wgs84(tif_path):
    ds = gdal.Open(tif_path)
    gt = ds.GetGeoTransform()
    cols = ds.RasterXSize
    rows = ds.RasterYSize

    ulx = gt[0]
    uly = gt[3]
    lrx = gt[0] + (cols * gt[1])
    lry = gt[3] + (rows * gt[5])

    # Reproject to EPSG:4326
    src_wkt = ds.GetProjection()
    transformer = Transformer.from_crs(src_wkt, "EPSG:4326", always_xy=True)
    sw = transformer.transform(ulx, lry)  # x=ulx, y=lry
    ne = transformer.transform(lrx, uly)

    return [[sw[1], sw[0]], [ne[1], ne[0]]]

def convert_to_png(input_raster, output_png):
    gdal.Translate(output_png, input_raster, format='PNG', creationOptions=["WORLDFILE=YES"])

@app.route('/')
def index():
    return redirect(url_for('upload'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part", 400
        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)

            # If it's .jp2, convert it to .tif first
            if filename.lower().endswith(".jp2"):
                tif_filename = filename.rsplit('.', 1)[0] + ".tif"
                tif_path = os.path.join(app.config['UPLOAD_FOLDER'], tif_filename)
                gdal.Translate(tif_path, input_path)
                input_path = tif_path

            # Convert to PNG
            png_filename = filename.rsplit('.', 1)[0] + ".png"
            png_path = os.path.join(app.config['UPLOAD_FOLDER'], png_filename)
            convert_to_png(input_path, png_path)

            # Get bounds
            bounds = get_bounds_wgs84(input_path)

            return render_template("index.html", raster_file=png_filename, bounds=bounds)

    return render_template("upload.html")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
