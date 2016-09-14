
### Project 2: Investigate a Dataset
In this project we analyze the Titanic dataset.

#### Motivation
When the Titanic sank, the majority of passengers and crew were killed. What factors made people more likely to survive?

#### Method
Here we investigate the given dataset of passenger personal information. First, we will explore its structure in order to select the most promising features for further analysis. We will investigate relationships between them and how they affect survival rate. To this end, we will use statistical summaries and various visualizations.

#### Exploring the dataset structure


```python
import numpy as np
import pandas as pd
%pylab inline
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('titanic_data.csv')
df.shape
```

    Populating the interactive namespace from numpy and matplotlib


    /Applications/anaconda/lib/python2.7/site-packages/IPython/html.py:14: ShimWarning: The `IPython.html` package has been deprecated. You should import from `notebook` instead. `IPython.html.widgets` has moved to `ipywidgets`.
      "`IPython.html.widgets` has moved to `ipywidgets`.", ShimWarning)





    (891, 12)



The dataset has 891 observations and 12 variables.


```python
df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PassengerId</th>
      <th>Survived</th>
      <th>Pclass</th>
      <th>Name</th>
      <th>Sex</th>
      <th>Age</th>
      <th>SibSp</th>
      <th>Parch</th>
      <th>Ticket</th>
      <th>Fare</th>
      <th>Cabin</th>
      <th>Embarked</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>0</td>
      <td>3</td>
      <td>Braund, Mr. Owen Harris</td>
      <td>male</td>
      <td>22</td>
      <td>1</td>
      <td>0</td>
      <td>A/5 21171</td>
      <td>7.2500</td>
      <td>NaN</td>
      <td>S</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1</td>
      <td>1</td>
      <td>Cumings, Mrs. John Bradley (Florence Briggs Th...</td>
      <td>female</td>
      <td>38</td>
      <td>1</td>
      <td>0</td>
      <td>PC 17599</td>
      <td>71.2833</td>
      <td>C85</td>
      <td>C</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>1</td>
      <td>3</td>
      <td>Heikkinen, Miss. Laina</td>
      <td>female</td>
      <td>26</td>
      <td>0</td>
      <td>0</td>
      <td>STON/O2. 3101282</td>
      <td>7.9250</td>
      <td>NaN</td>
      <td>S</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>1</td>
      <td>1</td>
      <td>Futrelle, Mrs. Jacques Heath (Lily May Peel)</td>
      <td>female</td>
      <td>35</td>
      <td>1</td>
      <td>0</td>
      <td>113803</td>
      <td>53.1000</td>
      <td>C123</td>
      <td>S</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>0</td>
      <td>3</td>
      <td>Allen, Mr. William Henry</td>
      <td>male</td>
      <td>35</td>
      <td>0</td>
      <td>0</td>
      <td>373450</td>
      <td>8.0500</td>
      <td>NaN</td>
      <td>S</td>
    </tr>
  </tbody>
</table>
</div>



The variable of interest is "Survived", indicating whether a certain passenger made it (value 1) or passed away (value 0). Let's look at some summary statistics.


```python
df.describe()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PassengerId</th>
      <th>Survived</th>
      <th>Pclass</th>
      <th>Age</th>
      <th>SibSp</th>
      <th>Parch</th>
      <th>Fare</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>891.000000</td>
      <td>891.000000</td>
      <td>891.000000</td>
      <td>714.000000</td>
      <td>891.000000</td>
      <td>891.000000</td>
      <td>891.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>446.000000</td>
      <td>0.383838</td>
      <td>2.308642</td>
      <td>29.699118</td>
      <td>0.523008</td>
      <td>0.381594</td>
      <td>32.204208</td>
    </tr>
    <tr>
      <th>std</th>
      <td>257.353842</td>
      <td>0.486592</td>
      <td>0.836071</td>
      <td>14.526497</td>
      <td>1.102743</td>
      <td>0.806057</td>
      <td>49.693429</td>
    </tr>
    <tr>
      <th>min</th>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>1.000000</td>
      <td>0.420000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>223.500000</td>
      <td>0.000000</td>
      <td>2.000000</td>
      <td>20.125000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>7.910400</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>446.000000</td>
      <td>0.000000</td>
      <td>3.000000</td>
      <td>28.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>14.454200</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>668.500000</td>
      <td>1.000000</td>
      <td>3.000000</td>
      <td>38.000000</td>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>31.000000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>891.000000</td>
      <td>1.000000</td>
      <td>3.000000</td>
      <td>80.000000</td>
      <td>8.000000</td>
      <td>6.000000</td>
      <td>512.329200</td>
    </tr>
  </tbody>
