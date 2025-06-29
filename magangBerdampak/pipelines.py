# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from itemadapter import ItemAdapter
import openpyxl

class MagangberdampakPipeline:
    def __init__(self):
        # Menyimpan semua item yang berhasil di-scrape
        self.items = []
        # Header kolom untuk file Excel
        self.headers = [
            "title", "field", "placement_location", "company_location",
            "description_company", "description_job", "assigments_details",
            "criteria", "learning_outcomes"
        ]
        
    def process_item(self, item, spider):
        # Menambahkan setiap item ke list untuk diproses nanti
        self.items.append(item)
        return item
        
    def close_spider(self, spider):
        # Mengurutkan item berdasarkan field 'field' secara alfabetis
        sorted_item = sorted(self.items, key=lambda x: x.get('field', '').lower())

        # Membuat workbook dan worksheet baru untuk Excel
        wb = openpyxl.Workbook()
        ws = wb.active
        # Menambahkan header ke baris pertama
        ws.append(self.headers)
        
        # Menuliskan setiap item ke baris berikutnya di Excel
        for item in sorted_item:
            ws.append([
                item.get("title", ""),
                item.get("field", ""),
                item.get("placement_location", ""),
                item.get("company_location", ""),
                item.get("description_company", ""),
                item.get("description_job", ""),
                item.get("assigments_details", ""),
                item.get("criteria", ""),
                item.get("learning_outcomes", "")
            ])
            
        # Menyimpan file Excel dengan nama berikut
        wb.save("data_magang_berdampak.xlsx")

