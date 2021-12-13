import pandas as pd
import matplotlib.pyplot as plt
import psycopg2


# BD connect
connection = psycopg2.connect(database="extractexcel", user="postgres", password="494NbA494", host="localhost", port="5432")

back = pd.read_sql('select * from "Main_excel" where uniq_id=\'cdd4e6ef-99a9-4892-98e1-4b187f93ff29\'', con=connection)

# Dynamic graph
ax = plt.gca()
back.plot(kind='line', figsize=(40, 10), y='amount', x='payday', ax=ax, color='red')
ax.set_xlabel('Срок платежа')
ax.set_ylabel('Задолженость рубли')
plt.title('Динамика задолжености контрагента')
plt.show()