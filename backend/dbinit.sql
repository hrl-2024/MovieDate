CREATE DATABASE IF NOT EXISTS MovieDate;
USE MovieDate;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Watch_Party;
DROP TABLE IF EXISTS ParticipatesIn;
DROP TABLE IF EXISTS Post;
DROP TABLE IF EXISTS PostBy;
DROP TABLE IF EXISTS Comments;
DROP TABLE IF EXISTS CommentsOn;
DROP TABLE IF EXISTS CommentedBy;
DROP TABLE IF EXISTS Likes;

CREATE TABLE Users (
	uid				INT AUTO_INCREMENT,
	uname 				TEXT,
	avatar				longblob,
	PRIMARY KEY  (uid)
);

CREATE TABLE FriendsWith(
    uid1           INT NOT NULL,
    uid2           INT NOT NULL,
    PRIMARY KEY (uid1,uid2),
    FOREIGN KEY (uid1) REFERENCES Users(uid)
    FOREIGN KEY (uid2) REFERENCES Users(uid)
);

CREATE TABLE FavorMovies(
    uid            INT NOT NULL,
    movieID       INT NOT NULL,
    PRIMARY KEY (uid,movieID),
    FOREIGN KEY (uid) REFERENCES Users(uid)
);

CREATE TABLE Watch_Party(
	wid INT AUTO_INCREMENT,
	ownerId INT NOT NULL,
	movieId INT NOT NULL,
    Dates DATETIME,
    Platform VARCHAR(255),
    CONSTRAINT Watch_Party_PK PRIMARY KEY (wid),
    CONSTRAINT Watch_Party_FK_OwnerId FOREIGN KEY (ownerId) REFERENCES Users(uid)
);

CREATE TABLE ParticipatesIn(
	wid INT NOT NULL,
	parId INT NOT NULL,
    CONSTRAINT ParticipatesIn_PK PRIMARY KEY(wid,parId),
    CONSTRAINT ParticipatesIn_ParticipateID FOREIGN KEY (parId) REFERENCES Users(uid)
);

CREATE TABLE Organizes(
	wid INT NOT NULL,
	ownerId INT NOT NULL,
    CONSTRAINT Organizes_PK PRIMARY KEY(wid,ownerId),
    CONSTRAINT Organizes_OwnerID FOREIGN KEY (ownerId) REFERENCES Users(uid)
);

CREATE TABLE Post (
pid 				INT AUTO_INCREMENT,
writer				INT,
movie_id			INT,
pdate				DATE,
content 				VARCHAR(255),
watch_party_id			INT,
PRIMARY KEY (pid),
FOREIGN KEY (writer) REFERENCES Users(uid)
FOREIGN KEY (watch_party_id) REFERENCES Watch_Party(wid) ON DELETE CASCADE
);

CREATE TABLE PostsBy(
	pid INT NOT NULL UNIQUE,
    uid INT NOT NULL,
    CONSTRAINT PostsBy_PK PRIMARY KEY (pid,uid),
    CONSTRAINT PostsBy_FK_pid FOREIGN KEY(pid) REFERENCES Post(pid),
    CONSTRAINT PostsBy_FK_uid FOREIGN KEY(uid) REFERENCES Users(uid)
);

CREATE TABLE Comments(
	cid INT AUTO_INCREMENT,
    content LONGTEXT,
    cdate DATETIME,
    PRIMARY KEY (cid)
);

CREATE TABLE CommentsOn(
	cid INT NOT NULL UNIQUE,
    pid INT NOT NULL,
    PRIMARY KEY (cid,pid),
    CONSTRAINT CommentsOn_FK_cid FOREIGN KEY (cid) REFERENCES Comments(cid),
    CONSTRAINT CommentsOn_FK_pid FOREIGN KEY (pid) REFERENCES Post(pid)
);

CREATE TABLE CommentedBy(
	cid INT NOT NULL UNIQUE,
    uid INT NOT NULL,
    PRIMARY KEY (cid,uid),
    CONSTRAINT CommentsBy_FK_cid FOREIGN KEY (cid) REFERENCES Comments(cid),
    CONSTRAINT CommentsBy_FK_uid FOREIGN KEY (uid) REFERENCES Users(uid)
);

CREATE TABLE Likes(
	pid INT NOT NULL,
    uid INT NOT NULL,
    PRIMARY KEY(pid,uid),
    CONSTRAINT Likes_FK_uid FOREIGN KEY (uid) REFERENCES Users(uid),
    CONSTRAINT Likes_FK_pid FOREIGN KEY (pid) REFERENCES Post(pid)
);

--Untested Sample Queries
INSERT INTO Users (uname, avatar) VALUES ('John Doe', NULL);
INSERT INTO Users (uname, avatar) VALUES ('Jona Doe', NULL);
INSERT INTO FavorMovies (uid, movieID) VALUES (1, 12345);
INSERT INTO Watch_Party (ownerId, movieId, Dates, Platform) VALUES (1, 12345, '2023-05-01 19:00:00', 'Netflix');
INSERT INTO ParticipatesIn (wid, parId) VALUES (1, 2);

INSERT INTO Comments (content, cdate) VALUES ('This movie is great!', '2023-05-01 19:30:00');
INSERT INTO PostsBy (pid, uid) VALUES (1, 3);
INSERT INTO CommentsOn (cid, pid) VALUES (1, 1);
INSERT INTO CommentedBy (cid, uid) VALUES (1, 3);
INSERT INTO Post (writer, movie_id, pdate, content, watch_party_id) VALUES (1, 12345, NOW(), 'This is my new post!', 1);