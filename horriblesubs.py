#!/usr/bin/python
# coding: iso-8859-15
import horriblesubs_config as config
from deluge_client import DelugeRPCClient
from pushbullet import Pushbullet

##### DELUGE ######

# connect to Deluge
def init_deluge():
    global deluge
    deluge = DelugeRPCClient(config.deluge_host, config.deluge_port, config.deluge_user, config.deluge_pass)
    deluge.connect()
    assert deluge.connected

# use a deluge method
def deluge_call(method, *args, **kwargs):
    global deluge
    return deluge.call(method, *args, **kwargs)

# attempts to rename files on Deluge
def attempt_file_rename(unrenamed_torrents):
    for torrent_id in unrenamed_torrents.keys():
        # check if there are any files in the torrent yet
        status = deluge_call('core.get_torrent_status', torrent_id, ['files'])

        # if there are files, then rename them
        if (len(status['files']) > 0):
            out_file = unrenamed_torrents[torrent_id]

            # with HorribleSubs, there's always just one file, at index 0
            deluge_call('core.rename_files', torrent_id, [(0, out_file)])

            # check this torrent off the to-do list
            unrenamed_torrents.pop(torrent_id)
    return unrenamed_torrents

##### PUSHBULLET #####

# connect to Pushbullet
def init_pushbullet():
    global pushbullet
    if config.pushbullet_enabled:
        pushbullet = Pushbullet(config.pushbullet_access_token)

# send a Pushbullet notification
def send_notification(title, body):
    global pushbullet
    if config.pushbullet_enabled:
        pushbullet.push_note('HS: '+title, body)
