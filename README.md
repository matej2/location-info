# location-info
Reddit bot which gets info about certain city, location or state.

> Ever wanted to know more about location where the picture was taken? Maybe open up a map or discover interesting things nearby? This bot will provide you with the info

## Example

User would tag bot below post:

> User: u/LocationInfoBot Saarland


Bot would reply:

> LocationInfoBot: Found match for Saarland.
> 
> - Wiki: https://en.wikipedia.org/wiki/Saarland
> - Instagram: ...
> - Map: ...
> - Turist information: ...


## Installation

1. Clone repo
2. Install pipenv
3. Create a Reddit app
4. Fill out environment variables:
    - CLIENT_ID
    - CLIENT_SECRET
    - USERNAME
    - PASS
5. Run `pipenv shell` and `python main.py`