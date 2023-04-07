import time

import fingerprints
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

# Generate fingerprints plus handling of edge cases 
# with "&" vs "and" / and spelling mistakes of limited
# @params input_string: string
def get_fingerprint_plus(input_string):
    if input_string is not None:
        input_string = input_string.replace(" AND ", " & ")
        input_string = input_string.replace(" LIMITD", " LIMITED")
    return fingerprints.generate(input_string)
