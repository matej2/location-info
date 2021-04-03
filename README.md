# location-info
This is a bot that will provide you more information about a certain city, landmark or region. It returns place's description and several useful links.

> Ever wanted to know more about location where the picture was taken? Maybe open up a map or discover interesting things nearby? Or find hike ideas on this location?

How is this bot better than Googling things:

1. On mobile: You dont have to switch between apps
2. Google is not indexing content from Instagram and Facebook, meaning you wont find such content by googling it
3. We will eventually be able to search all reddit posts by their location.

## Use

Tag user [u/LocationInfoBot](https://www.reddit.com/u/LocationInfoBot/) with the name of the location. This will also work for hills, landmarks and regions.

>u/LocationInfoBot <city_name>

### Example



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


## Content and links

Bot provides location description, taken from wikipedia link. 
Besides that, bot also provides multiple relevant links: map, hotels, hiking trails, activities and links to social medias.
All links are built using url and search string (location name).
