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
|-----------|------------------|-----------------------------|
| 15        |        1.02%     |  For Patient 15, the plots shows strong similarity to healthy profiles. The left plot, which considers all cells, has a very high overlap of 96.17%, indicating that the overall reconstruction error distribution closely matches the healthy baseline. Similarly, the right plot, focusing only on cells with high reconstruction error (MSE ≥ 0.02251), also shows a high overlap of 91.52%. This means even the "anomalous" cells in Patient 15 behave similarly to rare high-error cells naturally present in healthy individuals. |
|     16       |       4.35         | Patient 16 shows a high overall density overlap (89.69%) with healthy cells, indicating that most of their cells behave similarly to normal. However, in the high-error region (MSE ≥ 0.02251), the overlap drops to 69.36%, and the red distribution extends further right, suggesting a noticeable population of anomalous cells. This pattern indicates potential presence of MRD or abnormal cell activity that deviates from the healthy baseline. |

