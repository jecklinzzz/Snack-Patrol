import os
import pandas as pd
import streamlit as st

# 1. Konfigurasi Awal Halaman (Layout Wide)
st.set_page_config(
    page_title="Snack Patrol - Food Lab Analysis", page_icon="🧪", layout="wide"
)

# 2. Custom CSS Premium untuk Membuat Grid Cards, Tombol, dan Font Menarik
st.markdown(
    """
    <style>
    /* Mengatur Font Utama */
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    /* Desain Kartu Produk (Grid Card) */
    .product-card {
        background-color: #FFFDF0; /* Soft Cream */
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .product-card:hover {
        transform: translateY(-5px);
        border-color: #FF6B8B; /* Pink Aksen saat Hover */
    }
    
    /* Indikator Status/Badge */
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
    
    /* Judul Besar Snack Patrol */
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


# 3. Fungsi Memuat Data CSV (Menggunakan Sistem Kamu)
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "Database Snack.csv")
    data = pd.read_csv(csv_path, sep=";", encoding="utf-8-sig")
    data.columns = data.columns.str.strip()
    return data


try:
    df = load_data()

    # --- MENU NAVIGASI ATAS (Sesuai Foto Referensi Kamu) ---
    # Menggunakan st.tabs untuk membuat navigasi horizontal di bagian atas halaman
    menu_beranda, menu_berat, menu_bandingkan = st.tabs(
        ["🏠 Beranda", "⚖️ Berat Ideal", "📊 Bandingkan Produk"]
    )

    # ==============================================================================
    # TAB 1: BERANDA (Tampilan Utama Mirip Foto Referensi)
    # ==============================================================================
    with menu_beranda:
        # Tampilan Judul Besar di Tengah
        st.markdown(
            "<div class='main-title'>Snack Patrol</div>", unsafe_allow_html=True
        )
        st.markdown(
            "<div class='sub-title'>Periksa kandungan nutrisi snack & minumanmu secara presisi</div>",
            unsafe_allow_html=True,
        )

        # Search Bar Besar di Tengah
        search_query = st.text_input(
            "",
            placeholder="🔍 Cari snack atau minuman... (cth: Teh Pucuk, Oreo, Chitato)",
            key="search_home",
        )

        # Tombol Rekomendasi Cepat (Pills) di bawah search bar
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

        # LOGIKA PENCARIAN & GRID CARDS
        if search_query:
            # Jika user sedang mencari produk tertentu
            hasil_filter = df[
                df["Nama Produk"].str.contains(
                    search_query, case=False, na=False
                )
            ]

            if not hasil_filter.empty:
                st.markdown(
                    f"#### 🔍 Hasil Analisis untuk '{search_query}':"
                )

                # Jika hanya 1 produk yang diklik/dicari, munculkan Detail Lab aslimu
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
                    with col_gula:
                        st.markdown("### 🍬 **Uji Kandungan Gula**")
                        st.metric(
                            label="Massa Gula Terlarut",
                            value=f"{data_snack['Kandungan Gula (g)']} g",
                        )
                        st.caption(
                            f"🧪 Konsentrasi: **{data_snack['Sugar /100 g']}** per 100g"
                        )
                        st.caption(
                            f"📈 Harian: **{data_snack['Persen Gula Harian']}%** dari batas 50g"
                        )

                        if data_snack["Sugar Level"] == "GAWAT":
                            st.error(f"🔴 **STATUS: {data_snack['Sugar Level']}**")
                        elif data_snack["Sugar Level"] == "WASPADA":
                            st.warning(
                                f"🟡 **STATUS: {data_snack['Sugar Level']}**"
                            )
                        else:
                            st.success(
                                f"🟢 **STATUS: {data_snack['Sugar Level']}**"
                            )

                    with col_natrium:
                        st.markdown("### 🧂 **Uji Kandungan Natrium**")
                        st.metric(
                            label="Massa Natrium Terlarut",
                            value=f"{data_snack['Kandungan Natrium (mg)']} mg",
                        )
                        st.caption(
                            f"🧪 Konsentrasi: **{data_snack['Natrium /100 g']}** per 100g"
                        )
                        st.caption(
                            f"📈 Harian: **{data_snack['Persen Natrium Harian']}%** dari batas 2000mg"
                        )

                        if data_snack["Natrium Level"] == "GAWAT":
                            st.error(
                                f"🔴 **STATUS: {data_snack['Natrium Level']}**"
                            )
                        elif data_snack["Natrium Level"] == "WASPADA":
                            st.warning(
                                f"🟡 **STATUS: {data_snack['Natrium Level']}**"
                            )
                        else:
                            st.success(
                                f"🟢 **STATUS: {data_snack['Natrium Level']}**"
                            )

                    st.markdown("---")
                    st.markdown("### 🧬 **Laporan Komposisi & Toksikologi**")
                    st.info(f"🔮 **Senyawa Utama:** {data_snack['Senyawa Utama']}")
                    st.error(
                        f"⚠️ **Bahaya Berlebih:** {data_snack['Bahaya Berlebih']}"
                    )
                else:
                    # Tampilkan dalam bentuk Grid jika hasil pencarian banyak
                    cols = st.columns(3)
                    for idx, row in enumerate(hasil_filter.itertuples()):
                        with cols[idx % 3]:
                            badge_class = "badge-aman"
                            if (
                                row._5 == "GAWAT" or row._8 == "GAWAT"
                            ):  # Cek status level gula/natrium
                                badge_class = "badge-gawat"
                            elif (
                                row._5 == "WASPADA" or row._8 == "WASPADA"
                            ):
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

        else:
            # TAMPILAN DEFAULT: MENAMPILKAN SEMUA PRODUK (GRID 3 KOLOM SEPERTI FOTO REFERENSI)
            st.markdown("### 📦 Semua Produk Tersedia")
            grid_kolom = st.columns(3)

            for indeks, baris in df.iterrows():
                # Tentukan warna badge gabungan berdasarkan tingkat keparahan zat gizi
                if (
                    baris["Sugar Level"] == "GAWAT"
                    or baris["Natrium Level"] == "GAWAT"
                ):
                    css_badge = "badge-gawat"
                    status_teks = "GAWAT"
                elif (
                    baris["Sugar Level"] == "WASPADA"
                    or baris["Natrium Level"] == "WASPADA"
                ):
                    css_badge = "badge-waspada"
                    status_teks = "WASPADA"
                else:
                    css_badge = "badge-aman"
                    status_teks = "AMAN"

                # Masukkan ke kolom grid (0, 1, atau 2) secara bergantian
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

    # ==============================================================================
    # TAB 2: BERAT IDEAL
    # ==============================================================================
    with menu_berat:
        st.markdown(
            "## ⚖️ Kalkulator Berat Badan Ideal (Metode Broca)",
            unsafe_allow_html=True,
        )
        st.write("---")
        c1, c2 = st.columns(2)
        with c1:
            gender = st.radio("Jenis Kelamin Praktikan:", ["Pria", "Wanita"])
            tinggi = st.number_input(
                "Tinggi Badan (cm):", min_value=100, max_value=250, value=165, key="tb"
            )
        with c2:
            berat_sekarang = st.number_input(
                "Berat Badan Saat Ini (kg):", min_value=30, max_value=200, value=60, key="bb"
            )

        if gender == "Pria":
            berat_ideal = (tinggi - 100) - ((tinggi - 100) * 0.10)
        else:
            berat_ideal = (tinggi - 100) - ((tinggi - 100) * 0.15)

        st.markdown("### 📊 Hasil Analisis Klinis")
        st.metric(label="Berat Badan Ideal Target", value=f"{berat_ideal:.2f} kg")
        selisih = berat_sekarang - berat_ideal

        if abs(selisih) <= 2:
            st.success("🟢 Status: Berat badan Anda ideal! Pertahankan pola konsumsi.")
        elif selisih > 2:
            st.warning(f"🟡 Status: Kelebihan {selisih:.2f} kg. Batasi sampel berkadar gula tinggi.")
        else:
            st.info(f"🔵 Status: Kekurangan {abs(selisih):.2f} kg. Tingkatkan kalori sehat.")

    # ==============================================================================
    # TAB 3: BANDINGKAN PRODUK
    # ==============================================================================
    with menu_bandingkan:
        st.markdown("## 📊 Perbandingan Vektor Nutrisi Antar Sampel", unsafe_allow_html=True)
        st.write("---")
        daftar_snack = df["Nama Produk"].tolist()
        
        cx, cy = st.columns(2)
        with cx:
            p1 = st.selectbox("Pilih Sampel A:", daftar_snack, index=0)
        with cy:
            idx_def = 1 if len(daftar_snack) > 1 else 0
            p2 = st.selectbox("Pilih Sampel B:", daftar_snack, index=idx_def)

        if p1 and p2:
            data_p1 = df[df["Nama Produk"] == p1].iloc[0]
            data_p2 = df[df["Nama Produk"] == p2].iloc[0]

            matriks_komparasi = pd.DataFrame({
                "Parameter Uji": ["Massa Gula (g)", "Massa Natrium (mg)", "Porsi Sampel (g/mL)"],
                p1: [data_p1["Kandungan Gula (g)"], data_p1["Kandungan Natrium (mg)"], data_p1["Quantity (g or mL)"]],
                p2: [data_p2["Kandungan Gula (g)"], data_p2["Kandungan Natrium (mg)"], data_p2["Quantity (g or mL)"]]
            })
            st.table(matriks_komparasi)

            st.markdown("### 📉 Hasil Evaluasi Selisih Kandungan")
            sg = data_p1["Kandungan Gula (g)"] - data_p2["Kandungan Gula (g)"]
            sn = data_p1["Kandungan Natrium (mg)"] - data_p2["Kandungan Natrium (mg)"]

            st.write(f"• Gula **{p1}** {'lebih tinggi' if sg>0 else 'lebih rendah' if sg<0 else 'setara'} sebesar **{abs(sg):.1f} g** dibanding {p2}.")
            st.write(f"• Natrium **{p1}** {'lebih tinggi' if sn>0 else 'lebih rendah' if sn<0 else 'setara'} sebesar **{abs(sn):.1f} mg** dibanding {p2}.")

except FileNotFoundError:
    st.error("❌ File 'Database Snack.csv' tidak ditemukan.")
except Exception as e:
    st.error(f"❌ Terjadi gangguan sistem: {e}")