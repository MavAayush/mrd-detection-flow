import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.mixture import GaussianMixture
import joblib
import random as rn

RANDOM_SEED = 42
torch.manual_seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
rn.seed(RANDOM_SEED)

BATCH_SIZE = 256
LATENT_DIM = 4

patients = {
    1: ['Data/organized_fcs_data1a.csv', 'Data/organized_fcs_data1b.csv', 'Data/organized_fcs_data1c.csv'],
    2: ['Data/organized_fcs_data2a.csv', 'Data/organized_fcs_data2b.csv', 'Data/organized_fcs_data2c.csv'],
    3: ['Data/organized_fcs_data3a.csv', 'Data/organized_fcs_data3b.csv', 'Data/organized_fcs_data3c.csv'],
    4: ['Data/organized_fcs_data4a.csv', 'Data/organized_fcs_data4b.csv', 'Data/organized_fcs_data4c.csv'],
    5: ['Data/organized_fcs_data5a.csv', 'Data/organized_fcs_data5b.csv', 'Data/organized_fcs_data5c.csv'],
    6: ['Data/organized_fcs_data6a.csv', 'Data/organized_fcs_data6b.csv', 'Data/organized_fcs_data6c.csv'],
    7: ['Data/organized_fcs_data7.csv'],
    8: ['Data/organized_fcs_data8a.csv', 'Data/organized_fcs_data8b.csv', 'Data/organized_fcs_data8c.csv'],
    9: ['Data/organized_fcs_data9a.csv', 'Data/organized_fcs_data9b.csv'],
    10: ['Data/organized_fcs_data10a.csv', 'Data/organized_fcs_data10b.csv', 'Data/organized_fcs_data10c.csv'],
    11: ['Data/organized_fcs_data11.csv'],
    12: ['Data/organized_fcs_data12a.csv', 'Data/organized_fcs_data12b.csv', 'Data/organized_fcs_data12c.csv']
}

training_ids = [1, 2, 3, 4, 5, 6]
test_ids = [7, 8, 9, 10, 11, 12]

def load_and_concatenate(ids):
    all_data = []
    for pid in ids:
        dfs = [pd.read_csv(fp).drop(columns=['Time'], errors='ignore') for fp in patients[pid]]
        all_data.append(pd.concat(dfs))
    return pd.concat(all_data, ignore_index=True)


train_df = load_and_concatenate(training_ids)
test_df = load_and_concatenate(test_ids)

pipeline = Pipeline([('scaler', MinMaxScaler())])
pipeline.fit(train_df)
X_train = pipeline.transform(train_df)
X_test = pipeline.transform(test_df)


class CustomDataset(Dataset):
    def __init__(self, data):
        self.data = torch.tensor(data, dtype=torch.float32)
    def __len__(self):
        return len(self.data)
    def __getitem__(self, idx):
        return self.data[idx]
    

train_loader = DataLoader(CustomDataset(X_train), batch_size=BATCH_SIZE, shuffle=False)
test_loader = DataLoader(CustomDataset(X_test), batch_size=BATCH_SIZE, shuffle=False)

input_dim = X_train.shape[1]

class VarAutoEncoder(nn.Module):
    def __init__(self, input_dim, latent_dim=4):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 16), nn.ELU(),
            nn.Linear(16, 8), nn.ELU(),
            nn.Linear(8, 4), nn.ELU(),
        )
        self.fc_mu = nn.Linear(4, latent_dim)
        self.fc_log_var = nn.Linear(4, latent_dim)

        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 4), nn.ELU(),
            nn.Linear(4, 8), nn.ELU(),
            nn.Linear(8, 16), nn.ELU(),
            nn.Linear(16, input_dim), nn.ELU()
        )

    def reparameterize(self, mu, log_var):
        std = torch.exp(0.5 * log_var)
        eps = torch.randn_like(std)
        return mu + eps * std

    def forward(self, x):
        encoded = self.encoder(x)
        mu = self.fc_mu(encoded)
        log_var = self.fc_log_var(encoded)
        z = self.reparameterize(mu, log_var)
        decoded = self.decoder(z)
        return decoded, mu, log_var
    

