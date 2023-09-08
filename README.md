# Slave Ship Database

## Run a production server

First, install Docker on your system. Then, either download Docker Compose from https://github.com/docker/compose/releases, or install it using your package manager.

Then, run:

```
$ docker compose up
```

Or, if you downloaded a Docker Compose binary:

```
$ ../docker-compose-linux-x86_64 up
```


## Run a development environment

Follow the same steps as the production server, but use slightly different commands to overlay the development config on the production config:

```
$ docker compose -f docker-compose.yml -f docker-compose.dev.yml up
$ # OR
$ ../docker-compose-linux-x86_64 -f docker-compose.yml -f docker-compose.dev.yml up
```


## Interacting with the web page

The web site is available on both port 3000 and port 4000. You can enable / disable each at your convenience. Go to http://localhost:3000/ to interact with it!
