#!/usr/bin/env python3
import psycopg2
import xml.etree.ElementTree as ET

conn = psycopg2.connect(user='teetotaller', password='', dbname='alkolic')
cur = conn.cursor()
OneLic = {}

for event, elem in ET.iterparse("lic.xml", events=("start","end")):
    if elem.tag == "row" and event == "end":
        OneLic.clear()
        OneLic = dict.fromkeys(['NameOrg', 'INN', 'KPPorg', 'AddressOrg', 'Email', 'AddressObj', 'KPPObj', 'CodeSubjOrg', 'CodeSubjObj', 'TypeLic', 
                   'DateEndLic', 'NumLic', 'DetailLic', 'WhoGiveLic', 'Coord'])
        for el in list(elem):
            if el.tag == "Полное_и_сокращенное_наименование_организации_сельскохозяйственного_товаропроизводителя_с_указанием_ее_ОПФ":
                OneLic['NameOrg'] = el.text
            if el.tag == "ИНН_организации_сельскохозяйственного_товаропроизводителя_":
                OneLic['INN'] = el.text
            if el.tag == "КПП_организации_сельскохозяйственного_товаропроизводителя_":
                OneLic['KPPorg'] = el.text
            if el.tag == "Адрес__место_нахождения___организации_сельскохозяйственного_товаропроизводителя_":
                OneLic['AddressOrg'] = el.text
            if el.tag == "Адрес_электронной_почты_организации_сельскохозяйственного_товаропроизводителя_":
                OneLic['Email'] = el.text
            if el.tag == "Место_нахождения__адрес__обособленного_подразделения_организации__осуществляющего_лицензируемый_вид_деятельности":
                OneLic['AddressObj'] = el.text
            if el.tag == "КПП_обособленного_подразделения_организации__осуществляющего_лицензируемый_вид_деятельности":
                OneLic['KPPObj'] = el.text
            if el.tag == "Код_субъекта_Российской_Федерации_по_месту_нахождения_организации":
                OneLic['CodeSubjOrg'] = el.text
            if el.tag == "Код_субъекта_РФ_по_месту_нахождения_обособленного_подразделения_организации__осуществляющего_лицензируемый_вид_деятельности":
                OneLic['CodeSubjObj'] = el.text
            if el.tag == "Вид_лицензируемой_деятельности_организации":
                OneLic['TypeLic'] = el.text
            if el.tag == "Дата_окончания_действия_лицензии":
                OneLic['DateEndLic'] = el.text
            if el.tag == "Номер_лицензии__соответствующий_номеру_записи_в_реестре":
                OneLic['NumLic'] = el.text
            if el.tag == "Сведения_о_действии_лицензии":
                OneLic['DetailLic'] = el.text
            if el.tag == "Орган_выдавший_лицензию":
                OneLic['WhoGiveLic'] = el.text
            if el.tag == "Координаты":
                OneLic['Coord'] = el.text
        if OneLic['DetailLic'] == 'действующая' or OneLic['DetailLic'] == 'приостановлена':
            if (OneLic['TypeLic'].lower().find('розничная') != -1) and OneLic['AddressObj'] != None:
                cur.execute(
                    "INSERT INTO lics(NameOrg, INN, KPPorg, AddressOrg, Email, AddressObj, KPPObj, CodeSubjOrg, CodeSubjObj, TypeLic, DateEndLic, NumLic, DetailLic, WhoGiveLic, Coord) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (OneLic['NameOrg'], OneLic['INN'], OneLic['KPPorg'], OneLic['AddressOrg'], OneLic['Email'], OneLic['AddressObj'], OneLic['KPPObj'], OneLic['CodeSubjOrg'], OneLic['CodeSubjObj'], OneLic['TypeLic'], OneLic['DateEndLic'], OneLic['NumLic'], OneLic['DetailLic'], OneLic['WhoGiveLic'], OneLic['Coord'])
                )
        elem.clear()
conn.commit()
