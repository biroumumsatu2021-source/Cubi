import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Konfigurasi Halaman
st.set_page_config(page_title="CUBI - Cuti Biro Umum", page_icon="🏃", layout="wide")

# Inisialisasi State (Simulasi Database)
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'user_nip' not in st.session_state:
    st.session_state.user_nip = None

# Database Akun Pegawai
if 'db_users' not in st.session_state:
    st.session_state.db_users = pd.DataFrame(columns=[
        'NIP', 'Nama', 'Unit Kerja', 'Peran', 'Jabatan', 'TMT CPNS', 'Masa Kerja', 'Jenis Pegawai', 'Password'
    ])

# Database Akun Admin
if 'db_admins' not in st.session_state:
    st.session_state.db_admins = pd.DataFrame([
        {'NIP': 'masteradmin', 'Nama': 'Master Administrator', 'Password': 'Wewalkthetalknotonlytalktotalk'}
    ])

# Database Cuti
if 'db_cuti' not in st.session_state:
    st.session_state.db_cuti = pd.DataFrame(columns=[
        'ID', 'NIP', 'Nama', 'Peran Pemohon', 'Jenis Cuti', 'Tanggal Mulai', 'Tanggal Selesai', 'Durasi',
        'Alamat', 'No Telp', 'Alasan', 
        'Approval 1 (Status)', 'Approval 1 (Oleh)', 
        'Approval 2 (Status)', 'Approval 2 (Oleh)', 
        'Status Akhir'
    ])

# Daftar Unit Kerja
UNIT_KERJA_LIST = [
    "Bagian Pengadaan Barang Jasa", 
    "Bagian Tata Usaha", 
    "Bagian Rumah Tangga", 
    "Bagian Arsip",
    "Kepala Biro Umum", 
    "Sekretaris Jenderal"
]

# Daftar Hari Besar Nasional (Contoh untuk Tahun 2026)
HARI_BESAR_2026 = [
    "2026-01-01", # Tahun Baru
    "2026-01-29", # Tahun Baru Imlek
    "2026-02-16", # Isra Mi'raj
    "2026-03-20", # Hari Suci Nyepi
    "2026-03-20", # Wafat Yesus Kristus
    "2026-03-21", # Hari Paskah
    "2026-03-31", # Idul Fitri
    "2026-04-01", # Idul Fitri
    "2026-05-01", # Hari Buruh
    "2026-05-14", # Kenaikan Yesus Kristus
    "2026-05-21", # Hari Raya Waisak
    "2026-06-01", # Hari Lahir Pancasila
    "2026-06-06", # Idul Adha
    "2026-07-07", # Tahun Baru Islam
    "2026-08-17", # Hari Kemerdekaan RI
    "2026-09-15", # Maulid Nabi Muhammad SAW
    "2026-12-25", # Hari Raya Natal
]

# Fungsi Navigasi
def navigate_to(page_name):
    st.session_state.page = page_name

def logout():
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.user_name = None
    st.session_state.user_nip = None
    st.session_state.page = 'home'

def hitung_masa_kerja(tmt_date):
    today = datetime.now().date()
    diff = relativedelta(today, tmt_date)
    return f"{diff.years} Tahun, {diff.months} Bulan"

def hitung_hari_kerja(start_date, end_date):
    """
    Menghitung hari kerja mengecualikan akhir pekan dan hari besar nasional.
    """
    # Generate range tanggal
    days = pd.date_range(start=start_date, end=end_date)
    
    # Filter weekend (Saturday=5, Sunday=6)
    work_days = days[days.dayofweek < 5]
    
    # Filter Hari Besar Nasional
    final_days = [d for d in work_days if d.strftime('%Y-%m-%d') not in HARI_BESAR_2026]
    
    return len(final_days)

# --- HALAMAN UTAMA ---
if st.session_state.page == 'home':
    st.title("🏃 CUBI (Cuti Biro Umum)")
    st.subheader("Sistem Cuti Pegawai Internal Biro Umum")
    st.write("Silakan pilih akses login Anda:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👤 Login sebagai Pegawai", use_container_width=True):
            navigate_to('login_pegawai')
            st.rerun()
    with col2:
        if st.button("🔑 Login sebagai Admin", use_container_width=True):
            navigate_to('login_admin')
            st.rerun()

