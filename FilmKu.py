import streamlit as st
from streamlit_option_menu import option_menu
from supabase import create_client, Client
from collections import defaultdict

SUPABASE_URL = "https://dzfglcoctmwiefoqnuge.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR6ZmdsY29jdG13aWVmb3FudWdlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM0MzE5MTIsImV4cCI6MjA2OTAwNzkxMn0.NL2kqtyrnTuy3U8sH2lVKYIBu3eTl1gElOeaW0KhoDY"  # Ganti ini dengan anon key dari Supabase API
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class Film:
    def __init__(self, judul, genre, tahun, rating,username,ulasan,koleksi):
        self.judul = judul
        self.genre = genre
        self.tahun = tahun
        self.rating = rating
        self.username = username
        self.ulasan = ulasan
        self.koleksi = koleksi

    def tampilkan(self):
        return f"{self.judul}\nGenre: {self.genre}\nTahun: {self.tahun}\nRating: {self.rating}/10\nUlasan: {self.ulasan}"
    
    def to_dict(self):
        return {
            "movie_title": self.judul,
            "movie_genre": self.genre,
            "movie_productionYear": self.tahun,
            "movie_rating": self.rating,
            "user_name": self.username,
            "movie_review": self.ulasan,
            "movie_collection":self.koleksi
        }

if 'film_list' not in st.session_state:
    st.session_state.film_list = []

def tambah_film():
    st.subheader("🎬 Tambah Film Baru")
    judul = st.text_input("Judul Film")
    genre = st.text_input("Genre")
    tahun = st.number_input("Tahun Produksi", min_value=1900, max_value=2100, step=1)
    rating = st.slider("Rating", 1, 10)
    ulasan = st.text_area("Tulis Ulasan (opsional)")
    koleksi = st.session_state.judul_koleksi

    if st.button("Tambah Film"):
        if judul and genre:
            username = st.session_state.username
            film = Film(judul, genre, tahun, rating, username,ulasan,koleksi)
            st.session_state.film_list.append(film)
            st.success(f"Film '{judul}' berhasil ditambahkan!")
        else:
            st.warning("Judul dan genre tidak boleh kosong.")

def lihat_film():
    st.subheader("📺 Daftar Film")
    if not st.session_state.film_list:
        st.info("Belum ada film.")
    else:
        for idx, film in enumerate(st.session_state.film_list):
            st.markdown(f"**{idx+1}. {film.judul}**")
            st.text(film.tampilkan())
            st.markdown("---")
        if st.button("Cetak ke TXT"):
            cetak_ke_txt()

def edit_film():
    st.subheader("✏️ Edit Film")
    if not st.session_state.film_list:
        st.info("Belum ada film untuk diedit.")
        return

    pilihan = st.selectbox("Pilih film yang ingin diedit:", [f"{idx+1}. {f.judul}" for idx, f in enumerate(st.session_state.film_list)])
    idx = int(pilihan.split('.')[0]) - 1
    film = st.session_state.film_list[idx]

    judul = st.text_input("Judul Baru", value=film.judul)
    genre = st.text_input("Genre Baru", value=film.genre)
    tahun = st.number_input("Tahun Baru", min_value=1900, max_value=2100, value=film.tahun)
    rating = st.slider("Rating Baru", 1, 10, value=film.rating)

    if st.button("Simpan Perubahan"):
        film.judul = judul
        film.genre = genre
        film.tahun = tahun
        film.rating = rating
        st.success("Data film berhasil diperbarui!")

def hapus_film():
    st.subheader("🗑️ Hapus Film")
    if not st.session_state.film_list:
        st.info("Tidak ada film untuk dihapus.")
        return

    pilihan = st.selectbox("Pilih film yang ingin dihapus:", [f"{idx+1}. {f.judul}" for idx, f in enumerate(st.session_state.film_list)])
    idx = int(pilihan.split('.')[0]) - 1
    film = st.session_state.film_list[idx]

    if st.button(f"Hapus film"):
        st.session_state.film_list.pop(idx)
        st.success(f"Film '{film.judul}' berhasil dihapus.")

def panduan_pengguna():
    st.subheader("📖 Panduan Pengguna")
    st.markdown("""
    **Selamat datang di Aplikasi FilmKu!** 🎬

    Berikut adalah panduan singkat untuk menggunakan aplikasi ini:

    - **Tambah Film**: Gunakan menu "Tambah Film" untuk menambahkan film baru.
    - **Lihat Film**: Lihat semua film yang sudah ditambahkan. Anda juga bisa mencetak daftar ke file `.txt`.
    - **Edit Film**: Ubah informasi film yang sudah ada.
    - **Hapus Film**: Hapus film dari daftar.
    - **Cetak Film**: Di halaman "Lihat Film", klik tombol `Cetak ke TXT` untuk menyimpan daftar film.

    Semua data tersimpan selama sesi berlangsung (selama tab browser tidak ditutup atau di-refresh).
    """)

