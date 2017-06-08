# horriblesubs
by Hayden Schiff (oxguy3)

Looks for new episodes of our favorite shows on HorribleSubs, downloads them
with Deluge, and renames the files for Plex-style organization.

## Installation
Clone this repository somewhere on your machine, or
[download it as a ZIP file](https://github.com/oxguy3/horriblesubs/archive/master.zip)
and extract it somewhere. Open a terminal and `cd` to the repo's directory.

First, you need Python2 on your system. If you don't know which version you
have, you can check with `python --version`. You also need pip, which is
usually included with Python2. With pip, install the required packages for this
project like this:

```
pip install -r requirements.txt
```

Next, make a copy of horriblesubs_config.sample.py and name it
horriblesubs_config.py. Read the comments in the file and adjust all the
config options in that file to your liking.

## Usage
Once you've completed the installation section above, you can check for new
episodes by running the checkfeed.py file, and you can run renamefiles.py to
tell Deluge to rename the downloaded media files. The renamefiles.py script
should be run shortly after checkfeed.py a few times.

Most likely, you don't want to run this manually, so you'll probably want to
set up cron jobs. I recommend running checkfeed.py hourly and renamefiles.py
every ten minutes. Here are my cron settings (you can edit your own cron
settings with `crontab -e`):

```
10 * * * * python /path/to/horriblesubs/checkfeed.py
0,15,30,45 * * * * python /path/to/horriblesubs/renamefiles.py
```

That runs checkfeed.py 10 minutes past every hour (since HorribleSubs uploads
are usually a few minutes late), and runs renamefiles.py every 15 minutes.

## License
MIT License; see included LICENSE file for details
