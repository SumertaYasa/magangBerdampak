import scrapy
from magangBerdampak.items import MagangberdampakItem
import html
import json
import pprint

# fungsi membersihkan newline
def clean(text: str) -> str:
    return " ".join(text.replace("\n", " ").split())

class MagangstartSpider(scrapy.Spider):
    name = "magangStart"
    allowed_domains = ["simbelmawa.kemdikbud.go.id"]

    start_urls = [
            "https://simbelmawa.kemdikbud.go.id/magang/lowongan/lowongan-1"
        ]
    # start_urls = [
    #     f"https://simbelmawa.kemdikbud.go.id/magang/lowongan/lowongan-{i}" for i in range(1, 305)
    # ]

    def parse(self, response):
        internship = MagangberdampakItem()

        html_data = response.css("div[data-page]::attr(data-page)").get()

        if html_data:
            try:
                # mengubah html entities menjadi karakter asli
                decoded = html.unescape(html_data)
                # mengubah string JSON menjadi objek python
                data = json.loads(decoded)
                # pprint.pprint(data) # melihat struktur data
                lowongan = data.get("props", {}).get("lowongan", {})

                # get data yang ingin diambil
                internship['title'] = lowongan.get("posisi_magang", {}).get("nama")
                internship['field'] = lowongan.get("kategori_posisi", {}).get("nama")
                internship['placement_location'] = clean(lowongan.get("lokasi_penempatan"))
                internship['company_location'] = clean(lowongan.get("mitra", {}).get("alamat"))
                internship['description_company'] = clean(lowongan.get("mitra", {}).get("deskripsi"))
                internship['description_job'] = clean(lowongan.get("deskripsi"))
                internship['assigments_details'] = " · ".join([
                    item.get("deskripsi", "").replace("\n", " ").strip()
                    for item in lowongan.get("lowongan_tanggung_jawab", [])
                ])
                internship["learning_outcomes"] = " · ".join([
                    item.get("deskripsi", "").replace("\n", " ").strip()
                    for item in lowongan.get("lowongan_capaian", [])
                ])
                internship["criteria"] = " | ".join([
                    f"{item.get('kategori', '').capitalize()}: {item.get('deskripsi', '').replace('\n', ' ').strip()}"
                    for item in lowongan.get("lowongan_kriteria", [])
                ])
            
                yield internship

            except Exception as e:
                self.logger.warning(f"gagal decode JSON: {e}")
