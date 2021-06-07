import twint
import pandas
import json
import os
import sys


class Colors:
  """
  A class to set the color scheme that gets used when printing
  """

  RED = "\033[91m"
  GREEN = "\033[92m"
  BLUE = "\033[94m"
  ORANGE = "\033[38;2;255;165;0m"
  WHITE = "\033[0m"


class SocialAudit:
  """
  A class of functions for each step in the workflow
  """

  # Create a list where all of the reformatted tweets get read into memory
  tweet_list = []

  # Create a list where all of the reformatted json paths will get saved to
  file_list = []
  
  def __init__(self, usernames):
    """
    Allow usernames to get passed into this class
    :param usernames: A list of Twitter usernames
    """

    self.usernames = usernames

  def run(self):
    """
    Runs stages 1 - 3 for each username then loads data into pandas and prints
    """

    for username in self.usernames:  
      self.json_input_filename = "./data/data-" + username + ".ndjson"
      self.json_output_filename = "./data/data-" + username + ".json"
      self.clear_old_data()
      self.scrape_channel(username)
      self.format_data(username)
    
    self.make_dataframe()
    self.print_scrape()

  def clear_old_data(self):
    """
    Stage 1: Clear out old data from previous scrape for a Twitter username
    """

    if os.path.exists(self.json_output_filename):
      os.remove(self.json_output_filename)

  def scrape_channel(self, username):
    """
    Stage 2: Configure and run Twitter scrape for a Twitter username
    :param username: A Twitter username
    """

    c = twint.Config()
    c.Username = username
    c.Limit = 20
    c.Store_json = True
    c.Output = self.json_input_filename
    twint.run.Search(c)

  def format_data(self, username):
    """
    Stage 3: Optimize json formatting for pandas, write output to file,
    add output path to file list, and clear out unformatted data for a
    Twitter username
    :param username: A Twitter username
    """

    # Read line-delimited json into memory line by line then append it into a list
    try:
      with open(self.json_input_filename, "r") as tweets:
        for line in tweets.readlines():
          tweet = json.loads(line)
          self.tweet_list.append(tweet)

      print("Finished reading tweets into memory!")

      # Write non line-delimited json into a new file
      with open(self.json_output_filename, "w") as output_file:
        output_file.write(json.dumps(self.tweet_list))

      print("Finished writing tweets to file!")

      # Track all of the new non line-delimited files using a list of output pathnames,
      # then clear out the old line delimited files
      self.file_list.append(self.json_output_filename)
      os.remove(self.json_input_filename)

    # Try/Except is used instead of If/Else for more efficient error handling
    except:
      print("Twint does not support scraping this username (@" + username + ") due to a known issue.")

  def make_dataframe(self):
    """
    Load all of the collected data into a pandas dataframe,
    then put it in reverse chronological order
    """

    staging_df = []
    for file in self.file_list:
      staging_df.append(pandas.read_json(file))
    self.tweet_df = pandas.concat(staging_df, ignore_index=True)
    self.tweet_df.sort_values("created_at", inplace=True)

  def print_scrape(self):
    """
    Print scrape from dataframe
    """

    for _index, row in self.tweet_df.iterrows():
        print(f'{Colors.WHITE}{row["username"]}' \
            f'\n{Colors.RED}{str(row["date"]).split(" ")[0]} {row["time"]}' \
            f'\n\t{Colors.GREEN}{row["tweet"]}' \
            f'\n{Colors.ORANGE}{row["hashtags"]}' \
            f'\n{Colors.BLUE}{row["link"]}\n\n')

# Run socialAudit for selected channels
if __name__ == "__main__":
  selected_channels = sys.argv[1:]
  social_audit = SocialAudit(selected_channels)
  social_audit.run()