# --- HALAMAN LOGIN PEGAWAI ---
elif st.session_state.page == 'login_pegawai':
    if st.button("⬅️ Kembali"):
        navigate_to('home')
        st.rerun()
        
    st.title("Login Pegawai")
    nip_input = st.text_input("NIP")
    pass_input = st.text_input("Password", type="password")
    
    if st.button("Masuk"):
        user_check = st.session_state.db_users[st.session_state.db_users['NIP'] == nip_input]
        
        if nip_input == "pegawai" and pass_input == "123":
            st.session_state.logged_in = True
            st.session_state.user_role = 'pegawai'
            st.session_state.user_name = "Budi Santoso"
            st.session_state.user_nip = "pegawai"
            navigate_to('dashboard_pegawai')
            st.rerun()
        elif not user_check.empty:
            stored_password = user_check.iloc[0]['Password']
            if pass_input == stored_password:
                st.session_state.logged_in = True
                st.session_state.user_role = 'pegawai'
                st.session_state.user_name = user_check.iloc[0]['Nama']
                st.session_state.user_nip = nip_input
                navigate_to('dashboard_pegawai')
                st.rerun()
            else:
                st.error("Password salah")
        else:
            st.error("NIP tidak terdaftar")

# --- HALAMAN LOGIN ADMIN ---
elif st.session_state.page == 'login_admin':
    if st.button("⬅️ Kembali"):
        navigate_to('home')
        st.rerun()
        
    st.title("Login Admin")
    username = st.text_input("NIP Admin")
    password = st.text_input("Password", type="password")
    
    if st.button("Masuk"):
        admin_check = st.session_state.db_admins[st.session_state.db_admins['NIP'] == username]
        
        if not admin_check.empty:
            stored_password = admin_check.iloc[0]['Password']
            if password == stored_password:
                st.session_state.logged_in = True
                st.session_state.user_role = 'admin'
                st.session_state.user_name = admin_check.iloc[0]['Nama']
                st.session_state.user_nip = username
                navigate_to('dashboard_admin')
                st.rerun()
            else:
                st.error("Password Admin salah")
        else:
            st.error("NIP Admin tidak terdaftar")

