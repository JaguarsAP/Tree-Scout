# CS506-Final-Project
The final project for CS506 at Boston University


Description:
  I'm working with 1 partner, Anthony Hardimon. Together, we are going to be monitering the rate of deforestation globally in an effort to predict which areas of the world are most likely to be the target of deforestation next.

Data:
  We will be (mostly) using data from the GFW (Global Forest Watch), which is an API made with the goal of tracking various statistics relateed to deforestation. These include:
  - Tree cover loss (annual hectares lost)
  - Tree cover gain (annual hectares gained)
  - Primary forest loss (GLAD-S2 alerts)
  - Deforestation hotspots (daily confidence-scored alerts)
  - Cumulative forest change (loss − gain over multi-year spans)

Modeling:
  In terms pf modeling the data, we have not yet determined the best way to do this yet. However, based on the direction the class is trending, it is likely going to be a combination of clustering and fitting a linear model for predictions.

Visualization: 
  For this, I have some experience in making interactive plots, and so that's likely what we'll go with. Anthony has made a website in the past, so we'll probably do an interactive plot in a website.

Testing:
  Since we're training a predictive model, it's likely that we won't be able to use this year's data. In general, deforestation takes a long time, so we'll probably be using data from the last decade and before. By not using the data from ths year, we have data to test against.




  
