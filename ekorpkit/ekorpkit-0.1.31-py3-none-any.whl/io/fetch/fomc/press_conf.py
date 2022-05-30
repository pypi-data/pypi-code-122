import os
import sys
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pdfplumber

# Import parent class
from .base import FOMC


class PresConfScript(FOMC):
    """
    A convenient class for extracting press conference scripts from the FOMC website.
    It is only available from April 2011.
    """

    def __init__(self, content_type, **args):
        super().__init__(content_type, **args)
        left_pct = 0.05  # % Distance of left side of character from left side of page.
        top_pct = 0.10  # % Distance of top of character from top of page.
        right_pct = (
            0.95  # % Distance of right side of character from left side of page.
        )
        bottom_pct = 0.90  #% Distance of bottom of the character from top of page.
        self.crop_coords = [left_pct, top_pct, right_pct, bottom_pct]

    def _get_links(self, from_year):
        """
        Override private function that sets all the links for the contents to download on FOMC website
         from from_year (=min(2015, from_year)) to the current most recent year
        """
        self.links = []
        self.titles = []
        self.speakers = []
        self.dates = []

        r = requests.get(self.calendar_url)
        soup = BeautifulSoup(r.text, "html.parser")

        if self.verbose:
            print("Getting links for press conference scripts...")
        presconfs = soup.find_all(
            "a", href=re.compile("^/monetarypolicy/fomcpresconf\d{8}.htm")
        )
        presconf_urls = [
            self.base_url + presconf.attrs["href"] for presconf in presconfs
        ]
        for presconf_url in presconf_urls:
            r_presconf = requests.get(presconf_url)
            soup_presconf = BeautifulSoup(r_presconf.text, "html.parser")
            contents = soup_presconf.find_all(
                "a", href=re.compile("^/mediacenter/files/FOMCpresconf\d{8}.pdf")
            )
            for content in contents:
                # print(content)
                self.links.append(content.attrs["href"])
                self.speakers.append(
                    self._speaker_from_date(self._date_from_link(content.attrs["href"]))
                )
                self.titles.append("FOMC Press Conference Transcript")
                self.dates.append(
                    datetime.strptime(
                        self._date_from_link(content.attrs["href"]), "%Y-%m-%d"
                    )
                )
        if self.verbose:
            print("{} links found in current page.".format(len(self.links)))

        # Archived before 2015
        if from_year <= 2014:
            print("Getting links from archive pages...")
            for year in range(from_year, 2015):
                yearly_contents = []
                fomc_yearly_url = (
                    self.base_url
                    + "/monetarypolicy/fomchistorical"
                    + str(year)
                    + ".htm"
                )
                r_year = requests.get(fomc_yearly_url)
                soup_yearly = BeautifulSoup(r_year.text, "html.parser")

                presconf_hists = soup_yearly.find_all(
                    "a", href=re.compile("^/monetarypolicy/fomcpresconf\d{8}.htm")
                )
                presconf_hist_urls = [
                    self.base_url + presconf_hist.attrs["href"]
                    for presconf_hist in presconf_hists
                ]
                for presconf_hist_url in presconf_hist_urls:
                    # print(presconf_hist_url)
                    r_presconf_hist = requests.get(presconf_hist_url)
                    soup_presconf_hist = BeautifulSoup(
                        r_presconf_hist.text, "html.parser"
                    )
                    yearly_contents = soup_presconf_hist.find_all(
                        "a",
                        href=re.compile("^/mediacenter/files/FOMCpresconf\d{8}.pdf"),
                    )
                    for yearly_content in yearly_contents:
                        # print(yearly_content)
                        self.links.append(yearly_content.attrs["href"])
                        self.speakers.append(
                            self._speaker_from_date(
                                self._date_from_link(yearly_content.attrs["href"])
                            )
                        )
                        self.titles.append("FOMC Press Conference Transcript")
                        self.dates.append(
                            datetime.strptime(
                                self._date_from_link(yearly_content.attrs["href"]),
                                "%Y-%m-%d",
                            )
                        )
                if self.verbose:
                    print(
                        "YEAR: {} - {} links found.".format(
                            year, len(presconf_hist_urls)
                        )
                    )
            print("There are total ", len(self.links), " links for ", self.content_type)

    def _add_article(self, link, index=None):
        """
        Override a private function that adds a related article for 1 link into the instance variable
        The index is the index in the article to add to.
        Due to concurrent prcessing, we need to make sure the articles are stored in the right order
        """
        if self.verbose:
            sys.stdout.write(".")
            sys.stdout.flush()

        link_url = self.base_url + link
        pdf_filepath = (
            self.output_raw_dir
            + "/FOMC_PresConfScript_"
            + self._date_from_link(link)
            + ".pdf"
        )

        if not os.path.exists(pdf_filepath) or self.force_download:
            # Scripts are provided only in pdf. Save the pdf and pass the content
            res = requests.get(link_url)

            with open(pdf_filepath, "wb") as f:
                f.write(res.content)
        else:
            if self.verbose:
                print("File already exists: ", pdf_filepath)

        # Extract text from the pdf
        pdf_file_parsed = ""  # new line
        with pdfplumber.open(pdf_filepath) as pdf:
            for page in pdf.pages:
                pg_width = page.width
                pg_height = page.height
                pg_bbox = (
                    self.crop_coords[0] * float(pg_width),
                    self.crop_coords[1] * float(pg_height),
                    self.crop_coords[2] * float(pg_width),
                    self.crop_coords[3] * float(pg_height),
                )
                page_crop = page.crop(bbox=pg_bbox)
                text = page_crop.extract_text()
                pdf_file_parsed = pdf_file_parsed + "\n" + text
        paragraphs = re.sub("(\n)(\n)+", "\n", pdf_file_parsed.strip())
        paragraphs = paragraphs.split("\n")

        section = -1
        paragraph_sections = []
        for paragraph in paragraphs:
            if not re.search(
                "^(page|january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)",
                paragraph.lower(),
            ):
                if len(re.findall(r"[A-Z]", paragraph[:10])) > 5 and not re.search(
                    "(present|frb/us|abs cdo|libor|rp–ioer|lsaps|cusip|nairu|s cpi|clos, r)",
                    paragraph[:10].lower(),
                ):
                    section += 1
                    paragraph_sections.append("")
                if section >= 0:
                    paragraph_sections[section] += paragraph
        self.articles[index] = self.segment_separator.join(
            [paragraph for paragraph in paragraph_sections]
        )
