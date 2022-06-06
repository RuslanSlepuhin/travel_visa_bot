
def split_str(phrase: str, split_fix: int):
    phrase_split_list = []

    split = split_fix
    while split_fix < len(phrase):
        if len(phrase) > split and phrase[split_fix] == ' ':
            temp_phrase = phrase[:split_fix]
            phrase_split_list.append(temp_phrase)
            phrase = phrase[split_fix:]
        else:
            split = split_fix
            if len(phrase) > split_fix:
                for i in reversed(phrase[:split_fix]):
                    if i == ' ':
                        temp_phrase = phrase[:split]
                        phrase_split_list.append(temp_phrase)
                        phrase = phrase[split:]
                        break
                    else:
                        split -= 1
            # else:
            #     temp_phrase = phrase
            #     phrase_split_list.append(temp_phrase)
    else:
        if phrase:
            temp_phrase = phrase
            phrase_split_list.append(temp_phrase)

    return phrase_split_list

# text = 'Все иностранные граждане и лица без гражданства, независимо от возраста, следующие транзитом через территорию Российской Федерации должны предъявить медицинский сертификат об отрицательном результате ПЦР-теста на COVID-19, сделанном не ранее, чем за 48 часа до прибытия (сертификат предъявляется в распечатанном виде, на русском или английском языках (принимается нотариально заверенный перевод на русский язык). ' \
#        'Исключения: ' \
#        'граждане Российской Федерации. ' \
#        'Более подробная информация касательно правил въезда на территорию Российской Федерации изложена в Распоряжении Правительства Российской Федерации от 16.03.2020 N 635-р.; от 18.05.2021 г. №1291-р.'
#
# res = (split_str(text, 20))
# for i in res:
#     print(i)
# print(res[0:-1])
