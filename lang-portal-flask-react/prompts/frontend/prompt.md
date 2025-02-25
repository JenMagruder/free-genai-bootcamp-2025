# Role/Profession

Frontend Developer

# Project Description

## Project Brief

We are building a japanese langauge learning web-app which serves the following purposes:
- A portal to launch study activities
- to store, group and explore japanese vocabulary
- to review study progress

The web-app is intended for desktop only, so we don't have to be concerned with mobile layouts.

## Technical Requirements

- React.js as the frontend library
- Tailwind CSS as the css framework
- Vite.js as the local development server
- Typescript for the programming language
- ShadCN for components

## Frontend Routes

This is a list of routes for our web-app we are building
Each of these routes are a page and we'll describe them
in more details under the pages heading.

/dashboard
/study-activties
/study-activties/:id
/words
/words/:id
/groups
/groups/:id
/sessions
/settings

The default route / should forward to /dashboard

## Global Components

### Navigation 

There will be a horizontal navigation bar with the following links:
- Dashboard
- Study Activities
- Words
- Word Groups
- Sessions
- Settings

### Breadcrumbs

Beneath the navigation there will be breadcrumbs so users can easily
see where they are. Examples of breadcrumbs

Dashboard
Study Activities > Adventure MUD
Study Activities > Typing Tutor
Words > 始める
Word Groups > Core Verbs

## Pages

### Dashboard

This page provides a summary of the student's progression.

- Last Sesssion

### Study Activities Index

The route for this page /study-activties

This is a grade of cards which reresent and activity.

A card has a:
- thumbnail
- title
- "Launch" button
- "View" button

The Launch button will open a new address in a new tab.
Study activities are their own apps, but in order for them
to launch they need to be provided a group_id

eg. localhost:8081?group_id=4

This page requires no pagination because there is unlikely
to be more than 20 possible study actvities

The View button will go to the Student Activities Show Page.

### Study Activities Show

The route for this page /study-activties/:id

This page will have a information section which will contain:
- thumbnail
- title
- description
- launch button

There will be a list of sessions for this study activity
  - a session item will contain
    - Group Name: So you know what group name was used for the sessions
      - This will be a link to the Group Show Page
    - Start Time: When the session was created in YYY-MM-DD HH:MM format (12 hours)
    - End Time: When the last word_review_item was created
    - \# Review Items:  The number of reviews imtes

## Words Index

The route for this page /words

This is table of words with the following cells:
- Japanese: The japanese word with Kanji
  - This will also contain a small button to play the sound of the word
  - The japanese word will be a link to the Words Show page
- Romaji: The romaji version of the word
- English: The english version of the word
- \# Correct: Number of correct word review items
- \# Wrong: Number of wrong word review items

There should only be 50 words displayed at a time.

There needs to be pagination
  - Previous button: grey out if you cannot go further back
  - Page 1 of 3: With the current page bolded
  - Next button: greyed ouf if you canno go any further forwarded

All table headings should be sortable, If you click it will toggle between ASC and DESC.
An ascii arrow should indicate direction and the column being sorted with ASC pointing down and DESC pointing up.

## Words Show

The route for this page /words/:id

## Word Groups Index

The route for this page /word-groups

This is table of word groups with the following cells:
- Group Name: The name of the group
  - This will be a link to Word Groups Show
- \# Words: The number of words associated with this group

This page contains the same sorting and paginating logic as the Words Index page

## Word Groups Show

The route for this page /words-groups/:id

This has the same components as Words Index but its scoped to only show
words that are associated with this group.

## Sessions Index

The route for this page /sessions

This page contains a list of list of sessions similar to Study Activities Show

This page contains the same sorting and paginating logic as the Words Index page

## Settings Page

The route for this page /settings

Reset History Button: This has a button that allows us to reset the entire database.
We need to confirm this action in a dialog and type the word reset me to confirm.

Dark Mode Toggle: This is a toggle that changes from light to dark theme.
