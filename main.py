import ssl
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def get_info(url):
    try:
        print(">>> ", url)
        uh = urllib.request.urlopen(url, context=ctx)
        data = uh.read().decode()
        x = BeautifulSoup(data, 'html.parser')
        x = x.prettify()

        return ET.fromstring(x)
    except:
        print("Error from get_info function")
        quit()


def get_data(soup):
    try:
        s = ''
        dic = dict()
        new_data = soup.findall('body/div/div/div/div/div/div/div/a')
        for element in new_data:
            z = element.get('href')
            x = 0
            for i in range(len(z)):
                if z[len(z) - 1 - i] == '/':
                    break
                x += 1
            s += '\n' + z[-x:] + " "
            element = element.find('div/div')
            s += element.text.strip()
            dic[z[-x:]] = element.text.strip()
        print(s)
        return dic
    except:
        print("Error from get_data function")
        quit()


def chose():
    print("\nWybierz numer:")
    return input()

# strona agh:
u = "https://sylabusy.agh.edu.pl/pl/1/2/18/1/4"

# wybór wydziału:
x = get_info(u)
departments = get_data(x)
u += '/' + '17'#chose()

# wybór kierunku:
soup = get_info(u)
majors = get_data(soup)
major = '133'#chose()
u += '/' + major

# kierunek -> zapis do pliku:
zapis = get_info(u)
new_data = zapis.findall('body/div/div/div/div/div/div/div/div/div/table/tbody')
i = 1

try:
    name = majors[major] + '.txt'
except:
    name = "Syllabus.txt"

file = open(name, 'w')
file.write(majors[major]+'\n')
for element in new_data:
    a= '\n>>>Semestr'+ str(i) + ":\n"
    print(a)
    file.write(a)
    z = element.findall('tr/td')
    for x in z:
        try:
            one = (x.find('p').text.strip())

            if one.startswith("Student wybiera") or one.startswith('Zasady wyboru'):
                print("obieralny:")
                file.write("Obieralny:\n")
        except:
            pass
        try:
            two = (x.find('span').text.strip())
            if two.startswith("Student wybiera") or two.startswith('Zasady wyboru'):
                print("obieralny:")
                file.write("Obieralny:\n")
        except:
            pass
        if x.text.strip().startswith("Student wybiera"):
            print("obieralny")
            file.write("Obieralny:\n")
        ok = x.findall("div")
        for tekst in ok:
            try:
                variable = tekst.find('a')
                print(variable.text.strip())
                file.write(variable.text.strip())
            except:
                pass
            print(tekst.text.strip())
            file.write(tekst.text.strip())
            file.write('\n')

    i+=1
file.close()