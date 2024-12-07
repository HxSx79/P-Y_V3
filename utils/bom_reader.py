import pandas as pd
import os

class BOMReader:
    def __init__(self, bom_file="BOM.xlsx"):
        self.bom_file = bom_file
        self._load_bom()

    def _load_bom(self):
        if not os.path.exists(self.bom_file):
            raise FileNotFoundError(f"BOM file not found: {self.bom_file}")
        self.bom_data = pd.read_excel(self.bom_file)

    def get_part_info(self, class_name):
        try:
            part_info = self.bom_data[self.bom_data['Class_Name'] == class_name].iloc[0]
            return {
                'customer': part_info['Customer'],
                'program': part_info['Program'],
                'part_number': part_info['Part_Number'],
                'description': part_info['Description']
            }
        except (IndexError, KeyError):
            return {
                'customer': 'Unknown',
                'program': 'Unknown',
                'part_number': 'Unknown',
                'description': 'Unknown'
            }