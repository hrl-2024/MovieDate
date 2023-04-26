-- CREATE DATABASE IF NOT EXISTS MovieDate;
-- USE MovieDate;

DROP DATABASE IF EXISTS MovieDate;

DROP TABLE IF EXISTS CommentsOn;
DROP TABLE IF EXISTS CommentedBy;
DROP TABLE IF EXISTS Comments;
DROP TABLE IF EXISTS Likes;
DROP TABLE IF EXISTS PostsBy;
DROP TABLE IF EXISTS Post;
DROP TABLE IF EXISTS Organizes;
DROP TABLE IF EXISTS ParticipatesIn;
DROP TABLE IF EXISTS WatchParty;
DROP TABLE IF EXISTS FavorMovies;
DROP TABLE IF EXISTS FriendsWith;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
	uid				SERIAL PRIMARY KEY,
	uname 			TEXT,
	avatar			blob,
    email           TEXT NOT NULL UNIQUE,
    pwd             VARCHAR,
    favorMovies     INT ARRAY
);

CREATE TABLE FriendsWith(
    uid1           INT NOT NULL,
    uid2           INT NOT NULL,
    PRIMARY KEY (uid1,uid2),
    FOREIGN KEY (uid1) REFERENCES Users(uid) ON DELETE CASCADE,
    FOREIGN KEY (uid2) REFERENCES Users(uid) ON DELETE CASCADE
);

CREATE TABLE WatchParty(
	wid                 SERIAL PRIMARY KEY,
	ownerId             INT NOT NULL,
	movieId             INT NOT NULL,
    Dates               DATE,
    atTime              TIME,
    Platform            VARCHAR(255),
    CONSTRAINT Watch_Party_FK_OwnerId FOREIGN KEY (ownerId) REFERENCES Users(uid) ON DELETE CASCADE
);

CREATE TABLE ParticipatesIn(
	wid                 INT NOT NULL,
	parId               INT NOT NULL,
    CONSTRAINT ParticipatesIn_PK PRIMARY KEY(wid,parId),
    CONSTRAINT ParticipatesIn_ParticipateID FOREIGN KEY (parId) REFERENCES Users(uid) ON DELETE CASCADE,
    FOREIGN KEY (wid) REFERENCES WatchParty(wid) ON DELETE CASCADE
);

CREATE TABLE Post (
    pid 				SERIAL PRIMARY KEY,
    writer				INT,
    movie_id			INT,
    pdate				DATE NOT NULL,
    ptime               TIME NOT NULL,
    content 			VARCHAR(255),
    wid		            INT,
    FOREIGN KEY (writer) REFERENCES Users(uid) ON DELETE CASCADE,
    FOREIGN KEY (wid) REFERENCES WatchParty(wid) ON DELETE CASCADE
);

CREATE TABLE Comments(
	cid                 SERIAL PRIMARY KEY,
    content             TEXT NOT NULL,
    cdate               DATE NOT NULL,
    ctime               TIME NOT NULL,
    uid                 INT NOT NULL,
    pid                 INT NOT NULL,
    FOREIGN KEY(uid) REFERENCES Users ON DELETE CASCADE,
    FOREIGN KEY(pid) REFERENCES Post ON DELETE CASCADE
);

CREATE TABLE Likes(
	pid                 INT NOT NULL,
    uid                 INT NOT NULL,
    PRIMARY KEY(pid,uid),
    CONSTRAINT Likes_FK_uid FOREIGN KEY (uid) REFERENCES Users(uid) ON DELETE CASCADE,
    CONSTRAINT Likes_FK_pid FOREIGN KEY (pid) REFERENCES Post(pid) ON DELETE CASCADE
);
