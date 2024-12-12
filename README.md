# location-info
The goal of this application is to provide additional infromation and to improve SEO. It will provide more information about a certain city, landmark or region. It returns place's description and several useful links.


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
