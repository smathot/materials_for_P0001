## The PLR is affected by the luminance of the pre-saccadic target background

The main results are shown in %FigMain::a, in which the difference in pupil size between Land-on-Bright and Land-on-Dark trials is plotted over time. The PLR, which is a relative constriction on Land-on-Bight trials and shown as a negativity in the figure, is present in all conditions.

%--
figure:
 id: FigMain
 source: FigMain.svg
 caption:
  a) Mean difference in pupil size between Land-on-Bright and Land-on-Dark trials for the three conditions (solid lines) as a function of time relative to display change. The PLR is shown as a negativity. The red dotted line shows the inverse of the Swap condition, and is shown for comparison with the Constant condition. b, c, d) Mean pupil size on Land-on-Dark and Land-on-Bright trials over time for the Constant (b), Swap (c), and Onset (d) conditions. The PLR is shown as a decreased pupil size on Land-on-Bright trials, relative to Land-on-Dark trials. Line widths indicate 95% confidence intervals, such that non-overlapping lines correspond to p < .05. Gray background shadings indicate significant (p < .05) divergence between Land-on-Dark and Land-on-Bright trials for at least 200 consecutive samples. a, b, c, d) The vertical dotted lines correspond to mean saccade onset (left-most) and offset (right-most). The surrounding shadings indicate the full range of observed values. The display change (or a dummy change in the Constant condition) occurred at time 0, indicated by the dashed vertical line.
--%

To determine at which points in time there was a significant difference in pupil size between Land-on-Bright and Land-on-Dark trials we conducted linear mixed-effects (LME) analyses with Participant as random effect, Target Luminance (post-saccadic; Land-on-Dark or Land-on-Bright) as fixed effect, and Pupil Size as dependent measure. This analysis was performed separately for each time point and condition. Markov chain Monte Carlo (MCMC) simulation was used to estimate *p* values and 95% confidence intervals [@Baayen2008Mixed]. We considered divergence between Land-on-Dark and Land-on-Bright trials to be significant when p < .05 for at least 200 consecutive samples [cf. @Mathôt2013Plos].

Preparation of the PLR was evident in two main ways. Firstly, divergence occurred much earlier in the Constant condition (from 58 ms after saccade detection until trial end) than in the Onset condition (292 ms - trial end). Since the latency of the PLR is at least 250 ms [@Ellis1981], this extremely rapid modulation of pupil size, which occurs already 30 ms after saccade offset (≈ 58 ms after saccade-detection, see [Off-line saccade detection]), clearly shows that a PLR was prepared before the saccade was initiated.

Secondly, in the Swap condition there was initially an 'inverse PLR', again arising very rapidly (46 - 411 ms). This reflects a preparatory response to the pre-saccadic brightness of the target background, before the display had changed (%FigParadigm::b). Strikingly, the (inverse of the) Swap condition was indistinguishable from the Constant condition until about 250 ms after the saccade (compare the dotted-red and green lines in %FigMain::a). This suggests that it takes about 250 ms for the pupil to respond to the post-saccadic luminance, which is roughly consistent with the latency of the PLR in the Onset condition (292 ms, see above) as well as previous estimates of the PLR latency [e.g., @Ellis1981]. From about 600 ms onwards the Swap condition was indistinguishable from the Onset condition (compare the solid-red and blue lines in %FigMain::a), suggesting that by this time the preparatory component of the PLR had fully dissipated. Crucially, the results from the Swap condition show that when you prepare an eye movement towards a stimulus on a bright (or dark) background, a preparatory PLR is (partly) elicited even when the prepared-for luminance is changed before being brought into central vision.

## Modeling the PLR using exponential decay

In order to further characterize the difference between Constant and Onset trials, we modeled the shape of the PLR using an exponential-decay function. This modeling approach complements the LME analysis described above in two important ways.

