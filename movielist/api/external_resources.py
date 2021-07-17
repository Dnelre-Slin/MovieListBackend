import requests
import xml.etree.ElementTree as ET
import json
from rest_framework import status
from rest_framework.exceptions import NotFound


IMDB_BASE_SEARCH_URL = "https://www.imdb.com/find?q={movie_name}&s=tt"


def extract_data_title(html_dump, start_match='<script type="application/ld+json">', end_match='</script>'):
    i_start = html_dump.find(start_match)
    i_end = html_dump.find(end_match, i_start)
    print("start: " + str(i_start))
    print("end: " + str(i_end))
    reduced_data = html_dump[i_start+len(start_match):i_end]
    dict_data = json.loads(reduced_data)
    print(dict_data)


def extract_data_search(html_dump, start_match='<table', end_match='</table>'):
    result = []
    i_start = html_dump.find(start_match)
    i_end = html_dump.find(end_match)
    reduced_data = html_dump[i_start:i_end+len(end_match)]
    reduced_data = reduced_data.replace('<br>', '<br/>')
    reduced_data = reduced_data.replace('&', '&#38;')
    root = ET.fromstring(reduced_data)
    trs = root.findall('./tr')
    for tr in trs:
        data_dict = {}
        a_list = tr.findall('./td/a')
        for a in a_list:
            img = a.find('./img')
            if img is not None:
                data_dict["image"] = img.attrib["src"]
            else:
                data_dict["title"] = a.text
                data_dict["url"] = a.attrib["href"]
                data_dict["extra"] = a.tail.strip()
        result.append(data_dict)
    return result


def external_get_imdb_search(data):
    r = requests.get(IMDB_BASE_SEARCH_URL.format(**data))
    if r.status_code == status.HTTP_200_OK:
        res = extract_data_search(r.text)
        return res
    else:
        raise NotFound(detail="Could not retrive data from imdb", code=status.HTTP_404_NOT_FOUND)


# def external_get_imdb_details(data):
#     r = requests.get("https://www.imdb.com/title/tt0133093/?ref_=nv_sr_srsg_0")
#     res = extract_data_title(r.text)
#     if r.status_code == status.HTTP_200_OK:
#         res = extract_data_search(r.text)
#         return res
#     else:
#         raise NotFound(detail="Could not retrive data from imdb", code=status.HTTP_404_NOT_FOUND)