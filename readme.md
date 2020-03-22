ether-index-sql
===============

a python plugin for [etherpad-lite](https://github.com/ether/etherpad-lite/wiki/How-to-list-all-pads), that reads from the SQL database etherpad-lite is running from, and make a one-page index list of all the pads, plus some useful details for each.

## usage

### clone the repo

```
$ git clone git@github.com:hackersanddesigners/ether-index-sql.git
```

### setup python virtual environment

we’re using `pyenv` + `pipenv`. the upside is that `pipenv` works also as a package manager (better than `pip`), so we get a `Pipfile`.

you can use `virtualenv`, etc. we’re running with `python 3.7.3` (see the file `.python-version`) 

afterwards, install all the packages listed in the `Pipfile`.

### create .env

to store db credentials and etherpad’s url / port number, we use a `.env`.

```
# from the root project folder, eg /path/to/ether-index-sql/.

$ touch .env
```

then add the following with appropriate values (change them with your own values!)

```
DB_HOST=localhost
DB_USER=sql-username
DB_PASSWORD=some-pa$$word
DB_NAME=etherpad_lite_db
EP_PORT=9001
```

### run the app

```
$ python main.py
```

this starts the server, default port is `localhost:5005`.

## how to get a list of all the pads

[ref](https://github.com/ether/etherpad-lite/wiki/How-to-list-all-pads)

```
select distinct substring(store.key,5,locate(":",store.key,5)-5) as "pads" from store where store.key like "pad:%";
```

using a slightly simpler version of this, as the `pad.value` is a json string like `pad.key`, but more complex. easier to work that out in python.

## todos / ideas

- [ ] add search function
- [ ] add sort-by each key (title, timestamp, revisions number, authors number) (now it’s sorted by most recent edited pad)
- [ ] grab author’s color hex value, and build a gradient out of them all?

