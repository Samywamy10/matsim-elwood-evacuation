library(dplyr)
library(ggplot2)

#Bring in each iteration and put it in a data frame in ddat
maxBusNumber = 8
ddat <- as.list(rep("", 0)) 
for(i in 0:maxBusNumber) {
  ddat[[i+1]] = read.delim(paste("~/Documents/repos/matsim-evacuation/outputs/nobus",i,"-busspace121-rrwTRUE-clmwTRUE-flood120/iterationSummary.txt",sep=""))
}

#stack data frames by row into one big data frame with 'NAME' column representing which DF they came from
busSimulations = dplyr::bind_rows(ddat, .id = "NAME")
busSimulations$NAME = as.numeric(busSimulations$NAME) - 1

#Average Travel Times By Iteration and Number of Buses
ggplot(busSimulations, aes(x=busSimulations$ITERATION, y=busSimulations$AvgTripDuration, colour=busSimulations$NAME)) +
  geom_point(size=0.2) +
  labs(color="Number of buses",
       x = "Iteration",
       y = "Average travel time",
       title = "Average travel times by iteration and number of buses") +
  scale_colour_gradient(low = "red", high = "blue") +
  geom_hline(aes(yintercept=min(filter(busSimulations, NAME == 0)$AvgTripDuration)), colour="red") +
  geom_hline(aes(yintercept=min(filter(busSimulations, NAME == 8)$AvgTripDuration)), colour="blue")

#Work out percentage difference between best average time for that simulation and iteration 50
maxDifferences = c()
iterationDifferences = c()
for(j in 0:8) {
  minimumTripDuration = min(busSimulations[busSimulations$NAME == as.character(j),]$AvgTripDuration)
  maximumTripDuration = max(busSimulations[busSimulations$NAME == as.character(j),]$AvgTripDuration)
  maxDifferences[j] = maximumTripDuration - minimumTripDuration
}
for(j in 0:8) {
  differences = c()
  for(i in 100:499) {
      difference = filter(busSimulations, NAME == as.character(j) & ITERATION == 50)$AvgTripDuration[1] - filter(busSimulations, NAME == as.character(j) & ITERATION == i)$AvgTripDuration[1]
      differences[i-99] = (abs(difference) / maxDifferences[j])
  }
  iterationDifferences[j] = max(differences)
}
iterationDifferences
print(max(iterationDifferences)) #as a fraction

#Bus numbers with and without rerouting
results = read.delim("~/Documents/repos/matsim-evacuation/results.csv",sep=",")
effectsOfNumberOfBuses = results[results$ChangeLegMode == TRUE & results$SpeedOfFlood == 120 & results$BusSpacing == 120 & results$NumberOfBuses < 16,]
ggplot(effectsOfNumberOfBuses, aes(x=effectsOfNumberOfBuses$NumberOfBuses,y=effectsOfNumberOfBuses$AverageTimeLast, colour=effectsOfNumberOfBuses$ReRoute)) +
  labs(color="Car ReRouting Enabled",
       x = "Number of Buses",
       y = "Average travel time",
       title = "Average travel times by number of buses with rerouting enabled or disabled") +
  geom_point()

fit = lm(results$AverageTimeLast~results$NumberOfBuses, data=results)
summary(fit)

calculateDifference = function(x) {
  print(tail(x,n=1))
  #finalValue = tail(x[x$NAME==simulation], n=1)$AvgTripDuration[1]
  #difference = x[x$NAME==simulation]
}

newresults = lapply(X = busSimulations, FUN = calculateDifference)

  