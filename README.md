# vg-price-alert-cli

A command line application for those interested in tracking the price of video games, both physical and digital.

Given a video game title and a preferred platform, it will allow the user to scrape the price data from nearly all major Australian retailers.

# setup locally
- `pip3 install -r requirements.txt` to install dependencies
- `python3 price-alert.py` to run the application
- select option `0` to put it in automatic mode (will automatically scrape prices and send notifications at 12am, 6am, 9am & 12pm AEST)
- A pushbullet API key and valid phone number is required to utilise the SMS notification feature
