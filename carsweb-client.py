from flask import Flask, render_template, request, redirect, url_for
import json, requests
import os

# === PENGOBATAN JINJA ERROR (Deteksi Jalur Absolut Otomatis) ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'templates'), 
            static_folder=os.path.join(BASE_DIR, 'static'))

appType = 'Web Service'

# Terkoneksi aman ke server via IP Lokal 127.0.0.1 port 5012
alamatserver = "http://127.0.0.1:5012/cars"

@app.route('/')
def index():
    return render_template('index.html', appType=appType)

@app.route('/createcar')
def createcar():
    return render_template('createcar.html', appType=appType)

@app.route('/createcarsave', methods=['GET', 'POST'])
def createcarsave():
    datacar = {
        "carname" : request.form['carName'],
        "carbrand" : request.form['carBrand'], 
        "carmodel" : request.form['carModel'],
        "carprice" : request.form['carPrice']
    }
    headers = {'Content-Type':'application/json', 'Accept':'text/plain'}
    requests.post(alamatserver, data=json.dumps(datacar), headers=headers)
    return redirect(url_for('readcar'))

@app.route('/readcar')
def readcar():
    rows = []
    try:
        datas = requests.get(alamatserver)
        if datas.status_code == 200:
            rows = json.loads(datas.text)
    except:
        pass
    # Mengirim data ke readcar.html menggunakan variabel 'rows' bawaan dosen
    return render_template('readcar.html', rows=rows, appType=appType)

# === FITUR UPDATE YANG SUDAH DISESUAIKAN DENGAN FORM DOSEN ===
@app.route('/updatecar', methods=['GET', 'POST'])
def updatecar():
    if request.method == 'POST':
        # Mengambil data dari name="carName" dan name="carPrice" di updatecar.html
        datacar = {
            "carname" : request.form['carName'],
            "carprice" : request.form['carPrice']
        }
        headers = {'Content-Type':'application/json', 'Accept':'text/plain'}
        # Mengirim request PUT ke server untuk mengubah harga mobil
        requests.put(alamatserver, data=json.dumps(datacar), headers=headers)
        return redirect(url_for('readcar'))
        
    return render_template('updatecar.html', appType=appType)

@app.route('/deletecar')
def deletecar():
    return render_template('deletecar.html', appType=appType)

@app.route('/deletecarsave', methods=['GET', 'POST'])
def deletecarsave():
    datacar = {
        "carname" : request.form['carName']
    }
    headers = {'Content-Type':'application/json', 'Accept':'text/plain'}
    requests.delete(alamatserver, data=json.dumps(datacar), headers=headers)
    return redirect(url_for('readcar'))

# === FITUR SEARCH YANG SUDAH DISESUAIKAN DENGAN VARIABEL DATA DOSEN ===
@app.route('/searchcar', methods=['GET', 'POST'])
def searchcar():
    datas = []
    if request.method == 'POST':
        keyword = request.form['keyword']
        res = requests.get(f"{alamatserver}?keyword={keyword}")
        if res.status_code == 200:
            datas = json.loads(res.text)
            
    # Variabel dikirim dengan nama 'data=datas' agar terbaca oleh loop {% for row in data %} di searchcar.html
    return render_template('searchcar.html', data=datas, appType=appType)

if __name__ == '__main__':
    # Berjalan stabil di Port Client 5011
    app.run(host='0.0.0.0', debug=True, port=5011)