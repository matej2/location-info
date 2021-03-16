# location-info
Reddit bot which gets info about certain city, location or state.

> Ever wanted to know more about location where the picture was taken? Maybe open up a map or discover interesting things nearby? This bot will provide you with the info

## Use

`u/LocationInfoBot <city_name>`

### Example

User would tag bot below post:

> u/LocationInfoBot Saarland

Bot would reply:

> Found match for Saarland.
> 
> - Wiki: https://en.wikipedia.org/wiki/Saarland
> - Instagram: ...
> - Map: ...
> - Turist information: ...

![example](https://user-images.githubusercontent.com/11059438/111335197-79a33700-8674-11eb-8ee7-f259ad3946a1.png)


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
