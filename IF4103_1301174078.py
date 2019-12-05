import csv

#readfile
def readFile():
    fail = open('f:/SMT 5/AI/tupro 3/influencers.csv', 'r')
    data = csv.reader(fail)
    dataLama = []
    c=1
    for i in data:
        if c==1:
            c+=1
        else:
            dataMasuk = {
                'record': i[0],
                'follow' : int(i[1]),
                'rate'  : float(i[2])
            }
            dataLama.append(dataMasuk)
    fail.close()
    return dataLama

#Fuzzification Follower 
#batas rendah: 5000 - 15000
def rendahFollow(x):
    a = 5000
    b = 15000
    if x>=b: return 0
    elif (x<b) and (x>=a): return round((b-x)/(b-a),2)
    elif x<a: return 1

#batas sedang: bot to up 14000 - 25000 , at up 25000-40000 , up to bot 40000 - 50000
def sedangFollow(x):
    a = 14000
    b = 25000
    c = 40000
    d = 50000
    if x<=a or x>=d: return 0
    elif (x<b) and (x>a): return round((x-a)/(b-a),2)
    elif x>=b and x<=c: return 1
    elif x>c and x<=d: return round(-((x-d)/(d-c)),2)

#batas tinggi: 45000 - 90000
def tinggiFollow(x):
    a = 45000
    b = 90000
    if x<=a: return 0
    elif (x<=b) and (x>a): return round((x-a)/(b-a),2)
    elif x>b: return 1

#Fuzzification Engagement Rate
#batas rendah: 0.5 - 1.5
def rendahEngage(x):
    a = 0.5
    b = 1.5
    if x>=b: return 0
    elif (x<b) and (x>=a): return round((b-x)/(b-a),2)
    elif x<a: return 1

#batas sedang: bot to up 1.4 -  2.5, at up 2.5 - 4.0, up to bot 4.0 - 5.0
def sedangEngage(x):
    a = 1.4
    b = 2.5
    c = 4.0
    d = 5.0
    if x<=a or x>=d: return 0
    elif (x<b) and (x>a): return round((x-a)/(b-a),2)
    elif x>=b and x<=c: return 1
    elif x>c and x<=d: return round(-((x-d)/(d-c)),2)

#batas tinggi: 4.5 - 9.0
def tinggiEngage(x):
    a = 4.5
    b = 9.0
    if x<=a: return 0
    elif (x<=b) and (x>a): return round((x-a)/(b-a),2)
    elif x>b: return 1

#Membership data
def membershipData(x):
    dataBaru = []
    for data in x:
        dataMasuk = {
            'record' : data['record'],
            'tinggiF' : tinggiFollow(data['follow']), #Follower -> High
            'sedangF' : sedangFollow(data['follow']), #Follower -> Average
            'rendahF' : rendahFollow(data['follow']), #Follower -> Low
            'tinggiE' : tinggiEngage(data['rate']), #Engagement Rate -> Upper
            'sedangE' : sedangEngage(data['rate']), #Engagement Rate -> Middle
            'rendahE' : rendahEngage(data['rate'])  #Engagement Rate -> Bottom
        }
        dataBaru.append(dataMasuk)
    return dataBaru

#Rule Inferensi
def fuzzyRule(x):
    dataBaru = []
    for data in x:
        highup  = min(data['tinggiF'], data['tinggiE']) #cari MIN dari High dan Upper       (Accepted)
        highmid = min(data['tinggiF'], data['sedangE']) #cari MIN dari High dan Middle      (Accepted)
        highbot = min(data['tinggiF'], data['rendahE']) #cari MIN dari High dan Bottom      (Considered)

        aveup   = min(data['sedangF'], data['tinggiE']) #cari MIN dari Average dan Upper    (Accepted)
        avemid  = min(data['sedangF'], data['sedangE']) #cari MIN dari Average dan Middle   (Considered)
        avebot  = min(data['sedangF'], data['rendahE']) #cari MIN dari Average dan Bottom   (Rejected)

        lowup   = min(data['rendahF'], data['tinggiE']) #cari MIN dari Low dan Upper        (Accepted)
        lowmid  = min(data['rendahF'], data['sedangE']) #cari MIN dari Low dan Middle       (Rejected)
        lowbot  = min(data['rendahF'], data['rendahE']) #cari MIN dari Low dan Bottom       (Rejected)

        dataMasuk = {
            'record'    : data['record'],
            'acc'       : max(highup,highmid,aveup,lowup),        #cari MAX dari yang ACCEPTED
            'cons'      : max(highbot,avemid),                    #cari MAX dari yang CONSIDERED
            'rejec'     : max(avebot,lowmid,lowbot)               #cari MAX dari yang REJECTED
        }
        dataBaru.append(dataMasuk)
    return dataBaru

#Deffuzifucation with Takagi-Sugeno-Style
def deffuzification(x):
    dataBaru = []
    for data in x:
        takagi = (30*data['rejec']) + (60*data['cons']) + (100*data['acc'])
        finalTakagi = takagi / (data['rejec'] + data['cons'] + data['acc'])
        dataMasuk = {
            'record' : data['record'],
            'final'  : finalTakagi 
        }
        dataBaru.append(dataMasuk)
    return dataBaru

#Mengambil 20 data dengan Score terbesar
def bestGuy(x):
    c = 0
    dataBaru = []
    for data in x:
        if c<20:
            dataMasuk = {
                'Id' : data['record']
            }
            dataBaru.append(dataMasuk)
            c+=1
    return dataBaru

#Write File
def writeFile(x):
    with open('f:/SMT 5/AI/tupro 3/chosen.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['Id'])
            writer.writeheader()
            for data in x:
                writer.writerow(data)

dataLama = readFile()                       #Read File
dataInferensi = membershipData(dataLama)    #Membership Data
dataDefuzzy = fuzzyRule(dataInferensi)      #Inferensi Data dengan Fuzzy Rule yang dibuat
dataFinal = deffuzification(dataDefuzzy)    #Defuzzification dengan Takagi-Sugeno-Style
dataSuperFinal = sorted(dataFinal,key=lambda x:x['final'], reverse=True ) #Sorting berdasarkan Score terbesar
dataChosen = bestGuy(dataSuperFinal)        #Mengambil 20 data terbaik
writeFile(dataChosen)                       #Write Data To CSV