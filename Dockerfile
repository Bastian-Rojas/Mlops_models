FROM jenkins/jenkins:2.452.2-jdk17

USER root

# Instala las dependencias del sistema, incluyendo libgl1
RUN apt-get update && apt-get install -y lsb-release libgl1

# Instala Docker CLI
RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
  https://download.docker.com/linux/debian/gpg
RUN echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
  https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
RUN apt-get update && apt-get install -y docker-ce-cli

USER jenkins

# Instala plugins de Jenkins
RUN jenkins-plugin-cli --plugins "blueocean docker-workflow"
