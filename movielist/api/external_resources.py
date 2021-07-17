import requests
import xml.etree.ElementTree as ET
import json


IMDB_BASE_SEARCH_URL = "https://www.imdb.com/find?q={movie_name}&s=tt"

TEST_HTML="""<table class="findList">
<tr class="findResult odd">
<td class="primary_photo">
<a href="/title/tt0133093/?ref_=fn_tt_tt_1" >
<img src="https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_UX32_CR0,0,32,44_AL_.jpg" />
</a>
</td>
<td class="result_text">
<a href="/title/tt0133093/?ref_=fn_tt_tt_1" >
The Matrix
</a>
(1999)
</td>
</tr>
<tr class="findResult even">
<td class="primary_photo">
<a href="/title/tt0106062/?ref_=fn_tt_tt_2" >
<img src="https://m.media-amazon.com/images/M/MV5BYzUzOTA5ZTMtMTdlZS00MmQ5LWFmNjEtMjE5MTczN2RjNjE3XkEyXkFqcGdeQXVyNTc2ODIyMzY@._V1_UX32_CR0,0,32,44_AL_.jpg" />
</a>
</td>
<td class="result_text">
<a href="/title/tt0106062/?ref_=fn_tt_tt_2" >
Matrix
</a>
(1993) (TV Series)
</td>
</tr></table>"""

TEST_HTML2="""<table> <tr class="findResult odd"> <td class="primary_photo"> <a href="/title/tt5325370/?ref_=fn_tt_tt_197" ><img src="https://m.media-amazon.com/images/M/MV5BMWJlMDBhZmYtMDIxMi00Nzk5LTgwMGQtYTJjNzBlZjRlMTY2XkEyXkFqcGdeQXVyODA1NjQ0OTY@._V1_UX32_CR0,0,32,44_AL_.jpg" /></a> </td> <td class="result_text"> <a href="/title/tt5325370/?ref_=fn_tt_tt_197" >The Matrix Revolutions: Double Agent Smith</a> (2004) (Video) </td> </tr><tr class="findResult even"> <td class="primary_photo"> <a href="/title/tt5319308/?ref_=fn_tt_tt_198" ><img src="https://m.media-amazon.com/images/M/MV5BNDUzOWFjOWUtZmM5NS00M2QyLWFkYzQtOTIwZDg2ZGMwYzM5XkEyXkFqcGdeQXVyODA1NjQ0OTY@._V1_UX32_CR0,0,32,44_AL_.jpg" /></a> </td> <td class="result_text"> <a href="/title/tt5319308/?ref_=fn_tt_tt_198" >The Matrix: Follow the White Rabbit</a> (1999) (Video) </td> </tr><tr class="findResult odd"> <td class="primary_photo"> <a href="/title/tt2400262/?ref_=fn_tt_tt_199" ><img src="https://m.media-amazon.com/images/M/MV5BNTVmZTY5NzEtNmNiMC00YmZhLWJkMjgtN2E5NTE1OGQwZjVjXkEyXkFqcGdeQXVyMzA4MzMyNTU@._V1_UX32_CR0,0,32,44_AL_.jpg" /></a> </td> <td class="result_text"> <a href="/title/tt2400262/?ref_=fn_tt_tt_199" >Matrimonio</a> (2013) </td> </tr><tr class="findResult even"> <td class="primary_photo"> <a href="/title/tt1183619/?ref_=fn_tt_tt_200" ><img src="https://m.media-amazon.com/images/M/MV5BOWM5OGY0MWEtN2Y1MS00NDA5LTllNzYtNDc2ZjcxZmExMGQwXkEyXkFqcGdeQXVyMzM0NTc2MTE@._V1_UX32_CR0,0,32,44_AL_.jpg" /></a> </td> <td class="result_text"> <a href="/title/tt1183619/?ref_=fn_tt_tt_200" >El ultimo matrimonio feliz</a> (2008) (TV Series) </td> </tr></table>"""



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
    # print(reduced_data)
    root = ET.fromstring(reduced_data)
    trs = root.findall('./tr')
    # print(len(trs))
    for tr in trs:
        data_dict = {}
        td = tr.find('./td')
        # print(td)
        data_dict["extra"] = td.tail
        a_list = tr.findall('./td/a')
        # img = tr.findall('./td/a/img')
        # name = tr.findall('./td/a[text()]')
        # print(img)
        # print(name)
        # print(a_list)
        for a in a_list:
            img = a.find('./img')
            if img is not None:
                # print("Image: {}".format(img))
                data_dict["image"] = img.attrib["src"]
            else:
                data_dict["title"] = a.text
                data_dict["url"] = a.attrib["href"]
                data_dict["extra"] = a.tail.strip()
                # print("Title: {} - {}".format(a.text, a.attrib["href"]))
        result.append(data_dict)
    # root = ET.parse('test3.html')
    return result


def external_get_imdb_search(data):
    r = requests.get(IMDB_BASE_SEARCH_URL.format(**data))
    print(r.status_code)
    res = extract_data_search(r.text)
    print(res)
    # extract_data_search(TEST_HTML2)
    # r = requests.get("https://www.imdb.com/title/tt0133093/?ref_=nv_sr_srsg_0")
    # extract_data_title(r.text)