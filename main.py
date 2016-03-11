import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import json

import numpy as np
import pymysql

plt.matplotlib.rcParams.update({'font.size': 9})


def connection_to_db(path):
    """
    It opens the connection with the database by parsing the json file in which database credentials are listed
    :param path: path of the database details (i.e. username, password, ...)
    :return: the connection to the database
    """
    with open(path) as data_file:
            json_data = json.load(data_file)

    connection = pymysql.connect(host=json_data['HOST'],
                                 user=json_data['USER'],
                                 password=json_data['PASSWORD'],
                                 db=json_data['DB_NAME'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def fetch_data_from_db(db, company):
    """
    All data contanining the stock price info are retrieved from the database given the stock name
    :param db: connection name
    :param company: company name
    :return: the list of data just fetched
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM Stock_price WHERE company = %s", company)
    query_result = cur.fetchall()

    # list of dates
    result = []

    for i in query_result:
        date_formatted = (str(i['date_stock'])[0:10]).split("-")
        result.append(date_formatted[0]+""+date_formatted[1]+""+date_formatted[2]+","+str(i['close_price']))

    return result


def draw_window(my_dpi, data):

    fig = plt.figure(figsize=(1000/my_dpi, 700/my_dpi), dpi=96, edgecolor='k', facecolor='black')
    fig.suptitle("PIECEWISE SEGMENTATION INTERPOLATION", fontsize="15", color="white")

    try:
        stockFile = []
        try:
            for eachLine in data:
                splitLine = eachLine.split(',')
                if len(splitLine) == 2:
                    if 'values' not in eachLine:
                        stockFile.append(eachLine)
        except Exception as e:
            print(str(e), 'failed to organize pulled data.')
    except Exception as e:
        print(str(e), 'failed to pull pricing data')

    try:
        date, closep = np.loadtxt(stockFile, delimiter=',', unpack=True,
                                  converters={0: mdates.bytespdate2num('%Y%m%d')})
        SP = len(date)
        ax1 = plt.subplot2grid((3, 3), (0, 0), colspan=3)
        ax1.plot(date[-SP:], closep[-SP:], 'black', linewidth=1.0)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y\n%m'))
        ax1.grid(True, color='#949494')
        ax1.yaxis.label.set_color("w")
        ax1.xaxis.label.set_color("w")
        ax1.tick_params(axis='y', colors='w')
        ax1.tick_params(axis='x', colors='w')
        plt.ylabel('Stock Price')
        plt.title("Sliding window", color='w')

        ax2 = plt.subplot2grid((3, 3), (1, 0), colspan=3)
        ax2.plot(date[-SP:], closep[-SP:], 'black', linewidth=1.0)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y\n%m'))
        ax2.grid(True, color='#949494')
        ax2.yaxis.label.set_color("w")
        ax2.xaxis.label.set_color("w")
        ax2.tick_params(axis='y', colors='w')
        ax2.tick_params(axis='x', colors='w')
        plt.ylabel('Stock Price')
        plt.title("Top down", color='w')

        ax3 = plt.subplot2grid((3, 3), (2, 0), colspan=3)
        ax3.plot(date[-SP:], closep[-SP:], 'black', linewidth=1.0)
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y\n%m'))
        ax3.grid(True, color='#949494')
        ax3.yaxis.label.set_color("w")
        ax3.xaxis.label.set_color("w")
        ax3.tick_params(axis='y', colors='w')
        ax3.tick_params(axis='x', colors='w')
        plt.ylabel('Stock Price')
        plt.title("Bottom up", color='w')

        plt.subplots_adjust(hspace=0.3)
        plt.show()

        return ax1, ax2, ax3

    except e:
        print("Error")

if __name__ == '__main__':

    """
    CONSTANTS
    """
    MY_DPI = 96
    PATH_AWS_DB = 'resources/AWS_DB_details.json'

    # Connection to the database
    connection = connection_to_db(PATH_AWS_DB)

    # Data is fetched from db
    stock = input("Stock name: ")
    data = fetch_data_from_db(connection, stock)

    # Figure is built
    draw_window(MY_DPI, data)



