# AMP Validator Slack Bot ⚡
[![Build Status](https://travis-ci.org/JamesIves/amp-validator-slack-bot.svg?branch=master)](https://travis-ci.org/JamesIves/amp-validator-slack-bot) [![Issues](https://img.shields.io/github/issues/JamesIves/amp-validator-slack-bot.svg)](https://github.com/JamesIves/amp-validator-slack-bot/issues)

With this Slack bot you can validate [AMP documents](https://www.ampproject.org/) against the [Cloudflare AMP validator API](https://blog.cloudflare.com/amp-validator-api/). You can also validate your top performing pages according to Chartbeat on a timer to ensure your most popular content is making its way to the AMP cache.

## Installation Steps 💽
1. Visit your organizations [Slack API settings](https://api.slack.com/) and create a new application with a bot user and retrieve the bots access token.
2. Click the button below and enter the required fields to deploy the bot to [Heroku](http://heroku.com). If the required tokens were provided correctly the bot should appear online within Slack and begin responding to commands. You can get a full explanation of each setting within the configuration portion of this readme. 


[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/JamesIves/amp-validator-slack-bot/master)

---

If you'd like to run the application outside of [Heroku](http://heroku.com) you can run add the required [configuration options](#configurations) as environment variables and then run the following commands using [Python](https://www.python.org/) and [Pip](https://pypi.org/project/pip/).

```
# Install & Run
$ pip install -r requirements.txt
$ python app.py
```


## Chartbeat Integration :chart: 
> The following steps are optional. 

If you use Chartbeat you can validate pages that are returned from their API endpoints, this can be especially useful for publications which publish a high volume of content. In order for this to work you must provide a valid endpoint found within your [Chartbeat API settings](http://support.chartbeat.com/docs/api.html). 

The bot is also capable of automatically validating against this endpoint at intervals. For instance you can give it an interval value of `60`, and a channel name of `#editors`, which would mean that every hour it would automatically validate the pages returned from Chartbeat, and if an error was found it would publish them to that channel.

For information on how to set these up please refer to the configuration part of this readme. 


## Configuration :file_folder: 
The installation will require you to enter a number of API keys and settings as environment variables. Below you'll find an explanation of each.


| Key  | Value Information | Required |
| ------------- | ------------- | ------------- |
| `BOT_ID`  | The ID of your Slack bot user, this is required so the bot knows when a command is directed at it. If you're unsure what your bot ID is you can run `bot_id.py` which will print the ID, you'll need to make sure that the `BOT_NAME` field within the file corresponds with the one you setup in the Slack interface.  | **Yes** |
| `SLACK_BOT_TOKEN`  | The bot token found within the [Slack API settings](https://api.slack.com/bot-users).  | **Yes** |
| `CHARTBEAT_ENDPOINT`  | If you run Chartbeat analytics you can test your top performing pages against the Chartbeat API. This field requires an endpoint that you can find in your [Chartbeat API settings](http://support.chartbeat.com/docs/api.html), for more information see the Chartbeat part of this readme.   | **Optional**  |
| `CHARTBEAT_INTERVAL_TIME`  | If you'd like to periodically check the pages returned from the Chartbeat API without any user input you can enter an interval time for it to do so. This will silently check the pages and only alert if an error is found. Requires `CHARTBEAT_OUTPUT_CHANNEL` and `CHARTBEAT_ENDPOINT` to be entered for this to function. Requires a numeric value, for example `60` for 60 minutes. | **Optional** |
| `CHARTBEAT_OUTPUT_CHANNEL`  | If you'd like the interval check to work you need to enter a channel in order for errors to be logged to. Please see the [Slack API documentation on how to format this](https://api.slack.com/methods/chat.postMessage#channels). | **Optional** |


## Commands :computer: 
The following commands are accepted by the bot.

```
# Validates an AMP document, accepts either a regular page with a valid `amphtml` meta tag, or an amp document.
@bot validate <url>

# Validates all articles returned from the Chartbeat API. This only works if an endpoint enviroment variable is provided.
@bot chartbeat validate

# Returns the results of the last time the Chartbeat validator ran.
@bot chartbeat last

# Returns a list of all available commands
@bot help
```

![Example](assets/example.png)
