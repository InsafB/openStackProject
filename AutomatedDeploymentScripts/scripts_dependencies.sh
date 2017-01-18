#!/bin/bash

source project9-openrc.sh

export LC_ALL=C

sudo apt-get update

if sudo apt -y install python3-pip ; then
    echo "python3-pip installation succeeded"
else
    echo "python3-pip installation failed"
fi

if ("$1" = "ServerB" || "$1" = "ServerP") then
    if sudo apt-get -y install python3-swiftclient ; then
        echo "swiftclient installation succeeded"
    else
        echo "swiftclient installation failed"
    fi
fi   

if sudo pip3 install flask ; then
    echo "flask installation succeeded"
else
    echo "flask installation failed"
fi

if ("$1" = "ServerM") then
    if sudo pip3 install Flask-Mail ; then
        echo "flask-mail installation succeeded"
    else
        echo "flask-mail installation failed"
    fi
fi    

if ("$1" = "ServerB" || "$1" = "ServerP") then
    if sudo pip3 install pymysql ; then
        echo "pymysql installation succeeded"
    else
        echo "pymysql installation failed"
    fi
fi    

if ("$1" = "ServerW") then
    wget http://www.imagemagick.org/download/ImageMagick.tar.gz
    tar -xvf ImageMagick.tar.gz
    cd ImageMagick-7.*
    ./configure
    make
    if sudo make install ; then
        echo "MagikImage installation succeeded"
        sudo ldconfig /usr/local/lib 
    else
        echo "MagikImage installation failed"
    fi
fi
