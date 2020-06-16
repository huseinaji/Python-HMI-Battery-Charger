import http.client, urllib.request
import time
tic = time.perf_counter()
flag = 0
sendtime = 2

while True:
    toe = time.perf_counter()
    timm = toe - tic
    exx = "".join("{:0.2f}".format(timm % sendtime))

    print(float(exx))
    if float(exx) == 0:
        flag = flag + 1
        #print(flag)
        if flag == 1:
            print("xxx")
            #url = ("http://charging.genmotorcycles.com/index.php?bat_id=b0ffff2&volt=50&curr=4&soc=0&temp=0&capc=0&soh=0&cycle=0&B_over_charge=0&B_over_temp=0&B_under_temp=0&B_over_curr=0&B_over_volt=0&B_short_cirr=0&B_sys_failure=0&C_out_u_volt=0&C_out_o_volt=0&C_over_temp=0&C_under_temp=0&C_short_cirr=0&C_over_curr=0&C_in_o_voltage=0&C_in_u_voltage=0&C_lost_conn=0&doc=0&dot=0&dut=0&odc=0&imb=0&cs=0&ds=0&ss=0")
            #webUrl = urllib.request.urlopen(url)
            #print("result code " + str(webUrl.getcode()))
    else:
        flag = 0