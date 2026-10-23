# Sources for the Data Scientist

Where the Data Scientist's knowledge comes from. URLs were fetched and checked on 2026-10-24 by script: a row is `verified` when the page loaded and its text contained the title's key words; otherwise it is `unverified` (blocked, moved, or only a secondary page).

How to use these sources
- Ideas only, in our own words. Never copy passages. Cite a source by its ID, for example `[S-STA-1]`.
- Cite a source as fact only when its Status is `verified`. A row marked `unverified` is a lead: say "unverified" in the same line when you mention it.
- `verified` means the URL resolved and the page showed the title's words; the year is the well-known edition. A book listing proves the book exists, not that every claim in it was read.
- Free does not mean copyable: summarise, never paste. Some statements here about law (GDPR) are pointers, not advice.

## Experiments and A/B tests

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-EXP-1 | Trustworthy Online Controlled Experiments | Ron Kohavi, Diane Tang, Ya Xu | 2020 | https://experimentguide.com/ | The practical reference for designing, running and reading online experiments: metrics, sample ratio mismatch, pitfalls. | Book (paid); site free | verified |
| S-EXP-2 | Controlled experiments on the web: survey and practical guide | Ron Kohavi, Roger Longbotham, Dan Sommerfield, Randal Henne | 2009 | https://link.springer.com/article/10.1007/s10618-008-0114-1 | Survey of online controlled experiments and the mistakes that invalidate them. | Paywalled; abstract free | unverified |
| S-EXP-3 | How not to run an A/B test | Evan Miller | 2010 | https://www.evanmiller.org/how-not-to-run-an-ab-test.html | Why peeking and stopping early inflate false positives; fix the sample size first. | Free to read; licence unverified | unverified |
| S-EXP-4 | Sample size calculator for A/B tests | Evan Miller | ongoing | https://www.evanmiller.org/ab-testing/sample-size.html | Checking a sample-size calculation for a conversion-rate test. | Free to read; licence unverified | verified |
| S-EXP-5 | Sequential A/B testing | Evan Miller | 2015 | https://www.evanmiller.org/sequential-ab-testing.html | How to stop a test early without breaking the error rates. | Free to read; licence unverified | verified |
| S-EXP-6 | Always Valid Inference: Continuous Monitoring of A/B Tests | Ramesh Johari, Pete Koomen, Leo Pekelis, David Walsh | 2017 | https://arxiv.org/abs/1512.04922 | The statistics behind safe continuous monitoring of experiments (peeking). | Free (arXiv) | verified |
| S-EXP-7 | A power primer | Jacob Cohen | 1992 | https://doi.org/10.1037/0033-2909.112.1.155 | Effect sizes and power in plain terms; where small, medium and large effect conventions come from. | Paywalled; abstract free | verified |
| S-EXP-8 | Diagnosing sample ratio mismatch in online controlled experiments | Aleksander Fabijan et al. | 2019 | https://www.microsoft.com/en-us/research/publication/diagnosing-sample-ratio-mismatch-in-online-controlled-experiments-a-taxonomy-and-rules-of-thumb-for-practitioners/ | Why group sizes can differ from the plan and how to diagnose the cause. | Free to read; licence unverified | verified |

