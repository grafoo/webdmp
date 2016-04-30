#! /usr/bin/env python2

from argon2 import PasswordHasher
from flask import (
    g,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    Flask
)
import json
import os
import sqlite3


app = Flask(__name__)
app.config.from_object('config.DevelConfig')


def get_sqlite_database():
    return sqlite3.connect(app.config['DATABASE'])


def insert_bookmark(name='', url=''):
    try:
        g.db.execute(
            'insert into bookmarks (name, url) values (?, ?)', [name, url]
        )
        g.db.commit()
    except sqlite3.IntegrityError, e:
        # in case of an existing url return the bookmark id
        # todo: replace this hack in favor of more atomic functions
        return g.db.execute(
            'select id from bookmarks where url = ?', (url,)
        ).fetchone()[0]
    return g.db.execute('select last_insert_rowid()').fetchone()[0]


def insert_tag(name=''):
    g.db.execute('insert into tags (name) values (?)', (name,))
    g.db.commit()
    return g.db.execute('select last_insert_rowid()').fetchone()[0]


def get_tag_id(tag_name=''):
    tag_id = g.db.execute(
        'select id from tags where name = ?', (tag_name,)
    ).fetchone()
    if tag_id is not None:
        return tag_id[0]
    else:
        return insert_tag(name=tag_name)


def insert_bookmark_tag(bookmark_id, tag_id):
    g.db.execute(
        'insert into bookmark_tags (bookmark_id, tag_id) values (?, ?)',
        [bookmark_id, tag_id]
    )
    g.db.commit()


def select_bookmark(name=''):
    try:
        return g.db.execute(
            'select url from bookmarks where name = ?', (name,)
        ).fetchone()[0]
    except:
        return 'not found'


def get_bookmark_record(url=''):
    try:
        bookmark_id = g.db.execute(
            'select id from bookmarks where url = ?', (url,)
        ).fetchone()[0]
        cursor = g.db.execute(
            '''select name from tags
                where id in (
                 select tag_id from bookmark_tags where bookmark_id = ?
                )
            ''', (bookmark_id,)
        )
        tags = [{'tag': row[0]} for row in cursor.fetchall()]
        bookmark_tuple = g.db.execute(
            'select name, url from bookmarks where url = ?',
            (url,)
        ).fetchone()
        bookmark_record = {
            'name': bookmark_tuple[0],
            'url': bookmark_tuple[1],
            'tags': tags
        }
        return bookmark_record
    except Exception, e:
        return False


def select_bookmark_tag_id(bookmark_id, tag_id):
    return g.db.execute(
        'select id from bookmark_tags where bookmark_id = ? and tag_id = ?',
        (bookmark_id, tag_id,)
    ).fetchone()


def make_value_list_query_string(len=0):
    return ', '.join('?' * len)


def select_bookmarks_on_tagnames(tagnames):
    tagnames_len = len(tagnames)
    cursor = g.db.execute(
        '''select b.url, b.name from bookmarks as b
            join bookmark_tags as bt where b.id = bt.bookmark_id
            and bt.tag_id in (select id from tags where name in ({0}))
            group by b.url having count (b.url) = ?
        '''.format(make_value_list_query_string(tagnames_len)),
        tuple(tagnames) + (tagnames_len,)
    )
    return [{'url': row[0], 'title': row[1]} for row in cursor.fetchall()]


@app.before_request
def before_request():
    g.db = get_sqlite_database()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bookmark', methods=['GET', 'POST'])
def bookmark():
    if 'authenticated' in session:
        if request.method == 'POST':
            bookmark_id = insert_bookmark(
                name=request.form['name'],
                url=request.form['url']
            )
            tags = request.form.getlist('tag-list')
            if not tags:
                tag_id = get_tag_id(tag_name='notag')
                insert_bookmark_tag(bookmark_id, tag_id)
            else:
                for tag in tags:
                    tag_id = get_tag_id(tag)
                    bookmark_tag_id = select_bookmark_tag_id(
                        bookmark_id,
                        tag_id
                    )
                    if bookmark_tag_id is None:
                        insert_bookmark_tag(bookmark_id, tag_id)
            return redirect(request.form['url'])
        else:
            bookmark_record = get_bookmark_record(url=request.args['url'])
            if bookmark_record:
                return render_template(
                    'bookmark.html',
                    options=bookmark_record['tags'],
                    items=[item['tag'] for item in bookmark_record['tags']],
                    page=bookmark_record['url'],
                    name=bookmark_record['name']
                )
            else:
                return render_template(
                    'bookmark.html',
                    page=request.args['url'],
                    name=request.args['name']
                )
    else:
        return render_template('base.html')


@app.route('/tag', methods=['GET', 'POST'])
def tag():
    if 'authenticated' in session:
        if request.method == 'POST':
            g.db.execute(
                'insert into tags (name) values (?)', (request.form['name'],)
            )
            return '{} saved'.format(request.form['name'])
        else:
            query = request.args.get('query')
            cursor = g.db.execute(
                'select name from tags where name like ?', ('%' + query + '%',)
            )
            tags = [{'tag': row[0]} for row in cursor.fetchall()]
            return json.dumps(tags)


@app.route('/search')
def search():
    if 'authenticated' in session:
        if 'tag_names' in request.args:
            tag_names = request.args.get('tag_names').split(',')
        return json.dumps(select_bookmarks_on_tagnames(tag_names))


@app.route('/login', methods=['POST'])
def login():
    username = request.form['login_username']
    password = request.form['login_password']
    redirect_location = request.form['redirect_location']
    try:
        if PasswordHasher().verify(app.config['PASSWD'][username], password):
            session['authenticated'] = True
    except:
        print('login for {0} failed with wrong password'.format(username))
    return redirect(redirect_location)


@app.route('/logout')
def logout():
    if 'authenticated' in session:
        session.pop('authenticated')
    return 'logout successful'


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/x-icon'
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)
