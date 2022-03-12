# COVID-19 SES Data Hub, Hopkins Population Center

## Phase 5 Release of COVID-19 and Sociodemographic Data (3/11/2022)

The HPC Data Hub is a data service infrastructure of the Hopkins Population Center (HPC). The HPC Data Hub offers U.S. state-level and county-level data on COVID-19 and sociodemographic data necessary for population-based social science, epidemiological, medical and public health research to provide evidence-based policy recommendations for COVID-19 recovery. 

Timely and effective data on social, economic and health disparities are needed to record the pandemic course. Drawing from trusted sources, this data hub collects and manages state-level and county-level data on sociodemographic and health factors that intertwine to complicate the pandemic trajectory.

The Phase-5 release replaces the Phase-4 data on multiple fronts, including the separation of state-level data from county-level data, and the addition of key variables such as vaccination by age groups and race-ethnic group, and state policy on mask mandate.

The data files and the corresponding dictionary files are compiled in 3 folders on GitHub. The link to the GitHub repository will be displayed upon your completion of the [user registration form](https://docs.google.com/forms/d/e/1FAIpQLScCkT9_jOyNuT-edOrfgkbd8Y3ENtJGCPAKTZ9RtQM5xr_r5g/viewform?usp=sf_link).

On the GitHub page, click the green “Code” tab and then “Download zip” tab. The downloaded zip file includes 3 folders for pandemic time-series data, unemployment data, and prepandemic data. It also contains 1 folder of our scripts used for data processing and 1 folder for the FIPS code.

- **Pandemic** folder includes 4 data files in csv format, 1 dictionary file for state-level data in csv format, and 1 dictionary file for all county-level data in csv format
    
    - state_level_data.csv: all state-level variables, including cases and deaths, state-level policies, and vaccination progress
    - county_casesAndDeaths.csv: county-level time-series data on COVID-19 tested and confirmed cases and deaths
    - county_vaccination.csv: time-series county-level data on vaccination
    - county_mobility.csv: time-series data on human mobility and social distancing


- **Unemployment** folder includes 1 data file in csv format and 1 dictionary file in csv format

    - Monthly unemployment rate and size of labor force from January 2019 (monthly updates when its available at BLS)
    - The county identity of spatial neighbors (for spatial analysis)


- **Prepandemic** folder includes 3 data files in csv format and 1 dictionary file in csv format, containing the following data

    - Existing health and health care disparities 
    - Individual tax filing, individual and household income brackets
    - Population density per area and crowdedness per housing unit
    - Demographic structure by age, gender and race-ethnicity
    - Prevalence rates of diabetes, HIV, and smoking, conditions associated with more severe COVID-19 symptoms


All data files include state or county names and FIPS codes to facilitate data merging of Data Hub files with external files. The daily data in this Data Hub is scheduled to routine update every Monday.


## User Registration and Feedback
The success of HPC Data Hub relies on users’ questions, feedback, and suggestions. The HPC Data Hub includes a [registration form](https://docs.google.com/forms/d/e/1FAIpQLScCkT9_jOyNuT-edOrfgkbd8Y3ENtJGCPAKTZ9RtQM5xr_r5g/viewform?usp=sf_link) and a [feedback form](https://docs.google.com/forms/d/e/1FAIpQLSdraC_8Tu97pXo6W0q_gtuV-ew8Pbxy89EhtaQEiUxT5IgCXA/viewform?usp=sf_link). The HPC Data Hub team is devoted to timely responding to users’ questions and suggestions.

[User Registration Form](https://docs.google.com/forms/d/e/1FAIpQLScCkT9_jOyNuT-edOrfgkbd8Y3ENtJGCPAKTZ9RtQM5xr_r5g/viewform?usp=sf_link)

[User Feedback Form](https://docs.google.com/forms/d/e/1FAIpQLSdraC_8Tu97pXo6W0q_gtuV-ew8Pbxy89EhtaQEiUxT5IgCXA/viewform?usp=sf_link)


## The HPC Data Hub Team
- Phase 4-5
    - Faculty: Lingxin Hao
    - Student: Xingyun Wu, Gracyn Sollmann
- Phases 1-3
    - Faculty: Qingfeng Li (lead), Alexandre White, Lingxin Hao
    - Students: Xingyun Wu, Apoorv Dayal, Aditya Suru, Jiaolong He, Giuliana Nicolucci-Altman, Gwyneth Wei
