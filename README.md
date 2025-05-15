## Dokumentasi Aplikasi Analisis Customer Churn 

## Deskripsi Proyek
----------------
Customer Churn App adalah aplikasi berbasis web menggunakan Streamlit yang bertujuan untuk memprediksi pelanggan yang kemungkinan akan berhenti (churn). Aplikasi ini memungkinkan pengguna untuk mengunggah data pelanggan dalam format CSV, lalu melakukan prediksi dengan model machine learning yang telah dilatih. Selain itu, aplikasi menyajikan visualisasi distribusi churn, analisis fitur yang memengaruhi churn, dan memberikan rekomendasi strategi retensi.

## Fitur Utama:
- Upload file data pelanggan
- Prediksi pelanggan yang akan churn
- Visualisasi distribusi churn (asli dan hasil prediksi)
- Analisis fitur terhadap churn
- Rekomendasi strategi retensi berbasis data

## Cara Instalasi
--------------
1. Pastikan Python 3.8 atau lebih baru sudah terinstal.
2. Install dependensi yang dibutuhkan:
   **pip install streamlit pandas joblib matplotlib seaborn**
3. Pastikan file model machine learning bernama `model.pkl` berada di dalam folder proyek.

## Cara Menjalankan Program
------------------------
1. Jalankan aplikasi dengan perintah berikut di terminal atau command prompt:
   **streamlit run app.py**
2. Upload file CSV berisi data pelanggan saat diminta.
3. Aplikasi akan memproses data, melakukan prediksi, dan menampilkan visualisasi serta rekomendasi.

## Struktur Folder
---------------
- file berikut harus tersedia dalam satu folder:
    - `app.py`               : File utama aplikasi Streamlit
    - `model.pkl`            : File model machine learning (harus disiapkan sebelumnya)
    - `README.md`            : Dokumentasi proyek ini

## Informasi Tambahan
------------------
- Aplikasi ini mendukung berbagai fitur analitik dan rekomendasi berdasarkan nilai churn.
- Untuk membuat model.pkl, kamu bisa melatih model klasifikasi menggunakan scikit-learn, lalu menyimpannya dengan joblib.
- Data input harus memiliki kolom yang sesuai dengan data saat pelatihan model, seperti 'MonthlyCharges', 'tenure', 'Contract', dsb.
