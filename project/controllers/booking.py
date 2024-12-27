from flask import render_template, request, redirect, url_for, session
from project.models import Penyewa, Mobil, Transaksi
from project.utils.id_gene import transaksi_id_generator
from datetime import datetime


def pilih_mobil():
    if request.method == "POST":
        session['mobil_id'] = request.form.get('mobil_id')
        return redirect(url_for('booking.pickup_location'))
    cars = Mobil.get_all_cars()
    return render_template('jenis-supir.html', cars=cars) 
    
def lokasi_jemput():
    if request.method == "POST":
        session['lokasi_jemput'] = request.form['lokasi_jemput']
        return redirect(url_for('booking.contact_detail'))
    car = Mobil.get_by_id(session.get('mobil_id'))
    tanggal_mulai = session.get('tanggal_mulai')
    tanggal_selesai = session.get('tanggal_selesai')
    return render_template('jenis-pilihan.html', car=car, tanggal_mulai=tanggal_mulai, tanggal_selesai=tanggal_selesai)

def data_diri():
    if request.method == "POST":
        session['nama_penyewa'] = request.form.get('nama_penyewa')
        session['no_telepon'] = request.form.get('no_telepon')
        session['email'] = request.form.get('email')
        
        mobil_id = session.get('mobil_id')
        mobil = Mobil.get_by_id(mobil_id)
        
        if not mobil:
            return "Mobil tidak ditemukan", 400
        
        tanggal_mulai = session.get('tanggal_mulai')
        tanggal_selesai = session.get('tanggal_selesai')
        lokasi_jemput = session.get('lokasi_jemput')
        jenis_peminjaman = session.get('jenis_peminjaman')
        
        start_date = datetime.strptime(tanggal_mulai, '%Y-%m-%d')
        end_date = datetime.strptime(tanggal_selesai, '%Y-%m-%d')

        total_harga_harian = (end_date - start_date).days * mobil.harga_mobil
        
        biaya_tambahan = 0

        if "waktu_selesai" in session:
            waktu_selesai = session['waktu_selesai']
            full_datetime_selesai = f"{tanggal_selesai} {waktu_selesai}"
            waktu_selesai_obj = datetime.strptime(full_datetime_selesai, '%Y-%m-%d %H:%M')

            waktu_lebih = (waktu_selesai_obj - end_date).total_seconds()

            if waktu_lebih > 0:
                jam_lebih = waktu_lebih // 3600  
                if jam_lebih >= 1:
                    biaya_tambahan = jam_lebih * 50000 
        total_harga = total_harga_harian + biaya_tambahan

        transaksi_id = transaksi_id_generator()
        Penyewa.insert_rent(session.get('nama_penyewa'), session.get('no_telepon'), session.get('email'))
        penyewa = Penyewa.get_by_id(nama_penyewa=session.get('nama_penyewa'), no_telepon=session.get('no_telepon'))
        Transaksi.insertBooking(
            transaksi_id=transaksi_id, 
            tanggal_mulai=tanggal_mulai, 
            tanggal_selesai=tanggal_selesai, 
            biaya_tambahan=biaya_tambahan, 
            total_biaya=total_harga, 
            status_peminjaman=session.get('jenis_peminjaman'), 
            status_transaksi="Pending",
            penyewa_id=penyewa.penyewa_id,
            mobil_id=session.get('mobil_id')
        )

        session.clear()
        return redirect(url_for('main.index'))
    
    mobil_id = session.get('mobil_id')
    mobil = Mobil.get_by_id(mobil_id)

    if not mobil:
        return "Mobil tidak ditemukan", 400
    
    tanggal_mulai = session.get('tanggal_mulai')
    tanggal_selesai = session.get('tanggal_selesai')
    lokasi_jemput = session.get('lokasi_jemput')
    jenis_peminjaman = session.get('jenis_peminjaman')
    
    start_date = datetime.strptime(tanggal_mulai, '%Y-%m-%d')
    end_date = datetime.strptime(tanggal_selesai, '%Y-%m-%d')

    total_harga_harian = (end_date - start_date).days * mobil.harga_mobil
    
    biaya_tambahan = 0

    if "waktu_selesai" in session:
        waktu_selesai = session['waktu_selesai']
        full_datetime_selesai = f"{tanggal_selesai} {waktu_selesai}"
        waktu_selesai_obj = datetime.strptime(full_datetime_selesai, '%Y-%m-%d %H:%M')

        waktu_lebih = (waktu_selesai_obj - end_date).total_seconds()

        if waktu_lebih > 0:
            jam_lebih = waktu_lebih // 3600  
            if jam_lebih >= 1:
                biaya_tambahan = int(jam_lebih * 50000) 
    total_harga = int(total_harga_harian + biaya_tambahan)

    return render_template(
        'form.html', 
        car=mobil, 
        tanggal_mulai=tanggal_mulai, 
        tanggal_selesai=tanggal_selesai, 
        total_harga_harian=total_harga_harian, 
        lokasi_jemput=lokasi_jemput,
        jenis_peminjaman=jenis_peminjaman,
        biaya_tambahan=biaya_tambahan, 
        total_harga=total_harga, 
        status_peminjaman=session.get('jenis_peminjaman'), 
        status_transaksi="Pending"
    )