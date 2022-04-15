# Check Out This Song
### *A This Is My Jam clone*

*Check Out This Song* (*COTS*) is a lightly social music sharing web app inspired by [This Is My Jam](https://www.thisismyjam.com/) that allows users to post one song at a time that they feel that others should check out! *COTS* is my first capstone project for the Springboard Software Engineering program.


## API Selection:
Check Out This Song will use some or all of the following APIs to resolve user requests:

* Discogs API

        https://api.discogs.com/database/

* Youtube Data API

        https://www.googleapis.com/youtube/v3/search


## Database Design
COTS will use a relational database similar to the one described in the image below.

![COTS database diagram](resources/COTS_database_diagram.png)

<details>
<summary>code for quickdatabasediagrams.com diagram</summary>

    Users
    -
    ID PK int
    Username string UNIQUE
    Email string UNIQUE
    Password string

    Posts
    -
    ID PK int
    UserID int FK >- Users.ID
    SongID int FK >- Songs.ID

    Songs
    -
    ID PK int
    YoutubeURL string
    DbID int

    Likes
    -
    ID PK int
    PostID int FK >- Posts.ID
    UserID inf FK >- Users.ID

    Follows
    -
    FollowingUser int PK FK >- Users.ID
    FollowedUser int PK FK >- Users.ID
</details>