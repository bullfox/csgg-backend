# csgg-backend

This repository contains all of the tools I use and have used for collection of data through the Riot API for the CSGG web application. There are some basic analytics tools that I used as well, along with some example data returned from the API queries.

### Dependencies

Running the main crawler system requires these system packages:

* python3
* mongodb

and these python modules

* requests
* pymongo
* itertools

### Getting Started

With mongodb installed, there is no need to create any databases, as the script will do that itself. Be warned that exiting and re-running the crawler will cause it so drop any of the documents created, unless they are renamed. The default document is called 'winrates'. It is as simple then as running the crawler with the below command.

```
python3 crawlervX [api_key] [rate_limit_setting] [latest_patch_unixtimestamp]
```
