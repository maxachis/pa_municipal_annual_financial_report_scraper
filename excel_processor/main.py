"""
This page contains both the ExcelProcessor class
and the main function for processing excel files

"""

from excel_processor.core import ExcelProcessor

if __name__ == "__main__":
    processor = ExcelProcessor()
    # processor.process_downloaded_reports()
    processor.process_joined_pop_class_urban_rural()