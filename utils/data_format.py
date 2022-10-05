import pandas as pd


class DataFormat:
    def csv_saver(self, file_name_with_path, header, data):
        data_df = pd.DataFrame(data=data)
        data_df.to_csv(file_name_with_path, header=header, index=False)
        print('CSV FILE SAVED:', file_name_with_path)

    def csv_reader(self, file_name_with_path):
        print('CSV FILE READ:', file_name_with_path)
        return pd.read_csv(file_name_with_path)

    def txt_saver(self, file_name_with_path, data):
        with open(file_name_with_path, 'w') as f:
            f.write(''.join(data))
        f.close()
        print('TXT FILE SAVED:', file_name_with_path)

