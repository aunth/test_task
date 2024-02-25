import requests
from bs4 import BeautifulSoup
import re
from singleton import UsedUrlsSingleton

social_media = [
	"facebook.com",
	"twitter.com",
	"linkedin.com",
	"youtube.com",
	"skype.com",
	"pinterest.com",
	"instagram.com"
]


def normalize_phone_number(phone_number):
	# Remove non-numeric characters from the phone number
	digits_only = re.sub(r'\D', '', phone_number)
	
	# Check if the phone number starts with a country code
	if len(digits_only) == 10:
		return f"({digits_only[:3]}) {digits_only[3:6]}-{digits_only[6:]}"
	elif len(digits_only) == 11:
		return f"({digits_only[1:4]}) {digits_only[4:7]}-{digits_only[7:]}"
	else:
		return None

def make_url(site):
	if not site:
		return None
	if "," in site:
		urls = site.split(", ")
		urls = [f"https://{site}" if "https" and "http" not in site else site for site in urls]
		return urls
	return [f"https://{site}" if "https" not in site and "http" not in site else site]


def get_contact_us_url(url):
	# Extract the base domain
	domain = url.split('//')[-1].split('/')[0]

	# Check if the base domain starts with 'www.'
	if domain.startswith('www.'):
		domain = domain[4:]

	# Construct the About Us page URL
	about_us_url = [f"https://{domain}/contact-us", f"https://{domain}/contact"]
	return about_us_url


def extract_data(url):
	used_urls = UsedUrlsSingleton()
	if used_urls.if_here(url):
		return None
	try:
		user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'
		headers = {'User-Agent': user_agent}
		timeout = 10

		response = requests.get(url, headers=headers, timeout=timeout)
		response.raise_for_status()

	except requests.exceptions.RequestException as e:
		print(f"Error fetching the webpage: {e}\nURL: {url}")
		if "http" not in url:
			return extract_data(url.replace("https", "http"))
		return None

	soup = BeautifulSoup(response.content, 'html.parser')
	email_addresses = []
	phone_numbers = []
	social_networks = {}

	# Extract data from the main page
	extract_data_from_page(soup, email_addresses, phone_numbers, social_networks)


	if not email_addresses:
		contact_us_urls = get_contact_us_url(url)
		if contact_us_urls:
			for contact_us_url in contact_us_urls:
				try:
					contact_us_response = requests.get(contact_us_url, headers=headers, timeout=timeout)
					contact_us_response.raise_for_status()
					contact_us_soup = BeautifulSoup(contact_us_response.content, 'html.parser')
					extract_data_from_page(contact_us_soup, email_addresses, phone_numbers, social_networks)
				except Exception as e:
					pass

	used_urls.add(url)
	return {
		"emails": list(set(email_addresses)),
		"phones": list(set(phone_numbers)),
		"social networks": social_networks
	}

def extract_data_from_page(soup, email_addresses, phone_numbers, social_networks):
	for tag in soup.find_all(['p', 'a', 'span', 'div']):
		text = tag.get_text()

		print(text)

		emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text)
		if emails:
			email_addresses.extend(emails)

		for phone in re.findall(r'(?:\+?\d{1,3}[-.\s]?)?(?:\(\d{3}\)[-.\s]?)?\d{3}[-.\s]?\d{4}\b', text):
			formatted_phone = normalize_phone_number(phone)
			if formatted_phone:
				phone_numbers.append(formatted_phone)

		href = tag.get('href')
		if href:
			if href.startswith("mailto:"):
				email_address = href[len("mailto:"):]
				email_addresses.append(email_address)
			else:
				for site in social_media:
					if site in href:
						social_networks[site] = make_url(href)