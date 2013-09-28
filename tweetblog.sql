drop table if exists stack;
create table stack (
       stackid integer primary key autoincrement,
       twitter_id integer not null    references entries(twitter_id) on delete set null,
       text string not null,
       datetime text
);

drop table if exists entries;
create table entries (
       twitter_id integer  primary key, 
       oauth_token string  not null
);

PRAGMA foreign_key=true;

