# socialAudit
This tool allows the python Twint module to scrape multiple usernames from Twitter.

## Requirements
Given a list of Twitter usernames, scrape 20 tweets from each user and print in reverse chronological order.

## Design

[Twint](https://github.com/twintproject/twint) is a scraping tool that is used to collect data from the Twitter social media platform.  It is a non rate-limited alternative to Twitter's API for scraping data from Twitter.

The Twint module does not support specifying multiple Twitter usernames in the configuration.  As a workaround to this limitation, this script runs a Twint scrape for each Twitter username in a list of selected channels (Twitter usernames).  This functionality could be useful for anyone interested in collecting Twitter data from multiple users for analysis or to create an operations dashboard, such as news reporters/journalists.

My approach here was to create functions for each step in the workflow: clearing out old data (from any previous scrapes), scraping new data, reformatting the data so that it is no longer line-delimited json, bringing it into a pandas dataframe, and printing it.  A single class was used to store all of the Twitter usernames for better performance.

#### Classes and functions

First, the `Colors` class sets the color scheme that gets used when printing.

The `SocialAudit` class contains functions for each step in the workflow and is where all of the Twitter usernames are stored.

Within the `SocialAudit` class, the `__init__` function allows Twitter usernames to be passed into the class.

The `clear_old_data` function deletes stored data from previous scrapes if they exist.

Next, the `scrape_channel` function configures and runs the Twint scrape.  This step creates a line-delimited json file as output.

The `format_data` function reformats the Twint output to non line-delimited json to support compatibility with the pandas module by reading it into memory line by line and then appending each line to a list, then saves the reformatted output as a new file and deletes the original line-delimited file.

Next, the `make_dataframe` function brings all of the reformatted json files for each Twitter username into a pandas dataframe and sorts it in reverse chronological order.

The `print_scrape` function prints each tweet in the dataframe according to the color scheme along with information such as username, time, date, hashtags and an html link.

Finally, the `run` function executes the `clear_old_data`, `scrape_channel` and `format_data` functions for each Twitter username, then executes the `make_dataframe` function followed by the `print_scrape` function.

## Usage
This tool can be run for a preset of Twitter usernames by executing the `./bin/socialAudit.sh` bash script from the `socialAudit` parent directory.

#### Run for a preset of Twitter usernames
```bash
$ ./bin/socialAudit.sh
```

Alternatively, this tool can be run for  a custom set of Twitter usernames by executing the `./socialAudit.py` python script from the `socialAudit` parent directory with space-delimited Twitter usernames as arguments.

#### Run for a custom set of Twitter usernames
```bash
$ python3 ./socialAudit.py Username1 Username2 Username3
```

## Considerations
The Twint module does not support scraping from all Twitter usernames due to a known issue.  To address this, Try/Except was used in the `format_data` function instead of If/Else for more efficient error handling.  If/Else tests whether the file exists before deleting it, so requires checking the file twice, in contrast to Try/Except which attempts to delete the file and reports a non-critical error upon failure.  Because the `format_data` function is writing to a file, it is expected that a successful scrape will create the file, while an unsuccessful scrape will not. 

## Next Steps
The code could be made to run operations in parallel for better performance. In addition, command line argument parameters could be expanded to scrape a different number of tweets (default/minimum is 20, and twint supports increasing the number of tweets per scrape in increments of 20) for each user.
