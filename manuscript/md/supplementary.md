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

To test this, we divided trials into ten bins, separately for each participant, based on saccadic response time (SRT). Next, we determined the latency of the PLR (`t0`) for the Constant and Onset conditions for each bin, as described in the main text (*Modeling the PLR*).

%--
figure:
 id: FigLatency
 source: FigLatency.svg
 caption: Latency of the PLR (`t0`) as a function of saccadic reaction time (SRT) for the Constant and Onset conditions. Regardless of SRT, response latency is about 100 ms lower in the Constant than in the Onset condition.
--%

As shown in %FigLatency, the latency reduction of the PLR in the Constant condition relative to the Onset condition was around 100 ms independent of SRT, indicating that the PLR was locked to saccade onset, and not to the presentation of the auditory cue. This was confirmed by a Repeated Measures Analysis of Variance (ANOVA) with Bin (10 levels) and Condition (Constant; Onset) as within-subject factors and `t0` as dependent variable. This revealed a main effect of Condition (F(1, 7) = 106.12, p < .0001), reflecting an overall latency reduction, but no main effect of Bin (F(9, 7) = 1.21, p = .3056), nor a Condition by Bin interaction (F(9,9) = 0.30, p = .9726).

# A mixture model of the Onset condition

In the Swap condition, the preparatory component of the PLR is pitted against the 'regular' PLR that results from direct visual stimulation. The preparatory component of the Swap condition is shared with the Constant condition, whereas the regular component is shared with the Onset condition. Therefore, early after the display change, pupil size in the Swap condition should be predicted best by pupil size in the Constant condition. Later in time, the Swap condition should be predicted best by the Onset condition. To test this, we modeled the Swap condition as follows:

	Swap(t) = p(t) * -1 * Constant(t) + (1-p(t)) * Onset(t)

Here, `t` is time since display change, `Swap(t)`, `Constant(t)`, and `Onset(t)` are the difference in pupil size between Land-on-Bright and Land-on-Dark trials at time `t` in respectively the Swap, Constant, and Onset conditions. Finally, `p(t)` is the 'preparation index' at time `t`, which reflects whether the Swap condition is best predicted by the Constant condition (p > .5) or by the Onset condition (p < .5).

For every participant separately, we determined the point `t` at which `p(t)` dropped below .5 for at least 200 consecutive samples. This showed that the cross-over from a (predominantly) preparatory response to a (predominantly) regular response occurred 354 ms (SE = 14.7) after display change (see %FigSwapMixture).

%--
figure:
 id: FigSwapMixture
 source: FigSwapMixture.svg
 caption: |
  The preparation index (see text for definition) of the Swap condition, as a function of time since display change. Results across all participants.
--%

# Accounting for gaze bias prior to saccade onset

%FigAntiBiasMain and %FigAntiBiasFit show the core results after eliminating pre-saccadic gaze bias through a pairwise-matching algorithm. For details, see the main text.

%--
figure:
 id: FigAntiBiasMain
 source: FigAntiBiasMain.svg
 caption:
  Main results (cf. main-text Figure 2) after discarding 17.45% of trials to eliminate horizontal gaze-bias prior to saccade onset.
--%

%--
figure:
 id: FigAntiBiasFit
 source: FigAntiBiasFit.svg
 caption: |
  Modeling results (cf. main-text Figure 3) after discarding 17.45% of trials to eliminate horizontal gaze-bias prior to saccade onset.
--%
