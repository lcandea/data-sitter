# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                   BASIC CONFIG                                    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

FROM debian:bookworm

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG PYTHON_VERSION=3.12.8
ARG NODE_VERSION=22

ENV DEBIAN_FRONTEND=noninteractive

# Create a non-root user to use if preferred - see https://aka.ms/vscode-remote/containers/non-root-user.
RUN groupadd --gid $USER_GID $USERNAME && \
    useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME

# Add sudo support.
RUN apt-get update && apt-get install -y sudo && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

# ZSH config
RUN touch /home/${USERNAME}/.zshrc && \
    chown ${USER_UID}:${USER_GID} /home/${USERNAME}/.zshrc

# Volume for Python virtual env
RUN mkdir -p /workspace/.venv && \
    chown -R vscode:vscode /workspace/.venv

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                           INSTALLING PACKAGES WITH APT-GET                        #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get -y install --no-install-recommends \
        sudo git zsh curl wget ca-certificates build-essential unzip \
        locales openssh-client libpq-dev python3-dev \
        libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev \
        libffi-dev \liblzma-dev tk-dev xz-utils openssh-client 

# Installing Locales
RUN echo "LC_ALL=en_US.UTF-8" >> /etc/environment &&\
    echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen &&\
    echo "LANG=en_US.UTF-8" > /etc/locale.conf &&\
    locale-gen en_US.UTF-8

# Cleanup
RUN apt-get autoremove -y && \
    apt-get clean autoclean && \
    rm -rf /var/lib/apt/lists/*


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                            INSTALLING FROM OTHER SOURCES                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Installing Starship prompt
RUN curl -fsSL https://starship.rs/install.sh | sh -s -- --yes &&\
    printf 'eval "$(starship init zsh)"\n\n' >> /home/$USERNAME/.zshrc
RUN printf '\
    HISTFILE=~/.zsh_history\n\
    HISTSIZE=10000\n\
    SAVEHIST=10000\n\
    setopt appendhistory\n\
    setopt sharehistory\n\n' >> /home/$USERNAME/.zshrc

USER $USERNAME
# Install python with Pyenv 
RUN curl https://pyenv.run | bash
RUN printf 'export PYENV_ROOT="$HOME/.pyenv"\n' >> $HOME/.zshrc && \
    printf '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"\n' >> $HOME/.zshrc && \
    printf 'eval "$(pyenv init - zsh)"\n' >> $HOME/.zshrc && \
    printf 'eval "$(pyenv virtualenv-init -)"\n\n' >> $HOME/.zshrc && \
    $HOME/.pyenv/bin/pyenv install $PYTHON_VERSION &&\
    $HOME/.pyenv/bin/pyenv global $PYTHON_VERSION

# Adding Pyenv to sh too
RUN printf 'export PYENV_ROOT="$HOME/.pyenv"\n' >> $HOME/.profile && \
    printf '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"\n' >> $HOME/.profile && \
    printf 'eval "$(pyenv init --path)"\n' >> $HOME/.profile && \
    printf 'eval "$(pyenv virtualenv-init -)"\n' >> $HOME/.profile

# Install nvm
# RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash && \
#     export NVM_DIR="$HOME/.nvm" && \
#     [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" && \
#     nvm install $NODE_VERSION && \
#     nvm alias default $NODE_VERSION && \
#     nvm use default && \
#     corepack enable yarn

# RUN printf 'export NVM_DIR="$HOME/.nvm"\n' >> $HOME/.zshrc && \
#     printf '[ -s "$NVM_DIR/nvm.sh" ] && \\. "$NVM_DIR/nvm.sh"\n' >> $HOME/.zshrc && \
#     printf '[ -s "$NVM_DIR/bash_completion" ] && \\. "$NVM_DIR/bash_completion"\n' >> $HOME/.zshrc


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                              INSTALLING PYTHON PACKAGES                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
RUN export PATH="$HOME/.pyenv/shims:$PATH" &&\
    pip install --upgrade pip


# re-enable dialog mode for apt-get
ENV DEBIAN_FRONTEND=dialog