vae = VarAutoEncoder(input_dim=input_dim, latent_dim=LATENT_DIM)
vae.load_state_dict(torch.load("vae_4dim_6_final.pth"))
vae.eval()

#latent space extraction 
def extract_sampled_latents(model, loader):
    model.eval()
    latents = []
    with torch.no_grad():
        for batch in loader:
            encoded = model.encoder(batch)
            mu = model.fc_mu(encoded)
            log_var = model.fc_log_var(encoded)
            std = torch.exp(0.5 * log_var)
            eps = torch.randn_like(std)
            z = mu + eps * std 
            latents.append(z.numpy())
    return np.vstack(latents)


latent_train = extract_sampled_latents(vae, train_loader)
latent_test = extract_sampled_latents(vae, test_loader)

print(f"Train latent shape: {latent_train.shape}")
print(f"Test latent shape: {latent_test.shape}")

gmm = GaussianMixture(n_components=4, covariance_type='full', random_state=42)
gmm.fit(latent_train)
joblib.dump(gmm, 'vg2.pkl')

healthy_scores = gmm.score_samples(latent_train)
unhealthy_scores = gmm.score_samples(latent_test)

threshold = np.percentile(healthy_scores, 1)
print(threshold)

anomalies = unhealthy_scores < threshold
healthy_anomalies = healthy_scores < threshold

def load_patient_data(patient_ids):
    all_data = []
    for pid in patient_ids:
        dfs = [pd.read_csv(fp).drop(columns=['Time'], errors='ignore') for fp in patients[pid]]
        all_data.append(pd.concat(dfs))
    return pd.concat(all_data, ignore_index=True)


print("\nMRD percentage for each unhealthy patient:")
unhealthy_patient_ids = [7, 8, 9, 10, 11, 12]
start_idx = 0

predicted_percentages = []
actual_percentages = [3.28, 1.2, 9.3, 2.17, 14.6, 4.2] 

for pid in unhealthy_patient_ids:
    patient_data = load_patient_data([pid])
    patient_cells = len(patient_data)
    patient_anomalies = anomalies[start_idx:start_idx + patient_cells]
    mrd_percent = (np.sum(patient_anomalies) / patient_cells) * 100
    predicted_percentages.append(round(mrd_percent, 2))
    print(f"Patient {pid}: {mrd_percent:.4f}% MRD")
    start_idx += patient_cells


print("\nMRD percentage for each healthy patient:")
healthy_patient_ids = [1, 2, 3, 4, 5, 6]
start_idx = 0

for pid in healthy_patient_ids:
    patient_data = load_patient_data([pid])
    patient_cells = len(patient_data)
    patient_anomalies = healthy_anomalies[start_idx:start_idx + patient_cells]
    mrd_percent = (np.sum(patient_anomalies) / patient_cells) * 100
    print(f"Patient {pid}: {mrd_percent:.4f}% MRD")
    start_idx += patient_cells

import matplotlib.pyplot as plt
import seaborn as sns

patients = ['P7', 'P8', 'P9', 'P10', 'P11', 'P12']
df_plot = pd.DataFrame({
    'Patient': patients,
    'Predicted': predicted_percentages,
    'Actual': actual_percentages
})

# Bar Plot
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
bar_width = 0.35
x = np.arange(len(patients))

plt.bar(x - bar_width/2, df_plot['Predicted'], bar_width, label='Predicted %', color='skyblue')
plt.bar(x + bar_width/2, df_plot['Actual'], bar_width, label='Actual %', color='salmon')

plt.xlabel('Patients')
plt.ylabel('% of Cells Above Threshold')
plt.title('MRD Prediction vs Actual for Patients 7 to 12')
plt.xticks(ticks=x, labels=patients)
plt.legend()
plt.tight_layout()
plt.show()

# Line Plot
plt.figure(figsize=(10, 5))
plt.plot(patients, predicted_percentages, marker='o', label='Predicted %', linestyle='-', color='blue')
plt.plot(patients, actual_percentages, marker='s', label='Actual %', linestyle='--', color='red')

plt.xlabel('Patients')
plt.ylabel('% of Cells Above Threshold')
plt.title('Trend: Predicted vs Actual MRD')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
