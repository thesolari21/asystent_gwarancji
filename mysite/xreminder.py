import mysql.connector
import os
import environ
import smtplib, ssl, logging
from email.message import EmailMessage
from datetime import date

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

# SQL statement
sql_statement = """
select name, description, date_warranty_to from asystent_gwarancji_receipt
where status = 1 and date_warranty_to > '2024-01-01';
"""


def run_sql_statement(sql_statement):
    # Konfiguracja połączenia z bazą danych

    config = {
        'user': env('DATABASE_USER'),
        'password': env('DATABASE_PASS'),
        'host': env('DATABASE_HOST'),
        'database': env('DATABASE_NAME'),
        'raise_on_warnings': True
    }

    try:
        # Utworzenie połączenia z bazą danych
        with mysql.connector.connect(**config) as connection:
            with connection.cursor(buffered=True) as cursor:
                cursor.execute(sql_statement)

                #pobierz wszystkie wiersze wynikowe z zapytania
                rows = cursor.fetchall()

                if rows:

                    result_list = []
                    for row in rows:
                        #kazdy wiersz spakuj do slownika
                        dict_receipts = dict(zip(["name","description","date_warranty_to"], row))
                        #a slowniki do listy
                        result_list.append(dict_receipts)

                    return result_list

    except mysql.connector.Error as error:
        print("Błąd wykonania wyrażenia SQL:", error)

def sendmail(receipts):

    ####    nagłówek    ####
    head = """
            <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Prosty Email</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                }
        
                table {
                    width: 100%;
                    max-width: 600px;
                    margin: 20px auto;
                    border-collapse: collapse;
                    background-color: #ffffff;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
        
                th, td {
                    padding: 15px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }
        
                th {
                    background-color: #f2f2f2;
                }
        
                h1 {
                    text-align: center;
                    color: #333333;
                }
            </style>
        </head>
            """

    ####    lista wyników   ####
    result_list = ""
    for receipt in receipts:

        formatted_date = receipt["date_warranty_to"].strftime("%d %m %Y")
        temp = f"""
                <tr>
                <td>{receipt["name"]}</td>
                <td>{receipt["description"]}</td>
                <td>{formatted_date}</td>
                </tr>
                """
        result_list = result_list + temp

    ####    body    ####
    body = f"""
            <body>
            <h1>Te gwarancje niedługo wygasną</h1>
            <table>
                <thead>
                    <tr>
                        <th>Nazwa</th>
                        <th>Opis</th>
                        <th>Wygasa</th>
                    </tr>
                </thead>
                <tbody>
                    {result_list}
                </tbody>
            </table>
             </body>
            </html>        
            """

    # sklejamy w całość
    content= head + body

    # wysyłamy maila
    try:
        port = 465  # For SSL
        smtp_server = env('EMAIL_HOST')
        sender_email = env('EMAIL_HOST_USER')
        receiver_email = env('EMAIL_RECEIVER')
        password = env('EMAIL_HOST_PASSWORD')

        msg = EmailMessage()
        msg['Subject'] = 'Wygasające gwarancje! '
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg.set_content(content, subtype='html')

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.send_message(msg)
        print('Wysłano')

    except Exception as e:
        logging.exception('Mail function problem')
        print(e)

    return None


if __name__ == "__main__":
    receipts = run_sql_statement(sql_statement)

    if receipts:
        sendmail(receipts)
    else:
        print("Nic nowego")