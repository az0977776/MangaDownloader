import requests
from bs4 import BeautifulSoup
import sys
import shutil
import os
import img2pdf
from natsort import natsorted
from tabulate import tabulate

domain = "https://www.mangareader.net"
mangas = ["jagaaaaaan","kengan-ashua","shokugeki-no-soma","kingdom","bleach","naruto"]

def download_image(url,path):
    response = requests.get(url, stream=True)
    with open(path,'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

def num_chapters(manga_name):
    main_page = requests.get(domain+"/"+manga_name)
    soup = BeautifulSoup(main_page.text, "html.parser")
    links = soup.find("div",id ="chapterlist").find_all("a")
    return len(links)

def num_pages(manga_name,chapter):
    url = domain + "/" + manga_name + "/" + str(chapter)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    pages = soup.find("div",id="selectpage").find_all("option")
    return len(pages)

def get_image_from_page(manga_name,chapter,page):
    url = domain + "/" + manga_name + "/" + str(chapter) + "/" + str(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    image = soup.find("img",id="img")["src"]
    return image

def create_pdf(manga_name,chapter):
    path = manga_name + "/" + str(chapter)
    pdf_path = path + "/chapter" + str(chapter) + ".pdf"
    images = [path+"/"+i for i in os.listdir(path) if i.endswith(".jpg")]
    images = natsorted(images)
    with open(pdf_path, "wb") as f:
          f.write(img2pdf.convert(images))

def download_chapter(manga_name,chapter):
    path = manga_name + "/" + str(chapter)
    if not os.path.exists(path):
        os.makedirs(path)
    pages = num_pages(manga_name,chapter)
    print("Downloading " + str(pages) + " pages...")
    for page in range(pages):
        image_path = get_image_from_page(manga_name,chapter,page+1)
        save_location = path + "/" + str(page+1) + ".jpg"
        download_image(image_path,save_location)

def main():
    counter = 0
    table = []
    for manga in mangas:
        table += [[counter, manga]]
        counter = counter+1
    print(tabulate(table,headers=["Index","Manga"]))
    index = int(input("Choose manga index from the list: "))
    print("Chosen: " + mangas[index])
    chapters = num_chapters(mangas[index])
    chapter_to_download = input("What chapter do you want to download? (1 - %s)\n" % chapters)
    download_chapter(mangas[index],chapter_to_download)
    create_pdf(mangas[index],chapter_to_download)
    print("Download Complete!")

if __name__ == '__main__':
    main()
