# webdmp


## about

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
  -H /path/to/webdmp/app
```

### uwsgi production config
```
cat > /etc/nginx/nginx.conf <<EOF
server {
      listen       443 ssl;
      server_name  localhost;

      ssl_certificate      /etc/nginx/chain.pem;
      ssl_certificate_key  /etc/nginx/privkey.pem;

      ssl_session_cache    shared:SSL:1m;
      ssl_session_timeout  5m;

      ssl_ciphers  HIGH:!aNULL:!MD5;
      ssl_prefer_server_ciphers  on;

      location / {
          try_files $uri @webtag;
      }

      location @webtag {
          include uwsgi_params;
          uwsgi_pass 127.0.0.1:9090;
      }
}
EOF
```

```
cat > /etc/uwsgi/emperor.ini <<EOF
[uwsgi]
emperor = /etc/uwsgi/vassals
uid = http
gid = http
EOF
```

```
cat > /etc/uwsgi/vassals/webdmp.ini <<EOF
[uwsgi]
socket = 127.0.0.1:9090
chdir = /path/to/webdmp/app
plugin = python2
virtualenv = /path/to/webdmp
pythonpath = /path/to/webdmp/app/webtag.py
module = webtag
callable = app
EOF
```

`systemctl start emperor.uwsgi.service`


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
