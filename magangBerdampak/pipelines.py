# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import openpyxl


class MagangberdampakPipeline:
    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.append([
            "title", "field", "placement_location", "company_location",
            "description_company", "description_job", "assigments_details",
            "criteria", "learning_outcomes"
        ])
        
    def process_item(self, item, spider):
        self.ws.append([
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
        return item
    
    def close_spider(self, spider):
        self.wb.save("data_magang_berdampak.xlsx")
