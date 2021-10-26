#!/usr/bin/python

import sys
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import csv

env = Environment(loader=FileSystemLoader(f'{Path(__file__).parent}'))
template = env.get_template('template.html.j2')

publication_types = [{"name": "Publications Journals and Conferences", "data": "journals.csv", "output": "journals.html"}, {"name": "Book Chapters", "data": "books.csv", "output": "books.html"}]

for pub_type in publication_types:

        page = {"title": pub_type["name"], "author": "gravis", "description": "publications at gravis", "header": pub_type["name"]}
        publications = {}

        with open(pub_type["data"], mode='r') as input_file:
                reader = csv.reader(input_file, delimiter=";")
                for pub in reader:
                  entry = {"title": pub[1], "authors": pub[2], "publication": pub[3], "doi_link": pub[4], "pdf_file": pub[5]}
                  if len(pub) > 6 :
                    entry["extra"] = pub[6]
                  if pub[0] not in publications:
                        publications[pub[0]] = []
                  publications[pub[0]].append(entry)

        output = template.render(page=page, publications=publications, years=sorted(publications)[::-1])

        file_path_available = f"{Path(__file__).parent}/public/{pub_type['output']}"
        with open(file_path_available, "wb") as f:
          f.write(output.encode())

