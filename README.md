# Tugas Proyek 1 RPP – Sistem Berbasis Pengetahuan (Prolog)

Proyek ini adalah implementasi Sistem Berbasis Pengetahuan (Knowledge-Based System / KBS) yang memanfaatkan ontologi Dota 2 untuk melakukan inferensi terkait hero, role, ability, dan klasifikasi lanjutan menggunakan Prolog.

## 📁 Struktur Folder
```
.
├── KBS Prolog/
│   ├── abox_dota2.pl              # ABox – Fakta hero, ability, role
│   ├── aboxconvertprolog.py       # Script konversi JSON → ABox Prolog
│   ├── kbsrules_dota2.pl          # Rules inferensi (KBS)
│   ├── tbox_dota2.pl              # TBox – Definisi class/relasi
│   └── tubes1_main.pl             # ENTRY POINT yang harus dijalankan
│
├── Ontologi/
│   ├── dota2_ontology.owl         # Ontologi OWL
│   ├── dota2_ontology.rdf         # Ontologi RDF
│   ├── *.json                     # Data mentah hero, ability, item
│   └── json_to_ontology.py        # Script convert JSON→OWL
│
├── Laporan Tugas Proyek I Kelompok D.pdf
└── README.md
```

## 🛠️ Requirements
Dapat menggunakan salah satu:

#### ✔ SWI-Prolog

https://www.swi-prolog.org/

#### ✔ GNU Prolog

http://www.gprolog.org/

Pastikan Prolog sudah terpasang dan dapat dijalankan dari terminal.

## ▶️ Cara Menjalankan Program
1. Masuk ke folder KBS Prolog
    ```
    cd "KBS Prolog"
    ```
2. Jalankan Prolog
    ##### SWI-Prolog
    ```
    swipl
    ```

    ##### GNU Prolog
    ```
    gprolog
    ```
3. Load file utama (tubes1_main.pl)
    ```
    ?- [tubes1_main].
    ```
Jika berhasil, Akan terlihat pesan *"Dota 2 Knowledge Base loaded successfully!"*

# 🤵🏻 Contributors
| Contributors                     	| NIM      	|
|----------------------------------	|----------	|
| Sa'ad Abdul Hakim              	| 13522092 	|
| Rayhan Fadhlan Azka         	| 13522095 	|
| Rayendra Althaf Taraka Noor         	| 13522107 	|