FROM nvidia/cuda:12.0.0-devel-ubuntu22.04

USER root 
RUN apt-get update && apt-get upgrade -y && export DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y \
    git \
    libfontconfig1 \
    libfreeimage-dev \
    libgl1 \
    libjpeg-dev \
    libxi-dev \
    libxrender1 \
    libxxf86vm1 \
    libglib2.0-0 \
    python3-pip \
    libosmesa6-dev \
    freeglut3-dev \
    python3.10-venv \
    software-properties-common \
    wget \
    curl \
    python3-dev \
    python3-pip \
    python3-wheel \
    python3-setuptools \
    '^libxcb.*-dev' \
    libx11-xcb-dev \
    libglu1-mesa-dev \
    libxrender-dev \
    libxi-dev \
    libxkbcommon-dev \
    libxkbcommon-x11-dev \
    zlib1g-dev
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# ENV QT_DEBUG_PLUGINS=1

WORKDIR /BlenderProc2

# Create dir to mount volumes
RUN mkdir -p ./.vscode &&\
    mkdir -p ./DataGenerator &&\
    mkdir -p ./cc_textures &&\
    mkdir -p ./ground &&\
    mkdir -p ./object &&\
    mkdir -p ./Dataset &&\
    mkdir -p ./Config
    
# Copy and unpack the blender for linux tar.xz file
COPY blender-3.3.1-linux-x64.tar.xz .
RUN mkdir -p blender-3.3.1-linux-x64 \
    && tar -xf ./blender-3.3.1-linux-x64.tar.xz -C ./blender-3.3.1-linux-x64 \
    && rm ./blender-3.3.1-linux-x64.tar.xz

# Create a virtual environment
RUN python3 -m venv ./BlenderProcPython

# Set environment variables to use the virtual environment
ENV VIRTUAL_ENV=./BlenderProcPython
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"
ENV PYTHONPATH="${VIRTUAL_ENV}/lib/python3.10/site-packages:$PYTHONPATH"

# Install packages within the virtual environment
RUN ${VIRTUAL_ENV}/bin/pip install --upgrade pip 
RUN ${VIRTUAL_ENV}/bin/pip install -U wheel setuptools
COPY docker/requirements.txt .
RUN ${VIRTUAL_ENV}/bin/pip install --no-cache-dir -r ./requirements.txt

# Replace script with predefined blender exe location
COPY command_line.py ${VIRTUAL_ENV}/lib/python3.10/site-packages/blenderproc/

# Copy setup script
COPY setup.py ${VIRTUAL_ENV}/lib/python3.10/site-packages/blenderproc/scripts/

# Install debugpy and dependencies
RUN blenderproc run ${VIRTUAL_ENV}/lib/python3.10/site-packages/blenderproc/scripts/setup.py &&\
    blenderproc pip install debugpy 

ENV HOST_ID=1002
ENV HOST_GID=1002
ENV DISPLAY=$DISPLAY
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute

CMD sleep infinity
