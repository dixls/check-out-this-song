# Check Out This Song
### *A This Is My Jam clone*
<br>

*The live instance of Check Out This Song is no longer available due to the
ending of heroku's free tier*
<br>

*Check Out This Song* (*COTS*) is a lightly social music sharing web app inspired by [This Is My Jam](https://www.thisismyjam.com/) that allows users to post one song at a time that they feel that others should check out! *COTS* is my first capstone project for the Springboard Software Engineering program.
<br><br>
*COTS* was created using a Flask backend with a Postgresql relational database, pages served with jinja, and some front end features implemented with jQuery. Styling comes from Bulma's CSS framework, and testing is done with pytest.
<br><br>

## Features:
Some of the features implemented in *COTS* include:

* Following other users
  * I wanted users to be able to follow their friends so that their feed could be tailored in some way
* Youtube embeds
  * I didn't want users to need to navigate away from the site in order to listen to the songs that have been shared
* Normalized Song data from Last.fm
  * By getting formatted metadata from last.fm in the first step of posting a song, styling and information can be consistent
* User Search
  * implementing a recommendation system for users to follow would be helpful, but without that step, being able to search for users to follow makes it easy enough to find people.
<br><br>

## API Selection:
Check Out This Song will use some or all of the following APIs to resolve user requests:

* Youtube Data API

        https://www.googleapis.com/youtube/v3/search

* Last.fm API

        http://ws.audioscrobbler.com/2.0/
<br>

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
    Avatar string
    Bio string
    Admin boolean
    EmailConfirm bool
    AccountEnabled bool

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
    Title string
    Artist string

    Likes
    -
    PostID int PK FK >- Posts.ID
    UserID inf PK FK >- Users.ID

    Follows
    -
    FollowingUser int PK FK >- Users.ID
    FollowedUser int PK FK >- Users.ID
</details>
<br><br>

## User Flow

### Unregistered user

* When an unregistered visitor first visits the page the home page will have a short feed drawing from the most recent posts with the most likes.
* Attempting to post a new song will redirect them to login with an option to sign up
* Signup requires email, username, password, optional bio and (upload?) avatar
* Once signed up, user is taken to their homepage with a prompt to search for users to follow and a link to the user search page
* User search page returns a list of matching users with a follow (or unfollow) button next to each user
* User can now post new songs or return to visit the home page

### Registered user

* When a logged in user returns to Check Out This Song, their home page will be populated with the most recent posts from themselves and from users they follow.
* Users can click on their name in the navbar to view their profile and have the option to edit their profile information.
* Logged in users can also see a Heart icon at the bottom of each post to 'like' a post
* Users liked posts can be seen from their profile view page by clicking the "liked posts" link
* In the main feed users will also be able to see a trash can icon on their own posts in order to delete them, Admin users can see a trash can icon on any posts in order to delete offensive posts

### Posting flow

* Starting a new post the user is prompted to search for a song
* Search results are a list of normalized song data from last.fm
* After selecting the appropriate match, user is presented with a list of youtube videos based on the song they selected
* After picking a youtube video the user is prompted to write a description for why they are posting this song
* User will then be presented with a confirmation screen with a preview of their completed post
* Once confirmed the user will be returned to their home page where their post will be in the feed and visible near the top (high post volume notwithstanding)

<br>

## Still to do

* Figure out a reset password flow (emails?)
* confirmation modal for deleting posts would be nice
* reusing existing song entries for new posts


## Done

* Set up organization of application
* Create db models
* full main logic is ready
* deployed on heroku
* likes and delete implemented in javascript
* a bunch of tests
* improved js performance