## Statistics and honest inference

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-STA-1 | The ASA Statement on p-Values: Context, Process, and Purpose | Ronald Wasserstein, Nicole Lazar | 2016 | https://doi.org/10.1080/00031305.2016.1154108 | Six principles on what a p-value is and is not; the basis for how the role reports tests. | Open access | verified |
| S-STA-2 | Moving to a World Beyond p < 0.05 | Ronald Wasserstein, Allen Schirm, Nicole Lazar | 2019 | https://doi.org/10.64628/aai.mw37cmu4x | Why to report estimates and intervals, not significance labels. | Open access | verified |
| S-STA-3 | Why Most Published Research Findings Are False | John Ioannidis | 2005 | https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.0020124 | Why small samples, many tested relationships and flexible analysis produce false findings. | Open access | verified |
| S-STA-4 | False-Positive Psychology: Undisclosed Flexibility in Data Collection and Analysis | Joseph Simmons, Leif Nelson, Uri Simonsohn | 2011 | https://doi.org/10.1037/e519702015-014 | How analyst choices (stopping, covariates, outcomes) make any result significant; the p-hacking reference. | Paywalled; abstract free | verified |
| S-STA-5 | The garden of forking paths: Why multiple comparisons can be a problem, even when there is no fishing expedition | Andrew Gelman, Eric Loken | 2013 | http://www.stat.columbia.edu/~gelman/research/unpublished/forking.pdf | Hidden analysis choices count as multiple comparisons. | Free PDF | unverified |
| S-STA-6 | Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing | Yoav Benjamini, Yosef Hochberg | 1995 | https://doi.org/10.1111/j.2517-6161.1995.tb02031.x | The false discovery rate procedure used when many comparisons are made. | Paywalled; abstract free | verified |
| S-STA-7 | The New Statistics: Why and How | Geoff Cumming | 2014 | https://doi.org/10.1177/0956797613504966 | Reporting effect sizes with confidence intervals instead of bare significance. | Paywalled; abstract free | verified |
| S-STA-8 | Using Effect Size, or Why the P Value Is Not Enough | Gail Sullivan, Richard Feinn | 2012 | https://pmc.ncbi.nlm.nih.gov/articles/PMC3444174/ | Short plain explanation of effect size next to p-values. | Open access | unverified |
| S-STA-9 | Statistical Modeling: The Two Cultures | Leo Breiman | 2001 | https://projecteuclid.org/journals/statistical-science/volume-16/issue-3/Statistical-Modeling--The-Two-Cultures-with-comments-and-a/10.1214/ss/1009213726.full | Explaining versus predicting: when a model is for understanding and when for accuracy. | Open access | unverified |
| S-STA-10 | Simpson's Paradox | Stanford Encyclopedia of Philosophy | ongoing | https://plato.stanford.edu/entries/paradox-simpson/ | Why a trend in every group can reverse in the pooled data, and how causal reasoning decides which view is right. | Free to read; licence unverified | verified |
| S-STA-11 | Statistical Rethinking | Richard McElreath | 2020 | https://xcelab.net/rm/ | Teaching text on thinking with models, uncertainty and causal structure. | Book (paid); site free | unverified |
| S-STA-12 | Regression and Other Stories | Andrew Gelman, Jennifer Hill, Aki Vehtari | 2020 | https://avehtari.github.io/ROS-Examples/ | Applied regression done honestly: what coefficients mean, prediction versus causation. | Book (paid); site free | verified |
| S-STA-13 | An Introduction to Statistical Learning | Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani | 2021 | https://www.statlearning.com/ | Accessible text on resampling, regression, classification and model assessment. | Free PDF | verified |
| S-STA-14 | The Elements of Statistical Learning | Trevor Hastie, Robert Tibshirani, Jerome Friedman | 2009 | https://hastie.su.domains/ElemStatLearn/ | Deeper reference on validation, bias and variance, and model selection. | Free PDF | verified |
| S-STA-15 | OpenIntro Statistics | David Diez, Mine Cetinkaya-Rundel, Christopher Barr | 2019 | https://www.openintro.org/book/os/ | Plain introduction to inference, intervals and tests for non-statisticians. | Free PDF | verified |
| S-STA-16 | Think Stats | Allen Downey | 2014 | https://greenteapress.com/wp/think-stats-2e/ | Exploratory statistics with Python; distributions, bootstrap and hypothesis tests by simulation. | Free online | verified |
| S-STA-17 | Statistics Done Wrong | Alex Reinhart | 2015 | https://www.statisticsdonewrong.com/ | A catalogue of common statistical mistakes in practice. | Free online | verified |
| S-STA-18 | NIST/SEMATECH e-Handbook of Statistical Methods | NIST | ongoing | https://www.itl.nist.gov/div898/handbook/ | Reference for exploratory analysis, distributions, tests and sample sizes. | Public domain | verified |

