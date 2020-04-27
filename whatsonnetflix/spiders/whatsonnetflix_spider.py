from scrapy import Spider
from whatsonnetflix.items import WhatsonnetflixItem
import re

class WhatsonNetflixSpider(Spider):
	name = 'whatsonnetflix_spider'
	allowed_urls = ['https://www.whats-on-netflix.com/']
	start_urls = [f'https://www.whats-on-netflix.com/whats-new/?week={i+1}' for i in range(52)]
	def parse(self, response):
		
		date = response.xpath('//div[@class= "notification-area"]/b/text()').extract_first()
		date = re.search('(\d+/\d+/\d+) and (\d+/\d+/\d+)', date)
		date = date.group(2)

		movie_head = response.xpath('//div[@class="pad group"]/div[contains(@class, "new-title")]/@class').extract_first() # does this iterate for Movie in Movies?
		TV_or_Movie = movie_head[10:16]
		if TV_or_Movie == "standu":
			TV_or_Movie = "standup"
		Foreign_or_Domestic = movie_head[16:]
		if Foreign_or_Domestic == "p ":
			Foreign_or_Domestic = None
		if Foreign_or_Domestic == None:
			Foreign_or_Domestic = "Domestic"

		Movies = response.xpath('//div[@class="pad group"]/div[contains(@class, "new-title")]')

		for Movie in Movies:

			title = Movie.xpath('.//h5//text()').extract_first()

			Mvalues = Movie.xpath('.//div[@class="new-title-right"]/text()').extract()
			Mkeys = Movie.xpath('.//div[@class="new-title-right"]/b/text()').extract()
			dictionary = dict(zip(Mkeys, Mvalues[-len(Mkeys):]))
			genre = dictionary.get('Genre: ').strip()
			language = dictionary.get('Language: ').strip()
			#runtime = dictionary.get('Runtime: ')
			#runtime = int(re.findall('\d+', ''.join(runtime))
			try:
				IMDB_score = Movie.xpath('.//div[@class="new-title-ratings"]//text()[2]').extract_first()[1:4]
				IMDB_score = float(IMDB_score) 
			except:
				IMDB_score = None

			year = Movie.xpath('.//h5//text()').extract()[1] 
			try:
				year = int(re.findall('\d{4}', year)[0])
			except:
				year = None 

			if bool(Movie.xpath('.//div[contains(@class, "netflix-original-banner")]')) == True:
				Netflix_Original = 'Netflix Original'
			else:
				Netflix_Original = None 

			item = WhatsonnetflixItem()
			item['title'] = title
			item['genre'] = genre
			item['IMDB_score'] = IMDB_score
			item['year'] = year
			item['date'] = date
			item['TV_or_Movie'] = TV_or_Movie
			item['Foreign_or_Domestic'] = Foreign_or_Domestic
			item['language'] = language
			item['Netflix_Original'] = Netflix_Original
			#item['runtime'] = runtime

			yield item