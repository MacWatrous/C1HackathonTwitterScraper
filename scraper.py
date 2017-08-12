import os

y = 12
#change for 2017 to 0,6
for y in range(6,13):
    if y in (1,3,5,7,8,10,12):
        days = 30
        sinceDays = 32
    elif y in (4,6,9,11):
        days = 29
        sinceDays = 31
    else:
        #change for 2017 to 28
        days = 28
        sinceDays = 29
    for x in range(27,days+2):
        if y < 10:
            z = '0'+str(y)
        else:
            z = ''+str(y)
        if days < 10:
            days2 = '0'+str(x)
            sinceDays = "0"+str(x+1)
        else:
            days2 = ""+str(x)
            sinceDays = "" + str(x+1)
        os.system("python /Users/ap/Downloads/GetOldTweets-python-master/Exporter.py --querysearch 'capital one' --since 2016-"+z+"-"+days2+" --until 2016-"+z+"-"+sinceDays+" --maxtweets 2400 --output 2016-"+z+"-"+days2+".csv")