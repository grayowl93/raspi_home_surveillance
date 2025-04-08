# raspi_home_surveillance
raspberrypi0を使った、遠隔監視

一人暮らしの生活活動を１日毎通知する。  
冷蔵庫につけたスイッチで開閉をカウントする。  
焦電センサーで台所に立った回数をカウントする。  
午前０時にメールで、一日の活動を通知する。  

課題  
焦電センサーが過剰に反応して人感センサーとして機能していない。  
  

元ネタ

監視の概要  
https://qiita.com/Saito5656/items/ff9743e471592f38a463

AWSのセキュリティ設定  
https://qiita.com/Kazuya_Murakami/items/bc520430fc1efdd0d118

ハード：RaspberryPi　Zero  
配線  
             5V       NC  
13 GPIO_27   IR-OUT   LED-RED   5V  
             GND      LED-BLACK Tr-1+GPIO_23 16  
   GND       RED-SW   Door-SW-  GND  
15 GPIO_22   RED-SW   Door-SW+  GPIO_17      11  
  
18 Tr2+GPIO_24  
12 Tr3+GPIO_25   
22 Tr4+PWM0-Buzzer  
  
  
  サービスの登録  
/etc/systemd/system/zushi.service  

zushi.serviceの中身  
[Unit]  
Description=Survaillance zushi  
  
[Service]  
Type=simple  
WorkingDirectory=/home/orca  
ExecStart=/usr/bin/python3 -m surveillance_zushi.py  
  
[Install]  
WantedBy=multi-user.target  
  

ソースファイルの内容  
surveillance_zushi.py  :監視プログラム本体
  
chk_gpio.py           :GPIOのテスト  
IR_Test.py            :焦電センサーのテスト  
sendGmail.py          :Gmail送信テスト  
sendShortMessage.py   :ショートメッセージのテスト  
  
  
ターミナルターミナルターミナルterminal  
>ls -l /dev/tty.*  
  
moriou-no-MacBook-Pro:~ orca$ ls -l /dev/tty.*  
crw-rw-rw-  1 root  wheel   34,   0  2 22 19:41 /dev/tty.Bluetooth-Incoming-Port  
crw-rw-rw-  1 root  wheel   34,   2  2 23 11:59 /dev/tty.usbmodem14201  
ターミナル  
screen /dev/tty.usbmodem14201  
  
Wi-fi接続  
  
#/etc/ssh/sshd_config  
Port 7541  
  
#check  
sshd -t  
  
#service sshd restart  
Redirecting to /bin/systemctl restart sshd.service  
  
SSH接続  
ssh -p 7541 orca@raspberrypi.local  
  
USBシリアルシリアル　 serial  
/boot/config.txt  
dtoverlay=dwc2  
  
/boot/cmdline.txt  
modules-load=dw,g_serial  
  
change port number  
/etc/ssh/sshd_config  
  
リンクを追加  
cd /etc/systemd/system/getty.target.wants   
ln -s /lib/systemd/system/getty@.service getty@ttyGS0.serviceß  
  
piユーザーの削除と、追加  
$ sudo useradd -m -orca  
$ sudo passwd orca  
sudo gpasswd -a orca sudo  
  
login:orca  
password:native93orca  
  
SSH接続、ポート指定  
ssh -p 7541 orca@raspberrypi.local  
  
