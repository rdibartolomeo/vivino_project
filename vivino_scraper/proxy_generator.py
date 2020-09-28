import requests
import numpy as np
from bs4 import BeautifulSoup


class EliteProxy():

	"""
	A class to generate a random elite proxy from: https://www.us-proxy.org

	Attributes
	----------
	__connection_attempts : int
		Number of attempts to connect to the current list of proxies
	__proxy_list : list
		List of elite proxies scraped from https://www.us-proxy.org
	__len_proxy_list : int
		The length of __proxy_list

	Methods
	-------
	get_elite_proxies(self):
		Scrapes https://www.us-proxy.org and returns a list of proxies with
		the type 'elite proxy'. Returns a list of formatted elite proxies.
	get_proxy(self):
		Returns a random proxy from __proxy_list.
	"""


	def __init__(self):
		self.__connection_attempts = 0
		self.__proxy_list = self.get_elite_proxies()
		self.__len_proxy_list = len(self.__proxy_list)


	def get_elite_proxies(self):

		try:
			response = requests.get('https://www.us-proxy.org', timeout=20)
		except:
			print('Failed to connect to: https://www.us-proxy.org')

		# Parse the request reponse
		soup = BeautifulSoup(response.text, 'html.parser')

		# Locate the proxies table in the parsed response
		proxy_table = soup.find('table',class_="table table-striped table-bordered")
		# Find all table rows
		proxy_table_rows = proxy_table.find_all('tr')

		proxy_data = []

		for table_row in proxy_table_rows:

			# Parse table_row
			table_data = table_row.find_all('td')
			row = [item.text for item in table_data]

			try:
				# if the proxy is an 'elite proxy'
				if row[4] == 'elite proxy':
					proxy_address = row[0]
					proxy_port = row[1]
					#append formatted proxy IP address and port
					proxy_data.append('{}:{}'.format(proxy_address,proxy_port))
			except:
				pass

		return proxy_data


	def get_proxy(self):

		# If under 200 attempts have been made on the same proxy list
		if self.__connection_attempts < 200:
			# increment connection attempts by 1
			self.__connection_attempts += 1
			rand_index = int(np.random.random() * self.__len_proxy_list)
			#return random formatted elity proxy
			return self.__proxy_list[rand_index]

		else:
			# reset connection attempts
			self.__count = 0
			# Scrape and update __proxy_list
			self.__proxy_list = self.get_elite_proxies()
			# recursive call to get_proxy()
			self.get_proxy()
