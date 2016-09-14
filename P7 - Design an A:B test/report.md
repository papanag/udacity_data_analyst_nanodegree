# Project 7: Design an A/B test

## Experiment Design

### Metric Choice
*List which metrics you will use as invariant metrics and evaluation metrics here.*

* **Invariant metrics:** Number of cookies, Number of clicks, Click-through-probability
* **Evaluation metrics:** Gross conversion, Net conversion

*For each metric, explain both why you did or did not use it as an invariant metric and why you did or did not use it as an evaluation metric. Also, state what results you will look for in your evaluation metrics in order to launch the experiment.*

* **Number of cookies:** It is a count metric independent from the experiment, as a session starts before the pop up message (intervention) and thus it can be used as invariant metric.
* **Number of user-ids:** It is a count metric affected by the experiment, as a user id is created after enrollment and thus it can not be used as invariant metric. But it is not a good evaluation metric either, as the number of users found in the two groups may also be independent from our intervention.
* **Number of clicks:** It is a count metric independent from the experiment, as the click happens before the intervention and thus it can be used as invariant metric.
* **Click-through-probability:** It is a metric that can be used as invariant metric for the same reasons with "Number of clicks". We can use both at the same time as they gauge different concepts.
* **Gross conversion:** It is not suitable to be an invariant metric as it takes into account the number of enrolled users, which is affected by our intervention. For this reason it can be used as evaluation metric.
* **Retention:** It depends on the number of enrolled users and the number of paying users, both of which are affected by the experiment. Definitely it can not be used as invariant metric, but also it may be better to avoid using it as evaluation metric. This is because the two parts of the fraction may give contradictory trends and furthermore, by using "Gross conversion" and "Net conversion" as evaluation metrics we probe the same pieces of information one at a time.
* **Net conversion:** It is not suitable to be an invariant metric as it takes into account the number of paying users, which is affected by our intervention. For this reason it can be used as evaluation metric.

If we see a practically significant change in our evaluation metrics, we must consider launching the experiment. We expect **Gross conversion** to decrease and conversely **Net conversion** not to decrease. The first criterion serves the goal to reduce the number of unprepared enrollments and the second not to harm revenues.

### Measuring Standard Deviation
*List the standard deviation of each of your evaluation metrics.*

Both our evaluation metrics refer to probabilities, therefore they follow a binomial distribution with standard deviation given by `sqrt(p * (1-p) / N)`. The denominator of each metric is the number of clicks and thus `N` would be the same for both SDs. Also, as probabilities `p` are given for 40,000 pageviews and the sample size is 5,000, we use the 12,5% of the given number of clicks and we get `N = 400`. Finally, we use the formula above and we find:

```
SD of "Gross conversion": 0.0202
SD of "Net conversion": 0.0156
```

*For each of your evaluation metrics, indicate whether you think the analytic estimate would be comparable to the the empirical variability, or whether you expect them to be different (in which case it might be worth doing an empirical estimate if there is time). Briefly give your reasoning in each case.*

In choosing whether to use an analytical or empirical estimate for the evaluation metrics we should check the denominators, or the unit of analyses, and the unit of diversion. The evaluation metrics "Gross conversion" and "Net conversion" have as denominator the "number of unique cookies to click the "Start free trial" button", which is measured based on cookies, even though it refers to clicks. Also, we know from the experiment design that cookies are used as unit of diversion. Therefore, the units of diversion and analyses are the same and we can use the analytical estimate for both metrics.

### Sizing
#### Number of Samples vs. Power
*Indicate whether you will use the Bonferroni correction during your analysis phase, and give the number of pageviews you will need to power you experiment appropriately.*

We will **not use the Bonferroni correction**, as the metrics are highly correlated and thus the correction will generate conservative results.

Using the online sample size calculator with the given values of baseline rates and d<sub>min</sub>, we get a sample size of 25,835 per variation for "Gross conversion" and 27,413 for "Net conversion". Then, we must proceed with the biggest number to power the experiment, and multiply it with 2 to take into account both the control and the experiment group. Finally, we divide the last result by the "Click-through-probability" and we find the needed number of pageviews to be **685,325**.

#### Duration vs. Exposure
*Indicate what fraction of traffic you would divert to this experiment and, given this, how many days you would need to run the experiment.*

If we choose to divert **80%** of the traffic, the experiment will be running for **22 days**, based on the given pageviews per day and the required amount of pageviews for our experiment.

*Give your reasoning for the fraction you chose to divert. How risky do you think this experiment would be for Udacity?*

It is not recommended to run an experiment on the whole traffic, since it is possible to exist unexpected and undesirable effects. On the other hand, we want to run it for a reasonable amount of time and as a result the fraction should not be very low. Also, this experiment is not very risky for the company, as it does not affect users who would have made payments anyway and thus it does not put at risk revenues. All in all, we are able to set a pretty big fraction to be diverted.

