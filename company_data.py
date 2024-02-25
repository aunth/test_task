from excel_handler import DataHeaders
from data_parser import make_url
from singleton import UsedUrlsSingleton
from data_parser import normalize_phone_number


class CompanyData:
	def __init__(self, name="", location="", website="", phone="", social_networks=None, email=None):
		self.NAME = name
		self.LOCATION = location
		self.WEBSITE = website
		self.PHONE = [phone] if phone else []
		self.SOCIAL_NETWORKS = social_networks if social_networks is not None else {}
		self.EMAIL = [email] if email is not None else []

	def set_social_networks(self, social_networks):
		if not social_networks:
			self.SOCIAL_NETWORKS = {}
			return
		for social_network, link in social_networks.items():
			if social_network not in self.SOCIAL_NETWORKS:
				self.SOCIAL_NETWORKS[social_network] = link

	def make_for_excel(self):
		if self.PHONE:
			if type(self.PHONE) == list:
				result = ""
				for phone in self.PHONE:
					if not phone:
						continue
					else:
						result += f"{phone},"
				self.PHONE = result[:-1]
		else:
			self.PHONE = ""
		
		if self.SOCIAL_NETWORKS:
			result = ""
			if type(self.SOCIAL_NETWORKS) == dict:
				for social_network, link in self.SOCIAL_NETWORKS.items():
					result += f"{social_network}: {link}, "

				self.SOCIAL_NETWORKS = result[:-2]
		else:
			self.SOCIAL_NETWORKS = ""

		if self.EMAIL:
			result = ""
			if type(self.EMAIL) == list:
				result = ""
				for email in self.EMAIL:
					if not email:
						continue
					else:
						result += f"{email},"
				self.EMAIL = result[:-1]
		
		else:
			self.EMAIL = ""


	def set_basic_info(self, data):
		used_urls = UsedUrlsSingleton()
		for header, some_value in data:
			if header == DataHeaders.NAME:
				self.NAME = some_value
			elif header == DataHeaders.LOCATION:
				self.LOCATION = some_value
			elif header == DataHeaders.WEBSITE:
				if "," in some_value:
					url = [url for url in some_value.split(", ") if not used_urls.if_here(url)]
					some_value = ", ".join(list(set(url)))
				self.WEBSITE = make_url(some_value)[0]
			elif header == DataHeaders.PHONE:
				self.PHONE.append(normalize_phone_number(some_value))

	def add_email(self, email):
		if email not in self.EMAIL:
			self.EMAIL.append(email)


	def add_phone(self, data):
		self.PHONE.append(data)