Firstly, the LME analysis simply takes the first point in time at which there is significant divergence between Land-on-bright and Land-on-Dark trials as the onset of the PLR. However, a visual inspection of %FigMain::a suggests that preparation does not merely reduce the latency of the PLR, but qualitatively alters the shape of the PLR. More specifically, if preparation was possible (i.e. in the Onset condition), the PLR appeared to consist of a small initial bias, followed later by a much larger response, which we will call the 'full PLR' from now on. An important question is whether the effect of preparation is limited to this initial bias, or whether the latency of the full PLR is reduced as well.

Secondly, modeling exposes trivial differences between conditions, notably differences in noise level and response size. This is important, because larger and less noisy responses may seem to occur earlier when using significance testing (e.g., LME).

In a pilot study, we compared a number of decay functions and found that, given the right parameters, several functions fit the PLR (and the difference in pupil size between Land-on-Bright and Land-on-Dark trials, which we model here) very well. Here we chose an exponential-decay function, adapted from @HoeksLevelt1993, which models the difference in pupil size between Land-on-Bright and Land-on-Dark trials (`p(t)`) as a function of time since display change (`t`; see %FigExp). The advantage of exponential-decay, over other functions that we considered, is that its parameters have clear interpretations: full PLR latency (`t0`), initial pupil-size difference (`p1`), final pupil-size difference (`p2`), and response speed (the inverse of `s`). Because the Swap condition is a combination of two opposite responses (to the pre- and post-saccadic brightness of the target, see %FigMain::c), it is not properly modeled by exponential decay. Therefore, we model only the Constant and Onset conditions.

%--
figure:
 id: FigExp
 source: FigExp.svg
 caption: "The exponential-decay function used to model the difference in pupil-size between Land-on-Bright and Land-on-Dark trials (`p(t)`) as a function of time since display change (`t`). This function has four free parameters: full PLR latency (`t0`), initial pupil-size difference (`p1`), final pupil-size difference (`p2`), and response speed (the inverse of `s`)."
--%

For each participant separately, we determined the model parameters for the mean difference response in the Constant and Onset conditions (%FigFit). Next, we used paired-samples *t* tests to test for differences between model parameters, using a Bonferroni-corrected alpha level of .0125 (= .05 / 4 comparisons).

%--
figure:
 id: FigFit
 source: FigFit.svg
 caption: Observed difference in pupil size between Land-on-Bright and Land-on-Dark trials (solid lines) and model fits (dotted lines) for the Constant and Onset conditions. Vertical dashed lines indicate full PLR latencies (`t0`). The left pane depicts the grand mean response. The eight rightwards panes show the mean responses for each of the eight participants.
--%

Firstly and most importantly, full PLR latency (`t0`) was 107 ms lower on Constant trials (M = 268, SE = 16.0) than on Onset trials (M = 375, SE = 16.6, t(7) = 9.33, p < 0.0001). In addition, initial pupil-size difference (`p1`) was slightly smaller (i.e. more negative) on Constant (M = -0.0110, SE = 0.0038) than on Onset trials (M = -0.0004, SE = 0.0032, t(7) = 4.17, p = .0042), as was final pupil-size difference (`p2`; Constant: M = -0.2542, SE = 0.0236; Onset: M = -0.2187, SE = 0.0268; t(7) = 3.56, p = .0093). Response speed was slightly higher (i.e. a lower `s`) in the Constant condition (M = 491.3, SE = 79.64) than in the Onset condition (M = 623.5, SE = 83.96), but this difference was not significant (t(7) = 2.295, p = .0554).

In sum, the exponential-decay model allowed us to disentangle the initial bias in the PLR (`p1`), which is only observed when preparation is possible (i.e. in the Constant condition), from the full PLR, which has a reduced latency (`t0`) when preparation is possible (i.e. in the Constant condition relative to the Onset condition). This corroborates and extends the LME analysis, which did not distinguish between these two different components of the preparatory PLR.