## Experiment Analysis
### Sanity Checks
*For each of your invariant metrics, give the 95% confidence interval for the value you expect to observe, the actual observed value, and whether the metric passes your sanity check.*

We will follow these steps to calculate the 95% CI for each invariant metric:

* Find the probability `p` of the metric and the total size `N` across all groups
* Standard Error: `SE = sqrt(p * (1-p) / N.total)`
* Margin of Error: `m = 1.96 * SE`
* Lower CI Bound = `p - m`
* Upper CI Bound = `p + m`
* Observed = `N.cont / N.total`

Metric | Lower CI Bound | Upper CI Bound | Observed | Passes
------ | -------------- | -------------- | -------- | ------
Number of cookies | 0.4988 | 0.5012 | 0.5006 | YES
Number of clicks | 0.4959 | 0.5041 | 0.5005 | YES
Click-through-probability | 0.0812 | 0.0830 | 0.0822 | YES

We note that the first two are count metrics and thus a `p = 0.5` was used, whereas the third was calculated from control group to be `p = 0.0822`.

### Result Analysis

#### Effect Size Tests
*For each of your evaluation metrics, give a 95% confidence interval around the difference between the experiment and control groups. Indicate whether each metric is statistically and practically significant.*

We will follow these steps to calculate the 95% CI for each evaluation metric:

* Find the probabilities `p.cont`, `p.exp` and `p.pool` of the metric using the two groups
* Calculate the difference `d = p.exp - p.cont`
* Standard Error: `SE = sqrt(p.pool * (1-p.pool) * (1/N.cont + 1/N.exp)`
* Margin of Error: `m = 1.96 * SE`
* Lower CI Bound = `d - m`
* Upper CI Bound = `d + m`

Metric | Lower CI Bound | Upper CI Bound | Statistically significant | Practically significant
------ | -------------- | -------------- | ------------------------- | -----------------------
Gross conversion | -0.0291 | -0.0120 | YES | YES
Net conversion | -0.0116 | 0.0019 | NO | NO

A metric is statistically significant if the confidence interval does not include 0 and it is practically significant if the confidence interval does not include the practical significance boundary.

#### Sign Tests
*For each of your evaluation metrics, do a sign test using the day-by-day data, and report the p-value of the sign test and whether the result is statistically significant.*

Metric | p-value | Statistically significant
------ | ------- | -------------------------
Gross conversion | 0.0026 | YES
Net conversion | 0.6776 | NO

#### Summary
*State whether you used the Bonferroni correction, and explain why or why not. If there are any discrepancies between the effect size hypothesis tests and the sign tests, describe the discrepancy and why you think it arose.*

In our analysis we make multiple comparisons (2 metrics), thus we should consider using Bonferroni correction. However, the criteria to launch the experiment must be fulfilled at the same time, as we want to reduce enrollments and not harm revenue, making our results more susceptible to false negatives rather than false positives. Since the correction reduce false positives at the expense of an increased rate of false negatives, we conclude that Bonferroni correction should not be used. Also, we did not found any discrepancies between Effect size and Sign tests, as both tests rejected "Net conversion" as insignificant and kept only "Gross conversion".

### Recommendation
*Make a recommendation and briefly describe your reasoning.*

After analyzing the results of our experiment we find that we can rely on only one metric, the "Gross conversion". This metric showed a 2% decrease on the ratio of users clicking the "Start free trial" button versus users actually completing the enrollment. This result was found both statistically and practically significant and reveals the fact that the screener had in reality the desired effect. Nevertheless, we found evidence indicating that this was accompanied by a small decrease of 0.5% on paying users. Even though "Net conversion" was found statistically and practically not significant as a metric, we observed a trend opposite to the specifications. In conclusion, as far as the experiment aimed to reduce the workload of reviewers and improve the student's satisfaction, it seems to have succeeded, but this went with a decrease of payments, and thus it is recommended the experiment not to be launched.

## Follow-Up Experiment
*Give a high-level description of the follow up experiment you would run, what your hypothesis would be, what metrics you would want to measure, what your unit of diversion would be, and your reasoning for these choices.*

A follow-up experiment could aim in increasing students' engagement. Specifically, enrollments will randomly be assigned to a Control and an Experiment group. The experience for users in the Control group will remain unchanged. Users in the Experiment group will be presented with time management strategies when accessing course materials. For such an experiment we could use:

* The null hypothesis will be that proposing time management strategies to new enrollments will not increase Retention by a practically significant amount
* "user-id" will be the unit of diversion, as it is unique for each user after enrollment
* "Number of user-ids" will be the invariant metric, since they are created before our intervention, during enrollment
* "Retension" will be the evaluation metric, as we expect payments to increase from our intervention and the denominator (number of enrollments) is suitable for a post-enrollment experiment

## Resources
* [http://www.evanmiller.org/](http://www.evanmiller.org/)