# --- DASHBOARD PEGAWAI ---
elif st.session_state.page == 'dashboard_pegawai' and st.session_state.user_role == 'pegawai':
    col_title, col_logout = st.columns([0.85, 0.15])
    with col_title:
        st.title(f"Dashboard Pegawai")
    with col_logout:
        st.write("")
        if st.button("Logout 🚪", use_container_width=True):
            logout()
            st.rerun()

    user_data = st.session_state.db_users[st.session_state.db_users['NIP'] == st.session_state.user_nip]
    peran_user = user_data.iloc[0]['Peran'] if not user_data.empty else "Staff"
    is_struktural = peran_user in ["Eselon 1", "Eselon 2", "Eselon 3", "Eselon 4"]
    
    tab_list = ["👤 Profil Saya", "📝 Ajukan Cuti", "📜 Riwayat Cuti"]
    if is_struktural:
        tab_list.append("✅ Persetujuan Cuti")
    tab_list.append("⚙️ Ubah Password")
    
    tabs = st.tabs(tab_list)
    
    # 1. Profil Saya
    with tabs[0]:
        st.subheader("Informasi Rinci Pegawai")
        if not user_data.empty:
            row = user_data.iloc[0]
            c1, c2 = st.columns(2)
            with c1:
                st.write(f"**Nama Lengkap:** {row['Nama']}")
                st.write(f"**NIP:** {row['NIP']}")
                st.write(f"**Jenis Pegawai:** {row['Jenis Pegawai']}")
                st.write(f"**Unit Kerja:** {row['Unit Kerja']}")
            with c2:
                st.write(f"**Jabatan:** {row['Jabatan']}")
                st.write(f"**Peran:** {row['Peran']}")
                st.write(f"**TMT CPNS:** {row['TMT CPNS']}")
                st.write(f"**Masa Kerja:** {hitung_masa_kerja(row['TMT CPNS'])}")
        else:
            st.warning("Data profil tidak ditemukan.")

    # 2. Ajukan Cuti
    with tabs[1]:
        st.subheader("Form Pengajuan Cuti")
        if not user_data.empty:
            row_p = user_data.iloc[0]
            jenis_p = row_p['Jenis Pegawai']
            peran_p = row_p['Peran']
            
            if jenis_p == "PNS":
                opsi_cuti = ["Cuti Tahunan", "Cuti Besar", "Cuti Sakit", "Cuti Melahirkan", "Cuti Alasan Penting", "Cuti di Luar Tanggungan Negara (CLTN)"]
            elif jenis_p == "CPNS":
                opsi_cuti = ["Cuti Sakit", "Cuti Alasan Penting"]
            elif jenis_p == "PPPK":
                opsi_cuti = ["Cuti Tahunan", "Cuti Sakit", "Cuti Melahirkan"]
            else:
                opsi_cuti = ["Cuti Sakit", "Cuti Alasan Penting"]

            with st.container(border=True):
                with st.form("form_cuti", border=False):
                    st.markdown("##### 📅 Data Waktu & Jenis Cuti")
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        jenis_cuti = st.selectbox("Jenis Cuti", opsi_cuti)
                    with c2:
                        tgl_mulai = st.date_input("Tanggal Mulai", min_value=datetime.now())
                    with c3:
                        tgl_selesai = st.date_input("Tanggal Selesai", min_value=tgl_mulai)
                    
                    # Tampilan Durasi yang Dinamis & Akurat
                    durasi = hitung_hari_kerja(tgl_mulai, tgl_selesai)
                    st.info(f"⏱️ **Durasi Cuti:** {durasi} Hari Kerja (Mengecualikan Sabtu, Minggu, dan Hari Besar Nasional)")
                    
                    st.markdown("---")
                    st.markdown("##### 📍 Informasi Kontak & Alasan")
                    c4, c5 = st.columns(2)
                    with c4:
                        alamat_cuti = st.text_area("Alamat Selama Cuti", placeholder="Masukkan alamat lengkap tujuan cuti...", height=100)
                    with c5:
                        no_telp = st.text_input("Nomor Telepon/WA Aktif", placeholder="Contoh: 0812xxxxxxxx")
                        alasan = st.text_area("Alasan Cuti", placeholder="Berikan alasan singkat...", height=68)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    submit = st.form_submit_button("🚀 Kirim Pengajuan Cuti", use_container_width=True)
                    
                    if submit:
                        if not alamat_cuti or not no_telp or not alasan:
                            st.error("Mohon lengkapi Alamat, Nomor Telepon, dan Alasan Cuti!")
                        elif durasi <= 0:
                            st.error("Durasi cuti tidak valid (terdiri dari hari libur saja).")
                        else:
                            status_awal = "Menunggu Persetujuan"
                            if peran_p == "Eselon 1":
                                status_awal = "Disetujui"
                            
                            new_data = {
                                'ID': len(st.session_state.db_cuti) + 1,
                                'NIP': st.session_state.user_nip,
                                'Nama': st.session_state.user_name,
                                'Peran Pemohon': peran_p,
                                'Jenis Cuti': jenis_cuti,
                                'Tanggal Mulai': tgl_mulai,
                                'Tanggal Selesai': tgl_selesai,
                                'Durasi': f"{durasi} Hari Kerja",
                                'Alamat': alamat_cuti,
                                'No Telp': no_telp,
                                'Alasan': alasan,
                                'Approval 1 (Status)': 'Pending' if peran_p != "Eselon 1" else 'N/A',
                                'Approval 1 (Oleh)': 'N/A',
                                'Approval 2 (Status)': 'Pending' if peran_p in ["Staff", "Eselon 4"] else 'N/A',
                                'Approval 2 (Oleh)': 'N/A',
                                'Status Akhir': status_awal
                            }
                            st.session_state.db_cuti = pd.concat([st.session_state.db_cuti, pd.DataFrame([new_data])], ignore_index=True)
                            st.success("🎉 Pengajuan berhasil dikirim!")
        else:
            st.error("Silakan gunakan akun terdaftar.")

    # 3. Riwayat Cuti
    with tabs[2]:
        st.subheader("Riwayat Cuti Anda")
        df_user = st.session_state.db_cuti[st.session_state.db_cuti['NIP'] == st.session_state.user_nip]
        
        if df_user.empty:
            st.info("Belum ada riwayat pengajuan.")
        else:
            for _, row in df_user.sort_values(by='ID', ascending=False).iterrows():
                with st.container(border=True):
                    c1, c2, c3 = st.columns([0.25, 0.45, 0.3])
                    status_color = "orange"
                    if row['Status Akhir'] == "Disetujui": status_color = "green"
                    elif row['Status Akhir'] == "Ditolak": status_color = "red"
                    
                    with c1:
                        st.markdown(f"### ID #{row['ID']}")
                        st.markdown(f"**{row['Jenis Cuti']}**")
                        st.markdown(f"**:{status_color}[{row['Status Akhir']}]**")
                        st.caption(f"Total: {row['Durasi']}")
                    
                    with c2:
                        st.write(f"📅 **Periode:** {row['Tanggal Mulai']} s/d {row['Tanggal Selesai']}")
                        st.write(f"📍 **Alamat:** {row['Alamat']}")
                        st.write(f"📞 **Kontak:** {row['No Telp']}")
                        st.write(f"📝 **Alasan:** {row['Alasan']}")
                        
                    with c3:
                        st.markdown("**Detail Persetujuan:**")
                        app1_icon = "⏳"
                        if row['Approval 1 (Status)'] == "Disetujui": app1_icon = "✅"
                        elif row['Approval 1 (Status)'] == "Ditolak": app1_icon = "❌"
                        elif row['Approval 1 (Status)'] == "N/A": app1_icon = "➖"
                        st.write(f"{app1_icon} **Tahap 1:** {row['Approval 1 (Status)']} ({row['Approval 1 (Oleh)']})")
                        
                        if row['Approval 2 (Status)'] != "N/A":
                            app2_icon = "⏳"
                            if row['Approval 2 (Status)'] == "Disetujui": app2_icon = "✅"
                            elif row['Approval 2 (Status)'] == "Ditolak": app2_icon = "❌"
                            st.write(f"{app2_icon} **Tahap 2:** {row['Approval 2 (Status)']} ({row['Approval 2 (Oleh)']})")

    # 4. Approval
    if is_struktural:
        with tabs[3]:
            st.subheader("Daftar Pengajuan Perlu Persetujuan")
            
            def get_pending_approval(peran_approver):
                df = st.session_state.db_cuti
                if peran_approver == "Eselon 4":
                    return df[(df['Peran Pemohon'] == 'Staff') & (df['Approval 1 (Status)'] == 'Pending')]
                elif peran_approver == "Eselon 3":
                    staff_needs = df[(df['Peran Pemohon'] == 'Staff') & (df['Approval 1 (Status)'] == 'Disetujui') & (df['Approval 2 (Status)'] == 'Pending')]
                    e4_needs = df[(df['Peran Pemohon'] == 'Eselon 4') & (df['Approval 1 (Status)'] == 'Pending')]
                    return pd.concat([staff_needs, e4_needs])
                elif peran_approver == "Eselon 2":
                    e4_needs = df[(df['Peran Pemohon'] == 'Eselon 4') & (df['Approval 1 (Status)'] == 'Disetujui') & (df['Approval 2 (Status)'] == 'Pending')]
                    e3_needs = df[(df['Peran Pemohon'] == 'Eselon 3') & (df['Approval 1 (Status)'] == 'Pending')]
                    return pd.concat([e4_needs, e3_needs])
                elif peran_approver == "Eselon 1":
                    return df[(df['Peran Pemohon'] == 'Eselon 2') & (df['Approval 1 (Status)'] == 'Pending')]
                return pd.DataFrame()

            df_to_approve = get_pending_approval(peran_user)
            
            if df_to_approve.empty:
                st.info("Tidak ada pengajuan yang menunggu persetujuan Anda.")
            else:
                for idx, row in df_to_approve.iterrows():
                    with st.container(border=True):
                        c1, c2, c3 = st.columns([0.4, 0.4, 0.2])
                        with c1:
                            st.write(f"**Pemohon:** {row['Nama']} ({row['Peran Pemohon']})")
                            st.write(f"**Jenis Cuti:** {row['Jenis Cuti']} ({row['Durasi']})")
                            st.caption(f"Alasan: {row['Alasan']}")
                            st.caption(f"Kontak: {row['No Telp']}")
                        with c2:
                            st.write(f"📅 {row['Tanggal Mulai']} s/d {row['Tanggal Selesai']}")
                            is_step_2 = (row['Approval 1 (Status)'] == 'Disetujui')
                            st.write(f"🚩 Tahap: {'Persetujuan Akhir' if is_step_2 else 'Persetujuan Awal'}")
                            st.write(f"📍 Alamat: {row['Alamat']}")
                        with c3:
                            if st.button("✅ Terima", key=f"acc_{row['ID']}", use_container_width=True):
                                if not is_step_2:
                                    st.session_state.db_cuti.at[idx, 'Approval 1 (Status)'] = 'Disetujui'
                                    st.session_state.db_cuti.at[idx, 'Approval 1 (Oleh)'] = st.session_state.user_name
                                    if row['Approval 2 (Status)'] == 'N/A':
                                        st.session_state.db_cuti.at[idx, 'Status Akhir'] = 'Disetujui'
                                    else:
                                        st.session_state.db_cuti.at[idx, 'Status Akhir'] = 'Menunggu Persetujuan Lanjutan'
                                else:
                                    st.session_state.db_cuti.at[idx, 'Approval 2 (Status)'] = 'Disetujui'
                                    st.session_state.db_cuti.at[idx, 'Approval 2 (Oleh)'] = st.session_state.user_name
                                    st.session_state.db_cuti.at[idx, 'Status Akhir'] = 'Disetujui'
                                st.rerun()
                            
                            if st.button("❌ Tolak", key=f"rej_{row['ID']}", use_container_width=True, type="secondary"):
                                if not is_step_2:
                                    st.session_state.db_cuti.at[idx, 'Approval 1 (Status)'] = 'Ditolak'
                                    st.session_state.db_cuti.at[idx, 'Approval 1 (Oleh)'] = st.session_state.user_name
                                else:
                                    st.session_state.db_cuti.at[idx, 'Approval 2 (Status)'] = 'Ditolak'
                                    st.session_state.db_cuti.at[idx, 'Approval 2 (Oleh)'] = st.session_state.user_name
                                st.session_state.db_cuti.at[idx, 'Status Akhir'] = 'Ditolak'
                                st.rerun()

    # 5. Ubah Password
    with tabs[-1]:
        st.subheader("Perbarui Password")
        if not user_data.empty:
            with st.form("ubah_pass_pegawai"):
                p_lama = st.text_input("Password Saat Ini", type="password")
                p_baru = st.text_input("Password Baru", type="password")
                p_konf = st.text_input("Konfirmasi Password Baru", type="password")
                btn_pass = st.form_submit_button("Simpan Password")
                
                if btn_pass:
                    idx = user_data.index[0]
                    if p_lama != st.session_state.db_users.at[idx, 'Password']:
                        st.error("Password lama salah!")
                    elif p_baru != p_konf:
                        st.error("Konfirmasi password tidak cocok!")
                    elif len(p_baru) < 6:
                        st.error("Password minimal 6 karakter!")
                    else:
                        st.session_state.db_users.at[idx, 'Password'] = p_baru
                        st.success("Password berhasil diperbarui!")

