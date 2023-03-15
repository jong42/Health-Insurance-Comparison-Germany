import numpy as np
import pandas as pd

fees_path = '../data/fees.json'
out_path_providers = '../data/providers_cleaned.csv'
out_path_states = '../data/states_cleaned.csv'

##########################################
# Create dataframe with providers as rows
##########################################

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

fees_df.to_csv(out_path_providers)

##################################
# Create df with states as rows
##################################

states = ['Bayern', 'Baden-Württemberg', 'Berlin', 'Brandenburg', 'Bremen', 'Hamburg', 'Hessen',
                  'Mecklenburg-Vorpommern', 'Niedersachsen', 'Nordrhein-Westfalen', 'Rheinland-Pfalz', 'Saarland',
                  'Sachsen', 'Sachsen-Anhalt', 'Schleswig-Holstein', 'Thüringen']

df_states = pd.DataFrame(index=states)
df_states['state'] = states
df_states['provider_count'] = np.sum(fees_df.iloc[:, 4:20], axis=0)
df_states['avg_fee'] = [np.sum(fees_df['fee']*fees_df[state])/np.sum(fees_df[state]) for state in states]
df_states['avg_services_count'] = [np.sum(fees_df['services_count']*fees_df[state])/np.sum(fees_df[state]) for state in states]

df_states.to_csv(out_path_states)