def upload_ke_galeri():
    st.subheader("☁️ Unggah Film Anda ke Galeri Publik")
    if not st.session_state.get("film_list"):
        st.warning("Tidak ada film yang tersimpan. Silakan tambahkan film terlebih dahulu.")
        return

    if st.button("Unggah ke Galeri"):
        data_final = []

        for film in st.session_state.film_list:
            if isinstance(film, dict):
                film_dict = film.copy()
            else:
                film_dict = film.to_dict()

            data_final.append(film_dict)

        try:
            supabase.table("FilmKu_database").insert(data_final).execute()
            st.success("Berhasil mengunggah semua film ke galeri publik!")
            st.session_state.film_list.clear()
        except Exception as e:
            st.error(f"Gagal mengunggah: {e}")

def tampilkan_galeri():
    st.subheader("🌐 Galeri Film Publik")

    try:
        response = supabase.table("FilmKu_database").select("*").execute()
        data = response.data

        if not data:
            st.info("Belum ada data film di galeri.")
            return

        user_to_films = defaultdict(list)
        for film in data:
            user = film.get("user_name", "Tidak Diketahui")
            user_to_films[user].append(film)

        for user, daftar_film in user_to_films.items():
            st.markdown(f"## 👤 {user} ({len(daftar_film)} film)")
            for idx, film in enumerate(daftar_film, 1):
                if "movie_collection" in film and film["movie_collection"]:
                    st.markdown(f"📦 Koleksi: *{film['movie_collection']}*")
                st.markdown(f"**{idx}. {film['movie_title']}**")
                st.write(f"🎭 Genre: {film['movie_genre']}")
                st.write(f"📅 Tahun: {film['movie_productionYear']}")
                st.write(f"⭐ Rating: {film['movie_rating']}/10")
                if "movie_review" in film and film["movie_review"]:
                    st.write(f"✍️ Ulasan: {film['movie_review']}")
                st.markdown("---")

    except Exception as e:
        st.error(f"Gagal mengambil data dari database: {e}")

def cetak_ke_txt():
    if not st.session_state.film_list:
        st.warning("Tidak ada film untuk dicetak.")
        return

    with open("daftar_film.txt", "w", encoding="utf-8") as file:
        for idx, film in enumerate(st.session_state.film_list, 1):
            file.write(f"{idx}. {film.tampilkan()}\n\n")

    st.success("Data film berhasil disimpan ke 'daftar_film.txt'.")
    with open("daftar_film.txt", "r", encoding="utf-8") as f:
        st.download_button("📄 Download File TXT", f, file_name="daftar_film.txt")

def main():
    if 'username' not in st.session_state:
        st.session_state.username = ""

    if not st.session_state.username:
        username_input = st.text_input("Masukkan Nama Anda")
        if username_input:
            st.session_state.username = username_input
            st.rerun()
        st.warning("Silakan masukkan nama Anda terlebih dahulu.")
        st.stop()

    if 'judul_koleksi' not in st.session_state:
        st.session_state.judul_koleksi = ""

    if not st.session_state.judul_koleksi:
        judul_input = st.text_input("Masukkan Judul Koleksi Film Anda (misal: Top 5 Film Aksi)")
        if judul_input:
            st.session_state.judul_koleksi = judul_input
            st.rerun()
        st.warning("Silakan masukkan judul koleksi terlebih dahulu.")
        st.stop()

    with st.sidebar:
        pilihan = option_menu(
            menu_title="Navigasi",
            options=["Panduan", "Lihat Film", "Tambah Film", "Edit Film", "Hapus Film", "Unggah Data","Galeri Publik"],
            icons=["tv", "list", "plus-circle", "pencil-square", "trash","cloud-upload","globe"],
            menu_icon="film",
            default_index=0
        )

    if pilihan == "Lihat Film":
        lihat_film()
    elif pilihan == "Tambah Film":
        tambah_film()
    elif pilihan == "Edit Film":
        edit_film()
    elif pilihan == "Hapus Film":
        hapus_film()
    elif pilihan == "Panduan":
        panduan_pengguna()
    elif pilihan == "Unggah Data":
        upload_ke_galeri()
    elif pilihan == "Galeri Publik":
        tampilkan_galeri()

if __name__ == "__main__":
    main()
