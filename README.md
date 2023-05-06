# 411-A5-1
CS411 Team A5 Repo

# [Most updated implemetation walkthrough (May 5th)](https://drive.google.com/file/d/1FFnVdCbBdbWcYdkkEOzYx6B90Vuo8uSc/view?usp=sharing)

# MovieDate
Overview: social media platform focused on movies. Users can recommand a movie, talk about the movie, and plan for a watch party with their friends.

## Requirements:
- Database:
    - Store user's preference - i.e country
    - Store the user's favorite movies
    - Store the user's comments on a particular movies
- APIs:
    - [Movie API](https://developers.themoviedb.org/3/getting-started/introduction)
        - [Get movie detail](https://developers.themoviedb.org/3/movies/get-movie-details)
        - [Get movie availablity platform](https://developers.themoviedb.org/3/movies/get-movie-watch-providers)
        - [Get movie trailers](https://developers.themoviedb.org/3/movies/get-movie-videos)
        - [Get movie reviews](https://developers.themoviedb.org/3/reviews/get-review-details)
    - [Twillio](twillio.com)
        - [For chat server integration](https://www.twilio.com/blog/best-chat-api-messaging-sdk-platforms)
    - [Google Calendar](https://www.google.com/search?client=safari&rls=en&q=google+calendar+api&ie=UTF-8&oe=UTF-8)
        - Schedele user's Watch Party
- [OAuth](https://oauth.net/2/): We will use OAuth2.0 for user login/creation functionality
- Decoupled Architecture: 
    - Backend: Database, authentication for user log in
    - Frontend: use React for front-end


## User Story

Full Wireframe and prototype avilable on [Figma](https://www.figma.com/file/64uXWBA6ZJdBAPoJkRL7GO/Movie-Project?node-id=57-972&t=lbNufd8slbJqqiC5-0).

### User Story 1: first time use and user creation
* Scenario: I heard of this new social app that focuses on film lovers. I just installed the app.
* I launch the app and app asks me to sign up. I fill out the form and register for a new account.

<img src="https://i.imgur.com/m3BXlTe.png" width=250><br>

### User Story 2: Reinstalled app and sign in
* Scenario: I used MovieDate before. I am reinistaling this app, and the app asks me to sign in.
* I launch the app and app asks me for my credential. I filled in the form and login.

<img src="https://i.imgur.com/F6NDRV5.png" width=250><br>


### User story 3: Search for a specific movie
* Jon wants to watch the movie "Everything Everywhere All at Once." He want to know on which streaming platform the movie is on.
* Jon searches the movie title and found the movie he was looking for.
* Jon discovers that the movie is viewable on multiple platforms.
* From this point on:
    * Jon can click on the streaming platform, which redirects him to the movie on that platform.
    * Jon can watch the trailer, which redirects him to the movie trailor on YouTube.
    * Jon can add this movie to his favorite.
    * Jon can write review/post on this movie.
    * Jon can share this movie to his friend.
    * Jon can add to his To-Watch list.
    * Jon can start a movie watch party.
    
<img src="https://i.imgur.com/9TMScZf.png" width=250>
<img src="https://i.imgur.com/bJV9rTu.png" width=250>
<img src="https://i.imgur.com/u5j0jTo.png" width=250>
<img src="https://i.imgur.com/9HaRq0n.png" width=250> <br>


### User story 4: Watch Party
* Jen wants to host a movie night with her favorite movie "Back To The Future."
* Jen organizes a wach party event with the movie, time to start, and location. Jon posts this information in his community.
* Jen's friends can see this watch party in their "Community" page.
* The friends can click on "Join" to create a reminder.
* 5 minutes before the event, all participants get a notification.
* The app automatically creates a group chat for participants and organizers.
* The event is automatically moved to "finished" after the event is over.

<img src="https://i.imgur.com/Yr8j216.png" width=250> <br>


### User story 5: Profile Page
* Jen wants to check her profile page.
* Jen clicks on the "Profile" tab.
* There She can see her bio and edit the bio if she wants.
* She can see her favoirte movies, To-Watch list, upcoming Watch Parties, movie reviews.

<img src="https://i.imgur.com/EXmnWNU.png" width=250>
<img src="https://i.imgur.com/imw3qEZ.png" width=250><br>


## User Story 3 TODO List:
- [ ] Frontend: Translate design into code (10 hours)
- [ ] Search Functionality (3 hour)
    - [ ] Use MovieDataBase API to get result and display the replying JSON on screen
        - [ ] API call and parse result for available streaming platform, trailer
- [ ] Database (8 hours)
    - [ ] Add Favorite Movies to a user
    - [ ] Add movie to to-watch list
    - [ ] Create Post/Review for a movie
- [ ] share movie to friends by sending link (1 hour)

|                | Frontend | Database | API    | Share  |
|----------------|----------|----------|--------|--------|
| Team Agreement | 11 hours | 6 hours  | 1 hour | 1 hour |
| Ruihang        | 10 hours | 5 hours  | 1 hour | 1 hour |
| Andrew         | 11 hours | 8 hours  | 1 hour | 1 hour |
| Minos          | 12 hours | 6 hours  | 1 hour | 1 hour |
