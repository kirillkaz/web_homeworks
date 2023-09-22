import pandas as pd

class Printer:
    def column_print(data: list):
        for i in data:
            print(i)
    
    def row_print(data: list):
        print(data)

    def pd_print(data: pd.DataFrame):
        print(data)