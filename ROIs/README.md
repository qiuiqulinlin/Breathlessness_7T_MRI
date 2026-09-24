# Regions of interest

The 18 regions are **not** shared as image files. They can be recreated from the
atlas sources and MNI seed coordinates below. Masks were resampled into each
participant's native functional (EPI) space, and the hypothalamus was segmented
per participant, so no single group mask exists for it.

To reproduce the analysis, recreate each region, sample its resting-state
timeseries, and form the 153 pairwise edges named `ROIa_ROIb` (ordered list in
`../data/connectivity_edges_template.csv`).

## Region list

Seeds are 4 mm spheres at the listed MNI coordinate unless stated otherwise.

| ROI | Region | System | Definition (MNI x, y, z) |
|---|---|---|---|
| BLA | Basolateral amygdala | Subcortical | Inherited mask (22, -3, -19); Faull et al. 2016; Qiu 2024 |
| Piri | Piriform cortex | Subcortical | Sphere (16, -2, -14); adapted from Zhou et al. 2019 |
| dPAG | Dorsal periaqueductal grey | Brainstem | Inherited mask; Faull et al. 2016; Faull and Pattinson 2017 |
| vlPAG | Ventrolateral periaqueductal grey | Brainstem | Inherited mask; Faull et al. 2016; Faull and Pattinson 2017 |
| Hyp | Hypothalamus | Subcortical | Per-participant segmentation; FreeSurfer Hypothalamic Subunits (Billot et al. 2020) |
| sgACC | Subgenual anterior cingulate | Cingulate | Sphere (2, 14, -6); Kleckner et al. 2017 |
| pACC | Pregenual anterior cingulate | Cingulate | Sphere (13, 44, 0); Kleckner et al. 2017 |
| dACC | Dorsal anterior cingulate (aMCC) | Cingulate | Sphere (9, 22, 33); Kleckner et al. 2017 |
| dpIns | Dorsal posterior insula | Insula | Sphere (36, -32, 16); Kleckner et al. 2017 |
| dmIns | Dorsal middle insula | Insula | Sphere (41, 2, 3); Kleckner et al. 2017 |
| mvaIns | Medial ventral anterior insula | Insula | Sphere (30, 16, -14); Kleckner et al. 2017 |
| lvaIns | Lateral ventral anterior insula | Insula | Sphere (44, 6, -15); Kleckner et al. 2017 |
| PoI1 | Posterior insula 1 | Insula | Glasser et al. 2016 (HCP-MMP1.0) |
| PoI2 | Posterior insula 2 | Insula | Glasser et al. 2016 (HCP-MMP1.0) |
| dmPFC | Dorsomedial prefrontal cortex | Cortical | Harvard-Oxford atlas |
| vmPFC | Ventromedial prefrontal cortex | Cortical | Harvard-Oxford atlas |
| S1 | Primary somatosensory cortex | Cortical | Harvard-Oxford atlas |
| M1 | Primary motor cortex | Cortical | Harvard-Oxford atlas |

Selection rationale, putative function and cortical lamination are given in the
paper's Methods and Appendices 5 and 6.

## Sources

- **Kleckner et al. (2017):** MNI coordinates for the ACC and insula sphere seeds.
- **Glasser et al. (2016):** HCP-MMP1.0 atlas; PoI1 and PoI2 only. Subject to the
  Human Connectome Project Open Access Data Use Terms (see `../LICENSE`).
- **Harvard-Oxford atlas:** dmPFC, vmPFC, S1, M1.
- **Faull et al. (2016); Faull and Pattinson (2017); Qiu (2024):** inherited PAG
  and amygdala masks.
- **Zhou et al. (2019):** piriform cortex.
- **Billot et al. (2020):** FreeSurfer hypothalamic segmentation.
