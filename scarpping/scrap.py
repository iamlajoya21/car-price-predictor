import requests as r

URL = "https://auto.am/search/passenger-cars?q={%22category%22:%221%22,%22page%22:%221%22,%22sort%22:%22latest%22,%22layout%22:%22list%22,%22user%22:{%22dealer%22:%220%22,%22id%22:%22%22},%22make%22:[%22246%22],%22year%22:{%22gt%22:%221911%22,%22lt%22:%222023%22},%22usdprice%22:{%22gt%22:%220%22,%22lt%22:%22100000000%22},%22mileage%22:{%22gt%22:%2210%22,%22lt%22:%221000000%22}}"
page = r.get(URL)

print(page.text)