## Causal questions

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-CAU-1 | Causal Inference: What If | Miguel Hernan, James Robins | 2020 | https://miguelhernan.org/whatifbook | Definitions of causal effects, confounding and selection bias; when observational data can and cannot answer. | Free PDF | verified |
| S-CAU-2 | Causal Inference: The Mixtape | Scott Cunningham | 2021 | https://mixtape.scunning.com/ | Applied methods: matching, difference-in-differences, regression discontinuity, with code. | Free online | verified |
| S-CAU-3 | Causal Inference for the Brave and True | Matheus Facure | 2022 | https://matheusfacure.github.io/python-causality-handbook/ | Python walk-through of experiments, matching, diff-in-diff and instruments. | Free online | unverified |
| S-CAU-4 | A Crash Course in Good and Bad Controls | Carlos Cinelli, Andrew Forney, Judea Pearl | 2022 | https://ftp.cs.ucla.edu/pub/stat_ser/r493.pdf | Which variables to adjust for and which make a causal estimate worse. | Free PDF | unverified |
| S-CAU-5 | Difference-in-differences with variation in treatment timing | Andrew Goodman-Bacon | 2021 | https://doi.org/10.1016/j.jeconom.2021.03.014 | Why two-way fixed effects can mislead when treatment starts at different times. | Paywalled; abstract free | verified |
| S-CAU-6 | DoWhy documentation | PyWhy contributors | ongoing | https://www.pywhy.org/dowhy/ | A structured four-step process for causal analysis (model, identify, estimate, refute). | Open source docs | unverified |

## Modelling and validation

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-MOD-1 | Common pitfalls and recommended practices (scikit-learn) | scikit-learn developers | ongoing | https://scikit-learn.org/stable/common_pitfalls.html | Data leakage in preprocessing, randomness and pipelines, with fixes. | BSD licence docs | verified |
| S-MOD-2 | Cross-validation: evaluating estimator performance (scikit-learn) | scikit-learn developers | ongoing | https://scikit-learn.org/stable/modules/cross_validation.html | Splitting strategies including grouped and time-series splits. | BSD licence docs | verified |
| S-MOD-3 | Probability calibration (scikit-learn) | scikit-learn developers | ongoing | https://scikit-learn.org/stable/modules/calibration.html | Checking that predicted probabilities mean what they say. | BSD licence docs | verified |
| S-MOD-4 | Metrics and scoring (scikit-learn) | scikit-learn developers | ongoing | https://scikit-learn.org/stable/modules/model_evaluation.html | Choosing a metric that matches the decision (accuracy, precision, recall, AUC, error measures). | BSD licence docs | verified |
| S-MOD-5 | Permutation feature importance (scikit-learn) | scikit-learn developers | ongoing | https://scikit-learn.org/stable/modules/permutation_importance.html | A model-agnostic importance check and its limits with correlated features. | BSD licence docs | verified |
| S-MOD-6 | Rules of Machine Learning: Best Practices for ML Engineering | Martin Zinkevich | ongoing | https://developers.google.com/machine-learning/guides/rules-of-ml | Start with a simple baseline and good metrics before complexity. | Free; licence unverified | verified |
| S-MOD-7 | Hidden Technical Debt in Machine Learning Systems | D. Sculley et al. | 2015 | https://papers.nips.cc/paper_files/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html | Why models quietly become costly to maintain; entanglement and feedback loops. | Free (NeurIPS) | verified |
| S-MOD-8 | Datasheets for Datasets | Timnit Gebru et al. | 2018 | https://arxiv.org/abs/1803.09010 | Questions to document where a dataset came from and what it should and should not be used for. | Free (arXiv) | verified |
| S-MOD-9 | Model Cards for Model Reporting | Margaret Mitchell et al. | 2018 | https://arxiv.org/abs/1810.03993 | A short standard for reporting what a model does, how it was tested and its limits. | Free (arXiv) | verified |
| S-MOD-10 | Interpretable Machine Learning | Christoph Molnar | 2022 | https://christophm.github.io/interpretable-ml-book/ | Methods for explaining models and what each can and cannot tell you. | Free online | verified |
| S-MOD-11 | Stop Explaining Black Box Machine Learning Models for High Stakes Decisions and Use Interpretable Models Instead | Cynthia Rudin | 2019 | https://arxiv.org/abs/1811.10154 | When a simple interpretable model is the safer choice. | Free (arXiv) | verified |
| S-MOD-12 | The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets | Takaya Saito, Marc Rehmsmeier | 2015 | https://doi.org/10.1371/journal.pone.0118432 | Why ROC curves can look good on rare-event problems. | Open access | verified |
| S-MOD-13 | A note on the validity of cross-validation for evaluating autoregressive time series prediction | Christoph Bergmeir, Rob Hyndman, Bonsoo Koo | 2018 | https://doi.org/10.1016/j.csda.2017.11.003 | When ordinary cross-validation is and is not safe for time series. | Paywalled; abstract free | verified |
| S-MOD-14 | Data Leakage (Kaggle Learn) | Alexis Cook | ongoing | https://www.kaggle.com/code/alexisbcook/data-leakage | Worked examples of target leakage and train-test contamination. | Free to read; licence unverified | verified |

