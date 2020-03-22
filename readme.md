ether-index-sql
===============

a python plugin for etherpad, that reads from the SQL database etherpad-lite is running from, and build up a one-page with a list of all the pads, plus some useful details for each.

i began a `node-js` version that uses etherpad’s APIs to do the same. might finish it as a fully client-side app (the opposite of this one).

i just thought that having to first get a list of all the pads’ id, and then do another call to get the “useful details“ was a bit silly. but that’s what etherpad APIs provides.

reading straight from the db could be faster (?) and just one call. also, no javascript involved at all.

next version will be in `C`, lol.

## how to get a list of all the pads

[ref](https://github.com/ether/etherpad-lite/wiki/How-to-list-all-pads)

```
select distinct substring(store.key,5,locate(":",store.key,5)-5) as "pads" from store where store.key like "pad:%";
```

using a slightly simpler version of this, as the `pad.value` is a json string like pad.key, but more complex. easier to work that out in python.

## todos / ideas

- [ ] add search function
- [ ] add sort-by each key (title, timestamp, revisions number, authors number) (now it’s sorted by most recent edited pad)
- [ ] grab author’s color hex value, and build a gradient out of them all?

