# IMPORT LIBRARY PYTHON UNTUK MENUNJANG WSGI
import os
from flask import Flask, flash, request, redirect, send_file, render_template, send_from_directory
from werkzeug.utils import html, secure_filename
from filter import *
from remove_background import *
from smoothing import *

# UNTUK MEMANGGIL FUNGSI FLASK
app = Flask(__name__)

# LOKASI UPLOAD IMAGE
UPLOAD_FOLDER = 'static/upload/'  # LOKASI FOLDER

# JENIS FILE YANG DAPAT DIUPLOAD
ALLOWED_EXTENSIONS = {'png', 'PNG', 'JPG', 'jpg', 'JPEG', 'jpeg'}

# LOKASI UPLOAD PADA FLASK
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# FUNGSI JENIS FILE
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# HOMEPAGE
@app.route('/')
def home():
    return render_template('index.html') #render index.html


# PAGE FILTER
# METHOD UNTUK UPLOAD DAN DOWNLOAD FOTO
@app.route('/filter.html', methods=['GET', 'POST'])
def uploaded_file_filter():
    if request.method == 'POST':
        # periksa apakah permintaan posting memiliki file
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']

        # jika pengguna tidak memilih file, kemabli ke url filter
        # kirimkan bagian kosong print "tanpa nama file"
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            # lakukakan hal pertama
            try:
                # cek berkas extentions file di izinkan atau tidak
                file and allowed_file(file.filename)
                filename = secure_filename(file.filename)  # keamanan file

                # file disimpan di direktori 'static/upload/'
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                # lokasi hasil filter
                lokasi_gray = os.path.join(UPLOAD_FOLDER, "gray" + filename)
                lokasi_invert = os.path.join(UPLOAD_FOLDER, "invert" + filename)
                lokasi_pixel = os.path.join(UPLOAD_FOLDER, "pixel" + filename)

                # lokasi file image yang telah diupload
                image_upload = os.path.join(UPLOAD_FOLDER,  filename)

                # pemanggilan fungsi filter
                gray = filter_gray(image_upload, lokasi_gray)
                invert = filter_invert(image_upload, lokasi_invert)
                pixel = filter_pixelize(image_upload, lokasi_pixel)

                # lokasi untuk menampilkan di web
                hasil_gray = "gray" + filename
                hasil_invert = "invert" + filename
                hasil_pixel = "pixel" + filename

                # render template download_filter
                return render_template("download_filter.html",  value=filename,         # Value untuk nama file name (download file image)
                                                                gray=hasil_gray,        # sepia untuk menampilkan file name ke web (lokasi)
                                                                invert=hasil_invert,    # invert untuk menampilkan file name ke web (lokasi)
                                                                pixel=hasil_pixel)      # pixel untuk menampilkan file name ke web (lokasi)

            # jika terjadi error pada yang pertama maka redirect ke url filter
            except:
                return redirect('/filter.html')

    return render_template('filter.html')  # render filter.html

#url download file hasil gray
@app.route('/return-files/gray<filename>')
def return_files_gray(filename):
    file_path = UPLOAD_FOLDER + 'gray' + filename
    print(file_path)
    return send_file(file_path, as_attachment=True, attachment_filename='')

#url download file hasil invert
@app.route('/return-files/invert<filename>')
def return_files_invert(filename):
    file_path = UPLOAD_FOLDER + 'invert' + filename
    print(file_path)
    return send_file(file_path, as_attachment=True, attachment_filename='')

#url download file hasil pixel
@app.route('/return-files/pixel<filename>')
def return_files_pixel(filename):
    file_path = UPLOAD_FOLDER + 'pixel' + filename
    print(file_path)
    return send_file(file_path, as_attachment=True, attachment_filename='')



