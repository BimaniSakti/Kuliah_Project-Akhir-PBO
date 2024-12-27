from project.controllers.booking import pilih_mobil, lokasi_jemput, data_diri
from flask import Blueprint

booking = Blueprint('booking', __name__, url_prefix='/booking')

@booking.route('/', methods=['GET'])
def bookings():
    return 'Tugas Banyak'

@booking.route('/pilih_mobil', methods=['GET', 'POST'])
def car_select():
    return pilih_mobil()

@booking.route('/lokasi_jemput', methods=['GET', 'POST'])
def pickup_location():
    return lokasi_jemput()

@booking.route('/data-diri', methods=['GET', 'POST'])
def contact_detail():
    return data_diri()