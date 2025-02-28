# On efficiency and ease-of-understanding
## 6/18/2018
Right now, the code is "mostly" efficient (with one large issue), but very confusing to actually run.

### Efficiency issues
Right now that standard values are _not computed efficiently_ because we don't save the actual recommender system predictions. Instead we regenerate the predictions for each test. While we do batch quite a few tests at once, given memory constraints, it would be even faster to just _save the predictions_. In other words, for our boycott conditions, we should never need to train each recommender algorithm more than one time, ever. Similarly, saving predictions for other experiments would be helpful for deeper analysis of our results.



The whole data processing pipeline for the CSCW submission was quite manual.
It requires that a human specify carefully all the experiments, but then also make sure that the "no boycott standard results" are specified as well, and specified properly. There is room for human error here, e.g. if you forget an experiment it might not show up in the final results. Luckily we can check for this human error by inspecting the final results and looking for missing data points.

However, the organization of files is still quite confusing and there's a lot of potential confusing redundancy in the files, mainly due to the fact that each AWS spot instance is a full clone of the p
roject directory. For example, this means that the directories with standard results (currently in `rand_standards`) each have a copy of every `uid_sets` doc, even those these are unused. Future versions should clean out this redundant data to make human error harder.


## Things to double check
One important bit of code to double-check is that the boycott and like-boycott testing is implemented correctly.
i.e. make sure the like-boycott users are actually properly included in the training


# 7/19
Switched to using SVD with random state 0 to make it even more reproducible

# 7/20
Need to use joblib=0.11
https://github.com/joblib/joblib/issues/721

NOT TRUE
as long as you avoid memory error joblib 0.12 works, and it actually seems to be slightly better in terms of memory usage

# 7/23
Got a successful ml-20m AWS run
using 5 iterations with a m5.12xlarge
Took just over 2 hours. I did NOT save predictions for this run.


Dataset object is still taking way too much memory (or so it seems)
Consider this...
`Created dataframes 13.771659851074219
nonboycott.raw_ratings size 639977840
Created dataset objects 18.98782730102539`


# 7/29
AWS notes
for running 10 samples at once for ml-20m, r4.8xlarge works 100% of the time so far (i.e. never any memory error).
for ml-1m, trying out m5.4xlarge with 10 samples at once.
