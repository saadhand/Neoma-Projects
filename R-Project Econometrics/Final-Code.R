#########################################
This code was writen By Saad HANDAR And Josselin Masse
#########################################

pack<-c("car","readxl","ggplot2", "vtable","tidyverse", "jtools", "e1071", "tseries", 
        "ggplot2", "plotly", "fRegression","S","lmtest", "FinTS","rugarch")
#install.packages(pack)
lapply(pack, require, character.only = TRUE)

#________________________________Exercise 1______________________________________
lct <- Sys.getlocale("LC_TIME"); Sys.setlocale("LC_TIME", "C") #to fix Date Error
Stocks = read.csv("C:/Users/saadh/OneDrive/Documents/Neoma Business School/Econometrics/Assignment/Stocks_AC.csv",sep=",",header = TRUE)
Stocks$Date=as.Date(Stocks$Date, format = "%d-%b-%y")#change Date Format
cnames = colnames(Stocks)

print(cnames)

Date<-Stocks$Date
startDate <- Date[1]
endDate <- Date[length(Date)]
close_GM <-Stocks$GM_AC
close_F <-Stocks$F_AC

par(cex.axis = 1.5, cex.lab = 1.5, lwd = 2)
plot(Date, close_GM, type = 'l', xlab =" Date ",ylab =" General Motors price ",
     xlim=c(startDate, endDate)) #Plot of GM 
plot(Date, close_F, type = 'l', xlab =" Date ",ylab =" Ford price ") #Plot of Ford

#1.2) 
#computing Log returns
# log transformation
LP_GM=log(close_GM)
LP_F=log(close_F)

# log difference (log(pt)- log(pt-1))
LR_GM<- diff (log(close_GM))
LR_F<- diff (log(close_F))


samplesize_F=length(close_F)
samplesize_GM=length(close_GM)
#printing sample sizes
print(samplesize_F)
print(samplesize_GM)

ggplot() + geom_point(aes(x=LR_GM, y=LR_F))

#1.3)

returns <- data.frame(Ford = LR_F,
                      GM = LR_GM)
boxplot(returns, main="Box Plot") # here we create boxplots of the Data Frame

#1.4)
close_MSFT <-Stocks$MSFT_AC
close_MRK <-Stocks$MRK_AC

LP_MSFT=log(close_MSFT)
LP_MRK=log(close_MRK)

LR_MSFT<- diff (log(close_MSFT))
LR_MRK<- diff (log(close_MRK))

#plot(head(Date, -1) ,L_MSFT,type="l",col="black",xlab ="Date",ylab="Return")
#lines(head(Date, -1),L_MRK,col="red",xlab ="Date",ylab="Return")

ggplot() + geom_point(aes(x=LR_MSFT, y=LR_MRK))

returns_2 <- data.frame(Microsoft = LR_MSFT,
                        Merck = LR_MRK)
boxplot(returns_2, main="Box Plot")

#1.5)

ret_msft=LR_MSFT
print("For Microsoft")
summary(ret_msft)
kurtosis(ret_msft)
sd(ret_msft)
skewness(ret_msft)


ret_mrk=LR_MRK
print("For Merck")
summary(ret_mrk)
kurtosis(ret_mrk)
sd(ret_mrk)
skewness(ret_mrk)


ret_gm=LR_GM
print("For GM")
summary(ret_gm)
kurtosis(ret_gm)
sd(ret_gm)
skewness(ret_gm)

ret_f=LR_F
print("For Ford")
summary(ret_f)
kurtosis(ret_f)
sd(ret_f)
skewness(ret_f)


#Question 2
#2.1)
#####################   Price     #####################################
#Microsoft
acf(LP_MSFT, cex.axis=2, cex.main=2,cex.lab=2,lwd=3, 
    main = 'Logarithm of MSFT Price ', col="red")
pacf(LP_MSFT, lag.max=NULL, cex.axis=2, cex.main=2,cex.lab=2,lwd=3, 
     main = 'Logarithm of MSFT Price ', col="red")
#Ford
acf(LP_F, lag.max=NULL, cex.axis=2, cex.main=2,cex.lab=2,lwd=3, 
    main = 'Logarithm of Ford Price ', col="red")
pacf(LP_F, lag.max=NULL, cex.axis=2, cex.main=2,cex.lab=2,lwd=3, 
     main = 'Logarithm of Ford Price ', col="red")