## Forecasting

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-FOR-1 | Forecasting: Principles and Practice (3rd ed) | Rob Hyndman, George Athanasopoulos | 2021 | https://otexts.com/fpp3/ | The standard open text: naive baselines, decomposition, exponential smoothing, ARIMA, accuracy measures, prediction intervals. | Free online | unverified |
| S-FOR-2 | Forecasting at Scale | Sean Taylor, Benjamin Letham | 2018 | https://doi.org/10.1080/00031305.2017.1380080 | The additive trend, seasonality and holiday model behind Prophet and its assumptions. | Open access | verified |
| S-FOR-3 | The M4 Competition: 100,000 time series and 61 forecasting methods | Spyros Makridakis, Evangelos Spiliotis, Vassilios Assimakopoulos | 2020 | https://doi.org/10.1016/j.ijforecast.2019.04.014 | Evidence that simple methods and combinations often beat complex ones. | Paywalled; abstract free | verified |
| S-FOR-4 | Time series analysis (statsmodels) | statsmodels developers | ongoing | https://www.statsmodels.org/stable/tsa.html | Tools and caveats for time-series models in Python. | BSD licence docs | verified |

## Data quality and exploration

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-DQ-1 | Tidy Data | Hadley Wickham | 2014 | https://www.jstatsoft.org/article/view/v059i10 | A clear shape for analysis tables: one row per observation, one column per variable. | Open access | unverified |
| S-DQ-2 | Working with missing data (pandas user guide) | pandas developers | ongoing | https://pandas.pydata.org/docs/user_guide/missing_data.html | How missing values behave in Python and the options for handling them. | BSD licence docs | verified |
| S-DQ-3 | Merge, join, concatenate and compare (pandas user guide) | pandas developers | ongoing | https://pandas.pydata.org/docs/user_guide/merging.html | Join types and checks (validate=) that expose duplicate keys and fan-out. | BSD licence docs | verified |
| S-DQ-4 | Great Expectations documentation | Great Expectations contributors | ongoing | https://docs.greatexpectations.io/docs/ | Declarative data checks (ranges, uniqueness, nulls) as a model for audit steps. | Open source docs | verified |
| S-DQ-5 | Graphs in Statistical Analysis | Francis Anscombe | 1973 | https://doi.org/10.1080/00031305.1973.10478966 | Four datasets with identical statistics and different shapes: always plot. | Paywalled; abstract free | verified |
| S-DQ-6 | Same Stats, Different Graphs | Justin Matejka, George Fitzmaurice | 2017 | https://www.research.autodesk.com/publications/same-stats-different-graphs/ | A modern take on Anscombe's lesson. | Free to read; licence unverified | verified |
| S-DQ-7 | A Reformulation of Wald's Work on Survivorship Bias | Abraham Mangel, Francisco Samaniego | 1984 | https://doi.org/10.1080/01621459.1984.10478038 | The classic account of survivorship bias in the data you can see. | Paywalled; abstract free | unverified |
| S-DQ-8 | Flexible Imputation of Missing Data | Stef van Buuren | 2018 | https://stefvanbuuren.name/fimd/ | Why missingness has types and when imputation helps or harms. | Free online | verified |

## Reporting and reproducibility

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-COM-1 | Storytelling with Data | Cole Nussbaumer Knaflic | 2015 | https://www.storytellingwithdata.com/books | Writing and charting results so a non-technical reader acts on them. | Book (paid) | verified |
| S-COM-2 | Fundamentals of Data Visualization | Claus Wilke | 2019 | https://clauswilke.com/dataviz/ | Choosing honest charts and showing uncertainty. | Free online | verified |
| S-COM-3 | Ten Simple Rules for Reproducible Computational Research | Geir Kjetil Sandve et al. | 2013 | https://doi.org/10.1371/journal.pcbi.1003285 | Keep scripts, seeds and versions so every number can be reproduced. | Open access | verified |
| S-COM-4 | Good enough practices in scientific computing | Greg Wilson et al. | 2017 | https://doi.org/10.1371/journal.pcbi.1005510 | A small set of habits: raw data untouched, scripts, project layout, notes. | Open access | verified |
| S-COM-5 | Communicating uncertainty about facts, numbers and science | Anne Marthe van der Bles et al. | 2019 | https://doi.org/10.1098/rsos.181870 | How to say how sure we are without losing the reader. | Open access | verified |

