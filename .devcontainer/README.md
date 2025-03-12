# Dev Container

- Install [VSCode](https://code.visualstudio.com) with the following extensions:
  - [VSCode Docker](vscode:extension/ms-azuretools.vscode-docker)
  - [VSCode Remote Containers](vscode:extension/ms-vscode-remote.vscode-remote-extensionpack)
  - [VSCode Dev Containers](vscode:extension/ms-vscode-remote.remote-containers)
  - [VSCode Remote SSH](vscode:extension/ms-vscode-remote.remote-ssh)
  - [VSCode Remote SSH: Editing Configuration Files](vscode:extensionms-vscode-remote.remote-ssh-edit)

## Mac Setup

- Install [Docker for Apple Silicon](https://desktop.docker.com/mac/main/arm64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-mac-arm64) or  [Docker for Intel Chip](https://desktop.docker.com/mac/main/amd64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-mac-amd64) depending of your machine

  - If your machine is an Apple Silicon, you have to install Rosetta 2 on your computer running this command in your terminal:

    ```bash
    softwareupdate --install-rosetta
    ```

- Check that you have the following folders `~/.aws` and `~/.ssh` - if either of these are missing you will need to create them with `mkdir` or via the Finder.

## Ubuntu Setup

Install Docker (Ubuntu)

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

Add yourself to docker users

```bash
sudo usermod -aG docker steven
docker run hello-world
```

Test it

```bash
sudo docker run hello-world
```

Reboot, then test your own user

```bash
sudo reboot now
```

```bash
docker run hello-world
```

## Windows

Install WSL (Windows Subsystem for Linux)

```bash
wsl --update
```

## Opening the project in Container

Once you have everything installed in your system, you should open this project in VSCode, and then a notification should pop up in de bottom right corner with a blue button which says: `Reopen in Container`. Click on that button to start. The first time you open the container, Docker wil start installing all the components defined in the `Dockerfile` file.

## Debugging/FAQs

- Current configuration of devcontainer mounts in credentials from the parent system's ~/.aws and ~/.ssh directories. If these do not exist, `docker run` command that runs on container startup will fail (due to not being able to mount these directories into the container).
