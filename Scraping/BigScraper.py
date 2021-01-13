import requests
from bs4 import BeautifulSoup
import datetime
from textblob import TextBlob
import pandas as pd
import json
import numpy as np
import re


class BigScraper:
    """"Documentation
    This class allows to scrap several websites, some sites have a specific scraper (see list) and the others will be scraped by a generic scrapper (scrap_generic)
    """
    Cols = ["art_content", "art_content_html", "art_published_datetime", "art_lang", "art_title",
            "art_url", "src_name", "src_type", "src_url", "art_img", "art_auth", "art_tag"]

    def __init__(self):
        self.df = pd.DataFrame(columns=BigScraper.Cols)

    # def add_row(self, row_scrap):
    #     if type(row_scrap) == list:
    #         self.df.loc[len(self.df)] = row_scrap
    #     elif type(row_scrap) == dict:
    #         self.df = self.df.append(row_scrap, ignore_index=True)

    @staticmethod
    def get_base_url(url: str) -> str:
        """Documentation

        Parameter:
            url: complete url of an article

        Out:
            base_url: base url of a website

        """
        for val in re.finditer(r"(\w)+://[^/]+/", url):
            base_url = val.group(0)
        return base_url

    # Jason
    @staticmethod
    def scrap_changethework(url: str) -> list:
        """Documentation

        Parameters:
            url: url of the article to scrap

        Out:
            row: result of the scraping for each columns

        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        art_html = soup.find("div", {"style": "text-align: justify;"})
        art_html_str = str(art_html)
        art_content = art_html.get_text().strip().replace("\xa0", "")
        if soup.find("meta", {"property": "article:modified_time"})["content"] is None:
            if soup.find("meta", {"property": "article:published_time"})["content"] is None:
                art_extract_datetime = datetime.date.today()
            else:
                art_extract_datetime = soup.find(
                    "meta", {"property": "article:published_time"})["content"]
                art_extract_datetime = datetime.datetime.strptime(
                    art_extract_datetime, "%Y-%m-%dT%H:%M:%S%z").date()
        else:
            art_extract_datetime = soup.find(
                "meta", {"property": "article:modified_time"})["content"]
            art_extract_datetime = datetime.datetime.strptime(
                art_extract_datetime, "%Y-%m-%dT%H:%M:%S%z").date()
        art_lang = TextBlob(art_content).detect_language()
        art_title = soup.find("meta", {"property": "og:title"})["content"]
        art_url = soup.find("meta", {"property": "og:url"})["content"]
        src_name = soup.find("meta", {"property": "og:site_name"})["content"]
        src_type = "xpath_source"
        src_url = BigScraper.get_base_url(art_url)
        src_img = soup.find("meta", {"property": "og:image"})["content"]
        art_auth = [el.get_text().strip() for el in soup.find_all(
            "span", class_="elementor-post-author")]
        art_tag = np.nan
        row = [art_content, art_html_str, art_extract_datetime, art_lang, art_title,
               art_url, src_name, src_type, src_url, src_img, art_auth, art_tag]
        return row

    # Marianne
    @staticmethod
    def scrap_fncrr(url: str) -> list:
        """Documentation

        Parameters:
            url: url of the scraped page

        Out:
            row: list of values

        """
        response = requests.get(url)
        html_soup = BeautifulSoup(response.text, "html.parser")
        # content, content_html
        try:
            content = html_soup.find("div", {"class": "contenu_c"})
            content_html = str(content)
            content = content.text
        except:
            content_html = np.nan
            content = np.nan
        # date
        if html_soup.find("time", {"class": "updated"}) is not None:
            date = html_soup.find("time", {"class": "updated"})
        else:
            date = html_soup.find("time", {"class": "entry-date published"})
        try:
            date = date["datetime"]
            date = datetime.datetime.strptime(
                date, "%Y-%m-%dT%H:%M:%S%z").date()
        except:
            # if no date is specified, put scraping date
            date = datetime.date.today()
        # language
        art_lang = TextBlob(content).detect_language()
        # src_url
        src_url = BigScraper.get_base_url(url)
        # tag, title
        presentation = html_soup.find("div", {"class": "prensentation"})
        tag = np.nan  # tags are not always interesting
        title = presentation.find("h1")
        title = title.text
        # Remplissage du dataframe
        row = [content, content_html, date, art_lang, title, url,
               "fnccr", "xpath_source", src_url, np.nan, np.nan, tag]
        return row

    @staticmethod
    def scrap_cnil(url: str) -> list:
        """Documentation

        Parameters:
            url: url of the scraped page

        Out:
            new_row: data to put in dataframe

        """
        req = requests.get(url)
        html_soup = BeautifulSoup(req.text, "html.parser")
        #content, content_html
        try:
            content_html = str(html_soup.find(
                "div", {"class": "field-item even"}))
            content_html_str = str(content_html)
            content = content_html.text.replace("\xa0", "")
        except:
            # maybe find a way to take into account multiple article structures instead
            content_html = np.nan
            content = np.nan
        # date
        date = html_soup.find("div", {"class": "ctn-gen-auteur"}).text

        if date is None:
            date = datetime.date.today()
        else:
            trans_month = {"01": ["janvier"],
                           "02": ["février"],
                           "03": ["mars"],
                           "04": ["avril"],
                           "05": ["mai"],
                           "06": ["juin"],
                           "07": ["juillet"],
                           "08": ["août"],
                           "09": ["septembre"],
                           "10": ["octobre"],
                           "11": ["novembre"],
                           "12": ["décembre"]}

            date_tab = date.split(" ")
            day = date_tab[0]
            month = date_tab[1]
            for m in trans_month:
                if month.lower() in trans_month[m]:
                    month = m
            year = date_tab[2]
            date = datetime.date(int(year), int(month), int(day))

        # title
        zone_title = html_soup.find("div", {"class": "ctn-gen-titre"})
        title = zone_title.find("h1")
        title = title.text
        # img
        try:
            zone_img = html_soup.find("div", {"class": "ctn-gen-visuel"})
            img = zone_img.find("img")["src"]
        except:
            img = np.nan
        # lang
        art_lang = TextBlob(content).detect_language()
        # src_url
        src_url = BigScraper.get_base_url(url)
        # tag
        zone_tag = html_soup.find("div", {"class": "mots cles"})
        try:
            tags_li_list = zone_tag.find_all("li")
            tags_list = []
            for tag in tags_li_list:
                tags_list.append(tag.text[1:])  # [1:] to remove "#"
        except:
            tags_list = np.nan
        # add data to dataframe
        new_row = [content, content_html_str, date, art_lang, title, url,
                   "cnil", "xpath_source", src_url, img, np.nan, tags_list]
        return new_row

    @staticmethod
    def scrap_jdn(url: str) -> list:
        req = requests.get(url)
        html_soup = BeautifulSoup(req.text, "html.parser")
        # content_html, content (maybe clean a little the content)
        try:
            content_html = str(html_soup.find("div", {"id": "jArticleInside"}))
            content_html_str = str(content_html)
            content = content_html.text.replace("\xa0", "")
        except:
            content_html = np.nan
            content = np.nan
        # date
        try:
            date = html_soup.find("time", {"itemprop": "publishDate"})[
                "datetime"]
            format_end = date[-5:]
            date = datetime.datetime.strptime(
                date, "%Y-%m-%dT%H:%M:%S+" + format_end)
            date = datetime.date.strftime("%Y-%m-%d")
            # possibly change where the date is extracted
            # see <script type="application/ld+json">
        except:
            date = datetime.datetime.today().strftime("%Y-%m-%d")
        # art_lang
        art_lang = TextBlob(content).detect_language()
        # title
        try:
            zone_title = html_soup.find("div", {"id": "jStickySize"})
            title = zone_title.find("h1")
            title = title.text
        except:
            title = np.nan
        # src_url
        src_url = BigScraper.get_base_url(url)
        # img
        try:
            zone_img = content_html.find("p", {"class": "app_entry_lead"})
            img = zone_img.find("img")["src"]
        except:
            img = np.nan
        # author
        try:
            link_author = html_soup.find("a", {"rel": "author"})
            author = link_author.text
        except:
            author = np.nan
        # tags
        head = html_soup.find("head")
        scripts_list = head.find_all("script")
        script = str(scripts_list[1])
        pattern = re.compile(r"keywords: \[(\"(\w|\-|\d)*\",?)*\]")
        match = re.search(pattern, script)
        list_tag_str = match.group(0)
        list_tag_str = list_tag_str[11:-1]
        list_tag_str = list_tag_str.replace("-", " ")
        list_tag = list_tag_str.split(",")
        # data
        new_row = [content, content_html_str, date, art_lang, title, url,
                   "journal_du_net", "xpath_source", src_url, img, author, list_tag]
        return new_row

    @staticmethod
    def scrap_zdnet(url: str) -> list:
        """Documentation

        Parameters:
            url: url of the scraped page

        Out:
            new_row: data to put in dataframe

        """
        req = requests.get(url)
        html_soup = BeautifulSoup(req.text, "html.parser")
        # content, html_content
        content_html = html_soup.find("div", {"class": "storyBody"})
        content_html_str = str(content_html)
        content = content_html.text
        # date, author
        zone_infos = html_soup.find("div", {"class": "byline"})
        zone_infos = zone_infos.find("p", {"class": "meta"})
        # author
        try:
            zone_author = zone_infos.find("span")
            author = zone_author.find("span").text
        except:
            author = np.nan
        # date
        date = zone_infos.find("time")["datetime"]
        format_end = date[-5:]
        date = datetime.datetime.strptime(
            date, "%Y-%m-%dT%H:%M:%S+" + format_end)
        date = date.strftime("%Y-%m-%d")
        # title
        title = html_soup.find("h1").text
        # lang
        art_lang = TextBlob(content).detect_language()
        # src_url
        src_url = BigScraper.get_base_url(url)
        # img
        try:
            img = content_html.find("img")["src"]
        except:
            img = np.nan
        # tags
        zone_tags = html_soup.find("p", {"class": "relatedTopics"})
        list_tags_links = zone_tags.find_all("a")
        list_tags = []
        for link in list_tags_links:
            list_tags.append(link.text)
        # data to add in dataframe
        new_row = [content, content_html_str, date, art_lang, title, url,
                   "zdnet", "xpath_source", src_url, img, author, list_tags]
        return new_row

    @staticmethod
    def scrap_grhmulti(url: str) -> list:
        """Documentation

        Parameters:
            url: url of the website to scrap

        Out:
            new_row: data scraped 

        """
        req = requests.get(url)
        html_soup = BeautifulSoup(req.text, "html.parser")
        # content, html_content
        content_html = html_soup.find(
            "article", {"class": "col-md-9 item-page col2r"})
        content_html_str = str(content_html)
        content = content_html.text
        # date
        date = html_soup.find("meta", {"property": "article:published_time"})[
            "content"]
        format_end = date[-5:]
        date = datetime.datetime.strptime(
            date, "%Y-%m-%dT%H:%M:%S+" + format_end).date()
        date
        # title
        title = html_soup.find("meta", {"property": "og:title"})["content"]
        # art_lang
        art_lang = TextBlob(content).detect_language()
        # src_url
        src_url = BigScraper.get_base_url(url)
        # data to add in dataframe
        new_row = [content, content_html_str, date, art_lang, title, url,
                   "grh-multi", "xpath_source", src_url, np.nan, np.nan, np.nan]
        return new_row

    # Louis

    @staticmethod
    def scrap_sabbar(url: str) -> list:
        """Documentation

        Parameters:
            url: url of the article to be scraped

        Out:
            Data scraped

        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        # Récupération du contenu de la page web (les paragraphes, avec et sans les balises html)
        art_content_html = soup.find("div", class_="entry-content")
        art_content_html_str = str(art_content_html)
        art_content = art_content_html.get_text().replace("\xa0", "").strip()
        # Extraction de la date de l'article
        art_extract_datetime = json.loads(soup.find(
            "script", class_="yoast-schema-graph yoast-schema-graph--main").get_text())["@graph"][1]["dateModified"]
        art_extract_datetime = datetime.datetime.strptime(
            art_extract_datetime, "%Y-%m-%dT%H:%M:%S%z").date()
        # Langue de l'article
        art_lang = soup.find("meta", property="og:locale").get("content")
        # Titre
        art_title = soup.find("meta", property="og:title").get("content")
        # Url
        art_url = soup.find("link", rel="canonical").get("href")
        # Nom de la source
        src_name = "Sabbar"
        # Type de la source
        src_type = "xpath_source"
        # url source
        src_url = BigScraper.get_base_url(art_url)
        # Image(s)
        src_img = np.nan
        # Auteur de l'article
        art_auth = np.nan
        # Tag de l'auteur
        art_tag = np.nan

        return [art_content, art_content_html_str, art_extract_datetime, art_lang, art_title, art_url,
                src_name, src_type, src_url, src_img, art_auth, art_tag]

    @staticmethod
    def scrap_lebigdata(url: str) -> list:
        """Documentation

        Parameters:
            url: url of the article to be scraped

        Out:
            Data scraped

        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        art_content_html = soup.find("article")
        art_content_html_str = str(art_content_html)
        art_content = art_content_html.get_text().replace("\xa0", "")
        if soup.find("meta", property="article:modified_time") is not None:
            art_published_datetime = soup.find(
                "meta", property="article:modified_time").get("content")
            art_published_datetime = datetime.datetime.strptime(
                art_published_datetime, "%Y-%m-%dT%H:%M:%S%z").date()
        elif soup.find("meta", property="article:published_time") is not None:
            art_published_datetime = soup.find(
                "meta", property="article:published_time").get("content")
            art_published_datetime = datetime.datetime.strptime(
                art_published_datetime, "%Y-%m-%dT%H:%M:%S%z").date()
        else:
            art_published_datetime = datetime.date.today()
        art_lang = soup.find("meta", property="og:locale").get("content")
        art_title = soup.find("meta", property="og:title").get("content")
        art_url = soup.find("meta", property="og:url").get("content")
        src_name = soup.find("meta", property="og:site_name").get("content")
        src_type = "xpath_source"
        src_url = BigScraper.get_base_url(art_url)
        art_img = soup.find("meta", property="og:image").get("content")
        art_auth = soup.find(
            "meta", attrs={"name": "twitter:data1"}).get("content")
        art_tag = np.nan
        return [art_content, art_content_html_str, art_published_datetime, art_lang, art_title, art_url,
                src_name, src_type, src_url, art_img, art_auth, art_tag]

    @staticmethod
    def scrap_cadre(url: str) -> list:
        """Documentation

        Parameters:
            url: url of the article to be scraped

        Out:
            Data scraped

        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        art_content_html = soup.find(
            "div", class_="td-post-content").find_all("p")
        art_content_html_str = str(art_content_html)
        art_content = "".join([x.text for x in art_content_html])

        # Extraction de la date de l'article
        art_extract_datetime = soup.find(
            "meta", property="article:modified_time").get("content")

        # Langue de l'article
        art_lang = soup.find("meta", property="og:locale").get("content")

        # Titre
        art_title = soup.find("meta", property="og:title").get("content")

        # Url
        art_url = soup.find("link", rel="canonical").get("href")

        # Nom de la source
        src_name = soup.find("meta", property="og:site_name").get("content")

        # Type de la source
        src_type = "xpath_source"

        # url source
        src_url = soup.find("form", class_="td-search-form").get("action")

        # Image(s)
        src_img = soup.find("meta", property="og:image").get("content")

        # Auteur de l'article
        art_auth = soup.find("div", class_="td-post-author-name").text

        # Tag de l'auteur
        art_tag = np.nan

        return [art_content, art_content_html_str, art_extract_datetime, art_lang, art_title,
                art_url, src_name, src_type, src_url, src_img, art_auth, art_tag]

    @staticmethod
    def scrap_sap(url: str) -> list:
        """Documentation:

        Parameters:
            url: url of the article to scrap

        Out:
            Data scraped

        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        art_content_html = soup.find_all("div", class_="parContent")
        art_content_html_str = str(art_content_html)
        art_content = " ".join([x.text for x in art_content_html])

        date = soup.find(
            "video", class_="video-js vjs-default-skin vjs-big-play-centered vjs-fluid").get("data-publishingdate")
        art_published_datetime = datetime.datetime.strptime(
            date, "%Y-%m-%dT%H:%M:%S%z").date()

        art_lang = soup.find("meta", attrs={"name": "language"}).get("content")

        art_title = soup.find("meta", property="og:title").get("content")

        art_url = soup.find("meta", property="og:url").get("content")

        src_name = soup.find("meta", property="og:site_name").get("content")

        src_type = "xpath_source"

        src_url = BigScraper.get_base_url(art_url)

        src_img = soup.find('meta', property="og:image").get("content")

        art_auth = np.nan

        art_tag = soup.find("meta", attrs={"name": "keywords"}).get("content")

        return [art_content, art_content_html_str, art_published_datetime, art_lang, art_title, art_url,
                src_name, src_type, src_url, src_img, art_auth, art_tag]

    @staticmethod
    def scrap_datagouv(url: str) -> list:
        """Documentation

        Parameters:
            url: url of the article to scrap

        Out:
            Data scraped

        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        if soup.find_all("section", class_="content noncertified") == []:
            art_content_html = soup.find_all(
                "section", class_="content certified")
        else:
            art_content_html = soup.find_all(
                "section", class_="content noncertified")
        art_content_html_str = str(art_content_html)

        art_content = " ".join([x.text for x in art_content_html])

        art_extract_datetime = datetime.date.today()

        art_lang = TextBlob(art_content).detect_language()

        art_title = soup.find("meta", property="og:title").get("content")

        art_url = soup.find("link", rel="canonical").get("href")

        src_type = "xpath_source"

        src_url = BigScraper.get_base_url(art_url)

        src_name = src_url.replace("https://", "").replace("/", "")

        src_img = soup.find("meta", property="og:image").get("content")

        art_auth = soup.find("link", rel="author").get("href")

        art_tag = []
        tags = soup.find_all("a", class_="label label-default")
        for x in tags:
            art_tag.append(x.get("title"))

        return [art_content, art_content_html_str, art_extract_datetime, art_lang, art_title, art_url,
                src_name, src_type, src_url, src_img, art_auth, art_tag]

    @staticmethod
    def scrap_blockchain(url: str) -> list:
        """Documentation

        Parameters:
            url: url of the article to scrap

        Out:
            Data scraped

        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        art_content_html = soup.find_all("div", class_="site-content")
        art_content_html_str = str(art_content_html)
        art_content = " ".join([x.text for x in art_content_html])

        date = soup.find(
            "meta", property="article:modified_time").get("content")
        art_extract_datetime = datetime.datetime.strptime(
            date, "%Y-%m-%dT%H:%M:%S%z").date()

        art_lang = soup.find(
            "meta", attrs={"property": "og:locale"}).get("content")

        art_title = soup.find("meta", property="og:title").get("content")

        art_url = soup.find("meta", property="og:url").get("content")

        src_type = "xpath_source"

        src_url = BigScraper.get_base_url(art_url)

        src_name = src_url.replace("https://", "").replace("/", "")

        src_img = soup.find("meta", property="og:image").get("content")

        art_auth = np.nan

        if soup.find("meta", attrs={"name": "keywords"}):
            art_tag = soup.find("meta", attrs={"name": "keywords"})
        else:
            art_tag = np.nan

        return [art_content, art_content_html_str, art_extract_datetime, art_lang, art_title, art_url,
                src_name, src_type, src_url, src_img, art_auth, art_tag]

    @staticmethod
    def scrap_weka(url: str) -> list:
        """Documentation

        Parameters:
            url: url of the article to scrap

        Out:
            Data scraped

        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        art_content_html = soup.find_all("div", class_="site-content")
        art_content_html_str = str(art_content_html)
        art_content = " ".join([x.text for x in art_content_html])

        if soup.find("span", itemprop="datePublished") is None:
            art_published_datetime = datetime.datetime.now()
        else:
            art_published_datetime = soup.find(
                "span", itemprop="datePublished").text
            art_published_datetime = datetime.datetime.strptime(
                art_published_datetime, "%d/%m/%y").date()

        art_lang = soup.find(
            "meta", attrs={"property": "og:locale"}).get("content")

        art_title = soup.find("meta", property="og:title").get("content")

        art_url = url

        src_name = soup.find("meta", property="og:site_name").get("content")

        src_type = "xpath_source"

        src_url = BigScraper.get_base_url(art_url)

        src_img = soup.find("meta", property="og:image").get("content")

        art_auth = soup.find("span", rel="author").text

        art_tag = []
        art_tag.append(soup.find("a", attrs={"itemprop": "keywords"}).text)
        tags2 = soup.find("div", attrs={"id": "tag"}).find_all("a")
        for tag in tags2:
            art_tag.append(tag.text)

        return [art_content, art_content_html_str, art_published_datetime, art_lang, art_title, art_url,
                src_name, src_type, src_url, src_img, art_auth, art_tag]

    # Michael

    @staticmethod
    def scrap_theinnovation(url: str) -> list:
        """Documentation

        Parameters:
            url: url of the article to scrap

        Out:
            Data scraped

        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        art_content_html = soup.find("div", {"class": "entry-content"})
        art_content_html_str = str(art_content_html)
        art_content = art_content_html.text.replace("\xa0", "")
        if soup.find("meta", {"property": "article:modified_time"}) is not None:
            art_extract_datetime = soup.find(
                "meta", {"property": "article:modified_time"})["content"]
            art_extract_datetime = datetime.datetime.strptime(
                art_extract_datetime, "%Y-%m-%dT%H:%M:%S%z").date()
        elif soup.find("meta", {"property": "article:published_time"}) is not None:
            art_extract_datetime = soup.find(
                "meta", {"property": "article:published_time"})["content"]
            art_extract_datetime = datetime.datetime.strptime(
                art_extract_datetime, "%Y-%m-%dT%H:%M:%S%z").date()
        else:
            art_extract_datetime = datetime.date.today()
        art_lang = soup.find("meta", {"property": "og:locale"})["content"]
        art_title = soup.find("meta", {"property": "og:title"})["content"]
        art_url = soup.find("meta", {"property": "og:url"})["content"]
        src_name = soup.find("meta", {"property": "og:site_name"})["content"]
        src_type = "xpath_source"  # default value
        src_url = BigScraper.get_base_url(art_url)
        src_img = soup.find("meta", {"property": "og:image"})["content"]
        art_auth = soup.find("a", {"rel": "author"}).text
        art_tag = soup.find("meta", {"name": "keywords"})["content"].split(",")
        return [art_content, art_content_html_str, art_extract_datetime, art_lang, art_title, art_url,
                src_name, src_type, src_url, src_img, art_auth, art_tag]

    @staticmethod
    def scrap_myrhline(url: str) -> list:
        """Documentation

        Parameters:
            url: url of the article to scrap

        Out:
            Data scraped

        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        if soup.find("div", {"class": "post-detail-wrap"}) is None:
            art_content_html = np.nan
        else:
            art_content_html = soup.find("div", {"class": "post-detail-wrap"})
            art_content_html_str = str(art_content_html)

        art_content = art_content_html.get_text().replace("\xa0", "").strip()
        if art_content is None:
            art_content = np.nan

        if soup.find("meta", {"property": "article:modified_time"}) is not None:
            art_published_datetime = soup.find(
                "meta", {"property": "article:modified_time"})["content"]
            art_published_datetime = datetime.datetime.strptime(
                art_published_datetime, "%Y-%m-%dT%H:%M:%S%z").date()

        elif soup.find("meta", {"property": "article:published_time"}) is not None:
            art_published_datetime = soup.find(
                "meta", {"property": "article:published_time"})["content"]
            art_published_datetime = datetime.datetime.strptime(
                art_published_datetime, "%Y-%m-%dT%H:%M:%S%z").date()

        else:
            art_published_datetime = datetime.date.today()

        if art_content is not None:
            art_lang = TextBlob(art_content).detect_language()
        elif soup.find("meta", {"property": "og:locale"}) is not None:
            art_lang = soup.find("meta", {"property": "og:locale"})["content"]
        else:
            art_lang = np.nan

        if soup.find("meta", {"property": "og:title"}) is not None:
            art_title = soup.find("meta", {"property": "og:title"})["content"]
        elif soup.find("title") is not None:
            art_title = soup.find("title").text
        else:
            art_title = np.nan

        if soup.find("meta", {"property": "og:url"}) is not None:
            art_url = soup.find("meta", {"property": "og:url"})["content"]
        else:
            art_url = url

        if soup.find("meta", {"property": "og:site_name"}) is not None:
            src_name = soup.find("meta", {"property": "og:site_name"})[
                "content"]
        else:
            src_name = np.nan

        src_type = "xpath_source"  # default value

        src_url = BigScraper.get_base_url(art_url)

        if soup.find("meta", {"property": "og:image"}) is not None:
            art_img = soup.find("meta", {"property": "og:image"})["content"]
        else:
            art_img = np.nan

        if soup.find("meta", {"name": "author"}) is not None:
            art_auth = soup.find("meta", {"name": "author"})["content"]
        else:
            art_auth = np.nan

        if soup.find_all("a", {"rel": "tag"}) is not None:
            art_tag = [tag.text for tag in soup.find_all("a", {"rel": "tag"})]
        else:
            art_tag = np.nan

        return [art_content, art_content_html_str, art_published_datetime, art_lang, art_title, art_url,
                src_name, src_type, src_url, art_img, art_auth, art_tag]

    @staticmethod
    def scrap_usinedigitale(url: str) -> list:
        """Documentation

        Parameters:
            url: url of the article to scrap

        Out:
            Data scraped

        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # retrieval of the html content
        if soup.find("article", {"class": "contenuArticle"}) is None:
            art_content_html = np.nan
        else:
            art_content_html = soup.find(
                "article", {"class": "contenuArticle"})
            art_content_html_str = str(art_content_html)

        # retrieval of the article content
        art_content = art_content_html.text
        if art_content is None:
            art_content = np.nan

        # retrieval of the publication/modification date
        if soup.find("time", {"class": "dateEtiquette3"}) is None:
            art_published_datetime = datetime.datetime.now()
        else:
            art_published_datetime = soup.find(
                "time", {"class": "dateEtiquette3"})["datetime"]
            art_published_datetime = datetime.datetime.strptime(
                art_published_datetime, "%Y-%m-%dT%H:%M").date()

        # retrieval of the language
        if art_content is not None:
            art_lang = TextBlob(art_content).detect_language()
        elif soup.find("meta", {"property": "og:locale"}) is not None:
            art_lang = soup.find("meta", {"property": "og:locale"})["content"]
        else:
            art_lang = np.nan

        # retrieval of the title
        if soup.find("meta", {"property": "og:title"}) is not None:
            art_title = soup.find("meta", {"property": "og:title"})["content"]
        elif soup.find("title") is not None:
            art_title = soup.find("title").text
        else:
            art_title = np.nan

        # retrieval of the article url
        art_url = soup.find("meta", {"property": "og:url"})

        if art_url is None:
            art_url = url
        else:
            art_url = art_url["content"]

        # retrieval of the website name
        if soup.find("meta", {"name": "ipd:siteName"}) is not None:
            src_name = soup.find("meta", {"name": "ipd:siteName"})["content"]
        elif soup.find("meta", {"property": "og:site_name"}) is not None:
            src_name = soup.find("meta", {"property": "og:site_name"})[
                "content"]
        else:
            src_name = np.nan

        # retrieval of the source type
        src_type = "xpath_source"  # default value

        # retrieval of the source url
        src_url = BigScraper.get_base_url(art_url)
        if src_url is None:
            src_url = np.nan

        # retrieval of the article image
        art_img = soup.find("meta", {"property": "og:image"})
        if art_img is None:
            art_img = np.nan
        else:
            art_img = art_img["content"]

        # retrieval of the article author
        art_auth = soup.find("a", {"class": "nomAuteur"})
        if art_auth is None:
            art_auth = np.nan
        else:
            art_auth = art_auth.text

        # retrieval of the article tags
        if soup.find_all("a", {"rel": "tag"}) is not None:
            art_tag = [tag.text for tag in soup.find_all("a", {"rel": "tag"})]
        else:
            art_tag = np.nan

        return [art_content, art_content_html_str, art_published_datetime, art_lang, art_title,
                art_url, src_name, src_type, src_url, art_img, art_auth, art_tag]

    # Rémy

    @staticmethod
    def scrap_lemondeinformatique(url: str) -> list:
        """Documentation

        Parameters:
            url: url of the article to scrap

        Out:
            Data scraped

        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        art_content_html = soup.find("div", class_="article-body")
        art_content_html_str = str(art_content_html)
        art_content = art_content_html.get_text().replace("\xa0", "").strip()
        if soup.find("meta", {"itemprop": "datePublished"}) is not None:
            art_extract_datetime = soup.find(
                "meta", {"itemprop": "datePublished"})["content"]
            art_extract_datetime = datetime.datetime.strptime(
                art_extract_datetime, "%Y-%m-%dT%H:%M:%S%z").date()
        else:
            art_extract_datetime = datetime.date.today()
        art_lang = TextBlob(art_content).detect_language()
        art_title = soup.find("meta", {"property": "og:title"})["content"]
        art_url = soup.find("meta", {"property": "og:url"})["content"]
        src_name = soup.find("meta", {"property": "og:site_name"})["content"]
        src_type = "xpath_source"
        src_url = BigScraper.get_base_url(art_url)
        src_img = soup.find("meta", {"property": "og:image"})["content"]
        art_auth = soup.find(
            "div", class_="author-infos").find("b", {"itemprop": "name"}).get_text()
        art_tag = [el.get_text()
                   for el in soup.find_all("a", {"rel": "category tag"})]
        return [art_content, art_content_html_str, art_extract_datetime, art_lang, art_title, art_url, src_name, src_type, src_url, src_img, art_auth, art_tag]

    @staticmethod
    def scrap_erudit(url: str) -> list:
        """Documentation

        Parameters:
            url: url of the article to scrap

        Out:
            Data scraped

        """
        req = requests.get(url)
        html_soup = BeautifulSoup(req.text, "html.parser")
        # Retrieval of the content of the article with the html tags
        art_content_html = html_soup.find("section", {"id": "s1n1"})
        art_content_html_str = str(art_content_html)
        # Removal of the html tags and replacement of '\xa0' by ''
        art_content = art_content_html.text.replace("\xa0", "")
        # Retrieval of the date and conversion to the datetime format
        art_published_datetime = datetime.datetime.strptime(html_soup.find(
            "meta", {"name": "citation_online_date"})["content"], "%Y/%m/%d").date()
        # Analysis of the language of the text with the TextBlob library
        art_lang = TextBlob(art_content).detect_language()
        # Retrieval of the title in meta property, replacing '\xa0' by ''
        art_title = html_soup.find("meta", {"property": "og:title"})[
            "content"].replace("\xa0", "")
        # Retrieval of the url in meta property
        art_url = html_soup.find("meta", {"property": "og:url"})["content"]
        # Retrieval of the website's name in meta property
        src_name = html_soup.find(
            "meta", {"property": "og:site_name"})["content"]
        src_type = "xpath_source"  # default value
        src_url = BigScraper.get_base_url(art_url)
        # Concatenation of the base url of the website and the end of the url of the image representing the article
        art_img = "https://www.erudit.org" + \
            html_soup.find("meta", {"property": "og:image"})["content"]
        # Retrieval of a list of the author(s) of the article
        art_auth = [el.text.replace('\n      ', ' ') for el in html_soup.find_all(
            "span", {"class": "nompers"})]
        # No tags found on this website
        art_tag = np.nan
        return [art_content, art_content_html_str, art_published_datetime, art_lang, art_title, art_url, src_name,
                src_type, src_url, art_img, art_auth, art_tag]

    @staticmethod
    def scrap_citmar(url: str) -> list:
        """Documentation

        Parameters:
            url: url of the article to scrap

        Out:
            Data scraped

        """
        req = requests.get(url)
        html_soup = BeautifulSoup(req.text, "html.parser")

        paragraphe = html_soup.find_all("p")
        art_content_html = " ".join([str(x) for x in paragraphe])
        art_content_html_str = str(art_content_html)
        art_content = " ".join([x.text for x in paragraphe])

        art_published_datetime = html_soup.find(
            "time", {"class": "entry-date published"})["content"]

        language = TextBlob(art_content)
        art_lang = language.detect_language()

        art_title = html_soup.find(
            "h1", {"class": "hestia-title entry-title"}).text

        art_url = url

        src_name = "citoyen-ne-s-de-marseille"

        src_type = "xpath_source"

        src_url = BigScraper.get_base_url(art_url)

        art_img = np.nan

        art_auth = html_soup.find("strong", {"class": "fn"}).text

        art_tag = np.nan

        return [art_content, art_content_html_str, art_published_datetime, art_lang, art_title, art_url,
                src_name, src_type, src_url, art_img, art_auth, art_tag]

    @staticmethod
    def scrap_digitrec(url: str) -> list:
        """Documentation

        Parameters:
            url: url of the article to scrap

        Out:
            Data scraped

        """
        response = requests.get(url)
        html_soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = html_soup.find_all("p")
        art_content_html = " ".join([str(x) for x in paragraphs])
        art_content_html_str = str(art_content_html)
        art_content = " ".join([x.text for x in paragraphs])

        Datetemp = html_soup.find("ul", {"class": "list-inline infos"}).text
        art_extract_datetime = Datetemp.split("\n")[4]

        a = TextBlob(art_content)
        art_lang = a.detect_language()

        art_title = html_soup.find("meta", {"property": "og:title"})["content"]

        art_url = url

        src_url = BigScraper.get_base_url(art_url)

        src_name = src_url.replace("https://", "").replace("/", "")

        src_type = "xpath_source"

        src_img = html_soup.find("meta", {"property": "og:image"})["content"]

        authortemp1 = html_soup.find("ul", {"class": "list-inline infos"}).text
        authortemp2 = authortemp1.split("\n")[5]
        author = authortemp2.split(" ")[1:]
        art_auth = str(author[0] + " " + author[1])

        art_tag = np.nan

        return [art_content, art_content_html_str, art_extract_datetime, art_lang, art_title, art_url,
                src_name, src_type, src_url, src_img, art_auth, art_tag]

    @staticmethod
    def scrap_hellofuture(url: str) -> list:  # Scraping Rémy HelloFuture Orange
        """Documentation

        Parameters:
            url: url of the article to scrap

        Out:
            Data scraped

        """
        req = requests.get(url)
        html_soup = BeautifulSoup(req.text, "html.parser")

        paragraphe = html_soup.find_all("p")
        art_content_html = " ".join([str(x) for x in paragraphe])
        art_content_html_str = str(art_content_html)
        art_content = " ".join([x.text for x in paragraphe])

        Datetemp = html_soup.find("div", {"class": "article__content--author"})
        art_published_datetime = Datetemp.find("time")["datetime"]

        a = TextBlob(art_content)
        art_lang = a.detect_language()

        art_title = html_soup.find("h1", {"class": "h1"}).text

        art_url = url

        src_name = "hello_future_orange"

        src_type = "xpath_source"

        src_url = BigScraper.get_base_url(art_url)

        if html_soup.find("div", {"class": "article__media"}):
            art_img = html_soup.find(
                "div", {"class": "article__media"}).find("img")["src"]
        else:
            art_img = np.nan

        art_auth = np.nan

        art_tag = html_soup.find(
            "div", {"class": "article__tag"}).find("img")["alt"]

        return [art_content, art_content_html_str, art_published_datetime, art_lang, art_title, art_url,
                src_name, src_type, src_url, art_img, art_auth, art_tag]

    @staticmethod
    def scrap_silicon(url: str) -> list:  # Scraping Rémy silicon.fr
        """Documentation

        Parameters:
            url: url of the article to scrap

        Out:
            Data scraped

        """
        req = requests.get(url)
        html_soup = BeautifulSoup(req.text, "html.parser")

        # Retrieval of the content of the article with the html tags
        art_content_html = html_soup.find(
            "section", {"class": "article-content"})
        art_content_html_str = str(art_content_html)

        # Removal of the html tags and replacement of '\xa0' by ''
        art_content = art_content_html.text.replace("\xa0", " ")

        # Retrieval of the date and conversion to the datetime format
        art_published_datetime = datetime.datetime.strptime(html_soup.find("meta", {"itemprop": "datePublished"})["content"],
                                                            "%Y-%m-%dT%H:%M:%S%z").date()

        # Analysis of the language of the text with the TextBlob library
        art_lang = TextBlob(art_content).detect_language()

        # Retrieval of the title in meta property, replacing '\xa0' by ''
        art_title = html_soup.find("meta", {"property": "og:title"})[
            "content"].replace("\xa0", " ")

        art_url = url

        # Retrieval of the website's name in meta property
        src_name = html_soup.find(
            "meta", {"property": "og:site_name"})["content"]

        src_type = "xpath_source"

        src_url = BigScraper.get_base_url(art_url)

        # Retrieval of the image representing the article
        # Because this website the image can be found at two different places in the html code we use a if/else condition
        if html_soup.find("picture", {"class": "img"}) is not None:
            art_img = html_soup.find(
                "picture", {"class": "img"}).find("source")["srcset"]
        else:
            art_img = html_soup.find("meta", {"itemprop": "image"})["content"]

        # Retrieval of the author of the article
        art_auth = html_soup.find("meta", {"itemprop": "author"})["content"]

        # Retrieval of the tag(s) of the article in meta property, if there are no tags we return np.nan
        art_tag = [el["content"] for el in html_soup.find_all(
            "meta", {"property": "article:tag"})]
        if art_tag == []:
            art_tag = np.nan

        return [art_content, art_content_html_str, art_published_datetime, art_lang, art_title, art_url,
                src_name, src_type, src_url, art_img, art_auth, art_tag]

    # Sibel

    @staticmethod
    def scrap_riskinsight(url: str) -> list:
        """Documentation

        Parameters:
            url: url of the article to scrap

        Out:
            Data scraped

        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        art_content_html = soup.find("article")
        art_content_html_str = str(art_content_html)
        art_content = art_content_html.get_text()
        src_type = "xpath_source"
        art_url = soup.find("meta", {"property": "og:url"})["content"]
        src_url = BigScraper.get_base_url(art_url)
        src_name = soup.find("meta", {"property": "og:site_name"})["content"]
        if soup.find("meta", {"name": "twitter:data1"}) is not None:
            art_auth = soup.find("meta", {"name": "twitter:data1"})["content"]
        else:
            art_auth = np.nan
        if soup.find("meta", {"property": "article:modified_time"}) is not None:
            date = soup.find("meta", {"property": "article:modified_time"})[
                "content"]
            art_published_datetime = datetime.datetime.strptime(
                date, "%Y-%m-%dT%H:%M:%S%z").date()
        elif soup.find("meta", {"property": "article:published_time"}) is not None:
            date = soup.find("meta", {"property": "article:published_time"})[
                "content"]
            art_published_datetime = datetime.datetime.strptime(
                date, "%Y-%m-%dT%H:%M:%S%z").date()
        else:
            art_published_datetime = datetime.date.today()
        art_title = soup.title.get_text()
        art_lang = TextBlob(art_content).detect_language()
        if soup.find_all("a", {"class": "tag--link"}) is not None:
            art_tag = [el.get_text()
                       for el in soup.find_all("a", {"class": "tag--link"})]
        else:
            art_tag = np.nan
        if soup.find("meta", {"property": "og:image"}) is not None:
            art_img = soup.find(
                "meta", {"property": "og:image"})["content"]
        else:
            art_img = np.nan
        return [art_content, art_content_html_str, art_published_datetime, art_lang, art_title, art_url, src_name, src_type, src_url, art_img, art_auth, art_tag]

    @staticmethod
    def scrap_parlonsrh(url: str) -> list:
        """Documentation

        Parameters:
            url: url of the article to scrap

        Out:
            new_row: Data scraped

        """
        response = requests.get(url)
        html_soup = BeautifulSoup(response.text, "html.parser")
        # content
        paragraphe = html_soup.find_all("p")
        content = " ".join([x.text for x in paragraphe])
        # content_html
        content_html = " ".join([str(x) for x in paragraphe])
        content_html_str = str(content_html)
        # time
        time = html_soup.find(
            "span", {"class": "date updated value-title"})["title"]
        if time is None or time == []:
            time = 'no data'
        else:
            trans_month = {"01": ["janvier"],
                           "02": ["février"],
                           "03": ["mars"],
                           "04": ["avril"],
                           "05": ["mai"],
                           "06": ["juin"],
                           "07": ["juillet"],
                           "08": ["août"],
                           "09": ["septembre"],
                           "10": ["octobre"],
                           "11": ["novembre"],
                           "12": ["décembre"]}
            date_tab = time.split(" ")
            day = date_tab[0]
            month = date_tab[1]
            for m in trans_month:
                if month.lower() in trans_month[m]:
                    month = m
            year = date_tab[2]
            time = datetime.date(int(year), int(month), int(day))
        # title
        html_title = html_soup.title
        title = html_title.get_text()
        # img
        img = html_soup.find("meta", {"property": "og:image"})["content"]
        if img is None:
            img = np.nan
        # author
        author = html_soup.find("span", {"class": "fn"}).get_text()
        if author[11:29] == "La Team Parlons RH":
            author = author[11:29]
        else:
            author = author[11:34]
        # art_lang
        art_lang = TextBlob(content).detect_language()
        # src_url
        src_url = BigScraper.get_base_url(url)
        # tag
        html_tag = html_soup.find_all("meta", {"property": "article:tag"})
        tags = []
        for i in html_tag:
            tag_i = i["content"]
            tags.append(tag_i)
        if tags is None or tags == []:
            tags = np.nan
        new_row = [content, content_html_str, time, art_lang, title, url,
                   "parlonsrh", "xpath_source", src_url, img, author, tags]
        return new_row

    @staticmethod
    def scrap_inserm(url: str) -> list:
        """Documentation
        function which from a url creates a BeautifulSoup object, then extract different informations about the article and the 
        source. Then researches informations about the article and the website. It finally returns all this data as a list

        Parameters:
            url: The url that we will scrap 

        Out:
            new_row: it contains some propreties of the article and the sources 

        """
        response = requests.get(url)
        html_soup = BeautifulSoup(response.text, "html.parser")

        src_type = "xpath_source"
        src_url = BigScraper.get_base_url(url)
        src_name = "Inserm"
        art_url = url
        art_published_datetime = html_soup.find("time").get_text()
        art_title = html_soup.title.get_text()
        art_img = np.nan
        html_tag = html_soup.find("a", {"rel": "category"})
        if html_tag is None:
            art_tag = np.nan
        else:
            art_tag = html_tag.get_text()
        paragraphe = html_soup.find_all("p")
        art_content_html = " ".join([str(x) for x in paragraphe])
        art_content_html_str = str(art_content_html)
        paragraphe = html_soup.find_all("p")
        art_content = " ".join([x.text for x in paragraphe])
        a = TextBlob(art_title)
        art_lang = a.detect_language()
        art_auth = np.nan
        new_row = [art_content, art_content_html_str, art_published_datetime, art_lang,
                   art_title, art_url, src_name, src_type, src_url, art_img, art_auth, art_tag]
        return new_row

    @staticmethod
    def scrap_lemonde(url: str) -> list:
        """Documentation
        function which from a url creates a BeautifulSoup object, then extract different informations about the article and the 
        source. Then researches informations about the article and the website. It finally returns all this data as a list

        Parameters:
            url(str): The url that we will scrap 

        Out:
            new_row: it contains some propreties of the article and the sources 

        """
        response = requests.get(url)
        html_soup = BeautifulSoup(response.text, "html.parser")

        src_type = "xpath_source"
        src_url = BigScraper.get_base_url(url)
        src_name = "Le Monde"

        # find the article URL (art_url)
        if html_soup.find("meta", {"property": "og:url"}) is not None:
            art_url = html_soup.find("meta", {"property": "og:url"})["content"]
        else:
            art_url = url

        # find the article Title (art_title)
        art_title = html_soup.title.get_text().replace("\xa0", "")

        # find the article Author (art_auth)
        if html_soup.find("meta", {"property": "og:article:author"}) is not None:
            art_auth = html_soup.find(
                "meta", {"property": "og:article:author"})["content"]
            if art_auth == []:
                art_auth = np.nan
        else:
            art_auth = np.nan

        # find the date of publication of the article (art_published_datetime) (format: datetime)
        if html_soup.find("meta", {"property": "og:article:published_time"}) is not None:
            art_published = html_soup.find("meta", {"property": "og:article:published_time"})[
                "content"][:10]      # take the date and remove the hour
            art_published_datetime = datetime.datetime.strptime(
                art_published, "%Y-%m-%d").date()  # put at the format datetime
        # if there is no date, we replace None with the date of today
        else:
            art_published_datetime = datetime.datetime.today().date()     #

        # src_img
        if html_soup.find("figure", {"class": "article__media"}) is not None:
            art_img = html_soup.find(
                "figure", {"class": "article__media"}).find("img")["src"]
        else:
            art_img = np.nan

        # art_tag
        #art_tag = json.loads(html_soup.find('script', type = 'application/ld+json')['@type'])
        art_tag = np.nan

        #art_content_html  and  art_content
        try:
            art_content_html_corps = html_soup.find(
                "article", {"class": "article__content old__article-content-single"})
            if html_soup.find("p", {"class": "article__desc"}) is not None:
                art_content_html_intro = html_soup.find(
                    "p", {"class": "article__desc"})  # prend une sous balise en trop
                art_content_html = [
                    art_content_html_intro, art_content_html_corps]
                art_content = (art_content_html_intro.get_text(
                ) + art_content_html_corps.get_text()).replace("\xa0", "")
            else:
                art_content_html = art_content_html_corps
                art_content = art_content_html_corps.get_text().replace("\xa0", "")
                # REPLACE NE MARCHE PAS
        except:
            # problems with https://www.lemonde.fr/transition-ecologique/article/2020/08/03/les-villes-et-leurs-jumeaux-numeriques_6048030_179.html
            art_content_html = np.nan
            art_content = np.nan

        # art_lang
        art_lang = TextBlob(art_content).detect_language()

        art_content_html_str = str(art_content_html)

        # return art_content
        new_row = [art_content, art_content_html_str, art_published_datetime, art_lang,
                   art_title, art_url, src_name, src_type, src_url, art_img, art_auth, art_tag]
        return new_row

    @staticmethod
    def scrap_usinenouvelle(url: str) -> list:
        """Documentation
        function which from a url creates a BeautifulSoup object, then extract different informations about the article and the 
        source. Then researches informations about the article and the website. It finally returns all this data as a list

        Parameters:
            url: The url that we will scrap 

        Out:
            list: it contains some propreties of the article and the sources 

        """
        response = requests.get(url)
        html_soup = BeautifulSoup(response.text, "html.parser")

        src_type = "xpath_source"
        src_url = BigScraper.get_base_url(url)
        src_name = "L'Usine Nouvelle"

        # find the article URL (art_url)
        if html_soup.find("meta", {"property": "og:url"}) is not None:
            art_url = html_soup.find("meta", {"property": "og:url"})["content"]
        else:
            art_url = url

        # find the article Title (art_title)
        art_title = html_soup.title.get_text().replace("\xa0", "")

        # find the article Author (art_auth)
        if html_soup.find("meta", {"itemprop": "name"}) is not None:
            art_auth = html_soup.find("meta", {"itemprop": "name"})["content"]
            if art_auth == []:
                art_auth = np.nan
        else:
            art_auth = np.nan

        # find the date of publication of the article (art_published_datetime) (format: datetime)
        if html_soup.find("meta", {"name": "lastmod"}) is not None:
            art_published = html_soup.find("meta", {"name": "lastmod"})[
                "content"][:10]      # take the date and remove the hour
            art_published_datetime = datetime.datetime.strptime(
                art_published, "%Y-%m-%d").date()  # put at the format datetime
        elif html_soup.find("time") is not None:
            art_published = html_soup.find("time")["datetime"][:10]
            art_published_datetime = datetime.datetime.strptime(
                art_published, "%Y-%m-%d").date()
        # if there is no date, we replace None with the date of today
        else:
            art_published_datetime = datetime.datetime.today().date()     #

        # src_img
        if html_soup.find("meta", {"property": "og:image"}) is not None:
            art_img = html_soup.find(
                "meta", {"property": "og:image"})["content"]

        else:
            art_img = np.nan

        # art_tag
        art_tag = []
        if html_soup.find_all("meta", {"itemprop": "keywords"}) is not None:
            html_tag = html_soup.find_all("meta", {"itemprop": "keywords"})
            for i in html_tag:
                tag_i = i["content"]
                art_tag.append(tag_i)
        else:
            art_tag = np.nan

        #art_content_html  and  art_content
        art_content_html_intro = html_soup.find("h2", {"class": "chapo"})
        art_content_html_corps = html_soup.find(
            "div", {"class": "contenuArt"})  # prend une sous balise en trop
        art_content_html = [art_content_html_intro, art_content_html_corps]
        art_content = art_content_html_intro.get_text(
        ) + art_content_html_corps.get_text().replace("\'", " ' ")      # REPLACE NE MARCHE PAS

        # art_lang
        a = TextBlob(art_content)
        art_lang = a.detect_language()

        art_content_html_str = str(art_content_html)

        return [art_content, art_content_html_str, art_published_datetime, art_lang, art_title, art_url, src_name, src_type, src_url, art_img, art_auth, art_tag]

    @staticmethod
    def scrap_linternaute(url: str) -> list:
        """Documentation
        function which from a url creates a BeautifulSoup object, then extract different informations about the article and the 
        source. Then researches informations about the article and the website. It finally returns all this data as a list

        Parameters:
            url: the url that we will scrap 

        Out:
            list: it contains some propreties of the article and the sources 

        """
        response = requests.get(url)
        html_soup = BeautifulSoup(response.text, "html.parser")

        src_type = "xpath_source"
        src_url = BigScraper.get_base_url(url)
        src_name = "L'internaute"

        # find the article URL (art_url)
        if html_soup.find("meta", {"property": "og:url"}) is not None:
            art_url = html_soup.find("meta", {"property": "og:url"})["content"]
        else:
            art_url = url

        # find the article Title (art_title)
        art_title = html_soup.title.get_text().replace("\xa0", "")

        # find the article Author (art_auth)
        if html_soup.find("a", {"rel": "author"}) is not None:
            art_auth = html_soup.find("a", {"rel": "author"}).get_text()
            if art_auth == []:
                art_auth = np.nan
        else:
            art_auth = np.nan

        # find the date of publication of the article (art_published_datetime) (format: datetime)
        if html_soup.find("time") is not None:
            date = html_soup.find("time")["datetime"]
            # remove the hour of the date
            art_published = date[:10]
            art_published_datetime = datetime.datetime.strptime(
                art_published, "%Y-%m-%d").date()  # put at the format datetime
        # if there is no date we put the date of implement
        else:
            art_published_datetime = datetime.datetime.today().date()

        # src_img
        if html_soup.find("meta", {"property": "og:image"}) is not None:
            img = html_soup.find("meta", {"property": "og:image"})["content"]
            art_img = img
        else:
            art_img = np.nan

        # art_tag
        art_tag = []
        if html_soup.find_all("meta", {"name": "keywords"}) is not None:
            html_tag = html_soup.find_all("meta", {"name": "keywords"})
            for i in html_tag:
                tag_i = i["content"]
                art_tag.append(tag_i)
        elif (html_soup.find_all("div", {"name": "tag[]"}) is not None) or (html_soup.find_all("div", {"name": "tag[]"})):
            html_tag = html_soup.find_all("div", {"name": "tag[]"})
            for i in html_tag:
                tag_i = i.get_text()
                art_tag.append(tag_i[1:])
        else:
            art_tag = np.nan

        #art_content_html  and  art_content
        art_content_html = html_soup.find("div", {"id": "jArticleInside"})
        art_content = art_content_html.get_text().replace("\xa0", "")

        # art_lang
        a = TextBlob(art_content)
        art_lang = a.detect_language()

        art_content_html_str = str(art_content_html)

        return [art_content, art_content_html_str, art_published_datetime, art_lang, art_title, art_url,
                src_name, src_type, src_url, art_img, art_auth, art_tag]

    @staticmethod
    def scrap_generic(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Getting content
        list_balises = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'b', 'strong', 'i', 'em',
                        'pre', 'mark', 'small', 'del', 's', 'ins', 'u', 'sub', 'sup', 'dfn', 'p', 'span', 'ul', 'li']
        if soup.find('article') is not None:
            content_html = soup.find('article')
            if soup.find('article').find_all(list_balises, recursive=False):
                content = soup.find('article').find_all(
                    list_balises, string=True)
                content = ' '.join(tag.text for tag in content)
            else:
                list_p = soup.find('article').find_all(
                    'div', recursive='False')
                list_parent_p = [p.parent for p in list_p]
                if len(set(list_parent_p)) == 1:
                    content_html = list_parent_p[0]
                    content = ' '.join(
                        tag.text for tag in content_html.children if tag.name in list_balises)
                else:
                    content_html = soup.find('article')
                    content = [el.get_text() for el in list_parent_p]
                    content = ' '.join(content)
        else:
            list_div = list()
            for el in soup.find_all('div'):
                if el.find_all('p', recursive=False):
                    list_div.append(el)
            index_max = np.argmax([len(block.find_all('p'))
                                   for block in list_div])
            content_html = list_div[index_max]
            content = ' '.join(
                tag.text for tag in content_html.children if tag.name in list_balises)

        content = content.replace('\xa0', '').replace(
            '\t', '').replace('\r', '').strip()
        content_html_str = str(content_html)

        # Getting date of publication
        if soup.find("meta", {"property"
                              "article:modified_time"}) is not None:
            date = soup.find("meta", {"property"
                                      "article:modified_time"})["content"]
        elif soup.find("meta", {"property": "article:published_time"}) is not None:
            date = soup.find("meta", {"property": "article:published_time"})[
                "content"]
        else:
            date = datetime.date.today()

        # Getting language
        art_lang = TextBlob(content).detect_language()

        # Getting title
        if soup.find("meta", {"property": "og:title"}) is not None:
            title = soup.find("meta", {"property": "og:title"})["content"]
        elif soup.find("title") is not None:
            title = soup.find("title").get_text()
        else:
            title = np.nan

        # Getting article url
        if soup.find("meta", {"property": "og:url"}) is not None:
            art_url = soup.find("meta", {"property": "og:url"})["content"]
        elif soup.find("link", rel="canonical"):
            art_url = soup.find("link", rel="canonical")["href"]
        else:
            art_url = url

        # Getting source url
        src_url = BigScraper.get_base_url(art_url)

        # Getting source name
        if soup.find("meta", {"property": "og:site_name"}) is not None:
            src_name = soup.find("meta", {"property": "og:site_name"})[
                "content"]
        else:
            src_name = art_url.split(r"//")
            if "http" in src_name[0]:
                src_name = src_name[1]
            else:
                src_name = src_name[0]
            src_name = src_name.split(r"/")[0]
            for i in ["fr.", "www.", "www2.", ".org", ".fr", ".eu", ".net", ".com"]:
                src_name = src_name.replace(i, "")

        # Source type
        src_type = "xpath_source"

        # Getting image
        if soup.find("meta", {"property": "og:image"}) is not None:
            art_img = soup.find("meta", {"property": "og:image"})["content"]
        else:
            art_img = np.nan

        # Getting author
        if soup.find("meta", {"name": "author"}) is not None:
            art_auth = soup.find("meta", {"name": "author"})[
                "content"].split(",")
        elif soup.find("meta", {"name": "twitter:data1"}) is not None:
            art_auth = soup.find("meta", {'name': "twitter:data1"})[
                "content"].split(",")
        elif soup.find("meta", {"property": "sage:author"}) is not None:
            art_auth = soup.find("meta", {"property": "sage:author"})[
                "content"].split(",")
        else:
            art_auth = np.nan

        # Getting tags
        if soup.find("meta", {"name": "keywords"}) is not None:
            art_tag = soup.find("meta", {"name": "keywords"})[
                "content"].split(",")
        elif soup.find("meta", {"sage": "sageTags"}) is not None:
            art_tag = soup.find("meta", {"sage": "sageTags"})[
                "content"].split(",")
        elif soup.find("meta", {"property": "article:tag"}) is not None:
            art_tag = soup.find("meta", {"property": "article:tag"})[
                "content"].split(",")
        else:
            art_tag = np.nan

        return [content, content_html_str, date, art_lang, title, art_url, src_url, src_name, src_type, art_img, art_auth, art_tag]

    @staticmethod
    def assign_scraper(url: str) -> BigScraper:
        # Jason
        if "https://changethework.com/" in url:
            return BigScraper.scrap_changethework(url)
        # Marianne
        elif "https://www.fnccr.asso.fr/article/" in url:
            return BigScraper.scrap_fncrr(url)
        elif "https://www.cnil.fr/" in url:
            return BigScraper.scrap_cnil(url)
        elif "https://www.journaldunet.com/" in url:
            return BigScraper.scrap_jdn(url)
        elif "https://www.zdnet.fr/" in url:
            return BigScraper.scrap_zdnet(url)
        elif "https://grh-multi.net/" in url:
            return BigScraper.scrap_grhmulti(url)
        # Louis
        elif "http://sabbar.fr/" in url:
            return BigScraper.scrap_sabbar(url)
        elif "https://www.lebigdata.fr/" in url:
            return BigScraper.scrap_lebigdata(url)
        elif "https://www.cadre-dirigeant-magazine.com/" in url:
            return BigScraper.scrap_cadre(url)
        elif "https://www.sap.com/" in url:
            return BigScraper.scrap_sap(url)
        elif "https://www.data.gouv.fr/" in url:
            return BigScraper.scrap_datagouv(url)
        elif "https://blockchainfrance.net" in url:
            return BigScraper.scrap_blockchain(url)
        elif "https://www.weka.fr/" in url:
            return BigScraper.scrap_weka(url)
        # Michael
        elif "https://www.theinnovation.eu/" in url:
            return BigScraper.scrap_theinnovation(url)
        elif "https://www.myrhline.com/" in url:
            return BigScraper.scrap_myrhline(url)
        elif "https://www.usine-digitale.fr/" in url:
            return BigScraper.scrap_usinedigitale(url)
        # Rémy
        elif "https://www.lemondeinformatique.fr/" in url:
            return BigScraper.scrap_lemondeinformatique(url)
        elif "https://www.erudit.org/fr/" in url:
            return BigScraper.scrap_erudit(url)
        elif "https://citoyen-ne-s-de-marseille.fr/" in url:
            return BigScraper.scrap_citmar(url)
        elif "https://www.digitalrecruiters.com/" in url:
            return BigScraper.scrap_digitrec(url)
        elif "https://hellofuture.orange.com/" in url:
            return BigScraper.scrap_hellofuture(url)
        elif "https://www.silicon.fr/" in url:
            return BigScraper.scrap_silicon(url)
        # Sibel
        elif "https://www.riskinsight-wavestone.com/" in url:
            return BigScraper.scrap_riskinsight(url)
        elif "https://www.parlonsrh.com/" in url:
            return BigScraper.scrap_parlonsrh(url)
        elif "https://www.inserm.fr/" in url:
            return BigScraper.scrap_inserm(url)
        elif "https://www.lemonde.fr/" in url:
            return BigScraper.scrap_lemonde(url)
        elif "https://www.usinenouvelle.com/" in url:
            return BigScraper.scrap_usinenouvelle(url)
        elif "https://www.linternaute.fr/" in url:
            return BigScraper.scrap_linternaute(url)
        return BigScraper.scrap_generic(url)

    def scrap(self: BigScraper, url: str) -> list:
        """Documentation

        Parameters:
            url: url of an article to scrap

        Out:
            row: Data scraped from the article

        """
        row = BigScraper.assign_scraper(url)
        # self.add_row(row)
        return row
