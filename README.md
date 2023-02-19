# 411-A5-1
CS411 Team A5 Repo


# Project idea 1: Transit Calendar

- Overview: A mobile app that ingegrate User's Calendar. Use User's current location and the next appointment's location to give user an estimate of when they should leave to arrive on time by taking the transit.

## Requirements:
- Database: store account information, store the events
    - Use Micorosoft Azure/Cockroch
- 2 APIs: Google/Apple Map + Transit API
- OAuth: We will use OAuth to log in to Google and integrate user's Calendar
- Decoupled Architecture: 
    - Backend: Authentication, Database
    - Frontend: use React for front-end

# Project idea 2: Movie Haunting

- Overview: user searches for a movie and the app tells them which platform this movie is from

## Requirements:
- Database: Store the user's favourite movies
- APIs: Movie API and JustWatch API
- OAuth: We will use OAuth to integrate user's Calendar
- Decoupled Architecture: 
    - Backend: Database, authentication for user log in
    - Frontend: use React for front-end