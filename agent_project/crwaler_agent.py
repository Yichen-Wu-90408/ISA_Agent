from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time, pymysql, requests
from lxml import etree
import cfscrape

db = pymysql.connect(host='junhao.io', port=3306, user='crypto', passwd='iss2021', db='crypto',  charset='utf8mb4')
cursor = db.cursor()

def write_proxy(proxies):
    f = open("ip_proxy.txt", 'w+')
    f.close()
    for proxy in proxies:
        with open("ip_proxy.txt", 'a+') as f:
            f.write(proxy + '\n')


def get_proxy(html):
    selector = etree.HTML(html)
    proxies = []
    for each in selector.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')[1:]:
        ip = each.xpath("./td[1]/text()")[0]
        port = each.xpath("./td[2]/text()")[0]
        proxy = ip + ":" + port
        proxies.append(proxy)
    test_proxies(proxies)

def test_proxies(proxies):
    proxies = proxies
    url = "https://www.1688.com/"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        }
    normal_proxies = []
    count = 1
    for proxy in proxies:
        count += 1
        try:
            response = requests.get(url, headers=header, proxies={"http": proxy}, timeout=1)
            time = response.elapsed.total_seconds()
            if response.status_code == 200:
                normal_proxies.append(proxy)
            else:
                pass
        except Exception:
            pass
    write_proxy(normal_proxies)

def get_html(url):
    header = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    }
    response = requests.get(url,headers=header,)
    get_proxy(response.text)

def get_main_data():
	options = Options()
	prefs = {"profile.managed_default_content_settings.images": 2,'permissions.default.stylesheet':2}
	options.add_experimental_option("prefs", prefs)

	driver = webdriver.Chrome('chromedriver.exe', options=options)

	driver.get("https://icodrops.com/category/ended-ico/")

	html = driver.page_source
	soup = BeautifulSoup(html, 'html.parser')
	total_number = int(soup.find('li', id='tab-all').find('sub').get_text())

	ele = driver.find_element_by_tag_name('html')
	current_length = 0
	static = 0
	while True:
		ele.send_keys(Keys.END)
		html = driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		sss = []
		for h3 in soup.find_all('h3'):
			if 'rel=\"bookmark\"' in str(h3):
				sss.append(h3.get_text().replace('\n', ''))
		sss = list(set(sss))
		if len(sss) == current_length:
			static += 1
			if (total_number-current_length)<100 and static == 5:
				break
		else:
			current_length = len(sss)
			static = 0
		if current_length==total_number:
			break

	html = driver.page_source

	driver.quit()

	soup = BeautifulSoup(html, 'html.parser')

	# PROJECT
	project_list = []
	h3s = soup.find_all('h3')
	for h3 in h3s:
		if 'rel=\"bookmark\"' in str(h3):
			project_list.append(h3.get_text().replace('\n', ''))

	# INTEREST
	interest_list = []
	interests = soup.find_all('div', class_='interest')
	for interest in interests:
		interest_list.append(interest.get_text().replace('\n', ''))

	# CATEGORY
	category_list = []
	categorys = soup.find_all('div', class_='categ_type')
	for category in categorys:
		category_list.append(category.get_text().replace('\n', ''))

	# RECEIVED
	received_list = []
	receiveds = soup.find_all('div', id='new_column_categ_invisted')
	for received in receiveds:
		received_list.append(received.get_text().replace('\n', ''))

	# GOAL
	goal_list = []
	goals = soup.find_all('div', id='categ_desctop')
	for goal in goals:
		goal_list.append(goal.get_text().replace('\n', ''))

	# END DATE
	enddate_list = []
	enddates = soup.find_all('div', class_='date')
	for enddate in enddates:
		enddate_list.append(enddate.get_text().replace('\n', ''))

	# MARKET
	market_list = []
	markets = soup.find_all('div', id='t_tikcer')
	for market in markets:
		market_list.append(market.get_text().replace('\n', ''))

	# LINKS
	link_list = []
	links = soup.find_all('a', id='ccc')
	for link in links:
		link_list.append(link.attrs['href'])

	# print(len(project_list), len(interest_list), len(category_list), len(received_list), len(goal_list), len(enddate_list), \
	# 	len(market_list), len(link_list))


	if len(project_list) == len(interest_list) == len(category_list) == len(received_list) == len(goal_list) == len(enddate_list) == len(market_list) == len(link_list):
		print('data uploading')
		rows = []
		for i in range(len(project_list)):
			rows.append((project_list[i], interest_list[i], category_list[i], received_list[i], goal_list[i], enddate_list[i], market_list[i], link_list[i]))
		rows = list(set(rows))
		print(len(rows))
		'''
		query = "CREATE TABLE ENDEDICO(PROJECT varchar(80), INTEREST varchar(20), CATEGORY varchar(50), RECEIVED varchar(50), GOAL varchar(20), ENDDATE varchar(30), MARKET varchar(50), URL varchar(250))"
		cursor.execute(query)
		db.commit()
		cursor.execute('show tables')
		data = cursor.fetchall()
		print(data)
		'''
		cursor.execute('TRUNCATE TABLE ENDEDICO')
		db.commit()
		cursor.executemany("INSERT INTO ENDEDICO(PROJECT, INTEREST, CATEGORY, RECEIVED, GOAL, ENDDATE, MARKET, URL) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", rows)
		db.commit()
		print('upload finished')

	driver.quit()

