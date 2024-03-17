import requests
from bs4 import BeautifulSoup
def get_word_meaning(word):
    url = f'https://www.iciba.com/word?w={word}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        accent_list = []
        meanings3 = soup.find_all(class_='Mean_symbols__fpCmS')
        for ul in meanings3:
            uls = ul.find_all("li")
            for ul_s in uls:
                u = ul_s.get_text()
                accent_list.append(u)
        meanings_list = []
        meanings = soup.find_all(class_='Mean_part__UI9M6')
        for ul_tag in meanings:
            li_tags = ul_tag.find_all('li')
            for li in li_tags:
                type_tag = li.find('i')
                meaning_type = type_tag.text if type_tag else 'Unknown'
                description = li.find('div').text.strip()
                meaning = f'{meaning_type}: {description}'
                meanings_list.append(meaning)
        sentence_list = []
        meanings2 = soup.find_all(class_='NormalSentence_sentence__Jr9aj')
        for ul in meanings2:
            sentence_list_s = []
            en = ul.find_all(class_="NormalSentence_en__BKdCu")
            for ens in en:
                span_text = ens.find("span").text if ens.find("span") else "No span found"
                sentence_list_s.append(span_text)
            cn = ul.find_all(class_="NormalSentence_cn__gyUtC")
            for cns in cn:
                p_text = cns.text
                sentence_list_s.append(p_text)
            _from = ul.find_all(class_="NormalSentence_from__cMXrW")
            for _from_ in _from:
                _from_text = _from_.text
                sentence_list_s.append(_from_text)
            sentence_list.append(sentence_list_s)
        phrase = []
        meanings4 = soup.find_all(class_="Phrase_phrase__W3z3F")
        for ul in meanings4:
            phrase_s = []
            h5_tags = ul.find_all('h5')
            for tag in h5_tags:
                h_t = tag.text
                phrase_s.append(h_t)
            p_tags = ul.find_all('p')
            for tag in p_tags:
                p_t = tag.text
                phrase_s.append(p_t)
                # print(f'段落：{tag.text}')
            phrase.append(phrase_s)
        return accent_list,meanings_list,sentence_list,phrase
    else:
        state1 = "网络状态异常，请检查网络连接！"
        state2 = "网络状态异常，请检查网络连接！"
        state3 = "网络状态异常，请检查网络连接！"
        state4 = "网络状态异常，请检查网络连接！"
        return state1,state2,state3,state4