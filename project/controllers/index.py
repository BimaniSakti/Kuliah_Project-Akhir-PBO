from flask import render_template, request, redirect, url_for, session
from project.models import Penyewa, Mobil, Transaksi
from project.utils.id_gene import transaksi_id_generator


def index_page():
    if request.method == 'POST':
        session['tanggal_mulai'] = request.form['tanggal_mulai']
        session['tanggal_selesai'] = request.form['tanggal_selesai']
        session['waktu_mulai'] = request.form['waktu_mulai']
        session['waktu_selesai'] = request.form['waktu_selesai']
        session['jenis_peminjaman'] = request.form['jenis_peminjaman']
        return redirect(url_for('booking.car_select'))
    return render_template('index.html')
        