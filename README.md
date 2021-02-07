# PLEX Playlist Hosting Channel

This was built to work around a limitation of PLEX where it doesn't make Music playlists available to UPnP clients. This makes it difficult to use with systems like HEOS and other UPnP clients, which is sad because PLEX does a lot of things right with how it exposes music to these clients otherwise. 

It creates a new channel that simply passes along everything it finds in the server's Playlists. It will filter playlists to just audio playlists, giving a clean list.

Based off of: https://github.com/cp9999/MusicPlaylist.bundle

### Installation

Copy the PlaylistHost.bundle to the Plex Media Server plugins folder for your installation. 

See this link for further details: https://support.plex.tv/articles/201187656-how-do-i-manually-install-a-plugin/

## Configuration

Right now there's just three settings:

* IP Address of the Plex Server
* Port of the Plex Server
* Plex token to connect to the Plex Server

The first two are both set to sane defaults which should work in most cases. The [Plex token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/) needs to be found for each particular account (only once) and entered in the plugins settings.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

### TODO

* Allow HTTPS connections to PLEX, if possible.
* Allow Renaming of channel to something other than "Playlists", if possible.
* ~~Provide non-placeholder images for resources.~~

## Authors

* **Adam Thayer** - *Initial work* - [Kaiede](https://github.com/Kaiede)

See also the list of [contributors](https://github.com/Kaiede/PlaylistHost/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

Icons made by [Freepik](https://www.freepik.com) from [Flaticon](https://www.flaticon.com/)
