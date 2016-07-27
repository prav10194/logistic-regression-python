import csv
from math import sqrt
class LogisticRegression:
    filename=''

    def rsumvalue(self,inputList,numCol):
        rsum=[0]*numCol
        print("Total Rows: "+str(len(inputList)))
        for row in inputList:
            i=0
            for value in row:
                rsum[i]=rsum[i]+float(value)
                i=i+1
        return rsum

    def avgvalue(self,rsum,numCol,numRow):
        avg=[0]*numCol
        for i in range(0,numCol):
            avg[i]=rsum[i]/numRow
        return avg

    def xmeanvalue(self,inputList,avg,numCol):
        xmean=[0]*numCol
        for row in inputList:
            i=0
            for value in row:
                xmean[i]=xmean[i]+float((float(value)-avg[i])*(float(value)-avg[i]))
                i=i+1
        return xmean

    def sdvalue(self,xmean,numCol,numRow):
        sd=[0]*numCol
        for i in range(0,numCol):
            sd[i]=float(sqrt(xmean[i]))/numRow
        return sd
        
    def scaledCsv(self,inputList,avg,sd,numCol,lastCol):
        outputFile=open('scaledfile.csv','w',newline='')
        filename='scaledfile.csv'
        fwrite=csv.writer(outputFile)
        k=0
        for row in inputList:
            i=0
            listnew=[]
            for value in row:
                listnew.append(float(value)-avg[i]/sd[i])
                i=i+1
            listnew.append(lastCol[k])
            k=k+1
            fwrite.writerow(listnew)
        outputFile.close()

    def predictionCoeff(self,inputList,lastCol,numCol):
        coeff=[0]*(numCol)
        pred=0
        pr=0.0
        alpha=0.3
        k=0 #for looping lastCol matrix
        for row in inputList:
            pr=-coeff[0]*1 #important as x[0] is taken as 1
            i=1 #for looping coeff matrix
            for value in row:
                pr=pr-(float(coeff[i]*float(value)))
                i=i+1

                
            pred=1/(1+pow(2.73,pr))
            coeff[0]=coeff[0]+ float(float(alpha)*(float(lastCol[k])-pred)*float(pred)*float((1-pred))*float(1))
            i=1
            for value in row:
                coeff[i] =coeff[i]+ float(float(alpha)*(float(lastCol[k])-pred)*float(pred)*float((1-pred))*float(value))
                i=i+1
            k=k+1
        print("Coeffecient Matrix: "+str(coeff))
        return coeff
    
    def predictValues(self,inputList,lastCol,numRow,coeff):
        outputFile=open('predict.csv','w',newline='')
        fwrite=csv.writer(outputFile)
        vallist=[]
        for index in range(0,numRow):
            vallist=inputList[index]        
            p=-coeff[0]*1
            i=1
            for val in vallist:
                k=(float(coeff[i])*float(val))
                p=p-k
                #print(p)
                i=i+1
            #print(pr)
            pred=float(1/(1+float(pow(2.71,p))))
            
            r=[]
            r.append(pred)
            r.append(lastCol[index])
            fwrite.writerow(r)
        outputFile.close()
    
    def thresholdFactor(self):
        inputFile=open('predict.csv','r')
        fread=csv.reader(inputFile)
        inList=list(fread)

        szero=0.0
        czero=0
        sone=0.0
        cone=0
        highzero=0
        lowone=9999.00
        for row in inList:
            if int(row[1])==1:
                cone=cone+1
                sone=sone+float(row[0])
                if float(row[0])<lowone:
                    lowone=float(row[0])
            else:
                czero=czero+1
                szero=szero+float(row[0])
                if float(row[0])>highzero:
                    highzero=float(row[0])

                    

        azero=float(szero)/czero
        aone=float(sone)/cone

        cone=0
        czero=0
        for row in inList:
           
            if float(row[0])<highzero and float(row[0])>lowone:
                if int(row[1])==1:
                    cone=cone+1
                else:
                    czero=czero+1
        return aone,azero
        
    def main(self):
        filename=input('Enter filename: ')
        scale=input('Scaling required? Y/N: ')
        if scale=='Y' or scale=='y':
            
            inputFile=open(filename,'r')
            fread=csv.reader(inputFile)
            inList=list(fread)
            numCol=len(inList[0])
            numRow=len(inList)
            inputList=[]
            lastCol=[]
            limit=numCol-1
            for w in inList:
                inputList.append(w[0:limit])
                lastCol.append(w[-1])

        
            rsum,avg,sd,xmean=[0]*numCol,[0]*numCol,[0]*numCol,[0]*numCol
            #x-mean/sd
            rsum=self.rsumvalue(inputList,numCol)
            avg=self.avgvalue(rsum,numCol,numRow)       
            xmean=self.xmeanvalue(inputList,avg,numCol)
            sd=self.sdvalue(xmean,numCol,numRow)
            self.scaledCsv(inputList,avg,sd,numCol,lastCol)
        
        inputFile=open(filename,'r')
        fread=csv.reader(inputFile)
        inList=list(fread)
        inputList=[]
        lastCol=[]
        numCol=len(inList[0])
        numRow=len(inList)

        limit=numCol-1
        for w in inList:
            inputList.append(w[0:limit])
            lastCol.append(w[-1])
            
        coeff=self.predictionCoeff(inputList,lastCol,numCol)
        self.predictValues(inputList,lastCol,numRow,coeff)

        print('Enter values separated by , :')
        vallist = [float(x) for x in input().split(',')]

      
        p=-coeff[0]*1
        i=1
        for val in vallist:
            prod=(float(coeff[i])*float(val))
            p=p-prod
            i=i+1
            
        pred=float(1/(1+float(pow(2.71,p))))

        aone,azero=self.thresholdFactor()
        print("Average of all zero predictions - "+str(azero))
        print("Average of all one predictions - "+str(aone))
        if abs(aone-pred)>abs(azero-pred):
            print("Real prediction: "+str(float(pred)))
            print("Rounding off to 0")
        else:
            print("Real prediction: "+str(float(pred)))
            print("Rounding off to 1")
          
