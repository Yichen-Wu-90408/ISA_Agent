import os, pymysql
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time

def pdf_generation():

	db = pymysql.connect(host='junhao.io', port=3306, user='crypto', passwd='iss2021', db='crypto',  charset='utf8mb4')
	cursor = db.cursor()

	header = ['project', 'logo', 'description', 'FUND_GOAL', 'main_entries', 'social_links', 'our_rating', 'token_sale_details', 'market_return', 'short_review', 'additional_links', 'ENDDATE']

	cursor.execute('SELECT ENDEDICO_DETAIL.project, ENDEDICO_DETAIL.logo, ENDEDICO_DETAIL.description, ENDEDICO_DETAIL.FUND_GOAL, ENDEDICO_DETAIL.main_entries, ENDEDICO_DETAIL.social_links, ENDEDICO_DETAIL.our_rating, ENDEDICO_DETAIL.token_sale_details, ENDEDICO_DETAIL.market_return, ENDEDICO_DETAIL.short_review, ENDEDICO_DETAIL.additional_links, ENDEDICO.ENDDATE FROM ENDEDICO_DETAIL INNER JOIN ENDEDICO ON ENDEDICO_DETAIL.project = ENDEDICO.PROJECT')
	fetch_data = cursor.fetchall()
	data = []
	for row in fetch_data:
		data.append(list(row))

	df = pd.DataFrame(data, columns=header)
	df = df[df['ENDDATE'].str.contains('2021')]

	cursor.execute('SELECT PROJECT, ENDDATE FROM ENDEDICO')
	summary_data = cursor.fetchall()
	main_dic = {}
	for d in summary_data:
		main_dic[d[0]] = d[1].replace('Ended:', '').replace('\t', '').strip()

	cursor.execute('SELECT project, FUND_GOAL FROM ENDEDICO_DETAIL')
	summary_data = cursor.fetchall()
	detail_dic = {}
	for d in summary_data:
		if 'OF' in d[1]:
			dd = d[1].split('OF')
			detail_dic[d[0]] = int(dd[0].strip().replace('$', '').replace(',', ''))

	def whether_achieve_fund_goal_function():
		plt.clf()
		fund_goal_achieve = len(df[df['FUND_GOAL'].str.contains('(100%)')])
		fund_goal_not_set = len(df[df['FUND_GOAL'].str.contains('NOT SET')])
		fund_goal_not_achieve = len(df) - fund_goal_achieve - fund_goal_not_set
		attr = ["achieve fund goal", "do not achieve fund goal", "not set goal"]
		v1 = [fund_goal_achieve, fund_goal_not_achieve, fund_goal_not_set]
		plt.pie(x=v1, labels=attr, autopct='%.2f%%')
		plt.savefig("tex/whether_achieve_fund_goal.png", bbox_inches='tight')

		return v1

	def funding_range_function():
		plt.clf()
		ss = list(df['FUND_GOAL'])
		count = []
		for s in ss:
			if 'OF' in s:
				data = s.split('OF')
				count.append(int(data[0].strip().replace('$', '').replace(',', '')))
		d1 = d2 = d3 = d4 = d5 = 0
		for c in count:
			if c < 1000000:
				d1 += 1
			elif c <= 3000000:
				d2 += 1
			elif c <= 5000000:
				d3 += 1
			elif c <= 10000000:
				d4 += 1
			else:
				d5 += 1
		attr = ('below 1m $', '1m - 3m $', '3m - 5m $', '5m - 10m $', 'over 10m $')
		v1 = [d1, d2, d3, d4, d5]
		for a,b in zip(attr,v1):  
	 		plt.text(a, b, '%.0f' % b, ha='center', va='bottom') 
		plt.bar(attr, v1)
		plt.savefig("tex/funding_range.png", bbox_inches='tight')
		return v1

	def usage_function():
		plt.clf()
		a = len(df[df['short_review'].str.contains('Role of Token: Security')])
		b = len(df[df['short_review'].str.contains('Role of Token: Utility')])
		c = len(df[df['short_review'].str.contains('Role of Token: Governance')])

		attr = ["Security ("+str(a)+")", "Utility ("+str(b)+")", "Governance ("+str(c)+")"]
		v1 = [a, b, c]
		plt.pie(x=v1, labels=attr, autopct='%.2f%%')
		plt.savefig("tex/usage.png", bbox_inches='tight')

	def usage_funding_function():
		plt.clf()
		a = df[df['short_review'].str.contains('Role of Token: Security')]
		b = df[df['short_review'].str.contains('Role of Token: Utility')]
		c = df[df['short_review'].str.contains('Role of Token: Governance')]

		ss = list(a['FUND_GOAL'])
		count = []
		for s in ss:
			if 'OF' in s:
				data = s.split('OF')
				count.append(int(data[0].strip().replace('$', '').replace(',', '')))
		a = sum(count)

		ss = list(b['FUND_GOAL'])
		count = []
		for s in ss:
			if 'OF' in s:
				data = s.split('OF')
				count.append(int(data[0].strip().replace('$', '').replace(',', '')))
		b = sum(count)

		ss = list(c['FUND_GOAL'])
		count = []
		for s in ss:
			if 'OF' in s:
				data = s.split('OF')
				count.append(int(data[0].strip().replace('$', '').replace(',', '')))
		c = sum(count)

		attr = []
		v1 = []
		result_dict = {}
		if a > 0:
			a = float(str(a)[:len(str(a))-6] + '.' + str(a)[len(str(a))-6:len(str(a))-4])
			attr.append("Security ("+str(a)+"m $)")
			v1.append(a)
			result_dict['Security'] = a
		if b > 0:
			b = float(str(b)[:len(str(b))-6] + '.' + str(b)[len(str(b))-6:len(str(b))-4])
			attr.append("Utility ("+str(b)+"m $)")
			v1.append(b)
			result_dict['Utility'] = b
		if c > 0:
			c = float(str(c)[:len(str(c))-6] + '.' + str(c)[len(str(c))-6:len(str(c))-4])
			attr.append("Governance ("+str(c)+"m $)")
			v1.append(c)
			result_dict['Governance'] = c
		plt.pie(x=v1, labels=attr, autopct='%.2f%%')
		plt.savefig("tex/usage_funding.png", bbox_inches='tight')

		return result_dict

	def usage_function():
		plt.clf()
		a = len(df[df['short_review'].str.contains('Role of Token: Security')])
		b = len(df[df['short_review'].str.contains('Role of Token: Utility')])
		c = len(df[df['short_review'].str.contains('Role of Token: Governance')])

		attr = ["Security ("+str(a)+")", "Utility ("+str(b)+")", "Governance ("+str(c)+")"]
		v1 = [a, b, c]
		plt.pie(x=v1, labels=attr, autopct='%.2f%%')
		plt.savefig("tex/usage.png", bbox_inches='tight')

	def whether_kyc_function():
		plt.clf()
		ss = list(df['token_sale_details'])
		a = 0
		for s in ss:
			if '(KYC): Yes' in s:
				a += 1
		b = len(df) - a

		attr = ["KYC: YES", "KYC: NO"]
		v1 = [a, b]
		plt.pie(x=v1, labels=attr, autopct='%.2f%%')
		plt.savefig("tex/whether_kyc.png", bbox_inches='tight')

		return v1

	def time_funding_function():
		plt.clf()
		header = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
		v1 = []
		for month in header:
			ss = 0
			for key in main_dic.keys():
				if month in main_dic[key] and '2021' in main_dic[key] and key in detail_dic.keys():
					ss += detail_dic[key]
			v1.append(ss)

		for i in range(len(v1)):
			if v1[i] != 0:
				v1[i] = float(str(v1[i])[:len(str(v1[i]))-6] + '.' + str(v1[i])[len(str(v1[i]))-6:len(str(v1[i]))-4])
		plt.yticks([])
		attr = header
		for a,b in zip(attr,v1):  
	 		plt.text(a, b, '%.2f' % b, ha='center', va='bottom') 
		plt.bar(attr, v1)
		plt.savefig("tex/time_funding.png", bbox_inches='tight')

		return_dict = {}
		for i in range(len(header)):
			return_dict[header[i]] = v1[i]

		return return_dict

	cursor.close()
	db.close()

	results = whether_achieve_fund_goal_function()
	sec1_list = []
	sec1_list.append(str(sum(results)))
	for result in results:
		sec1_list.append(str(result))
		sec1_list.append(format(result/sum(results), '.2%').replace('%', '\%'))

	results = funding_range_function()
	sec2_list = []
	for result in results:
		sec2_list.append(str(result))
		sec2_list.append(format(result/sum(results), '.2%').replace('%', '\%'))

	result_dict = time_funding_function()
	sec3_list = []
	count = 0
	for key in result_dict.keys():
		if result_dict[key] > 0:
			count += 1
	sec3_list.append(count)
	results = sorted(result_dict.items(), key = lambda x:x[1], reverse = True)
	sec3_list.append(results[0][0])
	sec3_list.append(results[-1][0])
	sec3_list.append(results[0][1] - results[-1][1])
	sec3_list.append(results[0][0])
	sec3_list.append(results[0][1])
	sec3_list.append(results[1][0])
	sec3_list.append(results[1][1])
	sec3_list.append(results[2][0])
	sec3_list.append(results[2][1])

	result_dict = usage_funding_function()
	sec4_list = []
	results = sorted(result_dict.items(), key = lambda x:x[1], reverse = True)
	for result in results:
		sec4_list.append(result[0])
		sec4_list.append(str(result[1])+'m \$')
		sec4_list.append(format(result[1]/sum(list(result_dict.values())), '.2%').replace('%', '\%'))

	results = whether_kyc_function()
	sec5_list = []
	sec5_list.append(results[0])
	sec5_list.append(format(results[0]/sum(results), '.2%').replace('%', '\%'))
	sec5_list.append(results[1])
	sec5_list.append(format(results[1]/sum(results), '.2%').replace('%', '\%'))

	def generate_tex():
		f = open('tex/Daily_Report_template.tex', 'r', encoding = 'utf-8')
		tex_content = f.read()
		f.close()

		t_info = datetime.fromtimestamp(time.time()).strftime('%Y%m%d')
		weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
		t_info = t_info + ' ' + weekdays[datetime.now().isoweekday()-1]

		tex_content = tex_content.replace('$v_time$', t_info)

		for i in range(len(sec1_list)):
			tex_content = tex_content.replace('$v1_'+str(i+1)+'$', str(sec1_list[i]))
		for i in range(len(sec2_list)):
			tex_content = tex_content.replace('$v2_'+str(i+1)+'$', str(sec2_list[i]))
		for i in range(len(sec3_list)):
			tex_content = tex_content.replace('$v3_'+str(i+1)+'$', str(sec3_list[i]))
		for i in range(len(sec4_list)):
			tex_content = tex_content.replace('$v4_'+str(i+1)+'$', str(sec4_list[i]))
		for i in range(len(sec5_list)):
			tex_content = tex_content.replace('$v5_'+str(i+1)+'$', str(sec5_list[i]))

		f = open('tex/Daily_Report.tex', 'w+', encoding = 'utf-8')
		f.write(tex_content)
		f.close()

	generate_tex()

	os.chdir('tex/')
	os.system('C:/texlive/2020/bin/win32/bmeps -c funding_range.png funding_range.eps')
	os.system('C:/texlive/2020/bin/win32/bmeps -c time_funding.png time_funding.eps')
	os.system('C:/texlive/2020/bin/win32/bmeps -c usage_funding.png usage_funding.eps')
	os.system('C:/texlive/2020/bin/win32/bmeps -c whether_achieve_fund_goal.png whether_achieve_fund_goal.eps')
	os.system('C:/texlive/2020/bin/win32/bmeps -c whether_kyc.png whether_kyc.eps')
	os.system('C:/texlive/2020/bin/win32/xelatex Daily_Report.tex')

	return True