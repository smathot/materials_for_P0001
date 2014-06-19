---
title:
 "Supplement to: The Pupillary Light Response Reflects Eye-movement Preparation"
author:
  Sebastiaan Mathôt, Lotje van der Linden, Jonathan Grainger, and Françoise Vitu
affiliation:
 - Aix-Marseille University, CNRS, LPC UMR 7290, Marseille, France
correspondence:
 - Aix-Marseille University, CNRS
 - Laboratoire de Psychologie Cognitive, UMR 7290
 - 3 Place Victor Hugo
 - Centre St. Charles, Bâtiment 9, Case D
 - 13331 Marseille
 - France
authornote: |
 SM, JG, and FV were supported by ERC grant 230313 (<http://erc.europa.eu/>). LvdL was supported by a grant ('allocation de recherche') from the French ministry of research (2012–2015). The funders had no role in study design, data collection and analysis, decision to publish, or preparation of the manuscript. The authors declare no competing financial interests.
---


This supplement contains additional analyses to accompany the manuscript *The Pupillary Light Response Reflects Eye-movement Preparation*. All resources related to this manuscript (scripts, data, etc.) can be obtained from: <https://github.com/smathot/materials_for_P0001>.

# Overview

%--
toc:
 mindepth: 1
 exclude: [Overview]
--%

# The PLR is locked to saccade onset

An important question is whether the latency of the PLR is locked to the presentation of the auditory cue, or to the onset of saccadic response. If the PLR was locked to the cue, this would suggest that it is a high-level effect that results from an endogenous shift of attention towards the cued side [cf. @Binda2013Bright;@Mathôt2013Plos;@Naber2013Tracking]. In contrast, if the PLR was locked to the saccadic response, this would suggest that it is a low-level, motoric effect that is linked to the execution of the eye movement, similar to the pre-saccadic shift of attention [@Deubel1996Common; @Kowler1995;@Hoffman1995].

To test this, we divided trials into ten bins, separately for each participant, based on saccadic response time (SRT). Next, we determined the latency of the PLR (`t0`) for the Constant and Onset conditions for each bin, as described in the main text (*Modeling the PLR using exponential decay*).

%--
figure:
 id: FigLatency
 source: FigLatency.svg
 caption: Latency of the PLR (`t0`) as a function of saccadic reaction time (SRT) for the Constant and Onset conditions. Regardless of SRT, response latency is about 100 ms lower in the Constant than in the Onset condition.
--%

As shown in %FigLatency, the latency reduction of the PLR in the Constant condition relative to the Onset condition was around 100 ms independent of SRT, indicating that the PLR was locked to saccade onset, and not to the presentation of the auditory cue. This was confirmed by a Repeated Measures Analysis of Variance (ANOVA) with Bin (10 levels) and Condition (Constant; Onset) as within-subject factors and `t0` as dependent variable. This revealed a main effect of Condition (F(1, 7) = 106.12, p < .0001), reflecting an overall latency reduction, but no main effect of Bin (F(9, 7) = 1.21, p = .3056), nor a Condition by Bin interaction (F(9,9) = 0.30, p = .9726).

# Accounting for gaze bias due to fixational eye movements

When you attend to a stimulus without looking directly at it (i.e. covert attention), small fixational eye movements tend to gravitate towards the attended stimulus [@Engbert2003]. Since every saccadic eye movement is preceded by a covert shift of attention [e.g., @Deubel1996Common], one might expect that fixational eye movements bring the eyes slightly closer to the saccade target already before the eyes set in motion.

In our data, gaze position was indeed biased towards the saccade target from 242 ms before saccade onset, as determined using an LME analysis with Participant as random effect, Target Side (Left or Right) as fixed effect, and Horizontal Gaze Position as dependent measure. This bias gradually increased to 0.03° just before the onset of the saccade. Although this bias was extremely small, we nevertheless verified that it did not affect our results. First we discarded all trials in which gaze position was, on average, biased towards the saccade target (51.6%). This left a subset of data in which gaze was biased slightly away from the saccade target (0.3°). All analyses described above were repeated on this subset of data.

__NEW: Based on pair-wise matching using a 1px maximum error, 17.45% is discarded.__

Compared to the main analyses (described in the main text), there were only two minor differences: When estimating the model parameters, there was no longer a difference in final pupil-size difference between the Constant and Onset conditions (`p2`; t(7) = 0.7120, p = 0.4995), and the difference in initial the pupil-size bias (`p1`) was no longer significant using our Bonferroni-corrected alpha level of .0125 (t(7) = 2.537, p = .0387). Other than that, there were no notable differences between the full dataset and this subset of the data. Crucially, this illustrates that our results are not due to a gaze-position bias prior to the eye movement, and demonstrates the robustness of the results.

# Saccadic landing positions

As shown in %FigEndPoints and %TblEndPoints saccades were, on average, quite accurate, with a slight undershoot, but without any discernible difference between conditions.

%--
figure:
 id: FigEndPoints
 source: FigEndPoints.svg
 caption: |
  Saccadic landing positions as a function of Condition and Landing Luminance. Dots correspond to landing positions on individual trials. The intersections of the dotted lines correspond to the positions of the leftwards saccade target, the fixation dot, and the rightwards saccade target. Each plot represents a full display. Units are in pixels.
--%

%--
table:
 id: TblEndPoints
 source: TblEndPoints.csv
 caption: |
  Saccadic landing positions as a function Condition, Landing Luminance, and Saccade Direction. Units are in visual degrees relative to the display center.
--%
