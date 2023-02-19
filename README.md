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

# Project idea 2: Movie Haunting
Overview: user searches for a movie and the app tells them which platform this movie is on

## Requirements:
- Database:
    - Store user's preference - i.e country
    - Store the user's favorite movies
- APIs:
    - [Movie API](https://developers.themoviedb.org/3/getting-started/introduction)
        - [Get movie detail](https://developers.themoviedb.org/3/movies/get-movie-details)
        - [Get movie availablity platform](https://developers.themoviedb.org/3/movies/get-movie-watch-providers)
- OAuth: We will use OAuth2.0 for user login/creation functionality
- Decoupled Architecture: 
    - Backend: Database, authentication for user log in
    - Frontend: use React for front-end