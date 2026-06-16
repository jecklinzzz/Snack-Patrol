import os
import pandas as pd
import streamlit as st

# 1. Konfigurasi awal halaman dengan ikon tabung reaksi
st.set_page_config(
    page_title="Snack Patrol - Food Lab Analysis", 
    page_icon="🧪", 
    layout="wide"
)

st.markdown("""
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
""", unsafe_allow_html=True)

# Header bertema Food Lab yang lucu
st.markdown("<h1 style='text-align: center; color: #FF6B8B;'>🧪 SNACK PATROL 🔬</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #4A5568;'>Food Laboratory & Nutrition Scanner</h3>", unsafe_allow_html=True)
st.write("---")

# 2. Fungsi untuk memuat database CSV
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
    
    # Komponen Input dikemas dengan narasi laboratorium
    st.markdown("##### 🎛️ **Masukkan Sampel Snack atau Minuman:**")
    daftar_snack = df["Nama Produk"].tolist()
    pilihan_snack = st.selectbox("Pilih atau ketik nama produk di bawah ini:", ["-- Sampel apa yang ingin dianalisis? --"] + daftar_snack)
    
    # Jika user telah memilih snack
    if pilihan_snack != "-- Sampel apa yang ingin dianalisis? --":
        data_snack = df[df["Nama Produk"] == pilihan_snack].iloc[0]
        
        # Kotak Informasi Sampel
        st.markdown(f"""
        <div style='background-color: #FFFDF0; padding: 15px; border-radius: 10px; border-left: 5px solid #FF6B8B; margin-bottom: 20px;'>
            <h3 style='margin: 0; color: #2D3748;'>🧫 Hasil Pemindaian: {data_snack['Nama Produk']}</h3>
            <p style='margin: 5px 0 0 0; color: #718096;'><b>Kategori Objek:</b> {data_snack['Kategori']} | <b>Massa Total:</b> {data_snack['Quantity (g or mL)']} g/mL</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Pembagian 2 Kolom Uji Laboratorium
        kolom1, kolom2 = st.columns(2)
        
        with kolom1:
            st.markdown("#### 🍬 **Uji Kandungan Gula**")
            st.metric(label="Massa Gula Terlarut", value=f"{data_snack['Kandungan Gula (g)']} g")
            st.caption(f"🧪 Konsentrasi: **{data_snack['Sugar /100 g']} g** per 100g sampel")
            st.caption(f"📈 Konsumsi Harian: **{data_snack['Persen Gula Harian']}%** dari batas 50g/hari")
            
            level_gula = data_snack['Sugar Level']
            if level_gula == "GAWAT":
                st.error(f"🔴 **STATUS DATA: {level_gula}** (Kadar gula kritis!)")
            elif level_gula == "WASPADA":
                st.warning(f"🟡 **STATUS DATA: {level_gula}** (Mendekati ambang batas)")
            else:
                st.success(f"🟢 **STATUS DATA: {level_gula}** (Zat aman dikonsumsi)")
                
        with kolom2:
            st.markdown("#### 🧂 **Uji Kandungan Natrium**")
            st.metric(label="Massa Natrium Terlarut", value=f"{data_snack['Kandungan Natrium (mg)']} mg")
            st.caption(f"🧪 Konsentrasi: **{data_snack['Natrium /100 g']} g** per 100g sampel")
            st.caption(f"📈 Konsumsi Harian: **{data_snack['Persen Natrium Harian']}%** dari batas 2000mg/hari")
            
            level_natrium = data_snack['Natrium Level']
            if level_natrium == "GAWAT":
                st.error(f"🔴 **STATUS DATA: {level_natrium}** (Kadar natrium kritis!)")
            elif level_natrium == "WASPADA":
                st.warning(f"🟡 **STATUS DATA: {level_natrium}** (Mendekati ambang batas)")
            else:
                st.success(f"🟢 **STATUS DATA: {level_natrium}** (Zat aman dikonsumsi)")
                
        st.write("---")
        
        # Bagian Analisis Kimia & Toksikologi
        st.markdown("### 🧬 **Laporan Komposisi & Toksikologi**")
        
        st.markdown("**Senyawa Utama yang Teridentifikasi:**")
        st.info(f"🔮 {data_snack['Senyawa Utama']}")
        
        st.markdown("**Efek Samping Biologis (Bahaya Berlebih):**")
        st.error(f"⚠️ {data_snack['Bahaya Berlebih']}")
        
        st.caption("🤖 *Snack Patrol Food Lab System — Analisis presisi untuk camilan harianmu.*")

except FileNotFoundError:
    st.error("❌ File 'Database Snack.csv' tidak ditemukan di folder kerja ini.")
except Exception as e:
    st.error(f"❌ Terjadi gangguan pada sistem scanner: {e}")