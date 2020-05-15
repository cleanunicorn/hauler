# hauler

## Install

Setup Python environment.

```console
$ virtualenv ./venv
$ . ./venv/bin/activate
$ pip install -r ./requirements.txt
```

Start postgres database

```console
$ ./postgresql.sh
```

Check coinpaprika configuration and update it to your needs.

```python
# start
start = datetime.datetime.strptime("2015-01-01T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
# end
end = datetime.datetime.strptime("2020-12-31T23:59:59Z", "%Y-%m-%dT%H:%M:%SZ")
# coin
coin = "eth-ethereum"
```

`start` - Get price data starting from this moment, inclusive.
`end` - Get price data ending at from this moment, inclusive.
`coin` - What coin to scrape. The id is obtained from [this url](https://api.coinpaprika.com/v1/coins).

If you don't edit anything, it will scrape data for Ethereum, starting from 2015 up to 2020 end of year.

It will automatically create a table in the database with the coin name, in this case `eth-ethereum`.

Start the scraping by running:

```console
$ python ./coinpaprika.py
```

It will start to scrape coin prices for 5 minute intervals.

## Database snapshot

If you don't need recent price data, you can import a database snapshot. They are included in [./database](./database).