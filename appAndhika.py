from flask import Flask, render_template, request, redirect, url_for, session, make_response
import mysql.connector
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = 'dikaaw'
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_rawatinap_dhika'
    )

def hitung_biaya(id_pasien):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT SUM(DATEDIFF(r.tgl_keluar, r.tgl_masuk) * k.harga) as total_biaya
    FROM rawatinap_dhika r
    JOIN kamar_dhika k ON r.id_kamar = k.id_kamar
    WHERE r.id_pasien = %s
    """
    cursor.execute(query, (id_pasien,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result[0] else 0

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usernameDhika = request.form['usernameDhika']
        passwordDhika = request.form['passwordDhika']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_dhika WHERE username = %s AND password = %s", (usernameDhika, passwordDhika))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            session['logged_in'] = True
            session['username'] = user[2]
            session['role'] = user[1]
            return redirect(url_for('home'))
        else:
            return render_template('login_Andhika_db1.html')
    else:
        return render_template('login_Andhika_db1.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route('/transaksi')
def home():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT t.id_transaksi, t.id_pasien, t.total_biaya, r.tgl_masuk, r.tgl_keluar, t.status_pembayaran, t.tgl FROM transaksi_dhika t JOIN rawatinap_dhika r ON t.id_pasien = r.id_pasien;")
        transaksi_list = cursor.fetchall()
        cursor.execute("SELECT id_pasien, nama FROM pasien_dhika")
        pasien_list = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        transaksi_list = []
        pasien_list = []
        total_pasien = total_kamar = total_rawatinap = total_biaya = 0
    admin = session.get('role') == 'Admin'
    return render_template(
        'hasil_Andhika_db1.html',
        transaksi_list=transaksi_list,
        admin=admin,
        pasien_list=pasien_list
    )

@app.route('/input_db1', methods=['POST'])
def input_db1():
    try:
        conn_gen = get_db_connection()
        cursor_gen = conn_gen.cursor()
        cursor_gen.execute("SELECT id_transaksi FROM transaksi_dhika ORDER BY id_transaksi DESC LIMIT 1")
        last_andhika = cursor_gen.fetchone()
        if last_andhika and last_andhika[0].startswith('TR'):
            num = int(last_andhika[0][2:]) + 1
        else:
            num = 1
        id_transaksi = f"TR{num:03d}"
        cursor_gen.close()
        conn_gen.close()
    except Exception as e:
        return f"Terjadi kesalahan saat generate ID: {str(e)}"
    idPasienDhika = request.form['idPasienDhika']
    totalBiayaDhika = hitung_biaya(idPasienDhika)
    statusBayarDhika = request.form['statusBayarDhika']
    tglDhika = request.form['tglDhika']
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO transaksi_dhika (id_transaksi, id_pasien, total_biaya, status_pembayaran, tgl) VALUES (%s, %s, %s, %s, %s)"
        val = (id_transaksi, idPasienDhika, totalBiayaDhika, statusBayarDhika, tglDhika)
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('home'))
    except Exception as e:
        return f"Terjadi kesalahan saat memasukkan data: {str(e)}"

@app.route('/edit_db1/<id_transaksi>', methods=['POST'])
def edit_db1(id_transaksi):
    idPasienDhika = request.form['idPasienDhika']
    totalBiayaDhika = hitung_biaya(idPasienDhika)
    statusBayarDhika = request.form['statusBayarDhika']
    tglDhika = request.form['tglDhika']
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE transaksi_dhika SET id_pasien=%s, total_biaya=%s, status_pembayaran=%s, tgl=%s WHERE id_transaksi=%s", (idPasienDhika, totalBiayaDhika, statusBayarDhika, tglDhika, id_transaksi))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('home'))
    except Exception as e:
        return f"Terjadi kesalahan saat mengupdate data: {str(e)}"

@app.route('/delete_db1/<id_transaksi>', methods=['POST'])
def delete_db1(id_transaksi):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transaksi_dhika WHERE id_transaksi=%s", (id_transaksi,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('home'))
    except Exception as e:
        return f"Terjadi kesalahan saat menghapus data: {str(e)}"
    
@app.route('/pasien')
def pasien():
    if session.get('role') != 'Admin':
        return redirect(url_for('home'))
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pasien_dhika;") # masukin query buat ambil tabel apa aja bebas
        pasien_list = cursor.fetchall() # variablenya bebas, ini buat ambil semua data dari tabel
        cursor.close()
        conn.close()
    except Exception as e: # nampilin error kalo koneksi gagal
        pasien_list = []
    admin = session.get('role') == 'Admin'
    return render_template('pasien_Andhika_db1.html', pasien_list=pasien_list, admin=admin)

@app.route('/kamar')
def kamar():
    if session.get('role') != 'Admin':
        return redirect(url_for('home'))
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM kamar_dhika;") # masukin query buat ambil tabel apa aja bebas
        kamar_list = cursor.fetchall() # variablenya bebas, ini buat ambil semua data dari tabel
        cursor.close()
        conn.close()
    except Exception as e: # nampilin error kalo koneksi gagal
        kamar_list = []
    admin = session.get('role') == 'Admin'
    return render_template('kamar_Andhika_db1.html', kamar_list=kamar_list, admin=admin)

@app.route('/rawatinap')
def rawatinap():
    if session.get('role') != 'Admin':
        return redirect(url_for('home'))
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rawatinap_dhika;") # masukin query buat ambil tabel apa aja bebas
        rawatinap_list = cursor.fetchall() # variablenya bebas, ini buat ambil semua data dari tabel
        cursor.close()
        conn.close()
    except Exception as e: # nampilin error kalo koneksi gagal
        rawatinap_list = []
    admin = session.get('role') == 'Admin'
    return render_template('rawatinap_Andhika_db1.html', rawatinap_list=rawatinap_list, admin=admin)

@app.route('/cetak')
def cetak():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_pasien, nama, alamat, kontak FROM pasien_dhika")
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf', uni=True)
    pdf.add_page()
    pdf.set_font('DejaVu', '', 16)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 12, 'Data Pasien Rawat Inap', align='C', ln=1)
    pdf.ln(4)
    pdf.set_font('DejaVu', '', 12)
    pdf.set_fill_color(220, 220, 220)
    pdf.set_text_color(0, 0, 0)
    left_margin = (210 - (40+60+60+40)) // 2
    pdf.set_x(left_margin)
    pdf.cell(40, 10, 'ID Pasien', 1, 0, 'C', True)
    pdf.cell(60, 10, 'Nama Pasien', 1, 0, 'C', True)
    pdf.cell(60, 10, 'Alamat', 1, 0, 'C', True)
    pdf.cell(40, 10, 'Kontak', 1, 1, 'C', True)
    fill = False
    for d in data:
        pdf.set_x(left_margin)
        pdf.set_fill_color(245, 245, 245) if fill else pdf.set_fill_color(255,255,255)
        pdf.cell(40, 10, str(d['id_pasien']), 1, 0, 'C', fill)
        pdf.cell(60, 10, d['nama'], 1, 0, 'C', fill)
        pdf.cell(60, 10, d['alamat'], 1, 0, 'C', fill)
        pdf.cell(40, 10, d['kontak'], 1, 1, 'C', fill)
        fill = not fill
    pdf_bytes = pdf.output(dest='S')
    if isinstance(pdf_bytes, bytearray):
        pdf_bytes = bytes(pdf_bytes)
    response = make_response(pdf_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=data_pasien.pdf'
    return response

@app.route('/cetak/<id_pasien>')
def cetak_satu_pasien(id_pasien):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_pasien, nama, alamat, kontak FROM pasien_dhika WHERE id_pasien=%s", (id_pasien,))
    d = cursor.fetchone()
    cursor.close()
    conn.close()
    if not d:
        return 'Data tidak ditemukan', 404
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf', uni=True)
    pdf.add_page()
    pdf.set_font('DejaVu', '', 16)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 12, 'Data Pasien Rawat Inap', align='C', ln=1)
    pdf.ln(6)
    pdf.set_font('DejaVu', '', 12)
    left_margin = (210 - (40+60+60+40)) // 2
    pdf.set_x(left_margin)
    pdf.set_fill_color(220, 220, 220)
    pdf.cell(40, 10, 'ID Pasien', 1, 0, 'C', True)
    pdf.cell(60, 10, 'Nama Pasien', 1, 0, 'C', True)
    pdf.cell(60, 10, 'Alamat', 1, 0, 'C', True)
    pdf.cell(40, 10, 'Kontak', 1, 1, 'C', True)
    pdf.set_x(left_margin)
    pdf.set_fill_color(255,255,255)
    pdf.cell(40, 10, str(d['id_pasien']), 1, 0, 'C', True)
    pdf.cell(60, 10, d['nama'], 1, 0, 'C', True)
    pdf.cell(60, 10, d['alamat'], 1, 0, 'C', True)
    pdf.cell(40, 10, d['kontak'], 1, 1, 'C', True)
    pdf_bytes = pdf.output(dest='S')
    if isinstance(pdf_bytes, bytearray):
        pdf_bytes = bytes(pdf_bytes)
    response = make_response(pdf_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=struk_pasien_{id_pasien}.pdf'
    return response

if __name__ == '__main__':
    app.run(debug=True)