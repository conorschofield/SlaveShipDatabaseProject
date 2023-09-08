# Getting set up - the Docker way

While there is no need to use Docker since you can just follow the manual setup process, once you have Docker working (the hard part) getting the actual webapp running is a breeze. It's always up to you whether you actually use Docker!

The advantage of using Docker is that beyond the steps of installing Docker, its impact on your host system is constrained. If you want to clear all trace of this project having existed on your computer, just delete the folder and it's gone!


## If you are on Windows...

If you're on Windows (boo, hiss!) you'll need to apply a number of workarounds to get Docker to work nicely. Using Docker Desktop will let you skip all steps after step 1, however.

1. Set your WSL version to 2:
   ```
   wsl --set-default-version 2
   ```
2. Update the WSL version of your existing WSL instance, if needed:
   ```
   wsl --set-version Debian 2
   ```
3. Enter WSL in the root of the project:
   ```
   wsl
   ```
4. Work around the [WSL kernel not supporting nftables](https://github.com/microsoft/WSL/issues/6044):
   ```sh
   sudo update-alternatives --set iptables /usr/sbin/iptables-legacy
   sudo update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy
   ```
5. Now start the ["If you are on Linux..."](#if-you-are-on-linux) section, now that you have a working Linux environment on Windows.


As an additional workaround, remember to start Docker once it is ready. **You need to do this every time you start the WSL shell!!!** This step is not necessary on Linux.

```sh
sudo service docker start
```

After that, you can run `service docker status` to check whether Docker is running. If it is working properly, you should see:

```
$ service docker status
Docker is running.
```


## If you are on Linux...

1. Install Docker and Docker Compose (steps may differ based on distribution):
   ```sh
   sudo apt install docker-compose docker.io
   ```
2. Add yourself to the Docker user group (may not be necessary on all distributions):
   ```sh
   sudo usermod -a -G docker $(whoami)
   ```
3. You are now ready to run Docker commands.


## Running the webapp

Just run the following in your shell to get the whole app started!

```
docker-compose up
```

To fill in the database with imported spreadsheet data, run the following command:

TODO
