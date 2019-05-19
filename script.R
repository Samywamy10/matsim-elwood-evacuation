library(dplyr)
library(ggplot2)
library(reshape)

#Bring in each iteration and put it in a data frame in ddat
maxBusNumber = 8
ddat <- as.list(rep("", 0)) 
for(i in 0:maxBusNumber) {
  ddat[[i+1]] = read.delim(paste("~/Documents/repos/matsim-evacuation/outputs/nobus",i,"-busspace120-rrwFALSE-clmwTRUE-flood120/iterationSummary.txt",sep=""))
}

#stack data frames by row into one big data frame with 'NAME' column representing which DF they came from
busSimulations = dplyr::bind_rows(ddat, .id = "NAME")
busSimulations$NAME = as.numeric(busSimulations$NAME) - 1

#Average Travel Times By Iteration and Number of Buses
ggplot(busSimulations, aes(x=busSimulations$ITERATION, y=busSimulations$AvgTripDuration, colour=busSimulations$NAME)) +
  geom_point(size=1.2) +
  labs(color="Number of buses",
       x = "Iteration",
       y = "Average travel time",
       title = "Average travel times by iteration and number of buses") +
  scale_colour_gradient(low = "red", high = "blue")
#  geom_hline(aes(yintercept=min(filter(busSimulations, NAME == 0)$AvgTripDuration)), colour="red") +
#  geom_hline(aes(yintercept=min(filter(busSimulations, NAME == 8)$AvgTripDuration)), colour="blue")

minAverageTimeDrop = min(busSimulations[busSimulations$ITERATION == 0 & busSimulations$NAME > 0,]$AvgTripDuration - busSimulations[busSimulations$ITERATION == 1 & busSimulations$NAME > 0,]$AvgTripDuration)
maxAverageTimeDrop = max(busSimulations[busSimulations$ITERATION == 0 & busSimulations$NAME > 0,]$AvgTripDuration - busSimulations[busSimulations$ITERATION == 1 & busSimulations$NAME > 0,]$AvgTripDuration)

#Average Travel Times By Iteration with 0 buses
zeroBusSimulation = read.delim(paste("~/Documents/repos/matsim-evacuation/outputs/nobus0-busspace120-rrwFALSE-clmwTRUE-flood120/iterationSummary.txt",sep=""))
varianceBetweenMaxAndMin = max(zeroBusSimulation$AvgTripDuration) - min(zeroBusSimulation$AvgTripDuration)
ggplot(zeroBusSimulation, aes(x=zeroBusSimulation$ITERATION, y=zeroBusSimulation$AvgTripDuration)) +
  geom_point(size=2) +
  labs(x = "Iteration",
       y = "Average travel time",
       title = "Average travel times by iteration using zero buses")

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

#Bus numbers against travel time without rerouting
results = read.delim("~/Documents/repos/matsim-evacuation/results.csv",sep=",")

effectsOfNumberOfBuses = results[results$ChangeLegMode == TRUE & results$SpeedOfFlood == 120 & results$BusSpacing == 120 & results$NumberOfBuses < 16 & results$ReRoute==FALSE,]
ggplot(effectsOfNumberOfBuses, aes(x=effectsOfNumberOfBuses$NumberOfBuses,y=effectsOfNumberOfBuses$AverageTimeLast)) +
  labs(x = "Number of Buses",
       y = "Average travel time",
       title = "Average travel times by number of buses") +
  geom_point(size=3)

#Number of people taking buses without rerouting
results$NumberOfPeopleTakingBuses = 500 * (1 - results$ModeSplitLast)
results$MaximumBusCapacity = 90 * results$NumberOfBuses
effectsOfNumberOfBuses = results[results$ChangeLegMode == TRUE & results$SpeedOfFlood == 120 & results$BusSpacing == 120 & results$NumberOfBuses < 16 & results$ReRoute==FALSE,]
resultsWithCapacityMelted = melt(effectsOfNumberOfBuses, id.vars="NumberOfBuses", measure.vars=c("NumberOfPeopleTakingBuses","MaximumBusCapacity"))
ggplot(resultsWithCapacityMelted, aes(x=resultsWithCapacityMelted$NumberOfBuses,y=resultsWithCapacityMelted$value,color=resultsWithCapacityMelted$variable)) +
  labs(x = "Number of Buses",
       y = "Number of agents taking a bus",
       colour = " ",
       title = "Number of people taking buses by number of buses") + 
  stat_summary(fun.x="mean",geom="point", size=3)

#Bus numbers against mode split without rerouting
effectsOfNumberOfBuses = results[results$ChangeLegMode == TRUE & results$SpeedOfFlood == 120 & results$BusSpacing == 120 & results$NumberOfBuses < 16 & results$ReRoute==FALSE,]
ggplot(effectsOfNumberOfBuses, aes(x=effectsOfNumberOfBuses$NumberOfBuses,y=effectsOfNumberOfBuses$ModeSplitLast)) +
  labs(x = "Number of Buses",
       y = "Ratio of cars (to buses)",
       title = "Mode split by number of buses") +
  stat_summary(fun.x="mean",geom="point", size=3)

#Bus split against average travel time
effectsOfNumberOfBuses = results[results$ChangeLegMode == TRUE & results$SpeedOfFlood == 120 & results$BusSpacing == 120 & results$NumberOfBuses < 16 & results$ReRoute==FALSE,]
ggplot(effectsOfNumberOfBuses, aes(x=effectsOfNumberOfBuses$ModeSplitLast,y=effectsOfNumberOfBuses$AverageTimeLast)) +
  labs(x = "Mode split",
       y = "Average travel time",
       title = "Mode split against average travel time") +
  scale_x_reverse() +
  stat_summary(fun.x="mean",geom="point", size=2)

#Bus numbers against travel time with and without rerouting
effectsOfNumberOfBuses = results[results$ChangeLegMode == TRUE & results$SpeedOfFlood == 120 & results$BusSpacing == 120 & results$NumberOfBuses < 16,]
ggplot(effectsOfNumberOfBuses, aes(x=effectsOfNumberOfBuses$NumberOfBuses,y=effectsOfNumberOfBuses$AverageTimeLast, colour=effectsOfNumberOfBuses$ReRoute, alpha=0.8)) +
  labs(color="Car ReRouting Enabled",
       x = "Number of Buses",
       y = "Average travel time",
       title = "Average travel times by number of buses with rerouting enabled or disabled") +
  geom_point(size=3)

#People boarding time
1.5237 * 26 + 3.9631


#1 bus
effectsOfBusSpacingOneBus = results[results$SpeedOfFlood == 120 & results$ChangeLegMode == TRUE & results$ReRoute == FALSE & results$NumberOfBuses == 1,]
ggplot(effectsOfBusSpacingOneBus, aes(x=effectsOfBusSpacingOneBus$BusSpacing, y=effectsOfBusSpacingOneBus$AverageTimeLast, color=effectsOfBusSpacingOneBus$NumberOfBuses)) +
  ylim(1000, 3000) +
  scale_colour_gradient(low = "red", high = "blue") +
  geom_point()

#Linear regression
busResults = results[results$ChangeLegMode==TRUE,]
fit = lm(busResults$AverageTimeLast~busResults$NumberOfBuses+busResults$ReRoute+busResults$BusSpacing+busResults$SpeedOfFlood, data=busResults)
summary(fit)

  