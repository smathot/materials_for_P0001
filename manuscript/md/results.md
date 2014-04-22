## Pupil-trace analysis

Each trial was divided into three epochs: the baseline epoch, spanning the 100 ms prior to the presentation of the auditory cue; the pre-saccade epoch, from the cue until the detection of the saccade; and the post-saccade epoch, from the detection of the saccade until the end of the trial. We analyzed pupil surface relative to the mean pupil size during the baseline epoch [cf. @Mathôt2013Plos]. Missing data during blinks was reconstructed, where possible, using cubic-spline interpolation [@Math2013Blinks]. No signal smoothing was applied.

For the analysis, we used the EyeLink saccade-detection algorithm (velocity threshold: 35 °/s; acceleration threshold: 9500 °/s^2^), and considered the first saccade that was larger than 1.8°. Saccades were executed on average 543.6 ms (SD = 187.4) after the auditory cue. Off-line verification of timing, based on a trigger that was sent to the eye tracker immediately after the display change, showed that the display change occurred  27.09 ms (SD = 3.906) after saccade onset and 27.55 ms (SD = 7.852) before saccade offset. In other words, the display change fully occurred during the saccade, even allowing for the monitor's phosphor persistence [< 10 ms, @WangNikolic2011] and refresh cycle.

Trials were excluded when saccades were executed before the cue or in the wrong direction (8.4%), when saccade latency was less than 50 ms or more than 2000 ms (0.5%), when the display change did not occur during the saccade (4.9%; per off-line verification), or when blinks occurred and could not be reconstructed (4.5%). 2350 trials (81.4%) remained for further analysis.

## The effect of eye-movement preparation on the PLR

Pupil size depends on numerous factors, notably arousal [@Loewenfeld1958] and visual change [@BarburHarlowSahraie1992], but here we focus only on the effect of luminance (i.e. the PLR). The PLR is a relative constriction on Land-on-Bright trials and shown as a negativity in %FigMain::a.

%--
figure:
 id: FigMain
 source: FigMain.svg
 caption:
  a) Mean difference in pupil size between Land-on-Bright and Land-on-Dark trials for the three conditions as a function of time relative to display change. The PLR is shown as a negativity. The dotted line shows the inverse of the Swap condition, and is shown for comparison with the Constant condition. b, c, d) Mean pupil size on Land-on-Dark and Land-on-Bright trials over time for the Constant (b), Swap (c), and Onset (d) conditions. The PLR is shown as a decreased pupil size on Land-on-Bright trials, relative to Land-on-Dark trials. Line widths indicate 95% confidence intervals, such that non-overlapping lines correspond to p < .05. Background shadings indicate significant (p < .05) divergence between Land-on-Dark and Land-on-Bright trials for at least 200 consecutive samples. a, b, c, d) The vertical dotted lines correspond to mean saccade onset (left-most) and offset (right-most). The surrounding shadings indicate the full range of observed values. The display change (or a dummy change in the Constant condition) occurred at time 0, indicated by the dashed vertical line.
--%

To determine the earliest effects of luminance on pupil size, we conducted linear mixed-effects (LME) analyses with Participant as random effect, Target Luminance (post-saccadic; Land-on-Dark or Land-on-Bright) as fixed effect, and Pupil Size as dependent measure. This analysis was performed separately for each time point and condition. Markov chain Monte Carlo (MCMC) simulation was used to estimate *p* values and 95% confidence intervals [@Baayen2008Mixed]. We considered divergence between Land-on-Dark and Land-on-Bright trials to be significant when p < .05 for at least 200 consecutive samples [cf. @Mathôt2013Plos].

Eye-movement preparation affected the PLR in two main ways. Firstly, divergence occurred much earlier in the Constant condition (from 58 ms after display change until trial end) than in the Onset condition (292 ms - trial end). Since the latency of the PLR is at least 250 ms [@Ellis1981], this extremely rapid modulation of pupil size clearly shows that a PLR was prepared before saccade onset.

