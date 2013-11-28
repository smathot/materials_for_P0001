# Methods

## Materials and availability

Experimental scripts, participant data, and analysis scripts are available from the first author's website, or from <https://github.com/smathot/data_repository>.

## Participants and ethics statement

Eight observers (six naive participants and two authors; seven women; age range 20-30 years) participated in the experiment. Participants were recruited through the participant pool of Aix-Marseille Université. All participants provided written informed consent. The experiment was conducted with approval of the local ethics committee of Aix-Marseille Université, and was in accordance with the declaration of Helsinki.

## Software and apparatus

The right eye was recorded with an EyeLink 1000 (SR Research, Mississauga, Canada, ON), a video-based eye tracker sampling at 1000 Hz. Stimuli were presented on a 21" CRT monitor (1024 x 768 px, 100 Hz). Stimulus presentation was controlled with OpenSesame [@MathSchreij2012] using the PsychoPy back-end [@Peirce2007].

## Procedure and stimuli

Before the experiment, a nine-point eye-tracker calibration was performed. Before each trial, a single-point re-calibration was performed ('drift correction').

Each trial started with the presentation of three dim green dots (14.7 cd/m^2^; 0.1°), presented at the display center and 5.00° degrees to the right and left of the center (see %FigParadigm). Participants were instructed to fixate on the central dot. In the Constant and Swap conditions, the background was divided into a bright (88.5 cd/m^2^) and a dark (0.2 cd/m^2^) half, separated by a central luminance-gradient band (10.0°). In the Onset condition, the background was uniformly gray (20.8 cd/m^2^). After 3 s, a voice saying 'gauche' (left) or 'droite' (right) was played back through a set of desktop speakers, instructing participants to make a saccadic eye movement to the left or right dot. Saccades were detected on-line as the moment at which horizontal gaze position deviated more than 2.9° from the central dot for at least two consecutive gaze samples. (For the analysis we used an off-line detection algorithm, described under [Saccade detection].) As soon as a saccade was detected, one of three things could happen: In the Constant condition, the display did not change at all (%FigParadigm::a); In the Swap condition, the dark side of the screen turned bright and vice versa (%FigParadigm::b); In the Onset condition, the initially gray display was divided into a bright and a dark half (%FigParadigm::c). The trial ended after another 3 s.

Phrased differently, we used a fully crossed 2 x 3 design. The first factor was Landing Luminance (Land on Bright or Land on Dark), corresponding to the luminance of the target region after the saccade. The second factor was Condition (Constant, Swap, or Onset), as described above. For example, on a Land-on-Dark Constant trial, a saccade was prepared towards the dark side of the display, which did not change after the saccade (%FigParadigm::a). On a Land-on-Bright Swap trial, a saccade was prepared towards the dark side of the screen, which turned bright on saccade detection (%FigParadigm::b). Finally, on a Land-on-Bright Onset trial, a saccade was prepared towards a gray area, which turned dark on saccade detection (%FigParadigm::c). Saccade direction (Left or Right) was fully randomized and not entered as a factor into the design.

## Pupil-trace analysis

Each trial was divided into three epochs: The baseline epoch, spanning the 100 ms prior to the presentation of the cue; The pre-saccade epoch, from the cue until the detection of the saccade; And the post-saccade epoch, from the detection of the saccade until the end of the trial. We analyzed pupil surface relative to the mean pupil size during the baseline epoch [cf. @Math2013Plos]. Missing data during blinks was reconstructed, where possible, using cubic-spline interpolation [@Math2013Blinks]. No signal smoothing was applied.

## Trial-exclusion criteria

Trials were excluded based on the following criteria: A saccade was executed in the wrong direction or before the cue was presented (8.4%); Saccade latency was less than 50 ms or more than 2000 ms (0.5%); The display change did not occur during the saccade, as determined by off-line saccade detection (4.9%; See [Saccade detection]); Blinks occurred and could not be reconstructed (4.5%, see [Pupil-trace analysis]). After exclusion, 2350 trials (81.4%) remained for further analysis.

## Saccade detection

For the purpose of the analysis, we used the EyeLink saccade detection algorithm with the default parameters (velocity threshold: 35 °/s; acceleration threshold: 9500 °/s2) and the additional constraint that we considered only the first saccade that was larger than 1.8°. Saccades were executed on average 543.6 ms (SD = 187.4) after the cue. We did not provide any instructions regarding speed, and consequently there was considerable variability in saccadic response time between participants, ranging from 409 ms to 789 ms (participant means). After the display change had occurred, a trigger was sent to the eye tracker to allow off-line verification of timing. This showed that the display change occurred exactly in the middle of the saccade, 27.09 ms (SD = 3.906) after saccade onset and 27.55 ms (SD = 7.852) before saccade offset. The average saccade duration was 54.63 ms (SD = 7.407).
