import pandas as pd
from model.data_utils import Preprocess


class CollegePredictor:
    def keam_college_predictor(
        input_course, input_college_type, input_category, input_rank
    ):
        df = pd.read_csv("data/processed/keam_last_rank_processed.csv")

        # Filter dataframe based on course
        df2 = df.loc[df["Course"] == input_course]
        # Filter dataframe based on type of college (G, N, S)
        df3 = df2.loc[df2["Type"] == input_college_type]
        df4 = df3[["Code", "College Name", input_category, "Year"]]

        colleges_with_course = sorted(df4["Code"].unique())

        last_rank_dataframe_columns = [
            "Code",
            "College Name",
            "2022 Last Rank",
            "Expected Last Rank",
            "Admit Chance",
        ]

        last_rank_dataframe = pd.DataFrame(columns=last_rank_dataframe_columns)

        for i in colleges_with_course:
            temp_df = df4.loc[df4["Code"] == i]

            last_rank_dataframe_code = i
            last_rank_dataframe_admit_chance = "NULL"
            last_rank_dataframe_2022_last_rank = temp_df.loc[
                temp_df["Year"] == 2022, input_category
            ].values[0]

            college_name_with_code_df = pd.read_csv(
                "data/processed/keam_college_name_with_code.csv"
            )
            last_rank_dataframe_college_name = college_name_with_code_df.loc[
                college_name_with_code_df["Code"] == i, "College Name"
            ].values[0]

            last_rank_list = temp_df[input_category].values.tolist()

            last_rank_sum = sum(last_rank_list)

            last_rank_length = 0
            for j in last_rank_list:
                if j != 0:
                    last_rank_length = last_rank_length + 1

            last_rank_dataframe_expected_last_rank = int(
                last_rank_sum / last_rank_length
            )

            last_rank_dataframe.loc[len(last_rank_dataframe.index)] = [
                last_rank_dataframe_code,
                last_rank_dataframe_college_name,
                last_rank_dataframe_2022_last_rank,
                last_rank_dataframe_expected_last_rank,
                last_rank_dataframe_admit_chance,
            ]

            for index, row in last_rank_dataframe.iterrows():
                if row["Expected Last Rank"] < input_rank:
                    last_rank_dataframe = last_rank_dataframe.drop(index)
                else:
                    high_user_rank = input_rank + 2000
                    medium_user_rank = input_rank + 1000

                    if high_user_rank <= row["Expected Last Rank"]:
                        last_rank_dataframe.at[index, "Admit Chance"] = "High"

                    elif medium_user_rank <= row["Expected Last Rank"]:
                        last_rank_dataframe.at[index, "Admit Chance"] = "Medium"

                    else:
                        last_rank_dataframe.at[index, "Admit Chance"] = "Low"

                if row["2022 Last Rank"] == 0:
                    last_rank_dataframe.at[index, "2022 Last Rank"] = "Unavailable"

        last_rank_dataframe = last_rank_dataframe.drop(
            "Expected Last Rank", axis="columns"
        )

        return last_rank_dataframe
