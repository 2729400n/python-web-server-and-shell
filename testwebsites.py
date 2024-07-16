#!/usr/bin/bash


import threading,netifaces,ipaddress,io,builtins,systemd,socket,shutil,shlex,sched,multiprocessing

listen_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM,socket.IPPROTO_TCP)
connector_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM,socket.IPPROTO_TCP)
listen_sock.listen()
connector_sock.listen()
connector_sock.accept()
wr_file_listen =listen_sock.makefile("rwb")
wr_file_connector = connector_sock.makefile("rwb")


"""GET / HTTP/2
Host: www.google.com
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Cookie: CONSENT=YES+cb.20211026-09-p1.en+FX+681; NID=511=Z0Q-erYf0iMHRb10KT80sogAhV-JxYXdpHMkUtEXcll7qePVTE2Q5eWIoNHjPpVr-1gS1BmQr25gwCQpXWbwmvgX6e8S-8Iig3XpS3ZKUy3kumPzGlpE2hBs9Fe5XI9eUd0NBd-zO9b1jUvhRrEbPjFbaHkNE3tzBS51bZghEF64FboJut1iCi17pyspLo7HG5y5ylRILpO0qZyIJW984r8rPDdmtuIHo4ElB5tuyp57JmazbrAYUJmHp1RN-19cKYOQ3iTWe5gu6Em0R84BQZXlcVA65c5nDsSApLpG3pMEzpz8iQJKgoBaaKuQCfrs6WojMipTyDK5Ru6FL07Gxe83esp6cQVajO6P0jW4vRl11Jwm5h_i0j9RYV2a1SYGaA0sNHPOKLLj2KdCuGKsH24; 1P_JAR=2022-01-12-17; SID=FQiWKRXCAJ9Q2YaQFRflMeIjhiTLXCq_TSzKqbupnm7cr-W1yttjCpMsIR9VFm_YizD6BA.; __Secure-1PSID=FQiWKRXCAJ9Q2YaQFRflMeIjhiTLXCq_TSzKqbupnm7cr-W1zW0g3oGTUc8oIUGPjLw1Tw.; __Secure-3PSID=FQiWKRXCAJ9Q2YaQFRflMeIjhiTLXCq_TSzKqbupnm7cr-W1luaKxa-MUBh8w_erBjnH6g.; HSID=AzsKYfuGusfZ0TfXZ; SSID=Ar8ttjGEyj9taKNM4; APISID=zdZy06-lNsTSh1tZ/AIjjVVU3T4zMVmpNb; SAPISID=c9ujzyqujU4C_D3e/AUeAPoUzgby_LVPly; __Secure-1PAPISID=c9ujzyqujU4C_D3e/AUeAPoUzgby_LVPly; __Secure-3PAPISID=c9ujzyqujU4C_D3e/AUeAPoUzgby_LVPly; SIDCC=AJi4QfHdZiNRJDzptBW3Y7a0lWQNUVvFI_D9YhXTR4jtirZuBcOK4cOYLEeRqTEBU8IYFirgIg; __Secure-3PSIDCC=AJi4QfGjsHVad6Q8X-Zm9SmhlAb2bfj3zXRpOatL-9X_DrgzLQbF0fkTKu-ItfIHYK8nOQ46Jg; SEARCH_SAMESITE=CgQI9JMB; ANID=AHWqTUkqf9ot-dLnlEj3NkJH8GKpY9nvaiS8SLJCRTB0tPkG4aYeVQ7Jw04-GWR2; __Secure-1PSIDCC=AJi4QfFOb5r2S6TkhXMWtvCTd9WMmIx8fDaghHNVJF31Z1YPFm6FiFkx9AX6hsFfanCDGmU-NQ; OTZ=6323044_56_56_123900_52_436380
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1"""