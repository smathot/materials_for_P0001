## Participants, software, and apparatus

Eight observers (six naive participants and two authors; seven women; age range 20-30 years) participated in the experiment. Participants provided written informed consent. The experiment was conducted with approval of the Aix-Marseille Université ethics committee. The right eye was recorded with an EyeLink 1000 (SR Research, Mississauga, Canada, ON), a video-based eye tracker sampling at 1000 Hz. Stimuli were presented on a 21" ViewSonic pf227f CRT monitor (1024 x 768 px, 100 Hz) with OpenSesame [@MathSchreij2012] using the PsychoPy [@Peirce2007] back-end. Data, materials, and supplementary analyses are available from
<https://github.com/smathot/materials_for_P0001>.

## Stimuli and procedure

Before the experiment, a nine-point eye-tracker calibration was performed. Before each trial, a single-point re-calibration was performed.

%--
figure:
 id: FigParadigm
 source: FigParadigm.svg
 caption: Schematic experimental paradigm. a) An example of a Land-on-Dark Constant trial, in which the pupil prepares for, and lands on, a dark target background. b) An example of a Land-on-Dark Swap trial, in which the pupil prepares for brightness, but lands on darkness. c) An example of a Land-on-Dark Onset trial, in which the pupil prepares for an intermediate (unchanged) luminance, but lands on darkness. The display change occurred during the saccade.
--%

Each trial started with the presentation of three dim green dots (14.7 cd/m^2^; 0.1°) at the display center and 10.0° to the right and left of the center (see %FigParadigm). Participants fixated on the central dot. In the Constant and Swap conditions, the background was divided into a bright (88.5 cd/m^2^) and a dark (0.2 cd/m^2^) half, separated by a central luminance-gradient (10.0° wide). In the Onset condition, the background was uniformly gray (20.8 cd/m^2^). After 3 s, an auditory cue, *gauche* (left) or *droite* (right), instructed a leftwards or rightwards saccade. Saccades were detected on-line when horizontal gaze position deviated more than 2.9° from the central dot for at least two consecutive gaze samples. The target dot remained visible throughout the trial. The central and non-target dots were removed on saccade detection.

Upon saccade detection, one of three things happened. In the Constant condition, the display did not change (%FigParadigm::a). Therefore, pre-saccadic preparation should result in a reduction of PLR latency. In the Swap condition, the dark side of the screen turned bright and vice versa (%FigParadigm::b). Therefore, preparation should result in a brief (seemingly) inverse PLR, reflecting the PLR's preparatory component. In the Onset condition, the uniformly gray display was divided into a bright and a dark half (%FigParadigm::c). In this condition, preparation was impossible (or, rather, there was preparation for no change), because the central dot and the saccade target were (initially) on the same gray background. The trial ended 3 s after saccade detection.

Landing luminance (Land-on-bright, Land-on-Dark) and Condition (Constant, Swap, Onset) were equiprobable and randomly mixed within blocks. Saccade direction (Left, Right) was fully randomized. The experiment consisted of 360 trials across ten blocks, and lasted approximately 90 minutes.