## Product and game analytics

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-GAM-1 | Game Analytics: Maximizing the Value of Player Data | Magy Seif El-Nasr, Anders Drachen, Alessandro Canossa (eds.) | 2013 | https://link.springer.com/book/10.1007/978-1-4471-4769-5 | Reference on telemetry, retention, monetisation and player behaviour analysis in games. | Book (paid) | unverified |
| S-GAM-2 | Probability models for customer-base analysis | Peter Fader, Bruce Hardie | 2009 | https://doi.org/10.1016/j.intmar.2008.09.003 | Customer lifetime value and repeat purchase models and their assumptions. | Paywalled; abstract free | unverified |
| S-GAM-3 | Unity Analytics documentation | Unity Technologies | ongoing | https://docs.unity.com/ugs/en-us/manual/analytics/manual/overview | What events Unity records and how its retention and funnel views are defined. | Free to read; licence unverified | verified |
| S-GAM-4 | GameAnalytics documentation | GameAnalytics | ongoing | https://docs.gameanalytics.com/ | Event types and standard metrics (DAU, retention, ARPDAU) for games. | Free to read; licence unverified | verified |
| S-GAM-5 | Predicting Player Churn in the Wild | Fabian Hadiji et al. | 2014 | https://ieeexplore.ieee.org/document/6932876 | Churn prediction in free-to-play games and how the churn label is defined. | Paywalled; abstract free | unverified |

## Privacy and responsible use

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-PRI-1 | NIST Privacy Framework | NIST | 2020 | https://www.nist.gov/privacy-framework | A risk-based way to think about personal data in analysis. | Public domain | verified |
| S-PRI-2 | k-Anonymity: A Model for Protecting Privacy | Latanya Sweeney | 2002 | https://doi.org/10.1142/S0218488502001648 | Why small groups in a table can identify people; aggregate before showing. | Paywalled; abstract free | verified |
| S-PRI-3 | Robust De-anonymization of Large Sparse Datasets | Arvind Narayanan, Vitaly Shmatikov | 2008 | https://arxiv.org/abs/cs/0610105 | Evidence that removing names does not make data anonymous. | Free (arXiv) | verified |
| S-PRI-4 | The Algorithmic Foundations of Differential Privacy | Cynthia Dwork, Aaron Roth | 2014 | https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf | The formal idea of limiting what any released statistic reveals about one person. | Free PDF | unverified |
| S-PRI-5 | Regulation (EU) 2016/679 (General Data Protection Regulation) | European Union | 2016 | https://eur-lex.europa.eu/eli/reg/2016/679/oj | The text behind personal-data rules; the role flags these topics and never gives legal advice. | Public law text | unverified |
| S-PRI-6 | Fairness and Machine Learning: Limitations and Opportunities | Solon Barocas, Moritz Hardt, Arvind Narayanan | 2023 | https://fairmlbook.org/ | How models can treat groups unequally even when the data looks neutral. | Free online | verified |

## Tools and documentation

| ID | Title | Author | Year | URL | Use | Cost/licence | Status |
|---|---|---|---|---|---|---|---|
| S-TOOL-1 | pandas documentation | pandas developers | ongoing | https://pandas.pydata.org/docs/ | Reference for tables, grouping, time series and IO. | BSD licence docs | verified |
| S-TOOL-2 | NumPy documentation | NumPy developers | ongoing | https://numpy.org/doc/stable/ | Reference for arrays and random numbers (seeding). | BSD licence docs | verified |
| S-TOOL-3 | SciPy statistics reference (scipy.stats) | SciPy developers | ongoing | https://docs.scipy.org/doc/scipy/reference/stats.html | Tests, distributions and bootstrap functions with their assumptions. | BSD licence docs | verified |
| S-TOOL-4 | statsmodels documentation | statsmodels developers | ongoing | https://www.statsmodels.org/stable/ | Regression, GLMs, tests and power calculations. | BSD licence docs | verified |
| S-TOOL-5 | statistics: Mathematical statistics functions (Python standard library) | Python Software Foundation | ongoing | https://docs.python.org/3/library/statistics.html | What can be done with the standard library alone when nothing else is installed. | PSF licence docs | verified |
| S-TOOL-6 | csv: CSV File Reading and Writing (Python standard library) | Python Software Foundation | ongoing | https://docs.python.org/3/library/csv.html | Reading data safely with the standard library. | PSF licence docs | verified |