def get_details(names_urls, ip_list):
	scraper = cfscrape.create_scraper()
	# scraper = cfscrape.create_scraper(delay = 10)
	data = []
	count = 0
	for name_url in names_urls:
		project_name = name_url[0]
		url = name_url[1]		
		print(project_name, url)
		resp = scraper.get(url, proxies = {'http':ip_list[count%len(ip_list)]})	
		while str(resp.status_code) != '200':
			count += 1
			resp = scraper.get(url, proxies = {'http':ip_list[count%len(ip_list)]})	
		html = resp.content
		soup = BeautifulSoup(html, 'html.parser')
		block_list = soup.find_all('div', class_='white-desk ico-desk')
		logo = ''
		description = ''
		fund_goal = ''
		main_entries = ''
		social_links = ''
		our_rating = ''
		token_sale_details = ''
		market_return = ''
		short_review = ''
		additional_links = ''
		for block in block_list:
			if len(block.find_all('h3')) > 0:
				# LOGO
				logo = block.find('div', class_='ico-icon').find('img').attrs['src']
				# DESCRIPTION
				description = block.find('div', class_='ico-description').get_text().strip()
				'''
				# TOKEN SALE
				token_sale = block.find('div', class_='token-sale').get_text().strip().replace('\n', '')
				'''
				# FUND GOAL
				fund_goal = block.find('div', class_='fund-goal').get_text().strip().replace('\n', '')

				for inner_link in block.find_all('a'):
					if inner_link.get_text() != '':
						# WEBSITE, WHITEPAPER (AND OTHERS)
						main_entries += inner_link.get_text()+'@'+inner_link.attrs['href']+'\n'
					else:
						# SOCIAL LINKS
						try:
							social_links += inner_link.attrs['href']+'\n'
						except Exception as e:
							pass					
				main_entries = main_entries.strip()
				social_links = social_links.strip()
			else:
				block_title = block.find('h4').get_text().upper()
				if 'RATING' in block_title:
					# OUR RATING
					for inner_block in block.find_all('div', class_='rating-item'):
						our_rating += inner_block.get_text().strip().replace('\n', ': ')+'\n'
					for inner_block in block.find_all('div', class_='rating-result'):
						our_rating += inner_block.get_text().strip().replace('\n', ': ')+'\n'
					our_rating = our_rating.strip()
				elif 'TOKEN' in block_title:
					token_sale_details = block_title.strip().replace('\n', '').replace(':', ': ')+'\n'
					# TOKEN SALE DETAILS
					for inner_block in block.find_all('li'):
						token_sale_details += inner_block.get_text().strip()+'\n'
					token_sale_details = token_sale_details.strip()			
				elif 'MARKET' in block_title:
					# MARKET AND RETURNS
					for detail in block.get_text().strip().replace('\n\n\n\n', '/').replace('\n', ' ').split('/')[1:]:
						market_return += detail.strip()+'\n'
					market_return = market_return.strip()
				elif 'REVIEW' in block_title:
					# SHORT REVIEW
					for inner_block in block.find_all('li'):
						short_review += inner_block.get_text().strip().replace('\n', ': ')+'\n'
					short_review = short_review.strip()	
				elif 'ADDITIONAL LINKS' in block_title:
					# ADDITIONAL LINKS
					for inner_block in block.find_all('a'):
						additional_links += inner_block.get_text().strip()+': '+inner_link.attrs['href']+'\n'
					additional_links = additional_links.strip()	
		count += 1
		data.append((project_name, logo, description, fund_goal, main_entries, social_links, our_rating, token_sale_details, market_return, short_review, additional_links))
	cursor.executemany("INSERT INTO ENDEDICO_DETAIL"+"(project, logo, description, FUND_GOAL, main_entries, social_links, our_rating, token_sale_details, market_return, short_review, additional_links) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", data)
	db.commit()

	# cursor.execute('SELECT * FROM ENDEDICO_DETAIL')
	# results = cursor.fetchall()
	# print(results)

def get_hk_ip():
	options = Options()
	prefs = {"profile.managed_default_content_settings.images": 2,'permissions.default.stylesheet':2}
	options.add_experimental_option("prefs", prefs)
	driver = webdriver.Chrome('chromedriver.exe', options=options)
	driver.get("http://free-proxy.cz/zh/proxylist/country/HK/all/ping/all")
	html = driver.page_source
	soup = BeautifulSoup(html, 'html.parser')
	for tr in soup.find_all('tr'):
		try:
			if 'HTTP' in tr.find_all('td')[2].get_text().upper():
				ip_list.append(tr.find_all('td')[0].get_text().strip())			
		except Exception as e:
			continue
	driver.get("http://free-proxy.cz/zh/proxylist/country/HK/all/ping/all/2")
	html = driver.page_source
	soup = BeautifulSoup(html, 'html.parser')
	for tr in soup.find_all('tr'):
		try:
			if 'HTTP' in tr.find_all('td')[2].get_text().upper():
				ip_list.append(tr.find_all('td')[0].get_text().strip())			
		except Exception as e:
			continue
	driver.quit()

if __name__ == "__main__":
	get_main_data()

	base_url = "https://www.kuaidaili.com/free/inha/%s/"
	for i in range(1, 6):
	    url = base_url % i
	    get_html(url)
	ip_list = []
	for line in open('ip_proxy.txt'):
		ip_list.append(line.replace('\n', ''))

	project_url_list = []
	cursor.execute('SELECT * FROM ENDEDICO')
	projects = cursor.fetchall()
	for project in projects:
		project_url_list.append([project[0], project[-1]])

	cursor.execute('TRUNCATE TABLE ENDEDICO_DETAIL')
	db.commit()

	get_details(project_url_list, ip_list)
