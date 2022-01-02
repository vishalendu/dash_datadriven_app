### Dash data driven app

Simple Plotly Dash based application written with data in mind<br>
The application uses two data files 
* data/index.csv
* data/details.csv

The main screen creates Cards based on index.csv<br>
On clicking the Open button on any of the card, a modal window is opened with multiple tabs based on the "Number of Context" for a particular country.<br>
Each tab has context specific data (part of details.csv)
<br><br>
All of the objects are created programmatically based on the data in the dataframe, this makes the code generic and can be used to create dashboard/apps based on data rather than hard coded HTML/CSS.
