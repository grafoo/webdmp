# webdmp

browser independent bookmark and website binary store


## setup

```
virtualenv /path/to/webdmp
cd /path/to/webdmp
git clone https://github.com/grafoo/webdmp.git app
source bin/activate
pip install -r requirements.txt
./config.py init  # this will also remove any existing database

```

- install uwsgi including python plugin


### uwsgi debug config

```
cd /path/to/webdmp/app
source ../bin/activate
PYTHONPATH=/path/to/webdmp/app/webdmp.py uwsgi \
  --plugin python2 \
  --socket 127.0.0.1:9090 \
  --module webtag \
  --callable app \
  -H /path/to/app

```


## usage

- copy and paste the content of bookmarklet.js into the url field of a new bookmark
- hit the newly created bookmarklet on every page you'd like to bookmark
- create another bookmark for accessing webtag on it's default index page


## front end dependencies

- twitter-bootstrap 3.3.5
  - bootstrap.min.css
  - bootstrap.min.js

- jquery 2.1.4
  - jquery.min.js

- selectize.js 0.12.1 (standalone)
  - selectize.min.js
  - selectize.css
