# ================================================================
# Customer Churn Analysis App
# Copyright (c) 2025 Aqilah, Sun Kayla, Abida, Giselle, Adinda
# Licensed under the MIT License (see LICENSE file for details)
# ================================================================

import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.preprocessing import LabelEncoder

# Konfigurasi halaman
st.set_page_config(page_title="Customer Churn App", layout="wide")

# Custom CSS Styling
st.markdown("""
<style>
/* ========== UMUM ========== */
body {
    background-color: white;
}

/* Header Utama (Judul Aplikasi) */
h1 {
    background-color: #b30000;
    color: white !important;
    padding: 0.8em 1em;
    border-radius: 12px;
    font-size: 34px;
    text-align: center;
    margin: 1.5em 0 1em 0;  /* ↑↓ spasi atas bawah */
    font-weight: bold;
}

/* Box Info (st.info) */
.stAlert[data-testid="stAlert"] {
    background-color: #fff5f5;  /* merah muda terang */
    border-left: 6px solid #b30000;
    border-radius: 8px;
    padding: 1.2em;
    margin-bottom: 1.5em;
    margin-top: 0.8em;
}

.stAlert p {
    color: #4d0000;
    font-weight: 500;
    line-height: 1.6;  /* memperlebar antar baris */
}

/* Header Langkah (1️⃣, 2️⃣, dst.) */
h2 {
    color: #b30000 !important;
    font-weight: bold !important;
    border-bottom: 2px solid #b30000;
    padding-bottom: 0.3em;
    margin-top: 2em;
    margin-bottom: 0.8em;
}

/* Label Dropdown */
label[data-baseweb="select"] {
    background-color: #b30000;
    color: white;
    padding: 0.25em 0.5em;
    border-radius: 5px;
    font-weight: bold;
}

/* Selectbox pilihan fitur */
div[data-baseweb="select"] > div {
    background-color: #b30000 !important;
    color: white !important;
    font-weight: bold;
}

/* File Uploader */
section[data-testid="stFileUploader"] {
    border: 2px dashed #b30000;
    background-color: #fff5f5;
    padding: 1em;
    border-radius: 8px;
    margin-bottom: 1.5em;
}

/* Tombol Download */
.stDownloadButton > button {
    background-color: #b30000;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    transition: 0.3s ease;
    margin-top: 0.5em;
}

.stDownloadButton > button:hover {
    background-color: #800000;
}

/* Tabel Prediksi */
.stDataFrame {
    border: 2px solid #b30000;
    border-radius: 5px;
    margin-bottom: 2em;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Aplikasi Analisis Retensi Pelanggan")

st.info("""
⚠️ **Perhatian:**  
Pastikan data pelanggan yang anda upload mengikuti format yang sesuai.

📄 Jika anda belum punya data pelanggan sendiri atau ingin contoh format yang benar:
- Gunakan **template CSV** yang sudah disediakan.
- Apabila diperlukan, coba terlebih dahulu dengan **data contoh** yang ada di folder GitHub kami atau dapat pula diunduh pada tombol dibawah ini.

""")

col1, col2 = st.columns(2)
with col1:
    with open("dataset_template.csv", "rb") as file:
        st.download_button(
            label="⬇️ Download Template CSV",
            data=file,
            file_name="dataset_template.csv",
            mime="text/csv",
            use_container_width=True
        )
with col2:
    with open("Data/Data trial 1.csv", "rb") as file:
        st.download_button(
            label="⬇️ Download Data Contoh",
            data=file,
            file_name="Data trial 1.csv",
            mime="text/csv",
            use_container_width=True
        )

# Fungsi load model
@st.cache_resource
def load_model():
    model_path = "model/model.pkl"
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None

# ===== 1. Upload Data =====
st.header("1️⃣ Upload Data Pelanggan")
uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Data berhasil diupload!")
    st.write("### Cuplikan Data")
    st.dataframe(df.head())

    st.header("2️⃣ Prediksi Pelanggan yang Akan Churn")
    model = load_model()

    X = None  # Inisialisasi X agar tidak error
    if model:
        try:
            # Drop kolom target & ID jika ada
            drop_cols = ['Churn', 'customerID']
            X = df.drop(columns=[col for col in drop_cols if col in df.columns], errors='ignore')

            # AUTO ENCODE (tanpa ubah df asli)
            X_encoded = X.copy()
            for col in X_encoded.select_dtypes(include='object').columns:
                le = LabelEncoder()
                try:
                    X_encoded[col] = le.fit_transform(X_encoded[col].astype(str))
                except:
                    pass  # Lewati kolom yang tidak bisa di-encode

            # Prediksi
            pred = model.predict(X_encoded)
            df['Predicted_Churn'] = pred.astype(int)
            df['Predicted_Churn'] = pd.Categorical(df['Predicted_Churn'], categories=[0, 1], ordered=True)
            df['Predicted_Churn_Label'] = df['Predicted_Churn'].map({1: 'Akan Churn', 0: 'Tidak Churn'})

            st.success("✅ Prediksi berhasil dilakukan!")
            st.write("### 🧾 Tabel Hasil Prediksi Churn")

            pred_tabel = df[['Predicted_Churn_Label']]
            if 'customerID' in df.columns:
                pred_tabel.index = df['customerID']

            st.dataframe(pred_tabel.head())

            st.caption("Keterangan: 'Akan Churn' berarti pelanggan diprediksi akan berhenti berlangganan. "
                       "'Tidak Churn' berarti pelanggan diprediksi akan tetap bertahan.")

            # Simpan hasil prediksi
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download Hasil Prediksi", csv, "prediksi_churn.csv", "text/csv")

        except Exception as e:
            st.error(f"Gagal melakukan prediksi: {e}")
            model = None  # Nonaktifkan proses lanjut
    else:
        st.warning("❗ Model belum tersedia. Pastikan `model/model.pkl` ada di folder.")

    # ===== 3. Visualisasi Distribusi Prediksi Churn =====
    if model:
        st.header("3️⃣ Visualisasi Distribusi Prediksi Churn")

        fig, ax = plt.subplots(figsize=(6, 4), tight_layout=True)
        warna_churn = ["#1f77b4", "#ff7f0e"]
        labels_churn = ["Tidak Churn (0)", "Akan Churn (1)"]

        plot = sns.countplot(x='Predicted_Churn', data=df, ax=ax, palette=warna_churn, order=[0, 1])

        for p in plot.patches:
            count = int(p.get_height())
            x = p.get_x() + p.get_width() / 2
            y = p.get_height()
            ax.annotate(f'{count}', (x, y), ha='center', va='bottom', fontsize=9, fontweight='bold')

        ax.set_title("Distribusi Prediksi Churn")
        ax.set_xlabel("Prediksi Churn")
        ax.set_ylabel("Jumlah Pelanggan")
        ax.set_xticks([0, 1])
        ax.set_xticklabels(labels_churn)

        st.pyplot(fig)

        # ===== 4. Analisis Fitur terhadap Churn =====
        st.header("4️⃣ Analisis Fitur terhadap Churn")
        fitur = st.selectbox("Pilih fitur:", X.columns)
        fig, ax = plt.subplots(figsize=(10, 4), tight_layout=True)

        palette = warna_churn
        hue_order = [0, 1]

        if df[fitur].dtype == 'object' or df[fitur].nunique() <= 10:
            sns.countplot(data=df, x=fitur, hue='Predicted_Churn', palette=palette,
                          hue_order=hue_order, ax=ax)

            for p in ax.patches:
                height = p.get_height()
                if height > 0:
                    ax.annotate(f'{int(height)}',
                                (p.get_x() + p.get_width() / 2, height),
                                ha='center', va='bottom', fontsize=10, fontweight='bold')

            ax.set_title(f"Distribusi berdasarkan {fitur} dan Prediksi Churn")
            ax.set_ylabel("Jumlah Pelanggan")
            ax.legend(title="Predicted Churn", labels=labels_churn)
            ax.set_xlabel(fitur)

        else:
            sns.histplot(data=df, x=fitur, hue='Predicted_Churn', palette={0: "#1f77b4", 1: "#ff7f0e"},
                         hue_order=hue_order, kde=True, multiple="stack", ax=ax)

            for container in ax.containers:
                for patch in container:
                    height = patch.get_height()
                    if height > 0:
                        x = patch.get_x() + patch.get_width() / 2
                        y = height
                        ax.annotate(f'{int(height)}', (x, y),
                                    ha='center', va='bottom', fontsize=9, fontweight='bold')

            ax.set_title(f"Distribusi {fitur} berdasarkan Prediksi Churn")
            ax.set_ylabel("Jumlah Pelanggan")
            ax.set_xlabel(fitur)

            from matplotlib.patches import Patch
            legend_labels = [
                Patch(facecolor="#1f77b4", label="Tidak Churn (0)"),
                Patch(facecolor="#ff7f0e", label="Akan Churn (1)")
            ]
            ax.legend(handles=legend_labels, title="Predicted Churn")
        st.pyplot(fig)

        # ===== 5. Rekomendasi Strategi Retensi dengan Prioritas =====
        st.header("5️⃣ Rekomendasi Strategi Retensi Berdasarkan Prioritas")

        churned = df[df['Predicted_Churn'] == 1]

        strategi_prioritas = []

        def prop_churn_kategori(col, val=None):
            """
            Hitung proporsi churn berdasarkan kolom.
            Jika val diberikan, hitung proporsi churn untuk kategori val.
            Jika tidak, hitung proporsi churn keseluruhan berdasarkan kolom (rata-rata untuk numerik).
            """
            if col not in churned.columns:
                return 0
            if val is not None:
                total_churn = len(churned)
                if total_churn == 0:
                    return 0
                count_val = churned[churned[col] == val].shape[0]
                return count_val / total_churn
            else:
                # Jika kolom numerik, gunakan mean (proporsi jika 0/1)
                if pd.api.types.is_numeric_dtype(churned[col]):
                    return churned[col].mean()
                else:
                    # Untuk kategori, kembalikan proporsi terbesar kategori di churned
                    vals = churned[col].value_counts(normalize=True)
                    if len(vals) == 0:
                        return 0
                    return vals.iloc[0]
        
        # Mulai tentukan strategi dan proporsinya

        # 1. MonthlyCharges
        if 'Jumlah Tagihan per Bulan (MonthlyCharges)' in churned.columns:
            mean_all = df['Jumlah Tagihan per Bulan (MonthlyCharges)'].mean()
            mean_churn = churned['Jumlah Tagihan per Bulan (MonthlyCharges)'].mean()
            if mean_churn > mean_all:
                p = abs(mean_churn - mean_all) / mean_all  # prioritas proporsional beda tagihan
                strategi_prioritas.append((p, "💸 Rata-rata tagihan pelanggan churn lebih tinggi dari rata-rata pelanggan. Pertimbangkan pemberian diskon atau bundling layanan untuk mengurangi churn."))

        # 2. SeniorCitizen (Usia >65 Tahun)
        if 'Usia >65 Tahun (SeniorCitizen)' in churned.columns:
            prop_senior_churn = churned['Usia >65 Tahun (SeniorCitizen)'].mean()
            prop_senior_all = df['Usia >65 Tahun (SeniorCitizen)'].mean()
            diff = prop_senior_churn - prop_senior_all
            if diff > 0.05:
                strategi_prioritas.append((diff, "👴 Pelanggan lansia cenderung lebih sering churn. Sediakan layanan khusus atau hotline ramah lansia."))

        # 3. PaymentMethod (Metode Pembayaran)
        if 'Metode Pembayaran (PaymentMethod)' in churned.columns:
            metode_dom = churned['Metode Pembayaran (PaymentMethod)'].value_counts(normalize=True)
            if not metode_dom.empty:
                metode_tertinggi = metode_dom.idxmax()
                prop_tertinggi = metode_dom.max()
                if prop_tertinggi >= 0.3:
                    prioritas = prop_tertinggi
                    if "Electronic check" in metode_tertinggi:
                        strategi_prioritas.append((prioritas, "💳 Mayoritas pelanggan churn menggunakan 'Electronic check'. Tawarkan insentif untuk auto-payment."))
                    elif "Mailed check" in metode_tertinggi:
                        strategi_prioritas.append((prioritas, "📬 Banyak pelanggan churn menggunakan 'Mailed check'. Edukasi pelanggan tentang metode pembayaran otomatis yang lebih nyaman."))
                    elif "Bank transfer" in metode_tertinggi:
                        strategi_prioritas.append((prioritas, "🏦 Pelanggan churn banyak yang pakai 'Bank transfer (automatic)'. Periksa kemungkinan error atau gangguan pada sistem pembayaran otomatis."))
                    elif "Credit card" in metode_tertinggi:
                        strategi_prioritas.append((prioritas, "💳 'Credit card (automatic)' mendominasi metode pembayaran pelanggan churn. Pastikan keamanan dan kemudahan pembayaran."))

        # 4. Tenure (Lama Berlangganan)
        if 'Lama Berlangganan (tenure)' in churned.columns:
            mean_tenure_churn = churned['Lama Berlangganan (tenure)'].mean()
            if mean_tenure_churn < 6:
                # Prioritas bisa proporsional dengan seberapa kecil tenure
                prioritas = max(0, (6 - mean_tenure_churn) / 6)
                strategi_prioritas.append((prioritas, "📉 Banyak pelanggan churn baru bergabung <6 bulan. Tingkatkan onboarding dan edukasi awal."))

        # 5. OnlineSecurity (Keamanan Online)
        if 'Memiliki Keamanan Online (OnlineSecurity)' in churned.columns:
            no_security_count = churned['Memiliki Keamanan Online (OnlineSecurity)'].astype(str).str.contains("No", na=False).sum()
            total_churn = len(churned)
            if total_churn > 0:
                prop_no_security = no_security_count / total_churn
                if prop_no_security >= 0.3:
                    strategi_prioritas.append((prop_no_security, "🔐 Banyak pelanggan churn tidak menggunakan keamanan online. Tawarkan layanan keamanan gratis."))

        # 6. Contract (Jenis Kontrak)
        if 'Jenis Kontrak Pelanggan (Contract)' in churned.columns:
            contract_props = churned['Jenis Kontrak Pelanggan (Contract)'].value_counts(normalize=True)
            if not contract_props.empty:
                for contract_type, prop in contract_props.items():
                    if prop >= 0.3:
                        prioritas = prop
                        if "Month-to-month" in contract_type:
                            strategi_prioritas.append((prioritas, "🎯 Mayoritas pelanggan churn memiliki kontrak 'Month-to-month'. Tawarkan insentif atau diskon untuk upgrade ke kontrak tahunan agar lebih loyal."))
                        elif "One year" in contract_type:
                            strategi_prioritas.append((prioritas, "📆 Banyak pelanggan churn memiliki kontrak satu tahun. Evaluasi apakah layanan memenuhi ekspektasi selama periode tersebut."))
                        elif "Two year" in contract_type:
                            strategi_prioritas.append((prioritas, "🔐 Meskipun kontrak dua tahun, masih terjadi churn. Tinjau kembali kepuasan pelanggan jangka panjang dan beri bonus loyalitas."))

        # 7. InternetService (Jenis Layanan Internet)
        if 'Jenis Layanan Internet (InternetService)' in churned.columns:
            internet_dom = churned['Jenis Layanan Internet (InternetService)'].value_counts(normalize=True)
            if not internet_dom.empty:
                jenis_tertinggi = internet_dom.idxmax()
                prop_tertinggi = internet_dom.max()
                if prop_tertinggi >= 0.3:
                    prioritas = prop_tertinggi
                    strategi_prioritas.append((prioritas, f"🌐 Mayoritas pelanggan churn menggunakan layanan internet '{jenis_tertinggi}'. Tinjau kualitas layanan dan tawarkan promo upgrade."))

        # 8. TechSupport (Dukungan Teknis)
        if 'Memiliki Dukungan Teknis (TechSupport)' in churned.columns:
            no_tech_support_count = churned['Memiliki Dukungan Teknis (TechSupport)'].astype(str).str.contains("No", na=False).sum()
            total_churn = len(churned)
            if total_churn > 0:
                prop_no_tech_support = no_tech_support_count / total_churn
                if prop_no_tech_support >= 0.3:
                    strategi_prioritas.append((prop_no_tech_support, "🛠️ Banyak pelanggan churn tidak menggunakan layanan dukungan teknis. Tawarkan layanan TechSupport gratis atau prioritas."))

        # Urutkan berdasarkan prioritas descending
        strategi_prioritas = sorted(strategi_prioritas, key=lambda x: x[0], reverse=True)

        if len(strategi_prioritas) == 0:
            st.info("Data prediksi churn belum tersedia atau tidak ditemukan pola khusus untuk rekomendasi strategi.")
        else:
            st.write("Berikut adalah rekomendasi strategi retensi pelanggan berdasarkan fitur yang berpengaruh dan proporsi churn tertinggi:")

            for i, (score, strategi) in enumerate(strategi_prioritas, 1):
                st.markdown(f"**{i}. (Prioritas: {score:.2f})** {strategi}")

else:
    st.info("Silakan upload file CSV terlebih dahulu untuk memulai analisis.")

st.markdown(
    """
    <hr style='margin-top: 2em;'>
    <div style='text-align: center; color: grey; font-size: 0.9em;'>
        © 2025 Aqilah, Sun Kayla, Abida, Giselle, Adinda. Licensed under the 
        <a href="https://opensource.org/licenses/MIT" target="_blank">MIT License</a>.
    </div>
    """,
    unsafe_allow_html=True
)
