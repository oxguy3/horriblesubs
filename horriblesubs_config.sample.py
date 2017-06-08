#!/usr/bin/python
# coding: iso-8859-15
# Root folder of your anime library
media_folder = '/home/shared/anime'

# The shows you want to download. Each show should be a dict with:
#   -- name: Name of the show on HorribleSubs
#   -- local_name: Name of the show in your local filesystem. Optional; don't
#      set this if it's the same as `name`.
#   -- season_lengths: A list of ints, expressing how long each season is. This
#      allows the script to correct the season/episode numbers. Optional; don't
#      need to set this for single-season shows.
my_shows = [
    {
        'name': 'Busou Shoujo Machiavellianism',
    },
    {
        'name': 'Boku no Hero Academia',
        'local_name': 'My Hero Academia',
        'season_lengths': [13],
    },
    {
        'name': 'Sagrada Reset',
        'local_name': 'Sakurada Reset',
    },
    {
        'name': 'Shingeki no Kyojin S2',
        'local_name': 'Attack on Titan',
        'season_lengths': [25],
    },
]
# If the folders for a show don't already exist, this script will create them,
# and set their permissions to this value.
chmod = 0775

# Set to '480', '720', or '1080'
video_res = '1080'

# Access/login details for your Deluge server
#   -- Note: Use deluged's port, not the web UI's port.
#   -- Note: This script is not designed to work for hosts other than localhost.
deluge_host = '127.0.0.1'
deluge_port = 58846
deluge_user = 'localclient'
deluge_pass = 'secret'

# Pushbullet notification settings. You can generate an access token for your
# account here: https://www.pushbullet.com/#settings/account
pushbullet_enabled = True
pushbullet_access_token = 'secret'
