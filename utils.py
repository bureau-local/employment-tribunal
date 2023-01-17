import time

import requests

def requests_get_with_retries(url):
	timeout = 2
	error_msg = "Couldn't connect to gov.uk, waiting {}s and trying again..."
	while True:
		try:
			r =  requests.get(url)
			return r
		except:
			print(error_msg.format(timeout))
			time.sleep(timeout)
			timeout *= 2