</table>
</div>



#### Univariate analysis
We will continue our analysis focusing on "Age", "Sex" and "Pclass". Age should influence survival, since it is probable that children were saved first. Similarly, it is likely that women had also priority. Finally, it is intriguing to examine if people from upper classes had a better chance, as Pclass is a proxy for socio-economic status.


```python
# Passengers that survived vs passengers that passed away
print(df["Survived"].value_counts())

# As proportions
print(df["Survived"].value_counts(normalize = True))
```

    0    549
    1    342
    dtype: int64
    0    0.616162
    1    0.383838
    dtype: float64


Here, we verified that most people did not survive, as there was a 62% chance of dying.

Before examining the selected variables, we should make sure that there are not missing values.


```python
def missing_values(field):
    return len(df[field][pd.isnull(df[field])])

print 'Missing values of Age:' , missing_values('Age')
print 'Missing values of Sex:' , missing_values('Sex')
print 'Missing values of Pclass:' , missing_values('Pclass')
```

    Missing values of Age: 177
    Missing values of Sex: 0
    Missing values of Pclass: 0


At this point we must decide how to handle missing values. We could substitute each missing value with the median of the all present values. This way we may not affect statistics, but we will distort the age distribution. Thus, we will omit rows with missing age to plot the respective histogram. Later in our multivariate analysis, we should be careful to examine the distributions of other features among observations with missing age (aka missingness), before deciding how to handle them.


```python
df_clean = df[pd.notnull(df["Age"])]
```


```python
plt.hist(df_clean["Age"], bins = np.arange(0, 100, 5))
plt.xlabel('Age')
plt.xticks(np.arange(0, 100, 10));
```


![png](images/output_13_0.png)


Let's also create bar charts for the other two selected variables. Pclass may have integer values, but it is actually a qualitative variable.


```python
# vanilla matplotlib
# x = [1,2]
# y = df.groupby('Sex').size()
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.bar(x, y, width=0.5, align='center')
# ax.set_xlabel('Sex')
# ax.set_xticks(x)
# ax.set_xticklabels(['female', 'male']);

sns.countplot(x="Sex", data=df);
```


![png](images/output_15_0.png)



```python
# vanilla matplotlib
# x = [1,2,3]
# y = df.groupby('Pclass').size()
# plt.bar(x, y, width=.5, align='center')
# plt.xlabel('Pclass')
# plt.xticks(x);

sns.countplot(x="Pclass", data=df);
```


![png](images/output_16_0.png)


The bar charts above reveal that there were almost twice men as women, as also that passengers of 3rd class were more than passengers of 1st and 2nd class together.

#### Multivariate analysis
We will continue our analysis investigating the effect of the three selected predictor variables to the variable of interest "Survived".

First, we will depict the mean survival rate across age groups, using a bin width of 10 years.


```python
df['Age_group'] = pd.cut(df['Age'], 
                         bins=np.arange(0, 100, 10), 
                         labels=['0-10','10-20','20-30','30-40',
                                 '40-50','50-60','60-70','70-80',
                                 '80-90']
                        )
```


```python
# ax = df.groupby('Age_group').mean()['Survived'].plot()

# tsplot is unsuitable as it makes the assumption we have sampled the same units at each timepoint
# sns.tsplot(data=df_clean, time='Age', unit='PassengerId', condition="Pclass", value='Age')

sns.pointplot(x="Age_group", y="Survived", data=df);
```

    /Applications/anaconda/lib/python2.7/site-packages/matplotlib/collections.py:590: FutureWarning: elementwise comparison failed; returning scalar instead, but in the future will perform elementwise comparison
      if self._edgecolors == str('face'):



![png](images/output_20_1.png)