Secondly, in the Swap condition there was initially a (seemingly) inverse PLR, again arising very rapidly (46 - 411 ms). This reflects a preparatory response to the pre-saccadic brightness of the target background, before the display had changed (%FigParadigm::b). Strikingly, the (inverse of the) Swap condition was indistinguishable from the Constant condition until about 250 ms after the saccade (compare the dotted and solid lines in %FigMain::a). This suggests that it takes about 250 ms for the pupil to respond to the post-saccadic luminance, which is roughly consistent with the latency of the PLR in the Onset condition (292 ms, see above) as well as previous estimates of the PLR latency [e.g., @Ellis1981]. From about 600 ms onwards the Swap condition was indistinguishable from the Onset condition (compare the solid and dashed lines in %FigMain::a), suggesting that by this time the preparatory component of the PLR had fully dissipated. Crucially, the results from the Swap condition show that when you prepare an eye movement towards a stimulus on a bright (or dark) background, a preparatory PLR is (partly) elicited even when the luminance of the target background is changed before the target is brought into central vision.

## Modeling the PLR using exponential decay

A visual inspection of %FigMain::a suggests that preparation qualitatively alters the PLR's shape, rather than merely reduces its latency. More specifically, in the constant condition, the PLR appeared to consist of a small initial bias, followed later by a larger response, which we call the 'full PLR'. Through modeling, we can investigate whether the effect of preparation is limited to this initial bias, or whether the latency of the full PLR is reduced as well. In addition, modeling allows us to ascertain that the differences found with LME were not due to differences in noise level.

We chose an exponential-decay function, adapted from @HoeksLevelt1993, which models the difference in pupil size between Land-on-Bright and Land-on-Dark trials (`p(t)`) as a function of time since display change (`t`; see %FigExp).  There are several other functions that fit the PLR about equally well, but the advantage of exponential decay is that its parameters have clear interpretations: full PLR latency (`t0`), initial pupil-size difference (`p1`), final pupil-size difference (`p2`), and response speed (the inverse of `s`). Because the Swap condition is a combination of two opposite responses (to the pre- and post-saccadic brightness of the target, see %FigMain::c), it is not properly modeled in a way that allows for direct comparison with the other conditions. Therefore, we model only the Constant and Onset conditions.

%--
figure:
 id: FigExp
 source: FigExp.svg
 caption: "We used an exponential-decay function to model the difference in pupil-size between Land-on-Bright and Land-on-Dark trials (`p(t)`) as a function of time since display change (`t`). This function has four free parameters: full PLR latency (`t0`), initial pupil-size difference (`p1`), final pupil-size difference (`p2`), and response speed (the inverse of `s`)."
--%

For each participant separately, we determined the model parameters for the mean difference response in the Constant and Onset conditions (%FigFit). Next, we used paired-samples *t* tests to test for differences between model parameters, using a Bonferroni-corrected alpha level of .0125 (= .05 / 4 comparisons).

%--
figure:
 id: FigFit
 source: FigFit.svg
 caption: Observed difference in pupil size between Land-on-Bright and Land-on-Dark trials (solid and dashed lines) and model fits (dotted lines) for the Constant and Onset conditions. Vertical lines indicate full PLR latencies (`t0`) for the Constant (solid) and Onset (dashed) conditions. The left pane depicts the grand mean response. The eight rightward panes show the mean responses for each of the eight participants.
--%

Crucially, full PLR latency (`t0`) was 107 ms lower on Constant trials (M = 268, SE = 16.0) than on Onset trials (M = 375, SE = 16.6, t(7) = 9.33, p < 0.0001). In addition, initial pupil-size difference (`p1`) was slightly smaller (i.e. more negative) on Constant (M = -0.0110, SE = 0.0038) than on Onset trials (M = -0.0004, SE = 0.0032, t(7) = 4.17, p = .0042), as was final pupil-size difference (`p2`; Constant: M = -0.2542, SE = 0.0236; Onset: M = -0.2187, SE = 0.0268; t(7) = 3.56, p = .0093). Response speed was slightly higher (i.e. a lower `s`) in the Constant condition (M = 491.3, SE = 79.64) than in the Onset condition (M = 623.5, SE = 83.96), but this difference was not reliable (t(7) = 2.295, p = .0554).

In sum, the exponential-decay model confirms and extends the LME analyses by showing that preparation both induces an initial bias (`p1`) and reduces the latency of the PLR (`t0`).
