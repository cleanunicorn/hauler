from coinpaprika import client as Coinpaprika
import datetime
import psycopg2
import sys

# https://api.coinpaprika.com/v1/tickers/btc-bitcoin/historical?start=2017-01-01T00:00:00Z

# start
start = datetime.datetime.strptime("2015-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
# end
end = datetime.datetime.strptime("2020-12-31T23:59:59Z", "%Y-%m-%dT%H:%M:%SZ")
# coin
# coin = "btc-bitcoin"
coin = "eth-ethereum"

# Connect to database
try:
    connection = psycopg2.connect(
        user="postgres",
        password="docker",
        host="127.0.0.1",
        port="5432",
        database="postgres",
    )

    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print(connection.get_dsn_parameters(), "\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("Connected to - ", record, "\n")

    # Create table if needed
    create_table_query = """
        CREATE TABLE IF NOT EXISTS "%s"
        (
            "timestamp" timestamp without time zone NOT NULL,
            price numeric,
            volume_24h bigint,
            market_cap bigint,
            CONSTRAINT "timestamp_primary_key" PRIMARY KEY ("timestamp"),
            CONSTRAINT "timestamp_UNIQUE" UNIQUE ("timestamp")
        )
        WITH (
            OIDS = FALSE
        )
        TABLESPACE pg_default;
    """ % (
        coin
    )
    cursor.execute(create_table_query)
    connection.commit()
    print("Table {} created if needed".format(coin))

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

client = Coinpaprika.Client()

time_iterator = start

incrementor = datetime.timedelta(hours=10)


def time_format(d) -> str:
    return d.strftime("%Y-%m-%dT%H:%M:%SZ")


while time_iterator < end:
    print("Fetching {}".format(time_format(time_iterator)))

    # get data
    items = client.historical(
        coin,
        start=time_format(time_iterator),
        end=time_format(time_iterator + incrementor),
    )

    # save data
    for item in items:
        insert_price = (
            '''
            INSERT INTO public."'''
            + coin
            + """"(
            "timestamp", price, volume_24h, market_cap)
            VALUES (%s, %s, %s, %s);
        """
        )
        price_data = (
            item["timestamp"],
            item["price"],
            item["volume_24h"],
            item["market_cap"],
        )
        try:
            cursor.execute(insert_price, price_data)
        except:
            pass

    connection.commit()

    # Move to next interval
    time_iterator = time_iterator + incrementor


if connection:
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")