Indeed, children were saved first, with ages 0 to 10 having 1.5 times greater chance of surviving than the rest. We also notice ages 30 to 60 to have greater survival rate than expected. This may be the effect from other variables, like Sex or Pclass. We will create two helper variables to explore further these two age groups.


```python
df["Child"] = float(0)
df["Child"][df["Age"] < 10] = 1

df["Middle_aged"] = float(0)
df["Middle_aged"][(df["Age"] >= 30) & (df["Age"] < 60)] = 1
```

    /Applications/anaconda/lib/python2.7/site-packages/ipykernel/__main__.py:2: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame
    
    See the the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      from ipykernel import kernelapp as app
    /Applications/anaconda/lib/python2.7/site-packages/ipykernel/__main__.py:5: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame
    
    See the the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy



```python
# since Survived is either 0 or 1, we can use mean()
# to find the survival rate directly and avoid the following:
#
# df["Survived"][df["Child"] == 0].value_counts(normalize = True)
# df["Survived"][df["Child"] == 1].value_counts(normalize = True)

df.groupby('Child')['Survived'].mean().reset_index()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Child</th>
      <th>Survived</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>0.366707</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>0.612903</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.groupby('Sex')['Survived'].mean().reset_index()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Sex</th>
      <th>Survived</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>female</td>
      <td>0.742038</td>
    </tr>
    <tr>
      <th>1</th>
      <td>male</td>
      <td>0.188908</td>
    </tr>
  </tbody>
</table>
</div>



Here we confirm our hypothesis that women were given priority. Their survival rate was almost 4 times that of men.


```python
df.groupby('Pclass')['Survived'].mean().reset_index()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Pclass</th>
      <th>Survived</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>0.629630</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>0.472826</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>0.242363</td>
    </tr>
  </tbody>
</table>
</div>



Also, it seems that passengers of 1st and 2nd class had a much better chance of surviving. This is not necessarily a direct effect, but other factors such as age or gender may be interfering.

Thus, we will explore the age and gender distribution for each Pclass.


```python
# grouped = df.groupby('Pclass')
# grouped.boxplot(column='Age', layout=(1,3), return_type='axes');

ax = plt.axes()
# sns.kdeplot(df['Age'][df["Pclass"]==1], label="Pclass: 1")
# sns.kdeplot(df['Age'][df["Pclass"]==2], label="Pclass: 2")
# sns.kdeplot(df['Age'][df["Pclass"]==3], label="Pclass: 3")
gr = df.groupby('Pclass')['Age']
for label, arr in gr:
    sns.kdeplot(arr, label=label)
ax.set(title='Age distribution per Pclass');
```


![png](images/output_29_0.png)


First, we observe that higher classes correspond to greater mean age. Also, there is a bump in ages 0-10 for Pclass 2 and 3, but there is not one for Pclass 1.  
Furthermore, the middle aged group that showed a greater survival rate, seem to overlap with the majority of 1st class passengers. Therefore, here we observe how Pclass correlates with age and also affects directly chances of survival, against the inverse trend due to age.

Next, it would be interesting to explore the age distribution of each sex, as also the proportions of males/females for each Pclass. Instead, we will depict these relations in a combined graph.


```python
sns.violinplot(x="Pclass", y="Age", hue="Sex", data=df, split=True);
```


![png](images/output_32_0.png)


Male passengers of 1st class seem to be older on average than the female. On the contrary, passengers of 2nd and 3rd class are equally distributed between sexes.

Now let's explore survival rate across age groups as before, while discriminating each Pclass and then each sex.


```python
sns.pointplot(x="Age_group", y="Survived", data=df, hue="Pclass");
```


![png](images/output_35_0.png)


Here it is shown that Pclass was a much stronger factor to determine your fate, than your age.


```python
sns.pointplot(x="Age_group", y="Survived", data=df, hue="Sex");
```


![png](images/output_37_0.png)


Again, sex was a much stronger factor than age. Being a female increased dramatically your chances compared to males of same age. There is only one exception for ages 0-10, where their survival rate seem to have been independent of sex.


```python
sns.barplot(x="Sex", y="Survived", hue="Pclass", data=df);
```


