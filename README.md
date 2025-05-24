<h1 align="center">🤖 Instagram Automation Tools by KenXinDev</h1>

<p align="center">
  🔧 Tool multifungsi untuk automasi akun Instagram berbasis Python, cocok untuk upload, scrape, follow, unfollow, dan lainnya!
</p>


### 📦 Instalasi

1. **Clone repository:**

```bash
git clone https://github.com/KenXinDev/instagrapi-tools.git
cd instagrapi-tools
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

> 📁 Catatan: Gunakan Python 3.8 ke atas untuk kompatibilitas terbaik.

---

### 🔑 Login option
Buka 'assets/config.py' dan masukan username dan password
```python
USERNAME = "Isi username akunmu"
PASSWORD = "Isi password akunmu"
```

### ⚙️ Cara Penggunaan

```bash
python run.py
```


### 📂 Format File Input

Beberapa fitur seperti follow/unfollow memerlukan file input:

* Format file:

```
userid<=>username
12345678<=>kenxindev
```

---

### 💬 Catatan Tambahan

* Tool ini hanya berfungsi pada akun non-private dan tidak centang biru.
* Gunakan fitur dengan bijak agar tidak terkena limit dari Instagram.
* Fitur reels masih dalam proses pengembangan karena keterbatasan API dari `instagrapi`.

---

### 💡 Credits

* 🔥 Dibuat oleh: [KenXinDev](https://github.com/KenXinDev)
* ⚙️ Menggunakan library: `instagrapi`, `requests`, `rich`

---

### 📜 Lisensi

MIT License © 2025 KenXinDev


