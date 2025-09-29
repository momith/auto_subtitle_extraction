This (docker) service can be installed on your media server (emby, plex, ...). It will automatically extract embedded subtitles from mkv files.

Setup:
- Install docker and docker-compose if not already installed
- Fill environment variables in the docker-compose.yml
- WATCH_FOLDERS shall be the directories where to recursively check for MKV files from which to extract their embedded subtitles
- CHECK_INTERVAL the interval in which to check for new mkv files
- Run docker-compose up -d to start the service
