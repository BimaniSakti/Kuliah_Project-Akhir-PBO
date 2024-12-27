from project import db


class Penyewa(db.Model):
    __tablename__ = "penyewa"
    
    penyewa_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_penyewa = db.Column(db.String(255), nullable=False)
    no_telepon = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    transaksi = db.relationship('Transaksi', back_populates="penyewa")
    
    def __init__(self, nama_penyewa:str, no_telepon:str, email:str):
        self.nama_penyewa = nama_penyewa
        self.no_telepon = no_telepon
        self.email = email
        
    @staticmethod
    def get_by_id(nama_penyewa:str, no_telepon:str):
        return Penyewa.query.filter_by(nama_penyewa=nama_penyewa, no_telepon=no_telepon).first()    
    
    @staticmethod
    def insert_rent(nama_penyewa:str, no_telepon:str, email:str):
        rent = Penyewa(nama_penyewa=nama_penyewa, no_telepon=no_telepon, email=email)
        db.session.add(rent)
        db.session.commit()
        return rent
        
    def __repr__(self):
        return f"< Penyewa {self.penyewa_id} >"
    
class Mobil(db.Model):
    __tablename__ = "mobil"
    
    mobil_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    merk = db.Column(db.String(255), nullable=False)
    gambar_mobil = db.Column(db.String(255), nullable=False)
    deskripsi_mobil = db.Column(db.String(255), nullable=False)
    harga_mobil = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    transaksi = db.relationship('Transaksi', back_populates='mobil')
    
    def __init__(self, merk:str, deskripsi_mobil:str, harga_mobil:int):
        self.merk = merk
        self.deskripsi_mobil = deskripsi_mobil
        self.harga_mobil = harga_mobil
        
    @staticmethod
    def get_by_id(mobil_id:int):
        return Mobil.query.filter_by(mobil_id=mobil_id).first()
    
    @staticmethod
    def get_all_cars():
        return Mobil.query.all()
    
    def __repr__(self):
        return f"< mobil {self.mobil_id} >"


class Transaksi(db.Model):
    __tablename__ = "transaksi"
    
    transaksi_id = db.Column(db.Integer, primary_key=True)
    tanggal_mulai = db.Column(db.DateTime, nullable=False)
    tanggal_selesai = db.Column(db.DateTime, nullable=False)
    biaya_tambahan = db.Column(db.Integer, nullable=False, default=0)
    total_biaya = db.Column(db.Integer, nullable=False)
    status_peminjaman = db.Column(db.Enum('Dengan Supir', 'Lepas Kunci'), nullable=False)
    status_transaksi = db.Column(db.Enum('Selesai', 'Pending'), nullable=False, default='Pending')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    penyewa_id = db.Column(db.Integer, db.ForeignKey('penyewa.penyewa_id'), nullable=False)
    mobil_id = db.Column(db.Integer, db.ForeignKey('mobil.mobil_id'), nullable=False)
    
    penyewa = db.relationship('Penyewa', back_populates='transaksi')
    mobil = db.relationship('Mobil', back_populates='transaksi')

    def __init__(self, transaksi_id:str, tanggal_mulai:str, tanggal_selesai:str, biaya_tambahan:int, total_biaya:int, status_peminjaman:str, status_transaksi:str, penyewa_id:int, mobil_id:int):
        self.transaksi_id = transaksi_id
        self.tanggal_mulai = tanggal_mulai
        self.tanggal_selesai = tanggal_selesai
        self.biaya_tambahan = biaya_tambahan
        self.total_biaya = total_biaya
        self.status_peminjaman = status_peminjaman
        self.status_transaksi = status_transaksi
        self.penyewa_id = penyewa_id
        self.mobil_id = mobil_id
        
    @staticmethod
    def hitung_total_harga(harga_per_hari, start_datetime, end_datetime, biaya_tambahan_per_jam):
        """
        Hitung total harga berdasarkan parameter input.
        """
        duration = end_datetime - start_datetime
        days = duration.days
        hours = (duration.seconds // 3600)

        total_harga_harian = days * harga_per_hari
        waktu_lebih = hours * biaya_tambahan_per_jam
        return total_harga_harian + waktu_lebih   
    
    @staticmethod
    def insertBooking(transaksi_id:str, tanggal_mulai:str, tanggal_selesai:str, biaya_tambahan:int, total_biaya:int, status_peminjaman:str, status_transaksi:str, penyewa_id:int, mobil_id:int):
        transaksi = Transaksi(transaksi_id, tanggal_mulai, tanggal_selesai, biaya_tambahan, total_biaya, status_peminjaman, status_transaksi, penyewa_id, mobil_id)
        db.session.add(transaksi)
        db.session.commit()
    
    def __repr__(self):
        return f"< Transaksi {self.transaksi_id} >"