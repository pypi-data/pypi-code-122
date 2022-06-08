import pandas as pd
import matplotlib.pyplot as plt
import git

url = 'https://github.com/RikoWatanabe/MentalHelse.git'

to_path = 'ADS'

git.Repo.clone_from(
    url,
    to_path)

def main():
    data = pd.read_csv('prevalence-by-mental-and-substance-use-disorder.csv')
    population_data = pd.read_csv('prevalence-of-depression-males-vs-females.csv')

    data = pd.merge(population_data, data, on=['Entity', 'Year'])
    data.rename(columns = {'Prevalence - Schizophrenia - Sex: Both - Age: Age-standardized (Percent)': 'Schizophrenia', 'Prevalence - Bipolar disorder - Sex: Both - Age: Age-standardized (Percent)': 'Bipolar_disorder', 'Prevalence - Eating disorders - Sex: Both - Age: Age-standardized (Percent)': 'Eating_disorders', 'Prevalence - Anxiety disorders - Sex: Both - Age: Age-standardized (Percent)': 'Anxiety_disorders', 'Prevalence - Drug use disorders - Sex: Both - Age: Age-standardized (Percent)': 'Drug_use_disorders', 'Prevalence - Depressive disorders - Sex: Both - Age: Age-standardized (Percent)': 'Depressive_disorders', 'Prevalence - Alcohol use disorders - Sex: Both - Age: Age-standardized (Percent)': 'Alcohol_use_disorders', 'Population (historical estimates)': 'population'}, inplace=True)
    data.dropna(subset=['population'], inplace=True)
    data.to_csv('marge_data.csv')

    out_ = data[['Year', 'population']].groupby('Year').sum()

    list_name = ['Schizophrenia', 'Bipolar_disorder', 'Eating_disorders', 'Anxiety_disorders', 'Drug_use_disorders', 'Depressive_disorders', 'Alcohol_use_disorders']
    for name in list_name:
        print(name)
        data['Prevalence_population'] = data[name] * data['population']
        out_ = pd.merge(out_, data[['Year', 'Prevalence_population']].groupby('Year').sum(), on=['Year'])
        out_.rename(columns = {'Prevalence_population': name}, inplace=True)

    out_list = out_.values.tolist()
    print(out_list)
    plt.plot(out_.index,out_['population'],label='population')
    plt.plot(out_.index,out_['Schizophrenia'],label='Schizophrenia')
    plt.plot(out_.index,out_['Bipolar_disorder'],label="Bipolar_disorder")
    plt.legend()
    plt.savefig('result.png')
    plt.show()

    print(pd.show_versions)

if __name__ == '__main__':
    main()