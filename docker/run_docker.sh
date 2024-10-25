#!/bin/sh
uid=$(eval "id -u")
gid=$(eval "id -g")


docker run --rm -it --privileged --net=host --ipc=host --gpus all -e DISPLAY=$DISPLAY -d \
--name blenderproc2 \
-v $PWD/.vscode:/BlenderProc2/.vscode \
-v $PWD/DataGenerator:/BlenderProc2/DataGenerator \
-v $PWD/cc_textures:/BlenderProc2/cc_textures \
-v $PWD/ground:/BlenderProc2/ground \
-v $PWD/object:/BlenderProc2/object \
-v $PWD/Dataset:/BlenderProc2/Dataset \
-v $PWD/Config:/BlenderProc2/Config \
-v /dev:/dev:ro \
-v /tmp/.X11-unix:/tmp/.X11-unix:ro \
iras/blenderproc2
