import os
import pandas as pd
import streamlit as st

# 1. Konfigurasi awal halaman dengan ikon tabung reaksi
st.set_page_config(
    page_title="Snack Patrol - Food Lab Analysis", page_icon="🧪", layout="wide"
)

# Custom CSS bawaan kamu untuk mengatur ukuran font agar seragam
st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        font-size: 18px;
    }
    p, .stMarkdown, .stCaption {
        font-size: 18px !important;
    }
    .stMetric label {
        font-size: 20px !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        font-size: 36px !important;
    }
    h3 {
        font-size: 28px !important;
    }
    h4 {
        font-size: 24px !important;
    }
    .stAlert p {
        font-size: 18px !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# 2. Fungsi untuk memuat database CSV (Sesuai dengan setup kamu)
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "Database Snack.csv")

    # Membaca CSV dengan encoding khusus Excel dan membersihkan spasi nama kolom
    data = pd.read_csv(csv_path, sep=";", encoding="utf-8-sig")
    data.columns = data.columns.str.strip()
    return data


try:
    df = load_data()

    # --- SIDEBAR NAVIGASI BARU ---
    st.sidebar.markdown("### 🎛️ **Menu Laboratorium**")
    pilihan_menu = st.sidebar.radio(
        "Pilih Menu Analisis:",
        [
            "🔬 Scanner & Uji Kandungan",
            "⚖️ Kalkulator BB Ideal (Broca)",
            "📊 Komparasi Gizi Produk",
        ],
    )

    # ==============================================================================
    # FITUR 1: SCANNER & UJI KANDUNGAN (Kode Asli Kamu)
    # ==============================================================================
    if pilihan_menu == "🔬 Scanner & Uji Kandungan":
        # Header bertema Food Lab asli kamu
        st.markdown(
            "<h1 style='text-align: center; color: #FF6B8B;'>🧪 SNACK PATROL 🔬</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h3 style='text-align: center; color: #4A5568;'>Food Laboratory & Nutrition Scanner</h3>",
            unsafe_allow_html=True,
        )
        st.write("---")

        st.markdown("##### 🎛️ **Masukkan Sampel Snack atau Minuman:**")
        daftar_snack = df["Nama Produk"].tolist()
        pilihan_snack = st.selectbox(
            "Pilih atau ketik nama produk di bawah ini:",
            ["-- Sampel apa yang ingin dianalisis? --"] + daftar_snack,
        )

        if pilihan_snack != "-- Sampel apa yang ingin dianalisis? --":
            data_snack = df[df["Nama Produk"] == pilihan_snack].iloc[0]

            # Kotak Informasi Sampel
            st.markdown(
                f"""
            <div style='background-color: #FFFDF0; padding: 15px; border-radius: 10px; border-left: 5px solid #FF6B8B; margin-bottom: 20px;'>
                <h3 style='margin: 0; color: #2D3748;'>🧫 Hasil Pemindaian: {data_snack['Nama Produk']}</h3>
                <p style='margin: 5px 0 0 0; color: #718096;'><b>Kategori Objek:</b> {data_snack['Kategori']} | <b>Massa Total:</b> {data_snack['Quantity (g or mL)']} g/mL</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

            # Pembagian 2 Kolom Uji Laboratorium
            kolom1, kolom2 = st.columns(2)

            with kolom1:
                st.markdown("#### 🍬 **Uji Kandungan Gula**")
                st.metric(
                    label="Massa Gula Terlarut",
                    value=f"{data_snack['Kandungan Gula (g)']} g",
                )
                st.caption(
                    f"🧪 Konsentrasi: **{data_snack['Sugar /100 g']}** per 100g sampel"
                )
                st.caption(
                    f"📈 Konsumsi Harian: **{data_snack['Persen Gula Harian']}%** dari batas 50g/hari"
                )

                level_gula = data_snack["Sugar Level"]
                if level_gula == "GAWAT":
                    st.error(f"🔴 **STATUS DATA: {level_gula}** (Kadar gula kritis!)")
                elif level_gula == "WASPADA":
                    st.warning(
                        f"🟡 **STATUS DATA: {level_gula}** (Mendekati ambang batas)"
                    )
                else:
                    st.success(
                        f"🟢 **STATUS DATA: {level_gula}** (Zat aman dikonsumsi)"
                    )

            with kolom2:
                st.markdown("#### 🧂 **Uji Kandungan Natrium**")
                st.metric(
                    label="Massa Natrium Terlarut",
                    value=f"{data_snack['Kandungan Natrium (mg)']} mg",
                )
                st.caption(
                    f"🧪 Konsentrasi: **{data_snack['Natrium /100 g']}** per 100g sampel"
                )
                st.caption(
                    f"📈 Konsumsi Harian: **{data_snack['Persen Natrium Harian']}%** dari batas 2000mg/hari"
                )

                level_natrium = data_snack["Natrium Level"]
                if level_natrium == "GAWAT":
                    st.error(
                        f"🔴 **STATUS DATA: {level_natrium}** (Kadar natrium kritis!)"
                    )
                elif level_natrium == "WASPADA":
                    st.warning(
                        f"🟡 **STATUS DATA: {level_natrium}** (Mendekati ambang batas)"
                    )
                else:
                    st.success(
                        f"🟢 **STATUS DATA: {level_natrium}** (Zat aman dikonsumsi)"
                    )

            st.write("---")

            # Bagian Analisis Kimia & Toksikologi
            st.markdown("### 🧬 **Laporan Komposisi & Toksikologi**")

            st.markdown("**Senyawa Utama yang Teridentifikasi:**")
            st.info(f"🔮 {data_snack['Senyawa Utama']}")

            st.markdown("**Efek Samping Biologis (Bahaya Berlebih):**")
            st.error(f"⚠️ {data_snack['Bahaya Berlebih']}")

            st.caption(
                "🤖 *Snack Patrol Food Lab System — Analisis presisi untuk camilan harianmu.*"
            )

    # ==============================================================================
    # FITUR 2: HITUNG BERAT BADAN IDEAL (Menggunakan Rumus Broca)
    # ==============================================================================
    elif pilihan_menu == "⚖️ Kalkulator BB Ideal (Broca)":
        st.markdown(
            "<h1 style='text-align: center; color: #FF6B8B;'>⚖️ METRIKS FISIK</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h3 style='text-align: center; color: #4A5568;'>Kalkulator Berat Badan Ideal (Metode Broca)</h3>",
            unsafe_allow_html=True,
        )
        st.write("---")

        col1, col2 = st.columns(2)
        with col1:
            gender = st.radio("Jenis Kelamin Praktikan:", ["Pria", "Wanita"])
            tinggi = st.number_input(
                "Tinggi Badan (cm):", min_value=100, max_value=250, value=165
            )
        with col2:
            berat_sekarang = st.number_input(
                "Berat Badan Saat Ini (kg):", min_value=30, max_value=200, value=60
            )

        # Logika Algoritma Matematika Rumus Broca
        if gender == "Pria":
            berat_ideal = (tinggi - 100) - ((tinggi - 100) * 0.10)
        else:
            berat_ideal = (tinggi - 100) - ((tinggi - 100) * 0.15)

        st.markdown("### 📊 **Hasil Analisis Klinis**")

        # Menampilkan metrik hasil perhitungan
        st.metric(label="Berat Badan Ideal Target", value=f"{berat_ideal:.2f} kg")

        selisih = berat_sekarang - berat_ideal

        if abs(selisih) <= 2:
            st.success(
                "🟢 **Status:** Berat badan Anda saat ini ideal! Pertahankan pola konsumsi Anda."
            )
        elif selisih > 2:
            st.warning(
                f"🟡 **Status:** Kelebihan {selisih:.2f} kg. Disarankan membatasi sampel snack berkadar gula tinggi."
            )
        else:
            st.info(
                f"🔵 **Status:** Kekurangan {abs(selisih):.2f} kg dari angka ideal. Tingkatkan kalori sehat harian Anda."
            )

    # ==============================================================================
    # FITUR 3: PERBANDINGAN GIZI PRODUK (Operasi Vektor Selisih)
    # ==============================================================================
    elif pilihan_menu == "📊 Komparasi Gizi Produk":
        st.markdown(
            "<h1 style='text-align: center; color: #FF6B8B;'>📊 UJI KOMPARASI</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h3 style='text-align: center; color: #4A5568;'>Perbandingan Vektor Nutrisi Antar Sampel</h3>",
            unsafe_allow_html=True,
        )
        st.write("---")

        daftar_snack = df["Nama Produk"].tolist()

        col1, col2 = st.columns(2)
        with col1:
            produk_1 = st.selectbox("Pilih Sampel A:", daftar_snack, index=0)
        with col2:
            # Proteksi agar tidak error jika database sedikit
            idx_default = 1 if len(daftar_snack) > 1 else 0
            produk_2 = st.selectbox(
                "Pilih Sampel B:", daftar_snack, index=idx_default
            )

        if produk_1 and produk_2:
            data_p1 = df[df["Nama Produk"] == produk_1].iloc[0]
            data_p2 = df[df["Nama Produk"] == produk_2].iloc[0]

            st.markdown("### ⚔️ **Tabel Matriks Perbandingan**")

            # Membuat susunan matriks data gizi
            matriks_komparasi = pd.DataFrame(
                {
                    "Parameter Uji": [
                        "Massa Gula (g)",
                        "Massa Natrium (mg)",
                        "Porsi Sampel (g/mL)",
                    ],
                    produk_1: [
                        data_p1["Kandungan Gula (g)"],
                        data_p1["Kandungan Natrium (mg)"],
                        data_p1["Quantity (g or mL)"],
                    ],
                    produk_2: [
                        data_p2["Kandungan Gula (g)"],
                        data_p2["Kandungan Natrium (mg)"],
                        data_p2["Quantity (g or mL)"],
                    ],
                }
            )

            st.table(matriks_komparasi)

            # Analisis Selisih Linear (Vektor A - Vektor B)
            st.markdown("### 📉 **Hasil Evaluasi Selisih Kandungan**")
            selisih_gula = (
                data_p1["Kandungan Gula (g)"] - data_p2["Kandungan Gula (g)"]
            )
            selisih_natrium = (
                data_p1["Kandungan Natrium (mg)"]
                - data_p2["Kandungan Natrium (mg)"]
            )

            if selisih_gula > 0:
                st.write(
                    f"• **{produk_1}** memiliki kandungan gula **{abs(selisih_gula):.1f} g lebih tinggi** dibandingkan {produk_2}."
                )
            elif selisih_gula < 0:
                st.write(
                    f"• **{produk_1}** memiliki kandungan gula **{abs(selisih_gula):.1f} g lebih rendah** dibandingkan {produk_2}."
                )
            else:
                st.write(
                    f"• Kadar gula **{produk_1}** dan **{produk_2}** adalah **setara**."
                )

            if selisih_natrium > 0:
                st.write(
                    f"• **{produk_1}** memiliki kandungan natrium **{abs(selisih_natrium):.1f} mg lebih tinggi** dibandingkan {produk_2}."
                )
            elif selisih_natrium < 0:
                st.write(
                    f"• **{produk_1}** memiliki kandungan natrium **{abs(selisih_natrium):.1f} mg lebih rendah** dibandingkan {produk_2}."
                )
            else:
                st.write(
                    f"• Kadar natrium **{produk_1}** dan **{produk_2}** adalah **setara**."
                )

except FileNotFoundError:
    st.error("❌ File 'Database Snack.csv' tidak ditemukan di folder kerja ini.")
except Exception as e:
    st.error(f"❌ Terjadi gangguan pada sistem scanner: {e}")