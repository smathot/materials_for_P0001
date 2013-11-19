# Results

## The PLR is affected by pre-saccadic target luminance

The main results are shown in %FigMain::a, in which the difference in pupil size between Land-on-Bright and Land-on-Dark trials is plotted over time. The PLR, which is a relative constriction in Land-on-Bight trial and shown as a negativity in the figure, is present in all conditions.

Our analyses focus on the differential response, because the absolute shape of the pupillary response differs depends on various factor which are not, or may not, be identical between conditions [for reviews see @Laeng2012Window;@Loewenfeld1958] . Notably, there is an overall constriction in the Swap and Onset conditions (%FigMain::c,d), which is not present in the Constant condition (%FigMain::b). This constriction is due to the visual change that occurred in the Swap and Onset conditions [@Barbur1992], that is, the luminosity change that occurred during the eye movement. However, visual change is identical across Land-on-Bright and Land-on-Dark trials, and the differential responses (%FigMain::a) are therefore not distorted by visual-change-induced constriction.

First, we determined at which points in time there was a significant difference in pupil size between Land-on-Bright and Land-on-Dark trials. To this end, we conducted a linear mixed-effects (LME) analysis with participant as random effect, target luminance (Land-on-Dark or Land-on-Bright) as fixed effect, and pupil size as dependent measure. This analysis was performed separately for each time point and condition. Markov chain Monte Carlo (MCMC) simulation was used to estimate p values and 95% confidence intervals [@Baayen2008Mixed]. We considered divergence between Land-on-Dark and Land-on-Bright trials significant when p < .05 for at least 200 consecutive samples [cf. @Math2013Plos].

The anticipatory nature of the PLR was evident in two main ways. Firstly, as predicted, divergence occurred much earlier in the Constant condition (divergence from 58 ms - trial end) than in the Onset condition (292 ms - trial end). Since the latency of the PLR is at least 250 ms [@Ellis1981], the fact that pupil size is modulated already 58 ms after saccade detection, corresponding to 30 ms after saccade offset (see [Saccade detection]), is clear evidence for anticipation.

Secondly, in the Swap condition there was initially an 'inverse PLR' (46 - 411 ms). This reflects a response to the brightness of the target as it was before saccade onset, before the polarity of the luminance had changed (%FigParadigm::b). Strikingly, the (inverse of the) Swap condition was indistinguishable from the Constant condition until 250 ms after the eye movement (compare the dotted-orange and green lines in %FigMain::a). This suggests that it takes 250 ms for the pupil to respond to post-saccadic brightness of the target, consistent estimates of the latency of the PLR [e.g., @Ellis1981]. A 'normal' PLR to the post-saccadic brightness of the target arose later in time (464 ms - trial end), and from about 600 ms onwards the Swap condition was indistinguishable from the Onset condition (compare the solid-orange and red lines in %FigMain::a). Crucially, the results from th Swap condition show that when you prepare an eye movement towards a bright stimulus, a PLR may be partly elicited even when the bright stimulus is never actually brought into central vision.

%--
figure:
 id: FigMain
 source: FigMain.svg
 caption:
  a) The difference in pupil size between Land-on-Bright and Land-on-Dark trials over time for the three experimental conditions. The Inverse-swap condition (orange dotted line) is identical, but inverse to the Swap condition (orange solid line). b, c, d) Pupil size on Land-on-Dark and Land-on-Bright trials over time for the Constant (b), Swap (c), and Onset (d) condition. Line widths indicate 95% confidence intervals, such that non-overlapping lines correspond to p < .05. Gray shadings indicate significant divergence between Land-on-Dark and Land-on-Bright trials. Saccade onset is indicated by the green vertical lines. Saccade offset is indicated by the red vertical lines. The display change (a dummy change in the Constant condition) occurred at time 0, indicated by the dashed vertical line.
--%

## Modeling the PLR using exponential decay

In order to characterize the difference between Constant and Onset trials in more detail, we modeled the shape of the PLR using an exponential-decay function. This modeling approach complements the LME analyses described above in two ways. Firstly, by inspecting the model's parameters we can gain insight into the how the conditions differ qualitatively. Secondly, modeling would expose 'trivial' differences, notably differences in noise level between conditions, which could have affected the significance levels of the LME analyses.

In general, the PLR is characterized by an initial latency period, followed by a rapid constriction or dilation, which gradually slows down as the pupil approaches its new resting size. This response function is similar for responses to light and darkness (although the darkness response is generally less pronounced), as well as the differential response to light and darkness, which is what we model here (%FigMain::a). Because the Onset condition is a combination of two opposite responses (to the pre- and post-saccadic brightness of the target, see %FigMain::c), we model only the Constant and Onset conditions.

