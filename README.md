

miyawa-tarou.comデータとかでnginxは準備済みとする

```
sudo apt install python3-pip
python3 -m pip install bs4
/usr/bin/python3 get_latest_video.py
ln -s /var/www/yahoo_weather_videos/src/video_list.csv /var/www/miyawa_tarou_com/lab/video_list.csv

contab -e

25 * * * * cd /var/www/yahoo_weather_videos/src; /usr/bin/python3 get_latest_video.py > /var/www/yahoo_weather_videos/src/get_id.log 2>&1

```

min.txtとvideo_list.csvの最新はscpなどでサーバーから持ってくるしかない
データが消失すると一緒に死ぬ
