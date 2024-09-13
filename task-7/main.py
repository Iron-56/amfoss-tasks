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
@click.option('--file_size', '-s', default=None, help='Filter subtitles by movie file size.')
@click.option('--match_by_hash', '-h', is_flag=True, help='Match subtitles by movie hash.')
@click.option('--batch_download', '-b', is_flag=True, default=False, type=click.BOOL, help='Enable batch mode.')

def search(mp4_path, language, output, file_size, match_by_hash, batch_download):
	
	if not os.path.exists(mp4_path):
		click.echo("No such file exists")
		return -1

	movies = id.search_movie(mp4_path)

	domain = "https://www.opensubtitles.org/en/search2/sublanguageid-all"

	#if batch_download == True:
	#	batchPath = input("Enter batch download path: ")
	#if file_size is not None:
	#	domain += "/moviebytesize-"+file_size
	
	#if language is not None:
	#	domain += "/movielanguage-"+language

	hash, size = subs_hash.hash_size_File_url(mp4_path)
	print(hash, size)

	if len(movies) == 0:
		#
		domain += "/imdbid-0052077"#+movies[0].movieID
	elif match_by_hash:
		domain += "/moviebytesize-"+str(size)
		domain += "/moviehash-"+hash
		#print(BeautifulSoup(requests.get(domain).text, 'html.parser').prettify())
	#print(hash, size)
	

	domain += "/sort-7/asc-0"
	print(domain)
	soup = BeautifulSoup(requests.get(domain).text, 'html.parser')
	trs = soup.find("table", {"id":"search_results"}).find("tbody").find_all("tr")

	trs = soup.find_all("tr", {"class":"change even expandable"})
	trs.append(soup.find_all("tr", {"class":"change even odd"}))

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

	zipfile.ZipFile(io.BytesIO(requests.get(download_link).content))
	
def download_url(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)



search()