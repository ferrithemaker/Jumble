library(shiny)

covidData <- read.csv('https://opendata.ecdc.europa.eu/covid19/casedistribution/csv', header=TRUE, sep=",")
covidData$date <- as.Date(covidData$dateRep,format='%d/%m/%Y')
listOfTerritories <- unique(covidData["countriesAndTerritories"])

ui <- fluidPage(
  titlePanel(windowTitle="Updated real-time data of Covid-19 cases & deaths",title=h4("Updated real-time data of Covid-19 cases & deaths (weekly data x 100K population)", align="center")),
  selectInput("casesordeaths","Cases or deaths:",c("Cases","Deaths")),
  selectInput("country","Select country:",listOfTerritories$countriesAndTerritories),
  submitButton("Update graph", icon("refresh")),
  plotOutput("graph"),
  p("Data from opendata.ecdc.europa.eu"))

server <- function(input,output,session) {
  output$graph <- renderPlot({
    covidSubsetByCountry <- subset(covidData,countriesAndTerritories==input$country)
    if (input$casesordeaths=="Cases") {
      plot(covidSubsetByCountry$date,(covidSubsetByCountry$cases_weekly/covidSubsetByCountry$popData2019)*100000,type="l",xlab="Date",ylab="Weekly cases x 100K population")
    }
    if (input$casesordeaths=="Deaths") {
      plot(covidSubsetByCountry$date,(covidSubsetByCountry$deaths_weekly/covidSubsetByCountry$popData2019)*100000,type="l",xlab="Date",ylab="Weekly deaths x 100K population")
    }
  })
}

shinyApp(ui, server)