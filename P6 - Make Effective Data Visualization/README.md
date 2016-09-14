# Project 6: Make Effective Data Visualization

#### Summary
After having explored the Titanic dataset from Kaggle, the features Sex and Passenger Class were found to be strongly correlated with survival rate. Even though it was quite expected that females had increased chances compared to males with similar characteristics, it was striking that Passenger Class, which is a proxy for socio-economic status, had also a very strong effect. In fact, men of 1st class had almost the same chances for survival as women of 3rd class. Here, we aim to visualize the effect of these two factors on survival rate and ultimately to depict this unexpected observation.


#### Design
We intended to plot a quantitative variable ("mean survival rate") versus a qualitative ("sex"). The best choice for such a pair is to use a bar chart. At the same time we wanted to plot across another qualitative feature ("pclass"), so we used color to discriminate classes. Also, since we use dimplejs, interaction and animation features are included by default. Specifically, when hovering over a visual encoding a tooltip describing the data point pops up, and a dashed line intercepts y axis. Additionally, we introduced a delay parameter in the drawing function, so as to animate the the bar plotting.

The first version of the visualization was a quick sketch using percentages on the y axis. As each bar must add up to 1, adding the third variable creates a stacked bar chart. Feedback for this version was disappointing, as this graph does not show neither that women were more likely to be saved than men, nor that men of 1st class were given priority over women of lower classes.

On the second version, two important changes were implemented. The y axis with percentages was replaced by a regular axis, and instead the survival rates were calculated through aggregation and averaging on the series. Here we exploited the fact that the target variable "Survived" is either 0 or 1, so we can use the averages per group to find the mean survival rate directly. The second change was to pass the name of the third variable "Pclass" as argument in the x axis. This way we converted the graph into a vertical grouped bar chart.

The reception of this second version was much better. Survival rates were now correctly shown and it was easier to draw comparisons between them. Nevertheless, our visualization was lacking usability. The bars were unordered and it was unclear the meaning of each color. Thus, on the third and final version we added a rule to order the groups on x axis, as also a legend to explain different colors and a title to describe the chart. One downside was that it was impossible to add the name of the variable in the legend or to order the labels.


#### Feedback
The different versions of this visualization were shared with colleagues and feedback was collected. Comments on the first version revealed significant deficiencies: "There is no big difference between men and women" and "It is not clear what role play the colors".

Indeed, the vertical axis was wrong and it did not convey the information we wanted. It showed the percentage of passenger classes over survivors of each gender and naturally each bar summed up to 1, making it impossible to draw clear conclusions. Instead, we wanted to show percentages of survivors over the total population of each gender and class. Also, the discrimination between classes using colors was made clear by converting the stacked bar chart into vertical grouped.

After these changes, the second version was reviewed better: "Now the groups per gender and class stand out" and "I understand the vertical axis measures the chances of survival, but it is difficult to compare the bars".

In order to facilitate comparisons and emphasize the two messages we described in Summary, we devised the third and final version of the visualization. The bars were ordered by "Pclass" and informative text was added in a title and a legend. Actually, the feedback after these revisions made it clear that our chart was fulfilling its purpose: "It is obvious that females had much more chances to survive, as also that passengers of upper classes had priority" and "Yes, women of third class are at the same level with men of first class".


#### Resources
1. Dataset file and description from Kaggle  
https://www.kaggle.com/c/titanic/data
2. Exploratory analysis on this dataset from own previous work  
https://github.com/papanag/udacity_data_analyst_nanodegree/tree/master/P2%20-%20Investigate%20a%20Dataset
3. Example code from dimplejs official page
http://dimplejs.org/