# PAGE REMOVE
# METHOD UNTUK UPLOAD DAN DOWNLOAD FOTO
@app.route('/remove.html', methods=['GET', 'POST'])
def uploaded_file_remove():
    if request.method == 'POST':
        # periksa apakah permintaan posting memiliki file
        if 'file' not in request.files:

            return redirect(request.url)

        file = request.files['file']
        
        # jika pengguna tidak memilih file, kemabli ke url filter
        # kirimkan bagian kosong print "tanpa nama file"
        if file.filename == '':

            return redirect(request.url)
        else:
            # lakukakan hal pertama
            try:
                # cek berkas extentions file di izinkan atau tidak
                file and allowed_file(file.filename)

                # keamanan file
                filename = secure_filename(file.filename)  

                # file disimpan di direktori 'static/upload/'
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                # lokasi hasil remove
                lokasi_putih = os.path.join(UPLOAD_FOLDER, "putih" + filename)
                lokasi_hitam = os.path.join(UPLOAD_FOLDER, "hitam" + filename)
                lokasi_transparan = os.path.join(UPLOAD_FOLDER, "transparan" + filename)

                 # lokasi file image yang telah diupload
                image_upload = os.path.join(UPLOAD_FOLDER,  filename)
                image_transparan = 'kotak.jpg'

                # pemanggilan fungsi remove background
                transparan = remove_transparan(image_upload,image_transparan, lokasi_transparan)

                # lokasi untuk menampilkan di web
                hasil_remove_background_transparan = "transparan" + filename

                
                return render_template("download_remove.html",value=filename,                           # Value untuk nama file name (download file image)
                                                            transparan=hasil_remove_background_transparan) # transparan untuk menampilkan file name ke web (lokasi)
            except:
                return redirect('/remove.html')
            

    return render_template('remove.html')

#url download file hasil background transparan
@app.route('/return-files/transparan<filename>')
def return_files_background_transparan(filename):
    file_path = UPLOAD_FOLDER + 'transparan' + filename
    print(file_path)
    return send_file(file_path, as_attachment=True, attachment_filename='')


# PAGE SMOOTHING
@app.route('/smoothing.html', methods=['GET', 'POST'])
def uploaded_file_smoothing():
    if request.method == 'POST':
        # periksa apakah permintaan posting memiliki file
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        
        # jika pengguna tidak memilih file, kemabli ke url filter
        # kirimkan bagian kosong print "tanpa nama file"
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            # lakukakan hal pertama
            try:
                # cek berkas extentions file di izinkan atau tidak
                file and allowed_file(file.filename)
                filename = secure_filename(file.filename)  # keamanan file

                # file disimpan di direktori 'static/upload/'
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                # lokasi hasil smoothing
                lokasi_smoothing = os.path.join(UPLOAD_FOLDER, "smooth" + filename)

                # lokasi file image yang telah diupload
                image_upload = os.path.join(UPLOAD_FOLDER,  filename)

                # lokasi untuk menampilkan di web
                hasil_smoothing = "smooth" + filename

                # pemanggilan fungsi smoothing
                smoothing = filter_smoothing(image_upload, lokasi_smoothing)

                # render template download_smoothing
                return render_template("download_smoothing.html", value=filename,               # Value untuk nama file name (download file image)
                                                                 smoothing=hasil_smoothing)     # smoothing untuk menampilkan file name ke web (lokasi)
            except:
                # jika terjadi error pada yang pertama maka redirect ke url 
                return redirect('/smoothing.html')

    return render_template('smoothing.html')


#url download file hasil smooth
@app.route('/return-files/smooth<filename>')
def return_files_smoothing(filename):
    file_path = UPLOAD_FOLDER + 'smooth' + filename
    print(file_path)
    return send_file(file_path, as_attachment=True, attachment_filename='')


#url untuk menampilkan hasil seluruh dalam 'statc/upload' file image ke web
@app.route("/downloadfile/<filename>", methods=['GET', 'POST'])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename) #send dari direktori 'statc/upload' + filename


# MENJALANKAN FLASK
if __name__ == "__main__":
    app.run(debug=True)
