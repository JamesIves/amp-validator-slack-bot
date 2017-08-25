# AMP Validator Slack Bot
This is a Slack bot built with Python which validates [AMP documents](https://www.ampproject.org/) articles against the [Cloudflare AMP validator API](https://blog.cloudflare.com/amp-validator-api/).


## Requirements
This application requires [Python 2.7.13](https://www.python.org/) and the following packages which can be installed via pip.

```
requests==2.13.0
slackclient==1.0.7
schedule==0.4.3
```


## Deploying the Bot
This bot can be deployed to any service such as Heroku.

For Heroku simply deploy the most recent version and assign a dyno to the worker specified in the Procfile, and then scale it.

```
Instructions here
```

For one-click install to Heroku you can use the button below. Please refer to the Configuration portion of the readme for furhter instructions. 

## Configuration
There are a number of required enviroment variables required in order to power this bot, some which are required, and some which are optional. If you're deploying the bot to Heroku you'll need to go to the `Settings` tab of the application and click `Reveal Config Vars` and replace or add the fields depending on your chosen method of installaton.


| Key  | Value Information | Required |
| ------------- | ------------- | ------------- |
| `BOT_ID`  | This is the ID of your Slack bot user, this is required so the bot knows when a command is directed at it.  | **Yes** |
| `SLACK_BOT_TOKEN`  | This is the bot token found within the Slack API settings.  | **Yes** |
| `CHARTBEAT_ENDPOINT`  | If you run Chartbeat analytics you can test your top performing articles against the Chartbeat API. This field requires an endpoint that you can find in your Chartbeat API settings, for more information see the Chartbeat part of this README.   | **Optional**  |
| `CHARTBEAT_INTERVAL_TIME`  | If you'd like to periodically check the pages returned from the Chartbeat API without any user input you can enter an interval time for it to do so. This will silently check the articles and only alert if an error is found. Requires `CHARTBEAT_OUTPUT_CHANNEL` and `CHARTBEAT_ENDPOINT` to be entered. | **Optional** |
| `CHARTBEAT_OUTPUT_CHANNEL`  | If you'd like the interval check to work you need to enter a channel in order for errors to be logged to. Please see the Slack API documentation on how to format this. | **Optional** |

## Running the Application
This application can be executed locally by running `$ python app.py`. This will initialize the script and connect the bot.

There are a number of tests that can be run using `$ python tests.py` which test some of the utility functions of the bot.


## Commands
The following commands are accepted by the bot.

```
# Validates an AMP document, accepts either a regular page with a valid `amphtml` meta tag, or an amp document.
@bot validate <url>

# Validates all articles returned from the Chartbeat API. This only works if an endpoint enviroment variable is provided.
@bot chartbeat validate

# Returns the results of the last time the Chartbeat validator ran.
@bot chartbeat last
```

## This is a WIP