#General Motors
acf(LP_GM, lag.max=NULL, cex.axis=2, cex.main=2,cex.lab=2,lwd=3, 
    main = 'Logarithm of GM Price ', col="red")
pacf(LP_GM, lag.max=NULL, cex.axis=2, cex.main=2,cex.lab=2,lwd=3, 
     main = 'Logarithm of GM Price ', col="red")
#Merck
acf(LP_MRK, lag.max=NULL, cex.axis=2, cex.main=2,cex.lab=2,lwd=3, 
    main = 'Logarithm of MRK Price ', col="red")
pacf(LP_MRK, lag.max=NULL, cex.axis=2, cex.main=2,cex.lab=2,lwd=3, 
     main = 'Logarithm of MRK Price ', col="red")


#####################   Return     #####################################
#Microsoft
acf(LR_MSFT, cex.axis=2, cex.main=2,cex.lab=2,lwd=3, 
    main = 'Logarithm of MSFT Return ', col="blue")
pacf(LR_MSFT, lag.max=NULL, cex.axis=2, cex.main=2,cex.lab=2,lwd=3, 
     main = 'Logarithm of MSFT Return ', col="blue")
#Ford
acf(LR_F, lag.max=NULL, cex.axis=2, cex.main=2,cex.lab=2,lwd=3, 
    main = 'Logarithm of Ford Return ', col="blue")
pacf(LR_F, lag.max=NULL, cex.axis=2, cex.main=2,cex.lab=2,lwd=3, 
     main = 'Logarithm of Ford Return',col="blue")
#General Motors
acf(LR_GM, lag.max=NULL, cex.axis=2, cex.main=2,cex.lab=2,lwd=3, 
    main = 'Logarithm of GM Return ', col="blue")
pacf(LR_GM, lag.max=NULL, cex.axis=2, cex.main=2,cex.lab=2,lwd=3, 
     main = 'Logarithm of GM Return ', col="blue")
#Merck
acf(LR_MRK, lag.max=NULL, cex.axis=2, cex.main=2,cex.lab=2,lwd=3, 
    main = 'Logarithm of MRK Return ', col="blue")
pacf(LR_MRK, lag.max=NULL, cex.axis=2, cex.main=2,cex.lab=2,lwd=3, 
     main = 'Logarithm of MRK Return ', col="blue")

#2.2) and 2.3
MA_ret_GM <- arima(x = LR_GM, order = c(0, 0, 0)) #MA0
MA_ret_F <- arima(x = LR_F, order = c(0, 0, 0)) #MA0
MA_ret_MSFT <- arima(x = LR_MSFT, order = c(0, 0, 0)) #MA0
MA_ret_MERCK <- arima(x = LR_MRK, order = c(0, 0, 0)) #MA0
AR_price_GM <- arima(x = LP_GM, order = c(1, 0, 0)) #AR1
AR_price_F <- arima(x = LP_F, order = c(1, 0, 0)) #AR1
AR_price_MSFT <- arima(x = LP_MSFT, order = c(1, 0, 0)) #AR1
AR_price_MERCK <- arima(x = LP_MRK, order = c(1, 0, 0)) #AR1


#Stationnarity test
adf.test(LP_MSFT)
adf.test(LR_MSFT)
adf.test(LP_MRK)
adf.test(LR_MRK)
adf.test(LP_F)
adf.test(LR_F)
adf.test(LP_GM)
adf.test(LR_GM)

#Normality test on the series
jarque.bera.test(LP_MSFT)
jarque.bera.test(LR_MSFT)
jarque.bera.test(LP_MRK)
jarque.bera.test(LR_MRK)
jarque.bera.test(LP_F)
jarque.bera.test(LR_F)
jarque.bera.test(LP_GM)
jarque.bera.test(LR_GM)

#Serrially Corolated test
Box.test(MA_ret_GM$residuals, lag=5)
Box.test(MA_ret_F$residuals, lag=5)
Box.test(MA_ret_MSFT$residuals, lag=5)
Box.test(MA_ret_MERCK$residuals, lag=5)


#Homoskedasticity 
ArchTest(MA_ret_GM$residuals, lags=60, demean = TRUE)
ArchTest(MA_ret_F$residuals, lags=60, demean = TRUE)
ArchTest(MA_ret_MSFT$residuals, lags=60, demean = TRUE)
ArchTest(MA_ret_MERCK$residuals, lags=60, demean = TRUE)


