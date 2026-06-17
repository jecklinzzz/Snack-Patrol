import os
import pandas as pd
import streamlit as st
import plotly.express as px

# Konfigurasi layout utama halaman web
st.set_page_config(
    page_title="Snack Patrol - Food Lab Analysis", page_icon="🧪", layout="wide"
)

# Kumpulan Custom CSS untuk styling UI (Navigasi, Kartu Produk, dan Tipografi)
st.markdown(
    """
    <style>
    /* Memangkas ruang kosong berlebih di bagian paling atas halaman */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }

    /* Konfigurasi untuk menengahkan navigasi Tab horizontal */
    div[data-baseweb="tab-list"] {
        display: flex !important;
        justify-content: center !important; 
        width: 100% !important;
        gap: 15px !important; 
    }

    button[data-baseweb="tab"] {
        font-size: 20px !important; 
        font-weight: 700 !important; 
        height: 55px !important; 
        padding: 10px 20px !important;
    }
    
    /* Konfigurasi UI untuk kartu tampilan produk (Grid) */
    .product-card {
        background-color: #FFFDF0; 
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    
    .product-card:hover {
        transform: translateY(-5px);
        border-color: #FF6B8B; 
    }
    
    /* Konfigurasi palet warna untuk indikator peringatan nutrisi */
    .badge-gawat {
        background-color: #FED7D7;
        color: #9B2C2C;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
        display: inline-block;
    }
    
    .badge-waspada {
        background-color: #FEEBC8;
        color: #9C4221;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
        display: inline-block;
    }
    
    .badge-aman {
        background-color: #C6F6D5;
        color: #22543D;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
        display: inline-block;
    }
    
    /* Konfigurasi styling untuk judul halaman */
    .main-title {
        text-align: center;
        font-size: 50px !important;
        font-weight: 800;
        color: #FF6B8B;
        margin-bottom: 5px;
    }
    
    .sub-title {
        text-align: center;
        font-size: 20px !important;
        color: #4A5568;
        margin-bottom: 30px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Fungsi untuk memuat dataset dari file CSV
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "Database Snack.csv")
    data = pd.read_csv(csv_path, sep=";", encoding="utf-8-sig")
    data.columns = data.columns.str.strip()
    return data

# Blok Try-Except untuk menangani error pembacaan file
try:
    df = load_data()

    # ==========================================
    # HEADER UTAMA (MUNCUL DI SEMUA TAB)
    # ==========================================
    st.markdown("<div class='main-title'>Snack Patrol</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='sub-title'>Periksa kandungan nutrisi snack & minumanmu secara presisi</div>",
        unsafe_allow_html=True,
    )

    # Inisialisasi navigasi Tab dengan urutan baru yang telah disesuaikan
    menu_beranda, menu_bandingkan, menu_kontribusi, menu_berat = st.tabs(
        ["🏠 Beranda", "📊 Bandingkan Produk", "➕ Kontribusi Data", "⚖️ Berat Ideal"]
    )

    # ==========================================
    # BAGIAN 1: BERANDA & PENCARIAN PRODUK
    # ==========================================
    with menu_beranda:
        # Fitur kolom pencarian produk
        search_query = st.text_input(
            "",
            placeholder="🔍 Cari snack atau minuman... (cth: Teh Pucuk, Oreo, Chitato)",
            key="search_home",
        )

        # Tombol pintasan untuk sampel populer
        st.write("")
        st.markdown(
            "<p style='text-align: center; color: #718096; font-size: 15px;'>Coba klik sampel ini:</p>",
            unsafe_allow_html=True,
        )
        
        pills_kolom = st.columns([2, 1, 1, 1, 1, 1, 2])
        sampel_pills = ["Teh Pucuk", "Oreo", "Chitato"]

        with pills_kolom[2]:
            if st.button(f"🥤 {sampel_pills[0]}"):
                search_query = sampel_pills[0]
        with pills_kolom[3]:
            if st.button(f"🍪 {sampel_pills[1]}"):
                search_query = sampel_pills[1]
        with pills_kolom[4]:
            if st.button(f"🍿 {sampel_pills[2]}"):
                search_query = sampel_pills[2]

        st.markdown("---")

        # Logika pemrosesan hasil pencarian
        if search_query:
            hasil_filter = df[df["Nama Produk"].str.contains(search_query, case=False, na=False)]

            if not hasil_filter.empty:
                st.markdown(f"#### 🔍 Hasil Analisis untuk '{search_query}':")

                # Tampilan detail jika hanya 1 produk yang ditemukan
                if len(hasil_filter) == 1:
                    data_snack = hasil_filter.iloc[0]

                    st.markdown(
                        f"""
                    <div style='background-color: #F2F9F6; padding: 20px; border-radius: 15px; border-left: 6px solid #FF6B8B; margin-bottom: 25px;'>
                        <h2 style='margin: 0; color: #2D3748;'>🧫 Hasil Pemindaian: {data_snack['Nama Produk']}</h2>
                        <p style='margin: 5px 0 0 0; color: #718096;'><b>Kategori Objek:</b> {data_snack['Kategori']} | <b>Massa Total:</b> {data_snack['Quantity (g or mL)']} g/mL</p>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    col_gula, col_natrium = st.columns(2)
                    
                    # Kolom evaluasi metrik Gula
                    with col_gula:
                        st.markdown("### 🍬 **Uji Kandungan Gula**")
                        st.metric(label="Massa Gula Terlarut", value=f"{data_snack['Kandungan Gula (g)']} g")
                        st.caption(f"🧪 Konsentrasi: **{data_snack['Sugar /100 g']}** per 100g")
                        st.caption(f"📈 Harian: **{data_snack['Persen Gula Harian']}%** dari batas 50g")

                        if data_snack["Sugar Level"] == "GAWAT":
                            st.error(f"🔴 **STATUS: {data_snack['Sugar Level']}**")
                        elif data_snack["Sugar Level"] == "WASPADA":
                            st.warning(f"🟡 **STATUS: {data_snack['Sugar Level']}**")
                        else:
                            st.success(f"🟢 **STATUS: {data_snack['Sugar Level']}**")

                    # Kolom evaluasi metrik Natrium
                    with col_natrium:
                        st.markdown("### 🧂 **Uji Kandungan Natrium**")
                        st.metric(label="Massa Natrium Terlarut", value=f"{data_snack['Kandungan Natrium (mg)']} mg")
                        st.caption(f"🧪 Konsentrasi: **{data_snack['Natrium /100 g']}** per 100g")
                        st.caption(f"📈 Harian: **{data_snack['Persen Natrium Harian']}%** dari batas 2000mg")

                        if data_snack["Natrium Level"] == "GAWAT":
                            st.error(f"🔴 **STATUS: {data_snack['Natrium Level']}**")
                        elif data_snack["Natrium Level"] == "WASPADA":
                            st.warning(f"🟡 **STATUS: {data_snack['Natrium Level']}**")
                        else:
                            st.success(f"🟢 **STATUS: {data_snack['Natrium Level']}**")

                    st.markdown("---")
                    st.markdown("### 🧬 **Laporan Komposisi & Toksikologi**")
                    st.info(f"🔮 **Senyawa Utama:** {data_snack['Senyawa Utama']}")
                    st.error(f"⚠️ **Bahaya Berlebih:** {data_snack['Bahaya Berlebih']}")
                
                # Tampilan Grid Card jika pencarian menghasilkan lebih dari 1 produk
                else:
                    cols = st.columns(3)
                    for idx, row in enumerate(hasil_filter.itertuples()):
                        with cols[idx % 3]:
                            badge_class = "badge-aman"
                            if row._5 == "GAWAT" or row._8 == "GAWAT":
                                badge_class = "badge-gawat"
                            elif row._5 == "WASPADA" or row._8 == "WASPADA":
                                badge_class = "badge-waspada"

                            st.markdown(
                                f"""
                            <div class='product-card'>
                                <h3 style='margin:0; color:#2D3748;'>{row._1}</h3>
                                <p style='color:#718096; font-size:14px; margin-bottom:10px;'>{row.Kategori} · {row._3} g/mL</p>
                                <h4 style='margin:0; color:#FF6B8B;'>{row._4} g <span style='font-size:14px; color:#A0AEC0;'>Gula</span></h4>
                                <h4 style='margin:0 0 15px 0; color:#4A5568;'>{row._7} mg <span style='font-size:14px; color:#A0AEC0;'>Natrium</span></h4>
                                <div class='{badge_class}'>{row._5}</div>
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )
            else:
                st.warning("Produk tidak terdeteksi di database lab kami.")

        # Tampilan default (menampilkan 6 sampel saja) jika tidak ada pencarian
        else:
            st.markdown("### 📦 Sampel Produk Tersedia")
            grid_kolom = st.columns(3)

            # Membatasi iterasi hanya pada 6 baris pertama menggunakan .head(6)
            for indeks, baris in df.head(6).iterrows():
                if baris["Sugar Level"] == "GAWAT" or baris["Natrium Level"] == "GAWAT":
                    css_badge = "badge-gawat"
                    status_teks = "GAWAT"
                elif baris["Sugar Level"] == "WASPADA" or baris["Natrium Level"] == "WASPADA":
                    css_badge = "badge-waspada"
                    status_teks = "WASPADA"
                else:
                    css_badge = "badge-aman"
                    status_teks = "AMAN"

                with grid_kolom[indeks % 3]:
                    st.markdown(
                        f"""
                    <div class='product-card'>
                        <h3 style='margin: 0; color: #2D3748; font-size: 22px;'>{baris['Nama Produk']}</h3>
                        <p style='color: #718096; font-size: 14px; margin: 2px 0 15px 0;'>{baris['Kategori']} · {baris['Quantity (g or mL)']} g/mL</p>
                        <p style='margin: 0; font-size: 16px;'>🍬 Gula: <b>{baris['Kandungan Gula (g)']} g</b></p>
                        <p style='margin: 0; font-size: 16px;'>🧂 Natrium: <b>{baris['Kandungan Natrium (mg)']} mg</b></p>
                        <div style='margin-top: 15px;' class='{css_badge}'>{status_teks}</div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

    # ==========================================
    # BAGIAN 2: ANALISIS KOMPARATIF PRODUK
    # ==========================================
    with menu_bandingkan:
        st.markdown("## 📊 Perbandingan Vektor Nutrisi Antar Sampel", unsafe_allow_html=True)
        st.write("---")
        
        daftar_snack = df["Nama Produk"].tolist()
        cx, cy = st.columns(2)
        
        # Input pemilihan sampel untuk dikomparasi
        with cx:
            p1 = st.selectbox("Pilih Sampel A:", daftar_snack, index=0)
        with cy:
            idx_def = 1 if len(daftar_snack) > 1 else 0
            p2 = st.selectbox("Pilih Sampel B:", daftar_snack, index=idx_def)

        if p1 and p2:
            data_p1 = df[df["Nama Produk"] == p1].iloc[0]
            data_p2 = df[df["Nama Produk"] == p2].iloc[0]

            st.markdown("### ⚔️ **Matriks Perbandingan Nutrisi**")

            # Ekstraksi dataset untuk kebutuhan visualisasi Plotly
            df_grafik = pd.DataFrame({
                "Produk": [p1, p1, p2, p2],
                "Zat Gizi": ["Gula (g)", "Natrium (mg)", "Gula (g)", "Natrium (mg)"],
                "Nilai Kandungan": [
                    float(data_p1["Kandungan Gula (g)"]),
                    float(data_p1["Kandungan Natrium (mg)"]),
                    float(data_p2["Kandungan Gula (g)"]),
                    float(data_p2["Kandungan Natrium (mg)"])
                ]
            })

            # Render grafik batang berkelompok
            fig = px.bar(df_grafik, x="Zat Gizi", y="Nilai Kandungan", color="Produk", barmode="group",
                         text_auto=True, color_discrete_sequence=["#FF6B8B", "#4FD1C5"])

            # Penyesuaian layout grafik agar presisi
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=40, r=40, t=50, b=40),
                legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5) 
            )

            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            # Analisis selisih numerik kandungan gizi
            st.markdown("### 📉 **Hasil Evaluasi Selisih Kandungan**")
            sg = float(data_p1["Kandungan Gula (g)"]) - float(data_p2["Kandungan Gula (g)"])
            sn = float(data_p1["Kandungan Natrium (mg)"]) - float(data_p2["Kandungan Natrium (mg)"])

            if sg > 0:
                st.write(f"• Kandungan gula **{p1}** lebih tinggi sebesar **{abs(sg):.1f} g** dibandingkan dengan {p2}.")
            elif sg < 0:
                st.write(f"• Kandungan gula **{p1}** lebih rendah sebesar **{abs(sg):.1f} g** dibandingkan dengan {p2}.")
            else:
                st.write(f"• Kadar kandungan gula antara **{p1}** dan **{p2}** adalah setara.")

            if sn > 0:
                st.write(f"• Kandungan natrium **{p1}** lebih tinggi sebesar **{abs(sn):.1f} mg** dibandingkan dengan {p2}.")
            elif sn < 0:
                st.write(f"• Kandungan natrium **{p1}** lebih rendah sebesar **{abs(sn):.1f} mg** dibandingkan dengan {p2}.")
            else:
                st.write(f"• Kadar kandungan natrium antara **{p1}** dan **{p2}** adalah setara.")

    # ==========================================
    # BAGIAN 3: KONTRIBUSI DATA (CROWDSOURCING)
    # ==========================================
    with menu_kontribusi:
        st.markdown("## ➕ Berkontribusi untuk Database Lab", unsafe_allow_html=True)
        st.markdown("Bantu kami memperluas jangkauan *Snack Patrol* dengan mengirimkan sampel baru yang belum terdaftar di sistem analitik kami.")
        st.write("---")

        # Menggunakan st.form agar halaman tidak ter-refresh sebelum tombol kirim ditekan
        with st.form("form_kontribusi", clear_on_submit=True):
            st.markdown("### 📝 Form Pengajuan Sampel Baru")
            
            # Input data tekstual dan numerik
            nama_baru = st.text_input("Nama Produk Snack / Minuman:", placeholder="Contoh: Taro Net Seaweed")
            berat_baru = st.number_input("Berat Bersih Kemasan (g / mL):", min_value=1, value=50)
            
            st.markdown("### 📸 Lampiran Bukti Kemasan")
            # Upload area untuk foto kemasan
            foto_depan = st.file_uploader("Unggah Foto Kemasan Bagian Depan", type=["png", "jpg", "jpeg"])
            foto_gizi = st.file_uploader("Unggah Foto Tabel Informasi Nilai Gizi (Nutrition Facts)", type=["png", "jpg", "jpeg"])
            
            # Tombol submit
            submit_btn = st.form_submit_button("🚀 Kirim Data Sampel")

            # Logika ketika tombol kirim ditekan
            if submit_btn:
                if nama_baru and foto_depan and foto_gizi:
                    # Membuat direktori penyimpanan lokal (sebagai simulasi database cloud)
                    upload_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
                    os.makedirs(upload_dir, exist_ok=True)
                    
                    # Mengeksekusi penyimpanan file foto ke sistem
                    with open(os.path.join(upload_dir, f"depan_{foto_depan.name}"), "wb") as f:
                        f.write(foto_depan.getbuffer())
                    with open(os.path.join(upload_dir, f"gizi_{foto_gizi.name}"), "wb") as f:
                        f.write(foto_gizi.getbuffer())
                        
                    # Feedback visual ke pengguna
                    st.success(f"✅ Transmisi Berhasil! Data sampel **{nama_baru}** ({berat_baru} g/mL) telah dikirim ke tim laboratorium Snack Patrol untuk diverifikasi.")
                    st.balloons() 
                else:
                    st.error("⚠️ Proses gagal. Mohon lengkapi nama produk dan lampirkan kedua foto kemasan sebelum mengirimkan data.")

    # ==========================================
    # BAGIAN 4: KALKULATOR BERAT BADAN & CHATBOT AI
    # ==========================================
    with menu_berat:
        st.markdown("## ⚖️ Kalkulator Berat Badan Ideal (Metode Broca)", unsafe_allow_html=True)
        st.write("---")
        c1, c2 = st.columns(2)
        
        # Pengumpulan data antropometri praktikan
        with c1:
            gender = st.radio("Jenis Kelamin Praktikan:", ["Pria", "Wanita"])
            tinggi = st.number_input("Tinggi Badan (cm):", min_value=100, max_value=250, value=165, key="tb")
            
        with c2:
            berat_sekarang = st.number_input("Berat Badan Saat Ini (kg):", min_value=30, max_value=200, value=60, key="bb")

        # Logika perhitungan Metode Broca
        if gender == "Pria":
            berat_ideal = (tinggi - 100) - ((tinggi - 100) * 0.10)
        else:
            berat_ideal = (tinggi - 100) - ((tinggi - 100) * 0.15)

        # Output evaluasi klinis
        st.markdown("### 📊 Hasil Analisis Klinis")
        st.metric(label="Berat Badan Ideal Target", value=f"{berat_ideal:.2f} kg")
        selisih = berat_sekarang - berat_ideal

        if abs(selisih) <= 2:
            st.success("🟢 Status: Berat badan Anda ideal! Pertahankan pola konsumsi.")
        elif selisih > 2:
            st.warning(f"🟡 Status: Kelebihan {selisih:.2f} kg. Batasi sampel berkadar gula tinggi.")
        else:
            st.info(f"🔵 Status: Kekurangan {abs(selisih):.2f} kg. Tingkatkan kalori sehat.")

        # --- MODUL CHATBOT AI RULE-BASED ---
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### 🤖 Konsultasi AI Ahli Gizi (Beta)")
        st.info("Ketik kata kunci **'naik'** atau **'turun'** untuk mendapatkan protokol kalori dari asisten AI kami.")

        # Inisialisasi memori chat pada Session State agar chat tidak hilang saat direfresh
        if "memori_chat" not in st.session_state:
            st.session_state.memori_chat = []

        # Menampilkan riwayat chat yang tersimpan di memori
        for chat in st.session_state.memori_chat:
            with st.chat_message(chat["role"]):
                st.markdown(chat["content"])

        # Kolom input chat untuk pengguna
        input_user = st.chat_input("Tanyakan tips seputar berat badan (contoh: cara turun bb)...")

        if input_user:
            # 1. Simpan dan tampilkan pesan pengguna
            st.session_state.memori_chat.append({"role": "user", "content": input_user})
            with st.chat_message("user"):
                st.markdown(input_user)

            # 2. Logika pemrosesan teks untuk memberikan balasan (Rule-Based)
            teks_lower = input_user.lower()
            if "turun" in teks_lower or "kurus" in teks_lower or "diet" in teks_lower:
                balasan = """Untuk menurunkan berat badan secara sehat dan presisi, kunci utamanya adalah **Defisit Kalori** (kalori yang masuk lebih sedikit dibandingkan energi yang dibakar). Berikut adalah protokol yang direkomendasikan:
                
* 📉 **Kurangi Gula & Natrium:** Batasi camilan kemasan yang berstatus 'WASPADA' atau 'GAWAT' di *database Snack Patrol*. Gula berlebih memicu penumpukan lemak, dan natrium menahan air di tubuh.
* 🥦 **Tingkatkan Serat & Protein:** Fokus pada karbohidrat kompleks, sayuran, dan protein tanpa lemak (telur, dada ayam, tempe). Ini akan menjaga rasa kenyang lebih lama.
* 💧 **Hidrasi Optimal:** Konsumsi air putih minimal 2-2.5 liter per hari untuk melancarkan metabolisme.
* 🏃‍♂️ **Aktivitas Fisik:** Lakukan latihan kardio ringan dikombinasikan dengan latihan beban minimal 30 menit sehari."""
            
            elif "naik" in teks_lower or "gemuk" in teks_lower or "tambah" in teks_lower:
                balasan = """Untuk menaikkan berat badan, Anda memerlukan **Surplus Kalori** yang sehat. Fokusnya adalah meningkatkan massa otot, bukan sekadar menimbun lemak. Berikut adalah panduannya:

* 🥑 **Pilih Kalori Padat Nutrisi:** Daripada mengonsumsi makanan tinggi gula buatan, pilihlah kalori berkualitas seperti alpukat, kacang-kacangan, susu *full cream*, telur, dan daging segar.
* 🍽️ **Frekuensi Makan:** Jika kesulitan menghabiskan porsi besar, ubah pola makan menjadi porsi sedang namun lebih sering (5-6 kali sehari).
* 💪 **Fokus pada Protein:** Asupan protein sangat krusial untuk membangun jaringan otot yang baru.
* 🏋️‍♂️ **Latihan Beban (Hipertrofi):** Berbeda dengan kardio, angkat beban akan memberikan sinyal pada tubuh agar kalori ekstra yang masuk disintesis menjadi otot, bukan lemak."""
            
            else:
                balasan = "🤖 Maaf, saat ini modul AI Snack Patrol hanya diprogram untuk memberikan rekomendasi seputar **menaikkan** atau **menurunkan** berat badan. Silakan ketik kata kunci 'naik' atau 'turun'."

            # 3. Simpan dan tampilkan balasan sistem AI
            st.session_state.memori_chat.append({"role": "assistant", "content": balasan})
            with st.chat_message("assistant"):
                st.markdown(balasan)

# Penanganan error (*Exception Handling*)
except FileNotFoundError:
    st.error("File 'Database Snack.csv' tidak ditemukan.")
except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat data: {e}")