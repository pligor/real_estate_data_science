from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import numpy as np
import pandas as pd


class AdvancedOneHotEncoder(object):
    def encodePandasColAndMerge(self, data_frame, col_name, check_to_null=lambda vv: False):
        """check_to_null provided robustness against invalid values, simply filter those values so that they are not encoded
        Note that the values are repeated in all one hot encoded columns intact"""
        one_hot_encoded = self.encodePandasColumn(data_frame=data_frame, col_name=col_name, check_to_null=check_to_null)
        return pd.concat((data_frame, one_hot_encoded), axis=1).drop(labels=[col_name], axis=1)

    ##########################################################################################

    def encodePandasColumn(self, data_frame, col_name, check_to_null):
        # df = data_frame[:]
        # dataf = data_frame.copy()

        indsToOmit = []
        for ind in data_frame.index:
            value = data_frame.loc[ind][col_name]
            if check_to_null(value):
                indsToOmit.append(ind)

        mask = np.array([ind not in indsToOmit for ind in data_frame.index])

        le = LabelEncoder()

        #print len(data_frame)
        series_col = data_frame.loc[mask][col_name]
        #print len(series_col)

        le.fit(series_col)

        encoded_seriescol = pd.Series(le.transform(series_col), index=series_col.index)  # .astype(np.float)
        #print encoded_seriescol
        #dataf[col_name] = le.transform(dataf[col_name])  # .astype(np.float)
        # The categorical attributes must be gone and replaced by numbers

        encoder = OneHotEncoder()

        #transformation = encoder.fit_transform(dataf[col_name].to_frame())
        transformation = encoder.fit_transform(encoded_seriescol.to_frame())

        # print encoder.feature_indices_
        # Dummy variable trap
        # Because of the dummy variable  trap we need to drop one of the columns for each category
        # http: // www.algosome.com / articles / dummy - variable - trap - regression.html
        arr = transformation.toarray()[:, 1:]

        df = self.createNewPanda(arr=arr, col_name=col_name, index=encoded_seriescol.index.values)

        #take the invalids and repeat them for all the created
        invalids = data_frame.loc[np.logical_not(mask)][col_name]
        df_invalids = invalids.to_frame(name=df.columns[0])
        for col in df.columns[1:]:
            df_invalids.insert(len(df_invalids.columns), col, invalids)

        return df.append(df_invalids)

    @staticmethod
    def createNewPanda(arr, col_name, index):
        assert len(arr.shape) > 1
        cols = [col_name + "_{}".format(col_ind) for col_ind in range(arr.shape[1])]
        df = pd.DataFrame(arr, columns=cols, index=index)
        return df
