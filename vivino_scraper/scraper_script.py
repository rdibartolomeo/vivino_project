import vivino_scraper as vivino
import os
import time
import csv

def run_vivino_scraper(page_start, page_end, incremement):

	start_time = time.time()

	# instantiate the vivino.NapaScraper class
	wine_scraper = vivino.NapaScraper()

	# scrape 80 pages from vivino
	for page in range(page_start, page_end, incremement):
		last_page = page + (incremement-1)
		wine_scraper.scrape_data(page, last_page)
		current_time = time.time()
		print('Time elapsed for batch {}-{}: {} minutes'.format(page_start, page_end,round((current_time-start_time)/60,2)))

	end_time = time.time()

	print('Total time: {} minutes'.format(round((end_time-start_time)/60,2)))



def combine_csvs():

	# list all wine csv files
	wine_data_files = os.listdir('./wine_data')

	# remove .DS_Store from the list if captured
	if '.DS_Store' in wine_data_files:
			wine_data_files.remove('.DS_Store')

	# instantiate a set to hold column headers
	headers = set()


	for data_file in wine_data_files:

		# for each wine data file
		file_name = './wine_data/{}'.format(data_file)

		with open(file_name, 'r') as wine_data_csv:

			#read the first row of the file and add the column headers to headers set
			wine_data_reader = csv.reader(wine_data_csv)
			for row in wine_data_reader:
				[headers.add(item) for item in row]
				break
			print("headers from {} identified".format(file_name))

			# close the file
			wine_data_csv.close()

	# create a file to hold all wine data
	with open("./wine_data/wine_data_combined.csv", "w", newline="") as output:

		# write the headers to the first row
		writer = csv.writer(output)
		writer.writerow(headers)

		# write each wine csv file's data to the combined csv
		dict_writer = csv.DictWriter(output, fieldnames=headers)
		for data_file in wine_data_files:
			file_name = './wine_data/{}'.format(data_file)
			with open(file_name, "r", newline="") as wine_data_csv:
				wine_data_reader = csv.DictReader(wine_data_csv)
				for row in wine_data_reader:
					dict_writer.writerow(row)
				wine_data_csv.close()
			print('csv file {} have been combined'.format(file_name))

		# close the file
		output.close()
