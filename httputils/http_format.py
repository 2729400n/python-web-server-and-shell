import time

# This function formats the date into the HTTP Format


def local_http_time(settime: int = None):
    # checks if theere is a specified time
    # if not gets the current time
    # else it formats the specified time into a string
    if(settime == None):
        tempt1 = time.ctime(time.time())
    else:
        tempt1 = time.ctime(float(settime))
    tempt2 = tempt1.split()
    tempt3 = tempt1.split()
    tempt3[1] = tempt2[2]
    tempt3[2] = tempt2[1]
    tempt3[3] = tempt3[4]
    tempt3[4] = tempt3[3]
    tempt3.append("GMT")
    tempt3[0] = tempt3[0]+","
    return " ".join(tempt3)
