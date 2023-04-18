CREATE DATABASE IF NOT EXISTS MovieDate;
USE MovieDate;
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
    favorMovies     INT ARRAY
);

CREATE TABLE FriendsWith(
    uid1           INT NOT NULL,
    uid2           INT NOT NULL,
    PRIMARY KEY (uid1,uid2),
    FOREIGN KEY (uid1) REFERENCES Users(uid),
    FOREIGN KEY (uid2) REFERENCES Users(uid)
);

CREATE TABLE WatchParty(
	wid SERIAL PRIMARY KEY,
	ownerId INT NOT NULL,
	movieId INT NOT NULL,
    Dates DATE,
    Platform VARCHAR(255),
    CONSTRAINT Watch_Party_FK_OwnerId FOREIGN KEY (ownerId) REFERENCES Users(uid)
);

CREATE TABLE ParticipatesIn(
	wid INT NOT NULL,
	parId INT NOT NULL,
    CONSTRAINT ParticipatesIn_PK PRIMARY KEY(wid,parId),
    CONSTRAINT ParticipatesIn_ParticipateID FOREIGN KEY (parId) REFERENCES Users(uid),
    FOREIGN KEY (wid) REFERENCES WatchParty(wid)
);

CREATE TABLE Organizes(
	wid INT UNIQUE NOT NULL ,
	ownerId INT NOT NULL,
    CONSTRAINT Organizes_PK PRIMARY KEY(wid,ownerId),
    CONSTRAINT Organizes_OwnerID FOREIGN KEY (ownerId) REFERENCES Users(uid),
    FOREIGN KEY (wid) REFERENCES WatchParty(wid)
);

CREATE TABLE Post (
    pid 				SERIAL PRIMARY KEY,
    writer				INT,
    movie_id			INT,
    pdate				DATE,
    content 			VARCHAR(255),
    wid		            INT,
    FOREIGN KEY (writer) REFERENCES Users(uid),
    FOREIGN KEY (wid) REFERENCES WatchParty(wid) ON DELETE CASCADE
);

CREATE TABLE PostsBy(
	pid INT NOT NULL UNIQUE,
    uid INT NOT NULL,
    CONSTRAINT PostsBy_PK PRIMARY KEY (pid,uid),
    CONSTRAINT PostsBy_FK_pid FOREIGN KEY(pid) REFERENCES Post(pid),
    CONSTRAINT PostsBy_FK_uid FOREIGN KEY(uid) REFERENCES Users(uid)
);

CREATE TABLE Comments(
	cid SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    cdate DATE,
    uid INT,
    pid INT,
    FOREIGN KEY(uid) REFERENCES Users,
    FOREIGN KEY(pid) REFERENCES Post
);

CREATE TABLE CommentsOn(
	cid INT NOT NULL UNIQUE,
    pid INT NOT NULL,
    uid INT NOT NULL,
    PRIMARY KEY (cid,pid),
    CONSTRAINT CommentsOn_FK_cid FOREIGN KEY (cid) REFERENCES Comments(cid),
    CONSTRAINT CommentsOn_FK_pid FOREIGN KEY (pid) REFERENCES Post(pid),
    FOREIGN KEY (uid) REFERENCES Users
);

CREATE TABLE Likes(
	pid INT NOT NULL,
    uid INT NOT NULL,
    PRIMARY KEY(pid,uid),
    CONSTRAINT Likes_FK_uid FOREIGN KEY (uid) REFERENCES Users(uid),
    CONSTRAINT Likes_FK_pid FOREIGN KEY (pid) REFERENCES Post(pid)
);

--Init 2 users
INSERT INTO Users (uname, avatar) VALUES ('John Doe', NULL);
INSERT INTO Users (uname, avatar) VALUES ('Jona Doe', NULL);