# --- DASHBOARD ADMIN ---
elif st.session_state.page == 'dashboard_admin' and st.session_state.user_role == 'admin':
    col_title, col_logout = st.columns([0.85, 0.15])
    with col_title:
        st.title("Panel Admin CUBI")
    with col_logout:
        st.write("") 
        if st.button("Logout 🚪", use_container_width=True):
            logout()
            st.rerun()

    tabs = st.tabs(["➕ Tambah Akun Pegawai", "👥 Daftar Akun Pegawai", "➕ Tambah Admin", "👥 Daftar Admin", "⚙️ Ubah Password Saya"])
    tab_acc, tab_view, tab_add_adm, tab_view_adm, tab_pass = tabs
    
    with tab_acc:
        st.subheader("Pendaftaran Akun Pegawai Baru")
        with st.form("form_tambah_akun"):
            col_a, col_b = st.columns(2)
            with col_a:
                nama_baru = st.text_input("Nama Lengkap")
                nip_baru = st.text_input("NIP")
                peran_list = ["Eselon 1", "Eselon 2", "Eselon 3", "Eselon 4", "Staff"]
                peran_baru = st.selectbox("Peran", peran_list)
                jenis_pegawai_baru = st.selectbox("Jenis Pegawai", ["CPNS", "PNS", "PPPK"])
            with col_b:
                unit_kerja = st.selectbox("Unit Kerja", UNIT_KERJA_LIST)
                tmt_cpns = st.date_input(
                    "TMT CPNS", 
                    max_value=datetime.now(),
                    min_value=datetime.now() - relativedelta(years=70)
                )
                jabatan_baru = st.text_input("Jabatan")
            
            submit_akun = st.form_submit_button("Simpan Akun")
            
            if submit_akun:
                if nama_baru and nip_baru:
                    if nip_baru in st.session_state.db_users['NIP'].values:
                        st.error("NIP sudah terdaftar!")
                    else:
                        new_user = {
                            'NIP': nip_baru,
                            'Nama': nama_baru,
                            'Unit Kerja': unit_kerja,
                            'Peran': peran_baru,
                            'Jabatan': jabatan_baru,
                            'TMT CPNS': tmt_cpns,
                            'Masa Kerja': hitung_masa_kerja(tmt_cpns),
                            'Jenis Pegawai': jenis_pegawai_baru,
                            'Password': nip_baru 
                        }
                        st.session_state.db_users = pd.concat([st.session_state.db_users, pd.DataFrame([new_user])], ignore_index=True)
                        st.success(f"Akun {nama_baru} berhasil ditambahkan!")

    with tab_view:
        st.subheader("Data Akun Terdaftar")
        if st.session_state.db_users.empty:
            st.info("Belum ada akun pegawai yang terdaftar.")
        else:
            for index, row in st.session_state.db_users.iterrows():
                with st.container(border=True):
                    c1, c2, c3 = st.columns([0.3, 0.4, 0.3])
                    with c1:
                        st.markdown(f"**{row['Nama']}**")
                        st.caption(f"NIP: {row['NIP']} | {row['Jenis Pegawai']}")
                        st.write(f"💼 {row['Jabatan']}")
                    with c2:
                        try: idx_unit = UNIT_KERJA_LIST.index(row['Unit Kerja'])
                        except: idx_unit = 0
                        new_unit = st.selectbox(f"Unit Kerja", UNIT_KERJA_LIST, index=idx_unit, key=f"unit_{row['NIP']}")
                        if new_unit != row['Unit Kerja']:
                            st.session_state.db_users.at[index, 'Unit Kerja'] = new_unit
                            st.rerun()

                        opsi_peran = ["Eselon 1", "Eselon 2", "Eselon 3", "Eselon 4", "Staff"]
                        try: idx_peran = opsi_peran.index(row['Peran'])
                        except: idx_peran = 4
                        new_peran = st.selectbox(f"Peran", opsi_peran, index=idx_peran, key=f"peran_{row['NIP']}")
                        if new_peran != row['Peran']:
                            st.session_state.db_users.at[index, 'Peran'] = new_peran
                            st.rerun()
                    with c3:
                        st.write(f"⏱️ {hitung_masa_kerja(row['TMT CPNS'])}")
                        if st.button("🔑 Reset", key=f"reset_{row['NIP']}", use_container_width=True):
                            st.session_state.db_users.at[index, 'Password'] = row['NIP']
                            st.toast("Password direset!")
                        if st.button("🗑️ Hapus", key=f"del_{row['NIP']}", use_container_width=True):
                            st.session_state.db_users = st.session_state.db_users.drop(index).reset_index(drop=True)
                            st.rerun()

    with tab_add_adm:
        st.subheader("Tambah Administrator Baru")
        with st.form("form_tambah_admin"):
            nama_adm = st.text_input("Nama Lengkap Admin")
            nip_adm = st.text_input("NIP Admin (Username)")
            if st.form_submit_button("Simpan Administrator"):
                if nama_adm and nip_adm:
                    new_admin = {'NIP': nip_adm, 'Nama': nama_adm, 'Password': nip_adm}
                    st.session_state.db_admins = pd.concat([st.session_state.db_admins, pd.DataFrame([new_admin])], ignore_index=True)
                    st.success("Admin ditambahkan!")

    with tab_view_adm:
        st.subheader("Daftar Administrator Sistem")
        st.table(st.session_state.db_admins[['NIP', 'Nama']])

    with tab_pass:
        st.subheader("Ubah Password Akun Saya")
        admin_data = st.session_state.db_admins[st.session_state.db_admins['NIP'] == st.session_state.user_nip]
        if not admin_data.empty:
            with st.form("form_ubah_pass_adm"):
                pass_lama = st.text_input("Password Saat Ini", type="password")
                pass_baru = st.text_input("Password Baru", type="password")
                if st.form_submit_button("Perbarui Password"):
                    idx = admin_data.index[0]
                    if pass_lama == st.session_state.db_admins.at[idx, 'Password']:
                        st.session_state.db_admins.at[idx, 'Password'] = pass_baru
                        st.success("Password diperbarui!")
                    else: st.error("Password lama salah!")
