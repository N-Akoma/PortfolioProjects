select * from CovidDeaths
where continent is NOT NULL

select location_name,event_date,total_deaths,total_cases,population
from CovidDeaths
order by 4 desc

-- Looking at Total cases VS Total deaths

select location_name,event_date,total_deaths,total_cases, ( total_deaths/total_cases) * 100 AS Death_percentage
from CovidDeaths
where location_name like '%Africa%'
order by 5

-- Totlal Cases VS Population
select location_name,event_date,total_cases,population,( total_cases/population) * 100 AS Cases_percentage
from CovidDeaths
where location_name like '%Africa%'
order by 1,2

-- Looking at countries with infection rate compared to population
select location_name, population, max(total_cases) as MaxTotalCases,max(( total_cases/population))*100
AS PopulationCasePercentage
from dbo.CovidDeaths
Group by location_name, population
order by MaxTotalCases desc

-- Looking out how Deaths rate
select location_name, population, max(total_deaths) AS TotalDeathCount, max((total_deaths/population))*100
AS PopulationCasePercentage
from dbo.CovidDeaths
where continent IS NULL
Group by location_name, population
order by TotalDeathCount desc

--LOOKING AT THE WORLD DEATH ROLL ON DATE
select SUM(total_cases) AS TotalCaseCount, SUM(total_deaths) AS TotalDeathCoun,
	(SUM(total_deaths)/SUM(total_cases))*100 AS TotalDeathTotalCasePercentage
	from dbo.CovidDeaths

select SUM(new_cases) AS NewCaseCount, SUM(new_deaths) AS NewDeathCoun,
	(SUM(new_deaths)/SUM(new_cases))*100 AS NewDeathNewCasePercentage
	from dbo.CovidDeaths



-- LOOKING AT THE TOTAL POPULATION VS VACCINATION
--using CTC
With PopVsVac (continent,location_name,event_date,population,new_vaccinations,RollingPeopleVaccinations)
as
(
Select dea.continent, dea.location_name,dea.event_date, dea.population, vac.new_vaccinations,
SUM(vac.new_vaccinations) OVER (Partition by dea.location_name order by dea.location_name,dea.event_date)
as RollingPeopleVaccinations
--(RollingPeopleVaccinations/dea.population)
from CovidDeaths dea
Join CovidVaccines vac
	on dea.location_name = vac.location_name
	and dea.event_date = vac.event_date
where dea.continent IS NOT NULL
--order by 2
)

select *,(RollingPeopleVaccinations/population)*100 AS PopVcVacPercentage
from PopVsVac

-- Temp Table
Drop Table if exists #PopVcVacPercentage 
Create Table #PopVcVacPercentage
(
	continent nvarchar(50),
	location_name nvarchar(50),
	event_date date,
	population float,
	new_vaccination numeric,
	RollingPeopleVaccinations float
)

Insert Into #PopVcVacPercentage
	Select dea.continent, dea.location_name,dea.event_date, dea.population, vac.new_vaccinations,
SUM(vac.new_vaccinations) OVER (Partition by dea.location_name order by dea.location_name,dea.event_date)
as RollingPeopleVaccinations
--(RollingPeopleVaccinations/dea.population)
from CovidDeaths dea
Join CovidVaccines vac
	on dea.location_name = vac.location_name
	and dea.event_date = vac.event_date
--where dea.continent IS NOT NULL
--order by 2

select *,(RollingPeopleVaccinations/population)*100 AS PopVcVacPercentage
from #PopVcVacPercentage

-- Creating Views to store data for visualization 

Create View PercentPopulationVaccinated as
Select dea.continent, dea.location_name,dea.event_date, dea.population, vac.new_vaccinations,
SUM(vac.new_vaccinations) OVER (Partition by dea.location_name order by dea.location_name,dea.event_date)
as RollingPeopleVaccinations
--(RollingPeopleVaccinations/dea.population)
from CovidDeaths dea
Join CovidVaccines vac
	on dea.location_name = vac.location_name
	and dea.event_date = vac.event_date
where dea.continent IS NOT NULL

select * 
from PercentPopulationVaccinated