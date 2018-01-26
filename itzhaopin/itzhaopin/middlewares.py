import random
import base64
from settings import PROXIES

class RandomUserAgent(object):
	"""Randomly routate user agents based on a list of predefined ones"""
	
	def __init__(self, agents):
		self.agents = agents
	
	@classmethod
	def from_crawler(cls, crawler):
		return cls(crawler.settings.getlist('USER_AGENTS'))
	
	def process_request(self, request, spider):
		request.headers.setdefault("User-Agent", random.choice(self.agents))
	
class ProxyMiddleware(object):
	def process_request(self, request, spider):
		proxy = random.choice(PROXIES)
		request.meta['proxy'] = "http://%s"%proxy['ip_port']
		if proxy['user_pass'] is not None:
			encode_user_pass = base64.encodestring(proxy['user_pass'])
			request.headers['Proxy-Authorization'] = 'Basic' + encode_user_pass
