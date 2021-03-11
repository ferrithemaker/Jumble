library(shiny)
library(zoo)

covidData <- read.csv('https://opendata.ecdc.europa.eu/covid19/casedistribution/csv', header=TRUE, sep=",")
covidData$date <- as.Date(covidData$dateRep,format='%d/%m/%Y')
listOfTerritories <- unique(covidData["countriesAndTerritories"])

ui <- fluidPage(
  titlePanel(windowTitle="Updated real-time data of Covid-19 cases & deaths",title=h4("Updated real-time data of Covid-19 cases & deaths (daily data x 100K population)", align="center")),
  selectInput("casesordeaths","Cases or deaths:",c("Cases","Deaths")),
  selectInput("country","Select country:",listOfTerritories$countriesAndTerritories),
  submitButton("Update graph", icon("refresh")),
  plotOutput("graph"),
  p("Data from opendata.ecdc.europa.eu"))

server <- function(input,output,session) {
  output$graph <- renderPlot({
    covidSubsetByCountry <- subset(covidData,countriesAndTerritories==input$country)
    if (input$casesordeaths=="Cases") {
      covidSubsetByCountry <- covidSubsetByCountry[covidSubsetByCountry$cases >= 0,]
      dailycases <- (covidSubsetByCountry$cases/covidSubsetByCountry$popData2019)*100000
      dailycasesRM <- zoo::rollmean(dailycases, k = 7, fill = NA)
      plot(covidSubsetByCountry$date,dailycasesRM,type="l",xlab="Date",ylab="Daily cases x 100K population")
    }
    if (input$casesordeaths=="Deaths") {
      covidSubsetByCountry <- covidSubsetByCountry[covidSubsetByCountry$deaths >= 0,]
      dailydeaths <- (covidSubsetByCountry$deaths/covidSubsetByCountry$popData2019)*100000
      dailydeathsRM <- zoo::rollmean(dailydeaths, k = 7, fill = NA)
      plot(covidSubsetByCountry$date,dailydeathsRM,type="l",xlab="Date",ylab="Daily deaths x 100K population")
    }
  })
}

shinyApp(ui, server)