SCP転送、ポート指定  
$ scp -P 7541 ./*.py orca@192.168.3.77:/home/orca/  
  
copy SD card  
  
1.disk番号の確認  
>diskutil list  
  
2.アンマウント  
>diskutil unmountDisk /dev/disk_数字  
  
3.バックアップ、r付き  
>sudo dd if=/dev/rdisk4 of=backup1.img bs=1m  
  
4.コピー  
>sudo dd if=./backup1.img of=/dev/rdisk4 bs=1m  
  
 日本語化  
sudo dpkg-reconfigure locales  
a_JP.UTF-8を選択  
  
タイムゾーンの設定  
sudo raspi-config  
  
日本語フォント  
sudo apt-get install ttf-kochi-gothic xfonts-intl-japanese xfonts-intl-japanese-big xfonts-kaname -y  
  
    
日本語入力  
sudo apt-get install -y uim uim-anthy  
  
WiFi  
orca@raspberrypi:/etc/wpa_supplicant$   
orca@raspberrypi:/etc/wpa_supplicant$ ls -l  
合計 52  
-rwxr-xr-x 1 root root   937  2月 26  2021 action_wpa.sh  
-rw-r--r-- 1 root root 25569  2月 26  2021 functions.sh  
-rwxr-xr-x 1 root root  4696  2月 26  2021 ifupdown.sh  
-rw-r--r-- 1 root root   179  2月 21 14:46 wpa_supplicant.conf  
-rw-r--r-- 1 root root   125  2月 21 14:54 wpa_supplicant.conf.30F  
-rw-r--r-- 1 root root   125  2月 21 15:11 wpa_supplicant.conf.zushi  
  
Pyhon3をデフォルトに  
cd /usr/bin  
sudo unlink python  
sudo ln -s python3 python  
  
Gmail  
password:vipvim-doxvyk-9wiNty  
name: yardbirds gray  
address:yardbirds.zushi7541@gmail.com  
  
exim4をインストールする  
sudo apt-get install exim4  
  
  
exim4を設定  
sudo dpkg-reconfigure exim4-config  
  
# 以下をファイルの末尾に追加してください（もちろん全角文字のところは置き換えてね！）  
gmail-smtp.l.google.com:メールアドレス@gmail.com:アプリ パスワード  
*.google.com:メールアドレス@gmail.com:アプリ パスワード  
smtp.gmail.com:メールアドレス@gmail.com:アプリ パスワード  
  
# Example:  
### target.mail.server.example:login:password  
gmail-smtp.l.google.com:yardbirds.zushi7541.gmail.com:vipvim-doxvyk-9wiNty  
*.google.com:yardbirds.zushi7541.gmail.com:vipvim-doxvyk-9wiNty  
smtp.gmail.com:yardbirds.zushi7541.gmail.com:vipvim-doxvyk-9wiNty  
  
gmail-smtp.l.google.com:<メyardbirds.zushi7541@gmail.com:vipvim-doxvyk-9wiNty  
*.google.com:yardbirds.zushi7541@gmail.com:vipvim-doxvyk-9wiNty  
smtp.gmail.com:yardbirds.zushi7541@gmail.com:vipvim-doxvyk-9wiNty  
  
  
*.google.com:username@gmail.com:password  
smtp.gmail.com:username@gmail.com:password  
gmail-smtp-msa.l.google.com:username@gmail.com:password  
  
/etc/exim4/passwd.client のアクセス権変更  
$ sudo chmod 640 /etc/exim4/passwd.client  
$ sudo chown root:Debian-exim /etc/exim4/passwd.client  
$ sudo update-exim4.conf  
  
  
https://qiita.com/Kazuya_Murakami/items/bc520430fc1efdd0d118  
  
google app password  
oequbkwdzvuadojn  
  
$ sudo apt install ssmtp  
$ sudo vi /etc/ssmtp/ssmtp.conf  
  
修正前：root=postmaster  
修正後：root=メールアドレス@gmail.com  
  
修正前：mailhub=mail  
修正後：mailhub=smtp.gmail.com:587  
  
ファイル末尾に追加：  
AuthUser=メールアドレス@gmail.com  
AuthPass=アプリ パスワード（16文字空白なし）  
UseSTARTTLS=YES  
  


orca@raspberrypi:~$ python sendGmail.py
mail Sending now...
Traceback (most recent call last):
  File "/home/orca/sendGmail.py", line 42, in <module>
    sendMsg_eMail(mail_from, mail_to, mail_cc, mail_subject, mail_body, mail_encode)
  File "/home/orca/sendGmail.py", line 33, in sendMsg_eMail
    print("{0} send message.".format(to_addr))
NameError: name 'to_addr' is not defined


export PATH=$PATH:~/.local/bin 
# configures the path to include the directory with the AWS CLI
git clone https://github.com/aws/aws-cli.git 
# download the AWS CLI code from GitHub
cd aws-cli && git checkout v2 
# go to the directory with the repo and checkout version 2
pip3 install -r requirements.txt 
# install the prerequisite software

pip3 install . # install the AWS CLI 

証明書
raspberrypi_zushi.cert.pem
メッセージを送受信するスクリプト
start.sh
プライベートキー
raspberrypi_zushi.private.key
ポリシー
raspberrypi_zushi-Policy
ポリシーを表示
AWS IoT デバイス SDK
Python

cd ~
git clone https://github.com/awslabs/aws-iot-device-client aws-iot-device-client
mkdir ~/aws-iot-device-client/build && cd ~/aws-iot-device-client/build
cmake ../
cmake --build . --target aws-iot-device-client

./aws-iot-device-client --help

mkdir ~/certs/testconn
aws iot create-keys-and-certificate \
--set-as-active \
--certificate-pem-outfile "~/certs/testconn/device.pem.crt" \
--public-key-outfile "~/certs/testconn/public.pem.key" \
--private-key-outfile "~/certs/testconn/private.pem.key"

aws iot create-keys-and-certificate --set-as-active --certificate-pem-outfile "~/certs/testconn/device.pem.crt" --public-key-outfile "~/certs/testconn/public.pem.key" --private-key-outfile "~/certs/testconn/private.pem.key"

アカウaccount name:grayowl93
account ID:959363874591
accsess key:**************
sercret accsess key:*****************************
Default region name [None]: ap-northeast-1
Default output format [None]: text

コンソールパスワード
console password
https://959363874591.signin.aws.amazon.com/console

user name
raspberrypi_zushi

AWS
console password
reqke6-Zuwquw-tuzdag


user name
raspi_zushi
pass word: A$x1lC4=
  

awscli 1.27.80 has requirement botocore==1.29.80, but you'll have botocore 2.0.0.dev155 which is incompatible.
boto3 1.26.80 has requirement botocore<1.30.0,>=1.29.80, but you'll have botocore 2.0.0.dev155 which is incompatible.

/etc/systemd/system

/usr/bin/python3: Error while finding module specification for 'test.py' (ModuleNotFoundEr


IP setting

sudo nano /etc/dhcpcd.conf

interface wlan0
static ip_address=192.168.3.9/24
static routers=192.168.3.1
static domain_name_servers=192.168.3.1

192.168.0.236
->192.168.0.237
