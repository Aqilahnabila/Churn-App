# Copyright (c) 2025 Aqilah, Sun Kayla, Abida, Giselle, Adinda
# This software is licensed under the MIT License.

#!/usr/bin/env python
# coding: utf-8
# In[7]:

# 1. Import Library
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# 2. Load Data (pastikan path-nya sesuai)
df = pd.read_csv(r'C:\Users\LENOVO\OneDrive\ドキュメント\Semester 4\PASD\Customer Churn App (TUBES FIX) - Copy\Data Telco tanpa encode.csv')

# 3. Preprocessing
df.drop("customerID", axis=1, inplace=True, errors='ignore')

# TotalCharges bisa kosong → ubah ke float, drop baris NaN
df["Total Tagihan Selama Menjadi Pelanggan (TotalCharges)"] = pd.to_numeric(df["Total Tagihan Selama Menjadi Pelanggan (TotalCharges)"], errors="coerce")
df.dropna(inplace=True)

# Encode kolom target
df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

# Label Encoding untuk semua kolom object (kategorikal)
le = LabelEncoder()
for col in df.select_dtypes(include="object").columns:
    df[col] = le.fit_transform(df[col])

# 4. Split fitur dan target
X = df.drop("Churn", axis=1)
y = df["Churn"]

# 5. Train Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# 6. Simpan model
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/model.pkl")

print("✅ Model berhasil disimpan di model/model.pkl")

