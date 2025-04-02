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