#Normality
jarque.bera.test(MA_ret_GM$residuals)
jarque.bera.test(MA_ret_F$residuals)
jarque.bera.test(MA_ret_MSFT$residuals)
jarque.bera.test(MA_ret_MERCK$residuals)

hist(MA_ret_GM$residuals)

#2.3
AR_ret_GM <- arima(x = LR_GM, order = c(1, 0, 0))
AR_ret_GM
Box.test(AR_ret_GM$residuals, lag=5)
ArchTest(AR_ret_GM$residuals, lags=60, demean = TRUE)
jarque.bera.test(AR_ret_GM$residuals)


#2.4 ARMA GARCH
arma.garch = ugarchspec(mean.model=list(armaOrder=c(1,0)),
                        variance.model=list(garchOrder=c(1,1)))

GM.arma.garch = ugarchfit(data = LR_GM, spec=arma.garch)
GM.arma.garch

StandRes <- ts(residuals(GM.arma.garch, standardize=TRUE))
Box.test(StandRes)
ArchTest(StandRes)
jarque.bera.test(StandRes)
hist(StandRes)
d<-density(StandRes)
plot(d)
kurtosis(StandRes)
skewness(StandRes)

#2.5 EGARCH
egarch = ugarchspec(variance.model = list(model="eGARCH", garchOrder=c(1,1)), mean.model=list(armaOrder=c(1,0)))

gm_egarch = ugarchfit(egarch, data = LR_GM)
gm_egarch
msft_egarch = ugarchfit(egarch, data = LR_MSFT)
msft_egarch

#2.6 ARCH-DCC
GMMSFT_df<-data.frame(LR_GM,LR_MSFT)
spec1<- dccspec(uspec = multispec(replicate(2,egarch)),dccOrder = c(1,1),distribution = "mvnorm")
fit<- dccfit(spec1,data=GMMSFT_df)
print(fit)
plot(fit)


#___________________Exercice 3___________________________________
library(dplyr) 
TreasuryYields <- read_table2("Neoma Business School/Econometrics/Assignment/TreasuryYields.txt",col_types = cols(`1mo` = col_skip(),`20yr` = col_skip(),`7yr` = col_skip(),`30yr` = col_skip(),`5yr` = col_skip(),`10yr` = col_skip(), Date = col_date(format = "%m/%d/%y"),X13 = col_skip()))
cnames = colnames(TreasuryYields)
TreasuryYields<-na.omit(TreasuryYields) 


#3.1)
TreasuryYields$Date=as.Date(TreasuryYields$Date, format = "%m/%d/%y")
Date<-TreasuryYields$Date
`3mo`<-TreasuryYields$`3mo`
`6mo`<-TreasuryYields$`6mo`
`1yr`<-TreasuryYields$`1yr`
`2yr`<-TreasuryYields$`2yr`
`3yr`<-TreasuryYields$`3yr`

plot(Date ,`3mo`,type="s",col="black",xlab ="Date",ylab="Yield")
lines(Date,`6mo`,col="red",xlab ="Date",ylab="Yield")
lines(Date,`1yr`,col="blue",xlab ="Date",ylab="Yield")
lines(Date,`2yr`,col="green",xlab ="Date",ylab="Yield")
lines(Date,`3yr`,col="brown",xlab ="Date",ylab="Yield")
legend(x = "topright",
       col = c("black", "red","blue","green","brown"), lty = 1, lwd = 1,
       legend = c('3mo', '6mo','1yr','2yr','3yr'))


#3.2)
#acf

acf(`3mo`, lag.max=NULL, cex.axis=2, cex.main=2,cex.lab=2,lwd=3, 
    main = '3mo Yield ', col="blue")
acf(`6mo`, lag.max=NULL, cex.axis=2, cex.main=2,cex.lab=2,lwd=3, 
    main = '6mo Yield ', col="blue")
acf(`1yr`, lag.max=NULL, cex.axis=2, cex.main=2,cex.lab=2,lwd=3, 
    main = '1yr Yield ', col="blue")
acf(`2yr`, lag.max=NULL, cex.axis=2, cex.main=2,cex.lab=2,lwd=3, 
    main = '2yr Yield ', col="blue")
