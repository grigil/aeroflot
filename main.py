import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
import re
import psycopg2.extras
import time
import uuid

# BD connect
connection = psycopg2.connect(database="extractexcel", user="postgres", password="494NbA494", host="localhost", port="5432")
psycopg2.extras.register_uuid()

# Postgresql add data
def add_data(values):
    cursor = connection.cursor()
    postgres_insert_query = """ INSERT INTO "Main_excel" (name, amount, payday, doc_number, uniq_id) VALUES (%s,%s,%s,%s,%s)"""
    record_to_insert = values
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()

# Postgresql add data uniq
def add_data_uniq(values):
    cursor = connection.cursor()
    postgres_insert_query = """ INSERT INTO "uniq_name" (uniq_id, uniq_names) VALUES (%s,%s)"""
    record_to_insert = values
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()

# Filter to uniq name
def uniq_filter(word):
    result = word.replace('"', ' ').replace('(', '').replace(')', '').replace('»', '').replace('«', '')
    result = (re.sub(r'\bПубличное акционерное общество\b', 'ПАО', result, flags=re.IGNORECASE))
    result = (re.sub(r'\bАкционерное общество\b', 'АО', result, flags=re.IGNORECASE))
    result = (re.sub(r'\bАкционерное\b', '', result, flags=re.IGNORECASE))
    result = (re.sub(r'\bАвиапредприятие\b', 'АП', result, flags=re.IGNORECASE))
    result = (re.sub(r'\bавиакомпания\b', 'АК', result, flags=re.IGNORECASE))
    result = (re.sub(r'\bAktiengesellschaft\b', 'АО', result, flags=re.IGNORECASE))
    result = (re.sub(r'\bпубличное\b', '', result, flags=re.IGNORECASE))
    result = (re.sub(r'\bобщество\b', '', result, flags=re.IGNORECASE))
    result = (re.sub(r'\bОП Анапа\b', '', result, flags=re.IGNORECASE))
    result = (re.sub(r'\bDeutche\b', 'Deutsche', result, flags=re.IGNORECASE))
    result = (re.sub(r'\b\-\b', '', result, flags=re.IGNORECASE))
    result = (re.sub(r'\bакционерное\b', '', result, flags=re.IGNORECASE))
    result = (re.sub(r'\bРоссийские авиалинии\b', '', result, flags=re.IGNORECASE))
    result = (re.sub(r'\bАО\b', '', result))
    result = (re.sub(r'\bАП\b', '', result))
    result = (re.sub(r'\bАК\b', '', result))
    result = (re.sub(r'\bПАО\b', '', result)).rstrip().lstrip()
    result = (re.sub(r'\bООО\b', '', result)).replace("  ", " ").rstrip().lstrip()
    return(result)

# Excel extract
risks = pd.read_excel('risks.xlsx', skiprows=[0], sheet_name="3 q 2021")

# Agent filter
while not risks.empty:
    uniq_name = uniq_filter(risks.iloc[0]['Имя'])
    list_names = [risks.iloc[0]['Имя']]
    uniq_id = uuid.uuid4()
    risks = risks.drop(risks.first_valid_index())
    for index, row in risks.iterrows():
        name = uniq_filter(row['Имя'])
        if name.lower() == uniq_name.lower():
            if row['Имя'] not in list_names:
                list_names.append(row['Имя'])
            values = (row['Имя'], row['Сумма, руб.'], row['Срок платежа'], row['Номер документа'], uniq_id)
            add_data(values)
            risks = risks.drop(index)
    data = (uniq_id, list_names)
    print(list_names)
    add_data_uniq(data)

# Dynamic graph
# ax = plt.gca()
# back.plot(kind='line', figsize=(40, 10), y='Сумма, руб.', x='Срок платежа', ax=ax, color='red')
# ax.set_xlabel('Срок платежа')
# ax.set_ylabel('Задолженость рубли')
# plt.title('Динамика задолжености контрагента')
# plt.show()

