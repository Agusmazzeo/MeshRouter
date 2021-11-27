FROM raspbian/stretch:latest

RUN apt-get update
RUN apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev
RUN wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tar.xz
RUN tar xf Python-3.9.0.tar.xz && cd Python-3.9.0 && ./configure --enable-optimizations --prefix=/usr && make && make altinstall
RUN cd .. && rm -rf Python-3.9.0 && rm -rf Python-3.9.0.tar.xz && . ~/.bashrc
WORKDIR /app
COPY requirements.txt  /app
RUN python3.9 -m pip install --upgrade pip && python3.9 -m pip install -r requirements.txt 