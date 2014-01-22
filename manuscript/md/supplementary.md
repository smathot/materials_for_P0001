# Supplementary methods

## The PLR is locked to saccade onset

An important question is whether the latency of the PLR (`t0`)  is locked to the presentation of the auditory cue, or to the onset of saccadic response. If the PLR was locked to the cue, this would suggest that it is a high-level effect that results from an endogenous shift of attention towards the cued side [cf. @Binda2013Bright;@Mathôt2013Plos;@Naber2013Tracking]. In contrast, if the PLR was locked to the saccadic response, this would suggest that it is a low-level, motoric effect that is linked to the execution of the eye movement, similar to the pre-saccadic shift of attention [@Deubel1996Common; @Kowler1995;@Hoffman1995].

To test this, we divided trials into ten bins, separately for each participant, based on saccadic response time (SRT). Next, we determined the latency of the PLR (`t0`) for the Constant and Onset conditions for each bin, as described under [Modeling the PLR using exponential decay].

%--
figure:
 id: FigLatency
 source: FigLatency.svg
 caption: Latency of the PLR (`t0`) as a function of saccadic reaction time (SRT) for the Constant and Onset conditions. Regardless of SRT, response latency is about 100 ms lower in the Constant than in the Onset condition.
--%

As shown in %FigLatency, the latency reduction of the PLR in the Constant condition relative to the Onset condition was around 100 ms independent of SRT, indicating that the PLR was locked to saccade onset, and not to the presentation of the auditory cue. This was confirmed by a Repeated Measures Analysis of Variance (ANOVA) with Bin (10 levels) and Condition (Constant; Onset) as within-subject factors and `t0` as dependent variable. This revealed a main effect of Condition (F(1, 7) = 106.12, p < .0001), reflecting an overall latency reduction, but no main effect of Bin (F(9, 7) = 1.21, p = .3056), nor a Condition by Bin interaction (F(9,9) = 0.30, p = .9726).
 
## Visual-change-induced constriction

Our analyses focus on the difference between Land-on-Bright and Land-on-Dark trials, because the absolute shape of the pupillary response differs between conditions. More specifically, there is an overall constriction in the Swap and Onset conditions (%FigMain::c,d), which is not present in the Constant condition (%FigMain::b). This constriction is due to the intra-saccadic display change that occurred in the Swap and Onset conditions [@Barbur1992]. However, an identical visual change occurred in Land-on-Bright and Land-on-Dark trials, and we therefore assume that the difference between Land-on-Bright and Land-on-Dark trials (%FigMain::a) is not distorted by visual-change-induced constriction. Crucially, however, our main conclusions are not dependent on this assumption, because the latency of visual-change induced constriction is too high [somewhat higher than the PLR itself; @Gamlin1998] to account for the very early preparatory effects that we observe here. 

## Accounting for gaze bias due to fixational eye movements

When you attend to a stimulus without looking directly at it (i.e. covert attention), small fixational eye movements tend to gravitate towards the attended stimulus [@Engbert2003]. Since every saccadic eye movement is preceded by a covert shift of attention [e.g., @Deubel1996Common], one might expect that fixational eye movements bring the eyes slightly closer to the saccade target already before the eyes set in motion.

In our data, gaze position was indeed biased towards the saccade target from 242 ms before saccade onset, as determined using an LME analysis with Participant as random effect, Target Side (Left or Right) as fixed effect, and Horizontal Gaze Position as dependent measure. This bias gradually increased to 0.03° just before the onset of the saccade. Although this bias was extremely small, we nevertheless verified that it did not affect our results. First we discarded all trials in which gaze position was, on average, biased towards the saccade target (51.6%). This left a subset of data in which gaze was biased slightly away from the saccade target (0.3°). All analyses described above were repeated on this subset of data.

Compared to the main analyses, there were only two minor differences: When estimating the model parameters, there was no longer a difference in final pupil-size difference between the Constant and Onset conditions (`p2`; t(7) = 0.7120, p = 0.4995), and the difference in initial the pupil-size bias (`p1`) was no longer significant using our Bonferroni-corrected alpha level of .0125 (t(7) = 2.537, p = .0387). Other than that, there were no notable differences between the full dataset and this subset of the data. Crucially, this illustrates that our results are not due to a gaze-position bias prior to the eye movement, and demonstrates the robustness of the results.
