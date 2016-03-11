import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import json
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
    result = cur.fetchall()

    # list of dates
    date = []
    # list of close price
    price = []

    for i in result:
        date_formatted = (str(i['date_stock'])[0:10]).split("-")
        date.append(date_formatted[0]+""+date_formatted[1]+""+date_formatted[2])
        price.append(float(i['close_price']))

    return date, price

def plot_graph(data):
    print("Data plotted")


def draw_window(my_dpi):

    fig = plt.figure(figsize=(800/my_dpi, 700/my_dpi), dpi=96, edgecolor='k', facecolor='black')
    fig.suptitle("PIECEWISE SEGMENTATION INTERPOLATION", fontsize="15", color="white")

    ax1 = plt.subplot2grid((3, 3), (0, 0), colspan=3)
    ax1.grid(True, color='#949494')
    ax1.yaxis.label.set_color("w")
    ax1.xaxis.label.set_color("w")
    ax1.tick_params(axis='y', colors='w')
    ax1.tick_params(axis='x', colors='w')
    plt.ylabel('Stock Price')
    plt.title("Sliding window", color='w')

    ax2 = plt.subplot2grid((3, 3), (1, 0), colspan=3)
    ax2.grid(True, color='#949494')
    ax2.yaxis.label.set_color("w")
    ax2.xaxis.label.set_color("w")
    ax2.tick_params(axis='y', colors='w')
    ax2.tick_params(axis='x', colors='w')
    plt.ylabel('Stock Price')
    plt.title("Top down", color='w')

    ax3 = plt.subplot2grid((3, 3), (2, 0), colspan=3)
    ax3.grid(True, color='#949494')
    ax3.yaxis.label.set_color("w")
    ax3.xaxis.label.set_color("w")
    ax3.tick_params(axis='y', colors='w')
    ax3.tick_params(axis='x', colors='w')
    plt.ylabel('Stock Price')
    plt.title("Bottom up", color='w')

    plt.subplots_adjust(hspace=0.3)
    plt.show()

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
    date, price = fetch_data_from_db(connection, stock)

    print(date)
    print(price)

    # Figure is built
    draw_window(MY_DPI)



