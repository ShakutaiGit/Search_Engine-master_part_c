import os
import pandas as pd


class ReadFile:
    def __init__(self, corpus_path):
        self.corpus_path = corpus_path

    def read_file(self, file_name=''):
        # we have to check what is the prupose of the variable file_name in the reader class
        """
        This function is reading a parquet file contains several tweets
        The file location is given as a string as an input to this function.
        :param file_name: string - indicates the path to the file we wish to read.
        :return: a dataframe contains tweets.
        """
        documents = []
        paths = self.get_files_name(file_name)
        for path in paths:
            df = pd.read_parquet(path, engine="pyarrow").values.tolist()
            documents.extend(df)
        return documents

    def get_files_name(self, file_name):
        path_names = []
        if file_name == '':
            full_path = self.corpus_path
        else:
            full_path = self.corpus_path + '/' + file_name
        if os.path.isfile(full_path):
            path_names.append(full_path)
        elif os.path.isdir(full_path):
            for root, directories, files in os.walk(full_path):
                for name in files:
                    if name != ".DS_Store":
                        path_names.append(os.path.join(root, name).replace(os.path.sep, '/'))
        return path_names

    def read_txt_file(self, file_path):
        read_list = []
        f = open(file_path, encoding="utf8")
        while (True):
            # read next line
            line = f.readline()
            # if line is empty, you are done with all lines in the file
            if not line:
                break
            # you can access the line
            if len(line) > 1:
                read_list.append(line.strip())
            # self.names_dict[line.strip()] = line.strip()

        return read_list





