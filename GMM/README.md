# Gaussian Mixture Model (GMM) for Novelty Detection

This module implements a probabilistic clustering-based approach to detect Minimal Residual Disease (MRD) in flow cytometry data using Gaussian Mixture Models (GMM).

---

## ✅ Purpose

GMM assumes that our data is composed of several clusters, each following a multivariate Gaussian distribution (bell curve) in 14-dimensional space (cell features). We:

- **Train GMM only on healthy patient data (P1 to P6)** to learn how normal cells are distributed.
- Model the data as a mixture of Gaussians, each with its own:
  - **Mean vector** (center of the blob)
  - **Covariance matrix** (shape and spread)
  - **Weight** (relative importance of the blob)

Once trained, we feed test data (unhealthy patients) and:

- **Score each cell's log-likelihood** under the model.
- If the score is below a certain threshold (based on healthy cells), it's flagged as an anomaly.

---

## 🚀 Approach

- Due to the large dataset size (~27 million healthy cells), we tried:
  - **Downsampling to 100k cells** for faster fitting
  - **Intermediate sampling (1M, 20M)**
  - **Full dataset fitting** for final models
- Used **BIC** and **WCSS** to choose the optimal number of components (`n_components`)
- Scaled features with **StandardScaler**
- Trained GMM using **EM (Expectation-Maximization)**
- Used **1st percentile of healthy log-likelihood scores** as the anomaly threshold
- Scored both healthy and unhealthy patients and computed per-patient MRD %

---

## 📃 GMM Records

The trained GMM stores:

- Means (centers) of each Gaussian blob
- Covariance matrices (spread/shape)
- Weight of each Gaussian component
- Cluster membership probabilities for each point
- Log-likelihood scores for novelty detection

---

## 📈 GMM Outputs

- Log-likelihood scores for each cell (healthy & unhealthy)
- Anomaly classification based on threshold
- % of anomalous cells per patient (proxy for MRD)

**MRD Prediction Results (Patients 7-12):**

| Patient | Actual MRD (%) | Predicted MRD (%) |
| ------- | -------------- | ----------------- |
| P7      | 3.28           | 4.99              |
| P8      | 1.20           | 1.55              |
| P9      | 9.30           | 9.90              |
| P10     | 2.17           | 3.86              |
| P11     | 14.60          | 11.77             |
| P12     | 4.20           | 4.66              |

---

## 📊 Visualization

We use:

- **Bar charts** for comparing actual vs predicted MRD
- **Line charts** for trend analysis across patients


---

## ⚖️ Notes

- Multiple trials were conducted with different values of `n_components`
- Experiments included fitting on full vs sampled datasets
- Anomalies in healthy patients are low (as expected), validating model performance

---

## 📈 Dependencies

- `scikit-learn`
- `numpy`, `pandas`
- `matplotlib`, `seaborn`
- `joblib`

---

## 📖 References

- Flow Cytometry & MRD Literature
- Internship @ IIT Ropar (2024)

