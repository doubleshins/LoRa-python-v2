#!/bin/bash
network="168.95.1.1"              # 定義網域
for sitenu in $(seq 1 100)       
do
		sleep 3
	# 取得 ping 的回傳值是正確的還是失敗
        ping -c 1 -w 1 ${network} &> /dev/null && result=0 || result=1
	#最多6次 18秒 break
	    if [ ${sitenu} ==  6 ]; then	
				echo "break ${network} is ${sitenu}"
				break
	# 正確的啟動 (UP) 還是錯誤的沒有連通 (DOWN)
        elif [ "${result}" == 0 ]; then
                echo "Server ${network} is UP ${sitenu}"
				break
		else
                echo "Server ${network} is DOWN ${sitenu}"
        fi
done
