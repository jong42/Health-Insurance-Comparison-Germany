import numpy as np
import pandas as pd


fees_path = '../data/fees.json'
services_path = '../data/services.json'
out_path_providers = '../data/providers_cleaned.csv'
out_path_states = '../data/states_cleaned.csv'

##################################
# Services
##################################
services_df = pd.read_json(services_path)

# Remove duplicates
services_df = services_df[services_df.duplicated() == False]

# Reshape df so that each service is a column
services_df = services_df.pivot(index='provider', columns='service',values='offered')
services_df['provider'] = services_df.index
new_index = np.arange(len(services_df))
services_df = services_df.set_index(new_index)

# Remove columns that describe restrictions rather than services
cols_to_drop = ['Zuschuss zu Alternativen Heilmethoden nur über Bonusprogramm',
                'Zuschuss zu Alternativen Heilmethoden nur über Gesundheitskonto']
services_df = services_df.drop(cols_to_drop, axis=1)

# Count total number of services offered by each provider
services_df['services_count'] = services_df.iloc[:, :-1].sum(axis=1)

##################################
# Fees
##################################

fees_df = pd.read_json(fees_path)

# Remove redundant symbols
fees_df['name'] = fees_df['name'].str[2:-5]
fees_df['fee'] = fees_df['fee'].str[1:-2]
fees_df['location'] = fees_df['location'].str[1:-1]

# Remove row where no fee was given
index_to_drop = np.where(fees_df['fee'] == 'wird nicht erhobe')[0][0]
fees_df = fees_df.drop(index_to_drop, axis=0)

# Remove providers that are company-specific
pos_to_drop = np.where(fees_df['location'] == 'betriebs\xadbe\xadzogen (nur für Mitar\xadbeitende wählbar)')[0]
index_to_drop = fees_df.iloc[np.where(fees_df['location'] == 'betriebs\xadbe\xadzogen (nur für Mitar\xadbeitende wählbar)')[0],:].index
fees_df = fees_df.drop(index_to_drop, axis=0)

# Reset index
new_index = np.arange(len(fees_df))
fees_df = fees_df.set_index(new_index)

# Convert multivalue location column to multiple columns
states = ['Bayern', 'Baden-Württemberg', 'Berlin', 'Brandenburg', 'Bremen', 'Hamburg', 'Hessen',
                  'Mecklenburg-Vorpommern', 'Niedersachsen', 'Nordrhein-Westfalen', 'Rheinland-Pfalz', 'Saarland',
                  'Sachsen', 'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen']

for state in states:
    fees_df[state] = False

for i, loc in enumerate(fees_df['location']):
    loc = loc.split(',')
    loc = [i.strip() for i in loc]
    for state in states:
        if state in loc or loc == ['bundesweit']:
            fees_df[state][i] = True

# Convert fee to float type
fees_df['fee'] = fees_df['fee'].str.replace(',','.')
fees_df['fee'] = fees_df['fee'].astype(float)

##################################
# Merge both dataframes
##################################

# Align company names
services_df['provider'][services_df['provider'] == 'BERGISCHE Krankenkasse'] = 'BERGISCHE KRANKENKASSE'
services_df['provider'][services_df['provider'] == 'BKK DürkoppAdler'] = 'BKK_DürkoppAdler'
services_df['provider'][services_df['provider'] == 'BKK HERKULES'] = 'BKK Herkules'
services_df['provider'][services_df['provider'] == 'BKK SBH'] = 'BKK Schwarzwald-Baar-Heuberg'
services_df['provider'][services_df['provider'] == 'BKK VBU'] = 'BKK Verkehrsbau Union (BKK VBU) '
services_df['provider'][services_df['provider'] == 'BKK WIRTSCHAFT & FINANZEN'] = 'BKK Wirtschaft & Finanzen'
services_df['provider'][services_df['provider'] == 'Continentale BKK'] = 'Continentale Betriebskrankenkasse'
services_df['provider'][services_df['provider'] == 'DAK Gesundheit'] = 'DAK-Gesundheit'
services_df['provider'][services_df['provider'] == 'IKK - Die Innovationskasse'] = 'IKK - Die Innovationskasse (IK)'
services_df['provider'][services_df['provider'] == 'KKH Kaufmännische Krankenkasse'] = 'Kaufmännische Krankenkasse - KKH'
services_df['provider'][services_df['provider'] == 'Mobil Krankenkasse'] = 'Betriebskrankenkasse Mobil'
services_df['provider'][services_df['provider'] == 'SBK'] = 'Siemens-Betriebskrankenkasse (SBK)'
services_df['provider'][services_df['provider'] == 'SECURVITA Krankenkasse'] = 'SECURVITA BKK'
services_df['provider'][services_df['provider'] == 'Techniker Krankenkasse (TK)'] = 'Techniker Krankenkasse'
services_df['provider'][services_df['provider'] == 'energie-BKK'] = 'energie-Betriebskrankenkasse'
services_df['provider'][services_df['provider'] == 'hkk Krankenkasse'] = 'Handelskrankenkasse (hkk) '
services_df['provider'][services_df['provider'] == 'mhplus Krankenkasse'] = 'mhplus Betriebskrankenkasse'

# Merge dataframes
df_merged = pd.merge(fees_df, services_df, left_on='name', right_on='provider')
df_merged.to_csv(out_path_providers)

##################################
# Create df with states as rows
##################################

states = ['Bayern', 'Baden-Württemberg', 'Berlin', 'Brandenburg', 'Bremen', 'Hamburg', 'Hessen',
                  'Mecklenburg-Vorpommern', 'Niedersachsen', 'Nordrhein-Westfalen', 'Rheinland-Pfalz', 'Saarland',
                  'Sachsen', 'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen']

df_states = pd.DataFrame(index=states)
df_states['state'] = states
df_states['provider_count'] = np.sum(df_merged.iloc[:, 4:20], axis=0)
df_states['avg_fee'] = [np.sum(df_merged['fee']*df_merged[state])/np.sum(df_merged[state]) for state in states]
df_states['avg_services_count'] = [np.sum(df_merged['services_count']*df_merged[state])/np.sum(df_merged[state]) for state in states]

df_states.to_csv(out_path_states)
