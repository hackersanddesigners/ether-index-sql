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

to store db credentials and etherpad’s base url to redirect pads to, we use a `.env`.

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
EP_LINK=https//...
FILTER=__NOINDEX__
```

`FILTER` takes a string to use for filtering out pads: the basic rule is to put this special word on the first line of the pad, and this will tell the app to not display that pad on the final index page.

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

due to etherpad-lite’s useless way to use SQL — they are dumping the whole json database into one table with two columns (`store.key`, `store.value`), querying from SQL is far from easy and efficient. a row can be either the actual pad, or a revision entry for a specific pad.

given this, a way to get good performance (eg page load-time), is the following:

- fetch all pad titles 
- loop over them and fetch correct SQL row with pad content; get number of authors [1] and revisions value [2]
- use the revision value to build another query that matches the store.key of that pad latest revisions, to get the timestamp value

i’m a SQL noob, so probably it’s possible to combine more queries into one for this use case, but as a prototype this works fine.

[1]: to get author numbers, we loop over a field called ‘numToAttrib‘ that contains a bunch of keys, including authors; we take these and sum them up
[2]: by simply trying to understand the pad json data-structure, turned out that the `head` field is a reference to the number of pad’s revisions, which we can use to construct the store.key value to the correct SQL row of that revision

## todos / ideas

- [ ] add search function
- [ ] add sort-by each key (title, timestamp, revisions number, authors number) (now it’s sorted by most recent edited pad)
- [ ] add paging to result? possible but to get result in chronological order we need to query the whole database anyway

it would be nice to build a database mapper / adapter from the json data-structure to a meaningful SQL structure. so query would be way more efficient, the app code would do less, etc.
