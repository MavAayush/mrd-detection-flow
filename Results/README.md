# Plots and their Interpretations

---

## Left Plot → All Cells - Density Distribution

`To compare how similar the patient’s MSE distribution is to the healthy (baseline) distribution for all cells.` 

- X-axis : MSE  → Reconstruction error per cell. Higher value may indicate       abnormal cells
- Y-axis : Density → Normalized frequency (not raw count). Area under the entire curve sums to 1.
- Green bars : Baseline → Distribution of MSE values for healthy cells (from patient 1 to 6)
- Red/Yellow bars : Current patient → Distribution of MSE values for current patient. (Red for test patients and yellow for healthy patients).
- Overlap (Density): Measures how much the two distributions overlap.
- Higher % means more similar. Lower % means more deviations.

---

## Right Plot → To focus only on cells having MSE > Threshold

`To compare how similar the patient’s MSE distribution is to the healthy (baseline) distribution for the cells whose MSE value > Threshold.`

- X-axis : MSE > threshold  → Only those cells with high reconstruction error.
- Y-axis : Density → Normalized frequency (not raw count). Area under the entire curve sums to 1.
- Green bars : → Distribution of high error cells from healthy baseline. Typically very small.
- Red/Yellow bars : → Patients with high error cells.
- Overlap (Filtered) : Measures similarity b/w patients and healthy distributions only for abnormal looking cells.

---

## For Instance

| Patient_Id | MRD Percentage | Interpretation from the plot |
______________________________________________________________
|            |                |                              |
|            |                |                              |


