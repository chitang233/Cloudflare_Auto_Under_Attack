import requests
import logging
import time
import os

API_TOKEN = ""
ZONE_ID = ""
LOAD_LIMIT = 5
logging.basicConfig(level=logging.INFO)


def get_current_level():
	try:
		return requests.get(
			f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/settings/security_level",
			headers={
				"Authorization": f"Bearer {API_TOKEN}",
				"Content-Type": "application/json"
			},
		).json()['result']['value']
	except Exception as e:
		logging.error(e)


def change_security_level(level):
	try:
		requests.patch(
			f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/settings/security_level",
			headers={
				"Authorization": f"Bearer {API_TOKEN}",
				"Content-Type": "application/json"
			},
			data="{\"value\": \"" + level + "\"}"
		)
	except Exception as e:
		logging.error(e)


def main():
	origin_level = get_current_level()
	logging.info(f"Current security level: {origin_level}")
	while True:
		time.sleep(1)
		current_level = get_current_level()
		current_load = os.getloadavg()[0]
		if current_load > LOAD_LIMIT:
			logging.debug(f"Load average is {current_load}, changing security level to under_attack")
			if current_level != "under_attack":
				change_security_level("under_attack")
				logging.info("Security level changed to under_attack")
			else:
				logging.info("Security level is already under_attack, keeping it that way")
		else:
			logging.debug(f"Load average is {current_load}, changing security level to {origin_level}")
			if current_level != origin_level:
				change_security_level(origin_level)
				logging.info(f"Security level changed to {origin_level}")
			else:
				logging.info(f"Security level is already {origin_level}, keeping it that way")


if __name__ == "__main__":
	main()
