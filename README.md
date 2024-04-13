# NHL Gameday Bot for Lemmy
This project is a Python application that allows you to host an NHL gameday thread bot in a Lemmy community of your choice.

Disclaimer: I use podman, not docker. So all the docker commands are untested.

## Build it from source
1. Git clone the repo: `git clone git@github.com:dandroid126/lemmy-nhl-gdt-bot.git`
2. Create the out directory. ([See section](#create-the-out-directory))
3. Create the environment file. ([See section](#create-the-environment-file))
4. Open the project in Pycharm
5. Select the run configuration 'Docker'
6. Run it!

Alternatively, if you don't want to use Pycharm, you can build and run it from command line. 
```bash
git clone git@github.com:dandroid126/lemmy-nhl-gdt-bot.git
cd lemmy-nhl-gdt-bot
podman build --tag  lemmy-nhl-gdt-bot .
docker run --rm -d --name lemmy-nhl-gdt-bot -e TZ={{timezone}} -v ./.env:/app/.env -v ./out:/app/out localhost/lemmy-nhl-gdt-bot:latest
```
There's a shell script `run.sh` included in the repo to do this. This is what the run configuration in Pycharm actually calls. So if you want to make your life easy, you can use that.

## Just host it
1. Create the out directory. ([See section](#create-the-out-directory))
2. Create the environment file. ([See section](#create-the-environment-file))
3. Run it
```bash
docker run --rm --name lemmy-nhl-gdt-bot -e TZ={{timezone}} -v ./.env:/app/.env -v ./out:/app/out ghcr.io/dandroid126/lemmy-nhl-gdt-bot:main
```

## Create the out directory
1. If you are using docker, it is easy:
    ```bash
    mkdir -p lemmy-nhl-gdt-bot/out
    cd lemmy-nhl-gdt-bot
    chown -R 1000:1000 out
    ```
2. If you want to use rootless podman, it is a bit more complicated. Because of the complexity of UIDs in rootless podman, in my opinion, the easiest way is to make an out directory with 777 permissions, run the container, have it create some files, get the UID from those and set the ownership based on that, then reset the permissions.
    ```bash
    mkdir -p lemmy-nhl-gdt-bot/out
    cd lemmy-nhl-gdt-bot
    sudo chmod 777 out
    podman run --rm -d --name lemmy-nhl-gdt-bot -e TZ={{timezone}} -v ./.env:/app/.env -v ./out:/app/out ghcr.io/dandroid126/lemmy-nhl-gdt-bot:main
    sleep 5 # Only needed if running this in a script
    podman kill lemmy-nhl-gdt-bot
    userId=$(ls -al out/log.txt | cut -d " " -f 3)
    sudo chown -R $userId:$userId out
    sudo chmod 775 out
    ```

## Create the environment file
The environment file is used for configuring the script. You will need to set your bot account's credentials and what types of posts are made for each type of game. Optionally, you can add which teams you want posts created for. If this is left out, posts will be made for all teams. 

If a game type is listed in COMMENT_POST_TYPES, details of all games of that type are made as comments to a daily thread. If you have a large number of teams you are posting games for and a small community, this might be desired to reduce spam to you community. If a game type is listed in GDT_POST_TYPES, details of all games of that type are made as a post directly to the community, so you will get one post per game.

There is an example file that you can use as a template:
   ```bash
   wget -O .env 'https://raw.githubusercontent.com/dandroid126/lemmy-nhl-gdt-bot/main/environment_example'
   ```

TODO: add systemd service instructions
