apt-get install python3-pip -y
apt-get install python3-pil python3-pil.imagetk ffmpeg -y

pip3 install icalendar imutils Pillow scikit-image

cd ~
echo ">>Fetching OpenCV..."
git clone https://github.com/opencv/opencv.git
sudo apt-get install build-essentials -y
sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev -y
sudo apt-get install libgl1-mesa-dev -y
sudo apt install libgstreamer-plugins-base1.0-dev -y

cd ./opencv
mkdir release
cd release
echo ">>Compiling OpenCV..."
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local ..

make
sudo make install
