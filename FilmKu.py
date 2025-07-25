import streamlit as st
from streamlit_option_menu import option_menu

class Film:
    def __init__(self, judul, genre, tahun, rating):
        self.judul = judul
        self.genre = genre
        self.tahun = tahun
        self.rating = rating

    def tampilkan(self):
        return f"{self.judul}\nGenre: {self.genre}\nTahun: {self.tahun}\nRating: {self.rating}/10"

if 'film_list' not in st.session_state:
    st.session_state.film_list = []

def tambah_film():
    st.subheader("🎬 Tambah Film Baru")
    judul = st.text_input("Judul Film")
    genre = st.text_input("Genre")
    tahun = st.number_input("Tahun Produksi", min_value=1900, max_value=2100, step=1)
    rating = st.slider("Rating", 1, 10)

    if st.button("Tambah Film"):
        if judul and genre:
            film = Film(judul, genre, tahun, rating)
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
    st.set_page_config(page_title="Aplikasi Film", page_icon="🎞️", layout="centered")
    st.title("🎞️ FilmKu")

    with st.sidebar:
        pilihan = option_menu(
            menu_title="Navigasi",
            options=[ "Panduan","Lihat Film", "Tambah Film", "Edit Film", "Hapus Film"],
            icons=["tv", "plus-circle", "pencil-square", "trash", "book"],
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


if __name__ == "__main__":
    main()
