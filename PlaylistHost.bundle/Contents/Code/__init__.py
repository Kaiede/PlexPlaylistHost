# -*- coding: utf-8 -*-
#
# This is heavily based/inspired by https://github.com/cp9999/MusicPlaylist.bundle

import json
import os
from lxml import etree
from random import shuffle

NAME = 'Playlists'
PREFIX = '/music/playlisthost'
PLUGIN_DIR = 'com.plexapp.plugins.playlisthost'
LIBRARY_PLAYLISTS = '/playlists'
URL_MUSIC_PLAYLIST = 'http://com.plexapp.plugins.playlisthost/track'
ART = 'art-default.png'
ICON = 'icon-default.png'

# File version
CURRENT_VERSION_ALL = "1"
CURRENT_VERSION_SINGLE = "2"

# Preferences
PREFS__PLEXIP = 'plexip'
PREFS__PLEXPORT = 'plexport'

# Client / User information
CLIENT_UNKNOWN = 'Unknown'
CLIENT_USER_LIST = 'client_user_list'
DICT_KEY_CLIENT_LIST = CLIENT_USER_LIST

# Plex XML Parsing
PMS_XPATH_PLAYLIST = '//Playlist'
PMS_XPATH_TRACK = '//Track'

# XML Attribute names
ATTR_TITLE = 'title'
ATTR_KEY = 'key'
ATTR_THUMB = 'thumb'

ATTR_COMPOSITE = 'composite'
ATTR_LEAF_COUNT = 'leafCount'
ATTR_DURATION = 'duration'
ATTR_SUMMARY = 'summary'

ATTR_PARENT_TITLE = 'parentTitle'
ATTR_GRANDPARENT_TITLE = 'grandparentTitle'
ATTR_RATINGKEY = 'ratingKey'
ATTR_AUDIOCODEC = 'audioCodec'
ATTR_AUDIOCHANNELS = 'audioChannels'
ATTR_CONTAINER = 'container'
ATTR_PARTKEY = 'partkey'
ATTR_BITRATE = 'bitrate'

# String Resources
TEXT_MAIN_MENU = "TEXT_MAIN_MENU"

####################################################################################################
def Start():
    Plugin.AddPrefixHandler(PREFIX, MainMenu, NAME)
    Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
    #Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')
    #Plugin.AddViewGroup('Maintenance', viewMode='List', mediaType='items')

    ObjectContainer.title1 = L(TEXT_MAIN_MENU)
    ObjectContainer.view_group = 'List'
    ObjectContainer.art = R(ART)

    DirectoryObject.thumb = R(ICON)
    DirectoryObject.art = R(ART)    

    Log.Debug('Plugin Started With: %s' % (NAME))
    Log.Debug('Using Server: %s' % (GetPlexUrl()))
  
####################################################################################################
#@handler(PREFIX, NAME)
def MainMenu():   
    Log.Debug('Main Menu')
    oc = ObjectContainer(no_cache = True)
    oc.title1 = L(TEXT_MAIN_MENU)
        
    playlists = FetchPlaylists()
    for playlist in playlists:
        oc.add(CreatePlaylistObject(playlist))

    return oc

#@route(PREFIX +'/playlist')
def PlaylistMenu(title, key):
    Log.Debug('Playlist Menu')
    oc = ObjectContainer(no_cache = True)
    oc.title1 = title

    tracks = FetchTracks(key)
    for track in tracks:
        oc.add(CreateTrackObject(track))

    return oc

####################################################################################################
# Generating PopupDirectoryObject from Playlist XML

def CreatePlaylistObject(playlist):
    title = playlist.get(ATTR_TITLE)
    key = playlist.get(ATTR_KEY)

    callbackObject = Callback(PlaylistMenu, title=title, key=key)

    directoryObject = DirectoryObject(key=callbackObject, title=title)
    directoryObject.duration = attributeAsInt(playlist.get(ATTR_DURATION))
    directoryObject.summary = playlist.get(ATTR_SUMMARY)
    if playlist.get(ATTR_COMPOSITE) != None:
        directoryObject.thumb = playlist.get(ATTR_COMPOSITE)

    return directoryObject

####################################################################################################
# Conversion of Track XML to TrackObject

def CreateTrackObject(track):
    # Track Basics
    title = track.get(ATTR_TITLE)
    key = track.get(ATTR_KEY)
    ratingKey = track.get(ATTR_RATINGKEY)

    trackObject = TrackObject(title=title, key=key, rating_key=ratingKey)
    trackObject.artist = track.get(ATTR_GRANDPARENT_TITLE)
    trackObject.album = track.get(ATTR_PARENT_TITLE)
    if track.get(ATTR_THUMB) != None:
        trackObject.thumb = track.get(ATTR_THUMB)
    if track.get(ATTR_DURATION) != None:
        trackObject.duration = attributeAsInt(track.get(ATTR_DURATION))
    
    # Media Object
    partKey = track.get(ATTR_PARTKEY)
    mediaObject = MediaObject(parts=[PartObject(key=partKey)])
    mediaObject.duration = trackObject.duration
    mediaObject.bitrate = attributeAsInt(track.get(ATTR_BITRATE))
    mediaObject.audio_channels = attributeAsInt(track.get(ATTR_AUDIOCHANNELS))
    if track.get(ATTR_AUDIOCODEC) != None:
        mediaObject.audio_codec = track.get(ATTR_AUDIOCODEC)
    if track.get(ATTR_CONTAINER) != None:
        mediaObject.container = track.get(ATTR_CONTAINER)           
    trackObject.add(mediaObject)
    
    return trackObject

def attributeAsInt(attr_value, def_value = 0):
    if attr_value != None:
        try:
            if attr_value.isdigit():
                return int(attr_value)
        except Exception:
            pass
    return def_value

####################################################################################################
# PLEX Helpers

def GetPlexUrl(suffix=None):
    plexUrl = 'http://%s:%s' %(Prefs[PREFS__PLEXIP], Prefs[PREFS__PLEXPORT])
    if suffix is not None:
        plexUrl += suffix
    
    Log.Debug('Requesting Plex URL: %s' % (plexUrl))
    return plexUrl

def FetchPlaylists():
    Log.Debug('Fetching Playlists')

    playlistUrl = GetPlexUrl(LIBRARY_PLAYLISTS)
    el = XML.ElementFromURL(playlistUrl)
    Log.Debug(el)
    playlist_xpath = '%s[@playlistType="audio"]' % PMS_XPATH_PLAYLIST
    playlistXml = el.xpath(playlist_xpath)

    playlistXml.sort(key=lambda x: x.get(ATTR_TITLE), reverse=False)

    return playlistXml

def FetchTracks(playlistKey):
    Log.Debug('Fetching Tracks')

    playlistUrl = GetPlexUrl(playlistKey)
    el = XML.ElementFromURL(playlistUrl)
    playlist_xpath = '%s[@type="track"]' % PMS_XPATH_TRACK
    trackXml = el.xpath(playlist_xpath)

    return trackXml