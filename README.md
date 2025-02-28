# Location Information Service

This application is designed to enhance user experience and improve SEO by providing detailed information about cities, landmarks, and regions. It delivers a comprehensive description of a location along with a curated list of useful links, making it a valuable tool for users seeking relevant and actionable information.

---

## Example

![Example Output](https://user-images.githubusercontent.com/11059438/111335197-79a33700-8674-11eb-8ee7-f259ad3946a1.png)

---

## Installation

To set up the application, follow these steps:

1. Clone the repository to your local machine.
2. Install `pipenv` to manage dependencies.
3. Create a Reddit application to obtain API credentials.
4. Configure the required environment variables:
   - `CLIENT_ID`
   - `CLIENT_SECRET`
   - `USERNAME`
   - `PASS`
5. Activate the virtual environment using `pipenv shell` and start the application with `python main.py`.

---

## Features

- **Location Descriptions**: The application retrieves detailed descriptions of locations from Wikipedia, ensuring accurate and informative content.
- **Curated Links**: It generates and provides relevant links, including:
  - Maps
  - Hotels
  - Hiking trails
  - Activities
  - Social media profiles
- **Dynamic Link Generation**: All links are dynamically constructed using the location name as a search parameter, ensuring relevance and usability.

---

This project is ideal for users seeking to enrich their content with location-based insights and improve discoverability through SEO optimization.
