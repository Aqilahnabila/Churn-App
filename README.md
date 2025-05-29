## Customer Churn App
----------------
Customer Churn App adalah aplikasi berbasis web menggunakan Streamlit yang bertujuan untuk memprediksi pelanggan yang kemungkinan akan berhenti (churn). Aplikasi ini memungkinkan pengguna untuk mengunggah data pelanggan dalam format CSV, lalu melakukan prediksi dengan model machine learning yang telah dilatih. Selain itu, aplikasi menyajikan visualisasi distribusi churn, analisis fitur yang memengaruhi churn, dan memberikan rekomendasi strategi retensi.

## Fitur Utama:
- Upload file data pelanggan
- Prediksi pelanggan yang akan churn
- Visualisasi distribusi churn (asli dan hasil prediksi)
- Analisis fitur terhadap churn
- Rekomendasi strategi retensi berbasis data

## Cara Menjalankan Program
------------------------
1. Clone repositori ini dari GitHub:
   **git clone https://github.com/username/Churn-App.git**
   **cd nama-repo**
3. pip install -r requirements.txt 
4. Jalankan aplikasi dengan perintah berikut di terminal atau command prompt:
   **streamlit run app.py**

## Struktur Folder
---------------
- file berikut harus tersedia dalam satu folder:
    - `app.py`               : File utama aplikasi Streamlit
    - `model.pkl`            : File model machine learning (harus disiapkan sebelumnya)
    - `Data`                 : File data csv 

## Informasi Tambahan
------------------
- Aplikasi ini mendukung berbagai fitur analitik dan rekomendasi berdasarkan nilai churn.
- Untuk membuat model.pkl, kamu bisa melatih model klasifikasi menggunakan scikit-learn, lalu menyimpannya dengan joblib.
- Data input harus memiliki kolom yang sesuai dengan data saat pelatihan model, seperti 'MonthlyCharges', 'tenure', 'Contract', dsb.
