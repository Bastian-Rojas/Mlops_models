FROM jenkins/jenkins:2.452.2-jdk17

USER root

# Actualizar e instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    lsb-release \
    python3 \
    python3-venv \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Crear un entorno virtual y activar
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Instalar pip y paquetes de Python dentro del entorno virtual
RUN pip install --no-cache-dir \
    torch \
    torchvision \
    torchaudio \
    numpy \
    pyyaml \
    python-telegram-bot \
    ultralytics

# Añadir la clave GPG de Docker y el repositorio de Docker
RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc https://download.docker.com/linux/debian/gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.asc] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends docker-ce-cli \
    && rm -rf /var/lib/apt/lists/*

USER jenkins

# Instalar plugins de Jenkins
RUN jenkins-plugin-cli --plugins "blueocean docker-workflow"
