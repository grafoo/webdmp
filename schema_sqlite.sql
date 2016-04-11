create table bookmarks (
    id integer primary key autoincrement,
    name text,
    url text,
    unique (url)
);

create table tags (
    id integer primary key autoincrement,
    name text,
    unique (name)
);

create table bookmark_tags (
    id integer primary key autoincrement,
    bookmark_id integer,
    tag_id integer,
    foreign key (bookmark_id) references bookmarks (id),
    foreign key (tag_id) references tags (id)
);

