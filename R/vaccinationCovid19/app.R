library(shiny)
require(ggplot2)

covidVaccinationData <- read.csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv', header=TRUE, sep=",")
covidVaccinationData$real_date <- as.Date(covidVaccinationData$date,format='%Y-%m-%d')
covidVaccinationDataNoNA <- covidVaccinationData[!is.na(covidVaccinationData$total_vaccinations_per_hundred),]
listOfTerritories <- unique(covidVaccinationData["location"])

ui <- fluidPage(
    titlePanel(windowTitle="Updated real-time data of Covid-19 vaccination rates",title=h4("Updated real-time data of Covid-19 vaccination rates x 100 people", align="center")),
    selectInput("country","Select country:",listOfTerritories$location),
    submitButton("Update graph", icon("refresh")),
    plotOutput("graph"),
    p("Data from ourworldindata website and Oxford University."))

server <- function(input,output,session) {
    output$graph <- renderPlot({
        covidSubsetByCountry <- subset(covidVaccinationDataNoNA,location==input$country)
        #plot(covidSubsetByCountry$real_date,covidSubsetByCountry$total_vaccinations_per_hundred,type="b",,xlab="Date",ylab="Total vaccionation x 100 people")
        ggplot(covidSubsetByCountry, aes(real_date)) +
            xlab("Date") + ylab("Vaccinations") +
            geom_line(aes(y=total_vaccinations_per_hundred, colour="red")) +
            geom_line(aes(y=people_fully_vaccinated_per_hundred, colour="green")) +
            scale_color_discrete(name = "Vaccination", labels = c("Fully vaccinated", "1st dose"))
        })
}

shinyApp(ui, server)
