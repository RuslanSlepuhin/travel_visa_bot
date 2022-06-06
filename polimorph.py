
# Росс(ии) = Росс(ия)
# Лихтенштейн(а) = Лихтенштейн()
# Французск(ой) = Французск(ая)
# Багамск(их) = Багамск(ие)
# остров(ов) = остров(а)
# Герцоговин(ы) = Герцоговин(а)

def ends_of_words(word:str):

      mss = []
      str = ''
      word = word.replace('Флаг ', '')
      word = word.replace('флаг', '')
      mss = word.split()

      for i in mss:
            if i == "России":
                  str = str + 'Россия '
                  break
            if i == "Туркмении":
                  str = str + 'Туркменистан '
                  break
            if i == "Молдавии":
                  str = str + 'Молдова '
                  break
            if i == "Британии":
                  str = str + 'Великобритания '
                  break
            if i[-2:] == 'ла' or i[-2:] == 'са' or i[-2:] == 'ра':
                  str = str + i[:-1] + ' '
            elif i[-1:] == 'ы':
                  str = str + i[:-1] + 'а '
            elif i[-2:] == 'на':
                  str = str + i[:-2] + 'н '
            elif i[-2:] == 'ии':
                  str = str + i[:-2] + 'ия '
            elif i[-2:] == 'ев':
                  str = str + i[:-2] + 'и '
            elif i[-2:] == 'ой':
                  str = str + i[:-2] + 'ая '
            elif i[-2:] == 'их':
                  str = str + i[:-2] + 'ие '
            elif i[-4:] == 'ного':
                  str = str + i[:-3] + 'ый '
            elif i[-4:] == 'кого':
                  str = str + i[:-3] + 'ий '
            elif i[-2:] == 'ых':
                  str = str + i[:-2] + 'ые '
            elif i[-2:] == 'еи':
                  str = str + i[:-2] + 'ея '
            elif i[-2:] == 'си':
                  str = str + i[:-2] + 'сь '
            elif i[-2:] == 'ов':
                  str = str + i[:-2] + 'а '
            elif i[-2:] == 'ки':
                  str = str + i[:-2] + 'ка '
            elif i[-4:] == 'анда':
                  str = str + i[:-4] + 'анда'
            elif i[-2:] == 'да':
                  str = str + i[:-2] + 'ды '
            elif i[-2:] == 'ши':
                  str = str + i[:-2] + 'ша '
            elif i[-2:] == 'ля':
                  str = str + i[:-2] + 'ль '
            elif i[-2:] == 'ды':
                  str = str + i[:-2] + 'да '
            elif i[-2:] in ['ка', 'ша', 'га', 'ма', 'та', 'за', 'Да', 'Ра']:
                  str = str + i[:-1] + ' '
            else:
                  str = str + i + ' '

      return str[:-1]


# Египта
# Тринидады
# Филиппин
# Мальдив
# Китая
# Камбоджи
# Нидерландов - Нидерланда