In a pilot study, we compared a number of decay functions, and found that several functions fit the PLR very well given the right parameters. Here we use an exponential decay function, adapted from @HoeksLevel1993, because it has parameters with a clear interpretation (see %FigExp): Response latency (`t0`), initial pupil size (`p1`), final pupil size (`p2`), and response speed (the inverse of `s`).

%--
figure:
 id: FigExp
 source: FigExp.svg
 caption: "The exponential-decay function used to model the pupillary light response. This function models pupil size (`p(t)`) over time (`t`) and has four free parameters: response latency (`t0`), initial pupil size (`p1`), final pupil size (`p2`), and response speed (the inverse of `s`)."
--%

For each participant separately, we determined the model parameters for the average responses in the Constant and Onset conditions (%FigFit). Next, we used paired-samples *t* tests to test for differences between model parameters, using a Bonferroni-corrected alpha level of .0125 (= .05 / 4 comparisons).

%--
figure:
 id: FigFit
 source: FigFit.svg
 caption: Observed difference between Land-on-Bright and Land-on-Dark trials (solid lines) and model fits (dotted lines) for the Constant and Onset conditions. Vertical dashed lines indicate response latencies (`t0`). The large pane depicts the grand average response. Small panes correspond to individual participants.
--%

Firstly and most importantly, the latency (`t0`) of the PLR was 107 ms lower on Constant trials (M = 268, SE = 16.0) than on Onset trials (M = 375, SE = 16.6, t(7) = 9.33, p < 0.0001). In addition, initial pupil size (`p1`) was slightly smaller on Constant (M = -0.0110, SE = 0.0038) than on Onset trials (M = -0.0004, SE = 0.0032, t(7) = 4.17, p = .0042), as was final pupil size (`p2`; Constant: M = -0.2542, SE = 0.0236; Onset: M = -0.2187, SE = 0.0268; t(7) = 3.56, p = .0093). Response speed is slightly higher (i.e. a lower `s`) in the Constant condition (M = 491.3, SE = 79.64) than in the Onset condition (M = 623.5, SE = 83.96), but this difference is not significant (t(7) = 2.295, p = .0554).

In sum, the results from the model fits corroborate and extend those from the LME analyses. Most importantly, the latency of the PLR is reduced by 107 ms compared to the Onset condition. In addition, in the Constant there is a small bias in pupil size already before the onset of the PLR proper.

## The the PLR is locked to saccade onset

To test whether the PLR is locked to the presentation of the auditory cue or the onset of the saccadic response, we divided trials into ten bins, separately for each participant, based on saccadic response time. Next, we determined the latency of the PLR (`t0`) for the Constant and Onset conditions for each bin, as described under [Modeling].

%--
figure:
 id: FigLatency
 source: FigLatency.svg
 caption: Response latency `t0` as a function of saccadic reaction time (SRT) for the Constant and Onset conditions. The response latency is about 100 ms lower in the Constant than in the Onset condition, and does not reliably depend on SRT.
--%

As shown in %FigLatency, the latency reduction of the PLR in the Constant condition relative to the Onset condition was around 100 ms independent of saccadic response time, indicating that the PLR was locked to saccade onset. This was confirmed by a Repeated Measures Analysis of Variance (ANOVA) with Bin (10 levels) and Condition (Constant; Onset) as within-subject factors and `t0` as dependent variable. This revealed a main effect of Condition (F(1, 7) = 106.12, p < .0001), reflecting an overall latency reduction, but no main effect of Bin (F(9, 7) = 1.21, p = .3056), nor a Condition by Bin interaction (F(9,9) = 0.30, p = .9726).

## Accounting for bias due to fixational eye movements

When you attend to a stimulus without looking directly at it (i.e. covert attention), small fixational eye movements tend to gravitate towards the attended stimulus [@Engbert2003]. Since every saccadic eye movement is preceded by a covert shift of attention [e.g., @Deubel1996Common], one might expect that fixational eye movements bring the eyes closer to the saccade target already before the actual saccade is executed.

In our data, gaze position was indeed biased towards the saccade target from 242 ms before the onset saccade, as determined using an LME analysis with Participant as random effect, Target Side (Left or Right) as fixed effect, and Horizontal Gaze Position as dependent measure. This bias gradually increased to 0.03° just before the onset of the saccade. Although this bias was extremely small, we nevertheless verified that it did not affect our results. First we discarded all trials in which gaze position was biased towards the saccade target (51.6%). This left a subset of data in which gaze was biased slightly away from the saccade target (0.3°). All analyses described above were repeated on this subset of data.

Compared to the main analysis, there were only two differences: When estimating the fit parameters, there was no longer a difference in final pupil size (`p2`, t(7) = 0.7120, p = 0.4995), and the difference in initial pupil size (`p1`) was no longer significant using our Bonferroni-corrected alpha level of .0125 (t(7) = 2.537, p = .0387). Other than that, there were no notable differences between the full dataset and this subset of the data. This illustrates that our results are not due to a gaze-position bias prior to the eye movement.