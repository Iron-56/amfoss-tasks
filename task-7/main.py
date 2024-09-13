import click
from bs4 import BeautifulSoup
import requests, zipfile, io, os
import imdb
import subs_hash

id = imdb.IMDb()

@click.command()
@click.argument('mp4_path')
@click.option('--language', '-l', default="English", help='Filter subtitles by language.')
@click.option('--output', '-o', default=None, help='Specify the output folder for the subtitles.')
@click.option('--file_size', '-s', is_flag=True, help='Filter subtitles by movie file size.')
@click.option('--match_by_hash', '-h', is_flag=True, help='Match subtitles by movie hash.')
@click.option('--batch_download', '-b', is_flag=True, default=False, type=click.BOOL, help='Enable batch mode.')

def search(mp4_path, language, output, file_size, match_by_hash, batch_download):

	o = ""

	if output is not None:
		o = "/"+output
		if not os.path.exists(output):
			os.makedirs(output)

	if batch_download == True:
		for file in os.listdir(mp4_path):
			f = os.path.join(mp4_path, file)
			if os.path.isfile(f):
				if file.endswith(".mpeg4"):
					getFile(mp4_path+"/", file, language, file_size, match_by_hash, output)
	else:
		getFile("", mp4_path, language, file_size, match_by_hash, output)


def getFile(dir, filename, language, file_size, match_by_hash, output):
	if not os.path.exists(dir+filename):
		click.echo("No such file exists")
		return -1

	hash, size = subs_hash.hash_size_File_url(dir+filename)
	domain = "https://www.opensubtitles.org/en/search/sublanguageid-all"

	movies = id.search_movie(filename)

	if (language is not None) and (len(movies) == 0):
		domain += "/movielanguage-"+language
	
	if file_size:
		print("Size:", size)
		domain += "/moviebytesize-"+str(size)

	if len(movies) != 0:
		domain += "/imdbid-"+movies[0].movieID
	elif match_by_hash:
		print("Hash:", hash)
		domain += "/moviehash-"+hash
	

	domain += "/sort-7/asc-0"
	print("Getting results from:",domain)
	soup = BeautifulSoup(requests.get(domain).text, 'html.parser')

	try:
		trs = soup.find("table", {"id":"search_results"}).find("tbody").find_all("tr")
		trs = soup.find_all("tr", {"class":"change even expandable"})
		trs.append(soup.find_all("tr", {"class":"change even odd"}))
	except:
		print("No file with that size found.")
		return 0

	subtitles = []
	for tr in trs:
		try:
			subtitle = {}
			subtitle["id"] = tr.get('id').replace("name","")
			td = tr.find("td", {"id":"main"+subtitle["id"]})
			subtitleInfo = td.find("strong").find("a")
			subtitle["code"] = subtitleInfo.get("href").split("/")[3]
			subtitle["title"] = td.find("span").text.split("-", 1)[0]
			subtitle["title"] = subtitle["title"].split("...", 1)[0]
			subtitles.append(subtitle)

		except:
			continue
	
	click.echo(language+" subtitles:")
	for i in range(len(subtitles)):
		click.echo(str(i+1)+". "+subtitles[i]["title"])
	
	sub = int(click.prompt("Choose a format: ", click.INT))-1

	download_link = "https://www.opensubtitles.org/en/subtitleserve/sub/"+subtitles[sub]["code"]
	print("Downloading:",download_link)
	
	z = zipfile.ZipFile(io.BytesIO(requests.get(download_link).content))
	z.extractall(output)


search()