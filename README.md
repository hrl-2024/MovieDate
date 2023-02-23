# 411-A5-1
CS411 Team A5 Repo


# Project idea 1: Transit Calendar
Overview: A mobile app that ingegrate User's Calendar. Use User's current location and the next appointment's location to give user an estimate of when they should leave to arrive on time by taking the transit.

## Requirements:
- Database: store account information and preference (prefer which type of public transportation)
    - Use Micorosoft Azure/Cockroch Database
- APIs:
    - Google/Apple Map:
        - get user's current location, event's location, transit estimate time
    - [Transit API](https://transitapp.com/apis)
        - Real-time transit departures
- OAuth: We will use OAuth2.0 to log in to Google and/or Apple and integrate user's Calendar
- Decoupled Architecture: 
    - Backend: Authentication, Database
    - Frontend: use React for front-end

# Project idea 2: Movie 
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
    - [Twillio]
        - [For chat server integration](https://www.twilio.com/blog/best-chat-api-messaging-sdk-platforms)
    - [Google Calendar](https://www.google.com/search?client=safari&rls=en&q=google+calendar+api&ie=UTF-8&oe=UTF-8)
        - Schedele user's Watch Party
- [OAuth](https://oauth.net/2/): We will use OAuth2.0 for user login/creation functionality
- Decoupled Architecture: 
    - Backend: Database, authentication for user log in
    - Frontend: use React for front-end