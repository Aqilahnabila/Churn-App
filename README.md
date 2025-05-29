## Customer Churn App
----------------
Customer Churn App adalah aplikasi berbasis web menggunakan Streamlit yang bertujuan untuk memprediksi pelanggan yang kemungkinan akan berhenti berlangganan (churn). Aplikasi ini memungkinkan pengguna untuk mengunggah data pelanggan dalam format CSV, lalu melakukan prediksi dengan model machine learning yang telah dilatih. Selain itu, aplikasi menyajikan visualisasi distribusi churn, analisis fitur yang memengaruhi churn, dan memberikan rekomendasi strategi retensi.

## 🚀 Fitur Utama:
- 📂 Upload file data pelanggan (.csv) sesuai dengan template dataset yang tersedia di repository
- 📊 Prediksi status churn menggunakan model Random Forest terlatih
- 📥 Download hasil prediksi churn dalam bentuk file CSV
- 📈 Visualisasi distribusi churn (prediksi churn keseluruhan)
- 🧩 Analisis fitur terhadap churn secara individual
- 💡 Rekomendasi strategi retensi berdasarkan kontribusi fitur terhadap churn

##🛠️ Cara Menjalankan Program
------------------------
1. Clone repositori ini dari GitHub:
   **git clone https://github.com/Aqilahnabila/Churn-App.git**
   
   **cd Churn-App**
3. Install dependensi : 
   **pip install -r requirements.txt**
4. Jalankan aplikasi streamlit:
   **streamlit run app.py**

## 📁 Struktur Folder
---------------
- file berikut harus tersedia dalam satu folder:
    - `app.py`               : File utama aplikasi Streamlit
    - `model.pkl`            : File model machine learning (Random Forest) yang sudah dilatih
    - `Data.csv`             : File data csv
    - `requirements.txt`     : Daftar library yang dibutuhkan

## 📊 Format Data Input
---------------
- Data input harus berupa file CSV dengan kolom dan urutan yang sama persis seperti data saat pelatihan model (dataset_template.csv).
- Gunakan file dataset_template.csv sebagai acuan. Pastikan tidak ada kolom tambahan, nama kolom salah, atau urutan tidak sesuai.
- Contoh kolom yang umum digunakan:

  | gender | SeniorCitizen | tenure | MonthlyCharges | Contract | ... |

⛔ Jika format tidak sesuai, proses prediksi tidak akan berjalan dan aplikasi akan menampilkan peringatan.

## ℹ️ Informasi Tambahan
------------------
- Informasi dataset dapat diakses pada file 'Metadata Churn-App' pada repository.
- Model machine learning yang digunakan adalah Random Forest Classifier.
- Model telah dilatih sebelumnya menggunakan dataset pelanggan (Data Telco tanpa encode.csv).
- File model.pkl disimpan menggunakan library joblib.
- Aplikasi dapat berjalan secara lokal tanpa koneksi internet, selama dependensi telah diinstal.