![png](images/output_39_0.png)


Finally, we visualize mean survival rate across Sex and Pclass. The trend that passengers of higher class were saved first, is consistent between sexes. The most interesting fact is that men of 1st class had almost the same survival rate as women of 3rd class.

So far, we have depicted in numerous ways how our chosen features interweave. We have also shown that these variables affect strongly chances of survival. In order to investigate quantitatively the influence of each one, as also the dependencies between them, we will create a correlation matrix. Missing values are excluded by default. To include variable Sex, we must assign first a numerical value to each level of the categorical variable: male=0 and female=1.


```python
df["Sex_class"] = float('NaN')
df["Sex_class"][df["Sex"] == "male"] = 0
df["Sex_class"][df["Sex"] == "female"] = 1
```

    /Applications/anaconda/lib/python2.7/site-packages/ipykernel/__main__.py:2: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame
    
    See the the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      from ipykernel import kernelapp as app
    /Applications/anaconda/lib/python2.7/site-packages/ipykernel/__main__.py:3: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame
    
    See the the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      app.launch_new_instance()



```python
df[['Age','Sex_class','Pclass','Child','Middle_aged','Survived']].corr()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Age</th>
      <th>Sex_class</th>
      <th>Pclass</th>
      <th>Child</th>
      <th>Middle_aged</th>
      <th>Survived</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Age</th>
      <td>1.000000</td>
      <td>-0.093254</td>
      <td>-0.369226</td>
      <td>-0.544155</td>
      <td>0.609177</td>
      <td>-0.077221</td>
    </tr>
    <tr>
      <th>Sex_class</th>
      <td>-0.093254</td>
      <td>1.000000</td>
      <td>-0.131900</td>
      <td>0.075254</td>
      <td>0.014204</td>
      <td>0.543351</td>
    </tr>
    <tr>
      <th>Pclass</th>
      <td>-0.369226</td>
      <td>-0.131900</td>
      <td>1.000000</td>
      <td>0.104857</td>
      <td>-0.279976</td>
      <td>-0.338481</td>
    </tr>
    <tr>
      <th>Child</th>
      <td>-0.544155</td>
      <td>0.075254</td>
      <td>0.104857</td>
      <td>1.000000</td>
      <td>-0.196805</td>
      <td>0.128812</td>
    </tr>
    <tr>
      <th>Middle_aged</th>
      <td>0.609177</td>
      <td>0.014204</td>
      <td>-0.279976</td>
      <td>-0.196805</td>
      <td>1.000000</td>
      <td>0.050201</td>
    </tr>
    <tr>
      <th>Survived</th>
      <td>-0.077221</td>
      <td>0.543351</td>
      <td>-0.338481</td>
      <td>0.128812</td>
      <td>0.050201</td>
      <td>1.000000</td>
    </tr>
  </tbody>
</table>
</div>



The matrix shows that Sex, Pclass and Child are indeed variables with noticeable correlation with survival rate.

#### Conclusions
We have explored the Titanic dataset by investigating the distribution of selected features and their relationship to survival rate. Sex seem to have been the strongest factor to increase your chances of survival, as being a woman increased dramatically your chances compared to a man with similar other characteristics. Even so, passenger class was also such a strong factor, that men of 1st class had the same chances with women of 3rd class. Finally, we discovered that age generally did not played a decisive role for survival, with the exception that children of ages 0 to 10 were saved with absolute priority, regardless of sex or class. All in all, we confirmed our hypothesis that these features should have affected strongly the chances of survival of a passenger, using a variety of analyses, both qualitative and quantitative. Moreover, we have discovered dependencies between features, such as that middle aged passengers were travelling mainly 1st class.

Nevertheless, our findings do not imply that these factors solely were able to seal the fate of each passenger. There are other variables in this dataset that may play a significant role. For example, members of one family may have been saved together, or the lower the deck on which a passenger was, the more difficult it may have been to reach a lifeboat. Furthermore, it is likely to have some biases in the dataset, such as that available information may be inaccurate for passengers that did not survive or depending on where they issued their ticket. Still, we have discovered features with strong correlation with survival rate, and thus it is possible for someone to build a predictive model based on this dataset.
