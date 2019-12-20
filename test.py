from utils.csvFinder import csvFinder

CSV = csvFinder(csvPath="./CSVs/รายการบ้านสองชั้น.csv")
res = CSV.find_row(val="ครอบสันโค้ง" , limit=5)
print(res)