## Materials and availability

Experimental scripts, participant data, analysis scripts, and supplementary control analyses are available from the first author's website, or from <https://github.com/smathot/data_repository>.

## Participants and ethics statement

Eight observers (six naive participants and two authors; seven women; age range 20-30 years) participated in the experiment. Participants were recruited through the participant pool of Aix-Marseille Université (AMU), and provided written informed consent. The experiment was conducted with approval of the local ethics committee of AMU, and was in accordance with the 2013 Declaration of Helsinki (<http://www.wma.net/en/30publications/10policies/b3/>), except for point 35, which requires pre-registration of studies involving human participants.

## Software and apparatus

The right eye was recorded with an EyeLink 1000 (SR Research, Mississauga, Canada, ON), a video-based eye tracker sampling at 1000 Hz. Stimuli were presented on a 21" CRT monitor (1024 x 768 px, 100 Hz). Stimulus were presented with OpenSesame [@MathSchreij2012] using the PsychoPy back-end [@Peirce2007].

## Stimuli, task, and design

Before the experiment, a nine-point eye-tracker calibration was performed. Before each trial, a single-point re-calibration was performed ('drift correction').

%--
figure:
 id: FigParadigm
 source: FigParadigm.svg
 caption: Schematic experimental paradigm. a) An example of a Land-on-Dark Constant trial, in which the pupil prepares for, and lands on, a dark target background. b) An example of a Land-on-Dark Swap trial. in which the pupil prepares for brightness, but lands on darkness. c) An example of a Land-on-Dark Onset trial, in which the pupil prepares for no luminance change, but lands on darkness. The display change occurred as soon as the onset of a saccade was detected.
--%

Each trial started with the presentation of three dim green dots (14.7 cd/m^2^; 0.1°), presented at the display center and 10.00° degrees to the right and left of the center (see %FigParadigm). Participants fixated on the central dot. In the Constant and Swap conditions, the background was divided into a bright (88.5 cd/m^2^) and a dark (0.2 cd/m^2^) half, separated by a central luminance-gradient band (10.0° wide). In the Onset condition, the background was uniformly gray (20.8 cd/m^2^). After 3 s, a voice saying *gauche* (left) or *droite* (right) was played back through a set of speakers, instructing participants to make a saccade to the left or right dot. Saccades were detected on-line as the moment at which horizontal gaze position deviated more than 2.9° from the central dot for at least two consecutive gaze samples. (For analysis and verification we used an off-line detection algorithm, described under [Off-line saccade detection].)

As soon as a saccade was detected on-line, one of three things could happen. In the Constant condition, the display did not change at all (%FigParadigm::a). Therefore, pre-saccadic preparation of the PLR should result in a reduction of the PLR latency. In the Swap condition, the dark side of the screen turned bright and vice versa (%FigParadigm::b). Therefore, pre-saccadic preparation should result in a brief 'inverse' PLR, reflecting the PLR's preparatory component. In the Onset condition, the gray display was divided into a bright and a dark half (%FigParadigm::c). In this condition, there could be no pre-saccadic preparation of the PLR, because the central dot and the saccade target were (initially) on the same gray background. The trial ended 3 s after a saccade was detected.

In sum, we used a fully crossed 2 x 3 design. The first factor, Landing Luminance (Land on Bright or Land on Dark), corresponded to the post-saccadic luminance of the target background. The second factor was Condition (Constant, Swap, or Onset). Both factors were randomly mixed within blocks. Saccade direction (Left or Right) was fully randomized. The experiment consisted of 360 trials across 10 blocks, and lasted approximately 90 minutes.

## Pupil-trace analysis

Each trial was divided into three epochs: the baseline epoch, spanning the 100 ms prior to the presentation of the auditory cue; the pre-saccade epoch, from the cue until the detection of the saccade; and the post-saccade epoch, from the detection of the saccade until the end of the trial. We analyzed pupil surface relative to the mean pupil size during the baseline epoch [cf. @Mathôt2013Plos]. Missing data during blinks was reconstructed, where possible, using cubic-spline interpolation [@Math2013Blinks]. No signal smoothing was applied.

## Trial-exclusion criteria

Trials were excluded based on the following criteria: A saccade was executed in the wrong direction or before the cue was presented (8.4%); Saccade latency was less than 50 ms or more than 2000 ms (0.5%); The display change did not occur during the saccade, as determined by off-line verification of saccade detection (4.9%; See [Off-line saccade detection]); Blinks occurred and could not be reconstructed (4.5%, see [Pupil-trace analysis]). After exclusion, 2350 trials (81.4%) remained for further analysis.

## Off-line saccade detection

For the analysis, we used the EyeLink saccade-detection algorithm (velocity threshold: 35 °/s; acceleration threshold: 9500 °/s^2^). For each trial, we considered the first saccade that was larger than 1.8°. Saccades were executed on average 543.6 ms (SD = 187.4) after the cue, with considerable variation between participants (409 - 789 ms; participant means). The relatively high saccade latencies are presumably due to the instruction's emphasis on accuracy, the low saliency of the saccade target, and the use of an endogenous auditory cue.

Immediately after the display change, a trigger was sent to the eye tracker to allow off-line verification of timing. This showed that the display change occurred exactly in the middle of the saccade, 27.09 ms (SD = 3.906) after saccade onset and 27.55 ms (SD = 7.852) before saccade offset. The average saccade duration was 54.63 ms (SD = 7.407). All trials in which the display change did not occur during the saccade were discarded (see also [Trial-exclusion criteria]).
