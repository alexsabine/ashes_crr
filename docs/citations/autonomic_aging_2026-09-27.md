# PhysioNet Autonomic Aging 1.0.0: how the data were recorded (fetched 2026-09-27)

**Source.**
- Schumann, A., & Bär, K. (2021). *Autonomic Aging: A dataset to quantify changes of cardiovascular autonomic function
  during healthy aging* (version 1.0.0). PhysioNet. https://doi.org/10.13026/2hsy-t491.
- Published July 30, 2021. Licence ODC-ODbL 1.0.
- The project page https://physionet.org/content/autonomic-aging-cardiovascular/1.0.0/ was fetched 2026-09-27 (HTTP 200).

This is a note, not evidence (R8). The quotes below are verbatim from the page text.

> Electrocardiogram and continuous non-invasive blood pressure signals were recorded simultaneously at rest in 1,121 healthy volunteers.

> An ECG (lead II) was recorded at 1000 Hz either by an MP150 (ECG100C, BIOPAC systems inc., Golata, CA, USA) or Task Force Monitor system (CNSystems Medizintechnik GmbH, Graz AUT).

> Continuous blood pressure was recorded non-invasively using the vascular unloading technique [2]. In short, a cuff around the finger is controlled to maintain constant pressure, while blood volume is recorded via photoplethysmography.

> The recorded signal is mapped to brachial blood pressure that is measured oscillometricly once during initialization of the system.

> The MP150 system digitizes the signal acquired by a separate monitor CNAP 500 (CNSystems Medizintechnik GmbH, Graz AUT). The sampling frequency was 1000 Hz for both systems.

> After the subjects lied down comfortably on the examination tilt table, electrodes and pressure cuffs were placed. For the resting state recording, we instructed participants to avoid movement, yawning or coughing.

> The length of the recording was on average 19 minutes (8 - 45 minutes) and was supervised by the instructor.

> Recording device is either 0 (TFM, CNSystems) or 1 (CNAP 500, CNSystems; MP150, BIOPAC Systems).

**What the record 0061 header shows** (`data/raw/autonomic_aging/0061.hea`, a record already SEEN):
- 3 signals at 1000 Hz, 1,801,201 samples: ECG1, ECG2 (mV) and NIBP (mmHg).
- The other records carry either one or two ECG leads and NIBP.
