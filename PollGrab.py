import pandas as pd
import os
import get_data


def main():
    #  for future me: Each of the below calls pulls data for one week. You should be able to use this for future years
    #  as long as ESPN doesn't change the formating they use to display the data again.

    df1 = get_data.get_data(2018, 1, False)
    df2 = get_data.get_data(2018, 2, False)
    df3 = get_data.get_data(2018, 3, False)
    df4 = get_data.get_data(2018, 4, False)
    df5 = get_data.get_data(2018, 5, False)
    df6 = get_data.get_data(2018, 6, False)
    df7 = get_data.get_data(2018, 7, False)
    df8 = get_data.get_data(2018, 8, False)
    df9 = get_data.get_data(2018, 9, False)
    df10 = get_data.get_data(2018, 10, False)
    df11 = get_data.get_data(2018, 11, False)
    df12 = get_data.get_data(2018, 12, False)
    df13 = get_data.get_data(2018, 13, False)
    df14 = get_data.get_data(2018, 14, False)
    df15 = get_data.get_data(2018, 15, False)
    df16 = get_data.get_data(2018, 16, True)

    df= pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, df13, df14, df15, df16], axis=1)  # this joins all the polls together
    print(df)

    current_working_directory = os.getcwd()
    filename = 'data.csv'
    filepath = os.path.join(current_working_directory, filename)  # save csv file to working directory

    df.to_csv(filepath, index=None, header=True, encoding='latin1')  # print dataframe as csv


if __name__ == '__main__':
    main()
