import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
cerds = ServiceAccountCredentials.from_json_keyfile_name("cerds.json", scope)
client = gspread.authorize(cerds)
sheet = client.open("carparking").worksheet('sheet1') # เป็นการเปิดไปยังหน้าชีตนั้นๆ
cell=sheet.cell(4,2).value
pprint(cell)
sheet.update_cell(4,2,"แก้ไข")
cell=sheet.cell(4,2).value
pprint(cell)