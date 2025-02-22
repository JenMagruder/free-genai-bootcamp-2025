## Frontend Techinical Specs

## Pages

### Dashboard '/dashboard'

#### Purpose
The purpose of this page is to provide a summary of learning and act as the default page when a user visit the web-app

#### Components

 - Last Study Session
    shows last activity used
    shows when last activity used
    summarizes wrong vs corrrect from last activity
    has a link to the group 
 - Study Progress
    -total words study
        - across all study sessions show the total words studied out of all possible words in our database
    -display a mastry progress eg. 0%
 - Quick Stats
    - success rate eg. 80%
    - total study sessions eg. 4
    - total active groups eg. 3
    - study streak eg. 4 days
 - Start Studying Button
    - goes to study activities page

 We'll need the following API endpoints to power this page

 #### Needed API Endpoints

- GET /api/dashboard/last-study-session
- GET /api/dashboard/study-progress
- GET /api/dashboard/quick-stats

### Study Activites /study-activities

#### Purpose
The purpose of this page is to show a collection of study activites with a thumbnail and its name, to either launch or view the study activity.

#### Components

- Study Activity Card
    - show a thumbnail of the study activity
    - the name of the study activity
    - has a link to launch button that takes you to the launch page
    - the view page to view more information about past study sessions for that study activity

#### Needed API Endpoints

- GET /api/study-activities



