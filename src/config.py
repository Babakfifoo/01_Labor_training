STATFI_API_URL: str = "https://pxdata.stat.fi:443/PxWeb/api/v1/en/StatFin/"

STARTUP_QUERY = {
	"query": [
		{
			"code": "Alue",
			"selection": {
				"filter": "item",
				"values": [
					"SSS"
				]
			}
		},
		{
			"code": "Sukupuoli",
			"selection": {
				"filter": "item",
				"values": [
					"SSS"
				]
			}
		},
		{
			"code": "Ikäryhmitys",
			"selection": {
				"filter": "item",
				"values": [
					"SSS"
				]
			}
		},
		{
			"code": "Työllistämisen laji",
			"selection": {
				"filter": "item",
				"values": [
					"61",
					"62"
				]
			}
		},
		{
			"code": "Tiedot",
			"selection": {
				"filter": "item",
				"values": [
					"TYOLLISTETTYLOP"
				]
			}
		}
	],
	"response": {
		"format": "json-stat2"
	}
}