acf(`3yr`, lag.max=NULL, cex.axis=2, cex.main=2,cex.lab=2,lwd=3, 
    main = '3yr Yield ', col="blue")

adf.test(`3mo`)
adf.test(`6mo`)
adf.test(`1yr`)
adf.test(`2yr`)
adf.test(`3yr`)

#3.3
mcor=cor(x = TreasuryYields[2:6])
print(mcor)

regression <- lm(`3yr`~`3mo`)
res=regression$residuals
jarque.bera.test(res)
hist(res)
summ(regression)

#3.4)
Resids=regression$residuals
adf.test(Resids)

#3.5)
DL_3mo=diff(`3mo`)
DL_3yr=diff(`3yr`)
ResidsAdj <-Resids[1:length(Resids)-1]

ECM <- lm(DL_3yr~DL_3mo+ResidsAdj)
summ(ECM)

length(ECM)

plot(head(Date-1), ECM$residuals, type = 'l', col="red",
     xlab =" Date ",main ="Difference between 3mo and 3yr Yield", ylab ="Log-prices",
     cex.axis=1.5, cex.main=1.5,cex.lab=1.5,lwd=2)

#3.6)
regression2 <- lm(`3mo`~`3yr`)
summ(regression2)
Resids2=regression2$residuals
adf.test(Resids2)

ResidsAdj2 <-Resids2[1:length(Resids2)-1]

ECM2 <- lm(DL_3yr~DL_3mo+ResidsAdj2)
summ(ECM2)

#_____________________________Exercice 4___________________________________
#4.1)
pack2<-c("lmtest", "fGarch", "vars", "FinTS", "moments", "rugarch", "sandwich", "rmgarch",
         "urca", "xts") 
lapply(pack2, require, character.only = TRUE)
lct <- Sys.getlocale("LC_TIME"); Sys.setlocale("LC_TIME", "C") #to fix Date Error
Stocks = read.csv("C:/Users/saadh/OneDrive/Documents/Neoma Business School/Econometrics/Assignment/Stocks_AC.csv",sep=",",header = TRUE)
Stocks$Date=as.Date(Stocks$Date, format = "%d-%b-%y")#change Date Format
cnames = colnames(Stocks)

Date<-Stocks$Date
startDate <- Date[1]
endDate <- Date[length(Date)]
close_PFE <-Stocks$PFE_AC
LR_PFE <- diff (log(close_PFE))

plot(Date ,close_PFE,type="s",col="black",xlab ="Date",ylab="return",ylim=c(0,70))
lines(Date,close_MSFT,col="blue",xlab ="Date",ylab="return")
lines(Date,close_GM,col="brown",xlab ="Date",ylab="return")
legend(x = "topleft",
       col = c("black", "blue","brown"), lty = 1, lwd = 1,
       legend = c('PFE', 'MSFT','GM'))


plot(head(Date,-1) ,LR_PFE,type="s",col=rgb(red = 1,green=0,blue=0, alpha = 0.3),xlab ="Date",ylab="return")
lines(head(Date,-1),LR_MSFT,col=rgb(red = 0,green=1,blue=0, alpha = 0.3),xlab ="Date",ylab="return")
lines(head(Date,-1),LR_GM,col=rgb(red = 0,green=0,blue=1, alpha = 0.3),xlab ="Date",ylab="return")
legend(x = "bottomleft",
       col = c(rgb(red = 1,green=0,blue=0, alpha = 0.3), rgb(red = 0,green=1,blue=0, alpha = 0.3),rgb(red = 0,green=0,blue=1, alpha = 0.3)), lty = 1, lwd = 1,
       legend = c('PFE', 'MSFT','GM'))

#4.2)
VARData <- data.frame(LR_GM, LR_MSFT ,LR_PFE)
VARselect(VARData, lag.max=5)

VAR_Model <- VAR(VARData, p = 2)
summary(VAR_Model)

#4.3)

causality(VAR_Model, cause = "LR_GM")
causality(VAR_Model, cause = "LR_MSFT")
causality(VAR_Model, cause = "LR_PFE")

#4.4)
ir = irf(VAR_Model ,n.ahead = 20)
plot (ir)

#4.5)
vd = fevd (VAR_Model ,n.ahead = 20)
plot (vd)

