from uuid import uuid4

def transaksi_id_generator():
    return int(uuid4().hex[:5], 16)