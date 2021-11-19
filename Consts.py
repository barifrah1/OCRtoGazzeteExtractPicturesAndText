EXCEL_FILE = r'OG in progress.xlsx'
SHEET_NAME = 'Sheet1'
PAPERS_FOLDER = 'papers'
path_wkthmltoimage = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'
config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)
options={'format':'png','width':'250'}