import json
STATFI_API_URL: str = "https://pxdata.stat.fi:443/PxWeb/api/v1/en/StatFin/"

with open('../queries/startup_total.json') as f:
	STARTUP_QUERY = json.loads(f.read())
