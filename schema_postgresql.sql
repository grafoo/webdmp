create table bookmarks (
    id serial,
    name text,
    url text,
    unique (url),
    primary key (id)
);

create table tags (
    id serial,
    name text,
    unique (name),
    primary key (id)
);

create table bookmark_tags (
    id serial,
    bookmark_id integer,
    tag_id integer,
    foreign key (bookmark_id) references bookmarks (id),
    foreign key (tag_id) references tags (id),
    primary key (bookmark_id, tag_id)
);

