# Check Out This Song: Project Proposal

"Check Out This Song" is a web app designed to let users share songs they're enjoying. Users can follow other users and see their songs in a feed, and can 'like' songs they enjoy. 

* This site is for anyone who enjoys music, but is especialy targeting people who enjoy sharing new music with their friends online. Likely people ages 18-35
* This site will use music information data, likely from a music specific database, as well as most likely Youtube to show a playable embed of the songs chosen.

## How it's going to get made
* The database schema will comprise several tables:

    * A table for users with their relevant information
    * A table for each song shared, this will likely pull information from an external database
    * A table for posts that references the User posting and the song being posted
    * A table for likes that references posts and users who like it
    * A table for follows that references a user being followed and a user following

* API issues may include:

    * Resolving spelling issues
    * Endpoints moving
    * Multiple similar entries making it difficult to keep track of which songs have been posted already

* Sensitive information I'll need to secure includes passwords, and potentially email addresses
* Functionality will include:

    * Login
    * Registration
    * potentially email confirmation and password reset
    * Searching for a song to post and returning a match based on a music db API
    * Finding a corresponding playable embed (likely from youtube) and posting that to your page
    * Ability to follow other users and have their posts show up in a feed
    * Ability to like other users' posts and see a collection of you liked posts

        * maybe make a playlist from these?

* User flow:

    * Home page shows a few recent posts with high like count and prompt to join or login
    * If not registered, user goes through registration form to make new account
    
        * User is taken to the new post page with prompts (flashed?) to make their first post
        * User is then taken to their feed (maybe encouraged to follow 'popular' account)
        * prompt shown that user can like posts?

    * Already registered but not logged in user can log in

        * logged in user is then taken to their feed with users that they follow
        * navigation is shown for their own profile, making a new post, maybe one other destination?
* This site is 'more than CRUD' because it allows users to interact with the information, and in effect the other users on the service.

## Minimum Viable Product

For this project to be viable the minimum necessary features include:

* A form to accept a request to post a song
* an interface with an API to resolve the user request into a song
* an interface to find playable media for that song, OR a way to link to playable media