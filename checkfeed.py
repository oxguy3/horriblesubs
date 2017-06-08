#!/usr/bin/python
# coding: iso-8859-15

import horriblesubs as hs
import horriblesubs_config as config
import feedparser
import os
import re
import time
from pprint import pprint

hs.init_deluge()
hs.init_pushbullet()

feed = feedparser.parse('https://horriblesubs.info/rss.php?res='+config.video_res)

unrenamed_torrents = {}
new_episodes = []

for item in feed.entries:

    match = re.search("\[HorribleSubs\] (?P<show>.+?) - (?P<num>\d+(?:\.5)?) \[\d+p\](?P<ext>\.\w+)", item.title)
    assert match

    # TODO check that this isn't an item we've seen before

    for show in config.my_shows:
        name = show['name']
        # if this show is on our list
        if name == str(match.group('show')):

            local_name = show['local_name'] if ('local_name' in show) else name

            # we don't want to download half-episodes
            if match.group('num').endswith('.5'):
                print "SKIPPING HALF EPISODE"
                break

            # HorribleSubs returns absolute ep #; we convert to season+ep #s
            episode = int(match.group('num'))
            season = 1
            if 'season_lengths' in show:
                for sl in show['season_lengths']:
                    if sl < episode:
                        episode -= sl
                        season += 1
                    else:
                        break

            out_dir = config.media_folder + "/" + local_name + "/" + "Season " + str(season)
            out_file = local_name + " - s" + str(season).zfill(2) + "e" + str(episode).zfill(2) + match.group('ext')
            out = out_dir + "/" + out_file

            # create the output folder if it's absent
            if not os.path.isdir(out_dir):
                os.makedirs(out_dir, config.chmod)

            # verify the file doesn't already exist
            if os.path.isfile(out):
                continue

            # RPC method: add_torrent_url(url, options, headers=None)
            torrent_id = hs.deluge_call('core.add_torrent_magnet', item.link, {
                'download_location': out_dir,
            })

            new_episodes.append(local_name)

            unrenamed_torrents[torrent_id] = out_file

            break

# send notifications if we got any new episodes
if len(new_episodes) > 0:
    notif_body = "Shows: "
    for show in new_episodes:
        notif_body += show + ", "
    notif_body = notif_body[:-2]
    hs.send_notification('New eps of '+str(len(new_episodes))+' shows', notif_body)

# we can't rename the files until Deluge has downloaded the metadata and
# discovered the files, so we just have to keep polling for a bit
tries = 0
while len(unrenamed_torrents) > 0:
    time.sleep(3)
    unrenamed_torrents = hs.attempt_file_rename(unrenamed_torrents)
    tries += 1
    if (tries > 10):
        print "ERROR: Took too long to rename " + str(len(unrenamed_torrents)) + " torrents, giving up."
        break
