ip=192.168.1.3
puerto=4747
cam=0

sudo modprobe v4l2loopback
sudo ffmpeg -i http://${ip}:${puerto}/video -vf format=yuv420p -vcodec rawvideo -pix_fmt yuv420p -f v4l2 /dev/video${cam}