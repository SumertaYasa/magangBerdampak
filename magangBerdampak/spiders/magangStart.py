import scrapy
from magangBerdampak.items import MagangberdampakItem
import html
import json
# import pprint

# Fungsi untuk membersihkan karakter newline dan simbol tertentu dari teks
def clean(text: str) -> str:
    return " ".join(text.replace("\n", " ").replace("·", "-").split())

# Fungsi untuk menggabungkan field dari list of dict menjadi satu string
def get_joined_field(items, key="deskripsi", separator=" · "):
    if not items:
        return "Tidak tersedia"
    return separator.join(clean(item.get(key, "")) for item in items)

class MagangstartSpider(scrapy.Spider):
    name = "magangStart"
    allowed_domains = ["simbelmawa.kemdikbud.go.id"]
    
    # Membuat daftar URL lowongan yang akan di-scrape
    start_urls = [
        f"https://simbelmawa.kemdikbud.go.id/magang/lowongan/lowongan-{i}"
        for i in range(1, 345)
    ]

    def parse(self, response):
        # Membuat objek item untuk menyimpan hasil scraping
        internship = MagangberdampakItem()
        # Mengambil data HTML yang berisi JSON dari atribut data-page
        html_data = response.css("div[data-page]::attr(data-page)").get()

        if html_data:
            try:
                # Decode HTML entities dan parsing JSON
                decoded = html.unescape(html_data)
                data = json.loads(decoded)
                lowongan = data.get("props", {}).get("lowongan", {})

                # Mengisi field item dengan data yang sudah dibersihkan
                internship['title'] = lowongan.get("posisi_magang", {}).get("nama", "Tidak tersedia")
                internship['field'] = lowongan.get("kategori_posisi", {}).get("nama", "Tidak tersedia")
                internship['placement_location'] = clean(lowongan.get("lokasi_penempatan", "Tidak tersedia"))
                internship['company_location'] = clean(lowongan.get("mitra", {}).get("alamat", "Tidak tersedia"))
                internship['description_company'] = clean(lowongan.get("mitra", {}).get("deskripsi", "Tidak tersedia"))
                internship['description_job'] = clean(lowongan.get("deskripsi", "Tidak tersedia"))
                internship['assigments_details'] = get_joined_field(lowongan.get("lowongan_tanggung_jawab"))
                internship['learning_outcomes'] = get_joined_field(lowongan.get("lowongan_capaian"))
                internship["criteria"] = get_joined_field([
                    {
                        "deskripsi": f"{item.get('kategori', '').capitalize()}: {item.get('deskripsi', '')}"
                    }
                    for item in lowongan.get("lowongan_kriteria", [])
                ], separator=" | ")

                # Mengirim item ke pipeline
                yield internship

            except Exception as e:
                # Log jika gagal decode JSON
                self.logger.warning(f"gagal decode JSON: {e}")

