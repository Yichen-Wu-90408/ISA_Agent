import xlwt, pymysql

def write_summary():
	db = pymysql.connect(host='junhao.io', port=3306, user='crypto', passwd='iss2021', db='crypto',  charset='utf8mb4')
	
	cursor = db.cursor()

	xl = xlwt.Workbook(encoding='utf-8')

	sheet = xl.add_sheet('sheet1', cell_overwrite_ok=False)

	style = xlwt.XFStyle()

	font = xlwt.Font()

	font.name = 'Times New Roman'

	font.bold = True

	font.underline = False

	font.italic = False

	style.font = font

	cursor.execute('SELECT * FROM ENDEDICO')

	data = cursor.fetchall()

	header = ['PROJECT', 'INTEREST', 'CATEGORY', 'RECEIVED', 'GOAL', 'ENDDATE', 'MARKET', 'URL']

	for i in range(len(header)):

		sheet.write(0, i, header[i], style)

	font.bold = False

	style.font = font

	for i in range(len(data)):

		for j in range(len(data[i])):

			sheet.write(i+1, j, data[i][j], style)

	xl.save('PROJECT SUMMARY.xls')

	cursor.close()
	
	db.close()

	return True

def write_details():
	db = pymysql.connect(host='junhao.io', port=3306, user='crypto', passwd='iss2021', db='crypto',  charset='utf8mb4')
	
	cursor = db.cursor()

	xl = xlwt.Workbook(encoding='utf-8')

	sheet = xl.add_sheet('sheet1', cell_overwrite_ok=False)

	style = xlwt.XFStyle()

	font = xlwt.Font()

	font.name = 'Times New Roman'

	font.bold = True

	font.underline = False

	font.italic = False

	style.font = font

	cursor.execute('SELECT * FROM ENDEDICO_DETAIL')

	data = cursor.fetchall()

	header = ['project', 'logo', 'description', 'FUND_GOAL', 'main_entries', 'social_links', 'our_rating', 'token_sale_details', 'market_return', 'short_review', 'additional_links']

	for i in range(len(header)):

		sheet.write(0, i, header[i], style)

	font.bold = False

	style.font = font

	for i in range(len(data)):

		for j in range(len(data[i])):

			sheet.write(i+1, j, data[i][j], style)

	xl.save('PROJECT DETAILS.xls')

	cursor.close()

	db.close()

	return True