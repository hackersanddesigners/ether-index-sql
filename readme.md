ether-index-sql
===============

a python plugin for etherpad, that reads from the SQL database etherpad-lite is running from, and build up a one-page with a list of all the pads, plus some useful details for each.

there is a node-js version that uses etherpad’s APIs to do the same.

i just thought that having to first get a list of all the pads’ id, and then do another call to get the “useful details“ was a bit silly. but that’s what etherpad APIs provides.

reading straight from the db could be faster (?) and just one call. also, no javascript involved at all.

next version will be in C, lol.

## how to get a list of all the pads

[ref](https://github.com/ether/etherpad-lite/wiki/How-to-list-all-pads)

```
select distinct substring(store.key,5,locate(":",store.key,5)-5) as "pads" from store where store.key like "pad:%";
```
