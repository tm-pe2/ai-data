import os
import pandas as panda
import re

buildingTypes=["RefBldgSmallHotel","RefBldgLargeHotel",
"RefBldgMediumOffice","RefBldgLargeOffice",
"RefBldgSmallOffice"], ["smallHotel","largeHotel", 
"mediumOffice","largeOffice", "smallOffice"]


def generateSolar(type):
    buildingCounter=0
    totalSunnyAvg=0

    consumptionPerBuildingSunny=[]

    smallerThenAvg=[]
    solarPosition=[]

    path="C:\\Users\\kwint\\OneDrive\\Bureaublad\\PE2\\data\\data\\home\\ai\\new_data\\test"
    for dir in os.listdir(path):
        dirpath=path+"\\"+dir
        for file in os.listdir(dirpath):
            filepath=dirpath+"\\"+file
            if(bool(re.search(type, filepath))):
                buildingCounter+=1
                print("caclculating: "+ filepath)
                result=panda.read_csv(filepath, sep=";")
                dataMonthly=[0,0,0,0,0,0,0,0,0,0,0,0]
                sunnyMonths=0
                intDate=0
                for row in result:
                    i = 0
                    dates=result["Date/Time"]
                    usage=result["Electricity:Facility [kW](Hourly)"]

                    for date in dates:
                        if date[1:3]!='1/':    
                            intDate = int(date[1:3])

                            dataMonthly[intDate-1]+=usage[i]
                            i=i+1
                            if intDate>4 and intDate<9:
                                sunnyMonths+=dataMonthly[intDate-1]
                            
                        
                    sunnyDataAvg=sunnyMonths/4

                consumptionPerBuildingSunny.append(sunnyDataAvg)
                totalSunnyAvg+=sunnyDataAvg
    
    print("-------------------------------------------------------------------------------------------------------------------------------------")
    totalSunnyAvg/=buildingCounter

    buildingsWithSolarCounter=0
    buildingCounter=0
    for value in consumptionPerBuildingSunny:
        if value<totalSunnyAvg:
            smallerThenAvg.append(1)
            solarPosition.append(buildingCounter)
            
            buildingsWithSolarCounter+=1
        else:
            smallerThenAvg.append(0)
        buildingCounter+=1
    fileCounter=0
    solarPositionCounter=0
    for dir in os.listdir(path):
        dirpath=path+"\\"+dir
        for file in os.listdir(dirpath):
            filepath=dirpath+"\\"+file
            if(bool(re.search(type, filepath))):
                result=panda.read_csv(filepath, sep=";")
                if len(solarPosition)>0 and fileCounter < len(solarPosition) and fileCounter == solarPosition[solarPositionCounter]:
                    print("solar panels: "+filepath)
                    result['has_solarpanels'] =  result['has_solarpanels'].replace(0,1)
                    solarPositionCounter+=1
                fileCounter+=1
                result.to_csv(filepath, sep=";", index=False)
    print(str(solarPositionCounter)+" buildings now have solar panerls")
    print("done")
    print("\n\n")


for buildingTypeCounter in range(len(buildingTypes[0])):
    print(buildingTypes[1][buildingTypeCounter]+":")
    generateSolar(buildingTypes[0][buildingTypeCounter])