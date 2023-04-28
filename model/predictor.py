import pandas as pd


class CollegePredictor:
    def _get_college_name_and_code():
        college_name_dataframe = pd.read_csv("data/raw/keam_last_rank.csv")
        college_name_new = college_name_dataframe.drop(
            columns=[
                "Type",
                "SM",
                "EW",
                "EZ",
                "MU",
                "BH",
                "LA",
                "DV",
                "VK",
                "BX",
                "KU",
                "KN",
                "SC",
                "ST",
                "Course",
                "Year",
            ]
        )

        unique_colege_codes = college_name_new.drop_duplicates()
        my_dict = unique_colege_codes.set_index("Code")["College Name"].to_dict()

        return {k: my_dict[k] for k in sorted(my_dict)}

    def keam_college_predictor(
        input_course, input_college_type, input_category, input_rank
    ):
        last_rank_processed_data = pd.read_csv(
            "data/processed/keam_last_rank_processed.csv"
        )

        # Filter dataframe based on course
        dataframe_filtered_by_course = last_rank_processed_data.loc[
            last_rank_processed_data["Course"] == input_course
        ]
        # Filter dataframe based on type of college (G, N, S)
        dataframe_filtered_by_college_type = dataframe_filtered_by_course.loc[
            dataframe_filtered_by_course["Type"] == input_college_type
        ]

        df4 = dataframe_filtered_by_college_type[["Code", input_category, "Year"]]
        colleges_with_course = sorted(df4["Code"].unique())

        # Fetch the dictionary with college_names and codes
        college_codes_and_names_dictionary = (
            CollegePredictor._get_college_name_and_code()
        )

        last_rank_df_columns = [
            "Code",
            "College Name",
            "2022 Last Rank",
            "Expected Last Rank",
            "Admit Chance",
        ]
        last_rank_dataframe = pd.DataFrame(columns=last_rank_df_columns)

        for i in colleges_with_course:
            # Create sub-dataframe corresponding to user input
            temp_df = df4.loc[df4["Code"] == i]

            # Fetch the college code
            last_rank_dataframe_code = i

            # Detch the college Name
            last_rank_dataframe_college_name = college_codes_and_names_dictionary[i]
            if last_rank_dataframe_college_name[-1] == ".":
                last_rank_dataframe_college_name = last_rank_dataframe_college_name[:-1]

            # Fetch 2022 Last Rank
            try:
                last_rank_dataframe_2022_last_rank = int(
                    temp_df.loc[temp_df["Year"] == 2022, input_category].values[0]
                )
            except:
                last_rank_dataframe_2022_last_rank = "Unavailable"

            # Expected 2023 Last Rank
            last_rank_list = temp_df[
                input_category
            ].values.tolist()  # List of last ranks of clg in 2018 - 2022

            last_rank_sum = sum(
                last_rank_list
            )  # Calculate average rank for non zero ranks

            last_rank_length = 0
            for j in last_rank_list:
                if j != 0:
                    last_rank_length = last_rank_length + 1

            try:
                last_rank_dataframe_expected_last_rank = int(
                    last_rank_sum / last_rank_length
                )
            except:
                last_rank_dataframe_expected_last_rank = "Unavailable"

            # Expected Admit Chance
            last_rank_dataframe_admit_chance = "NULL"

            last_rank_dataframe.loc[len(last_rank_dataframe.index)] = [
                last_rank_dataframe_code,
                last_rank_dataframe_college_name,
                last_rank_dataframe_2022_last_rank,
                last_rank_dataframe_expected_last_rank,
                last_rank_dataframe_admit_chance,
            ]

        for index, row in last_rank_dataframe.iterrows():
            if row["Expected Last Rank"] == "Unavailable":
                last_rank_dataframe = last_rank_dataframe.drop(index)

            elif int(row["Expected Last Rank"]) < input_rank:
                last_rank_dataframe = last_rank_dataframe.drop(index)

            else:
                high_user_rank = input_rank + 2000
                medium_user_rank = input_rank + 1000

                if high_user_rank <= int(row["Expected Last Rank"]):
                    last_rank_dataframe.at[index, "Admit Chance"] = "High"

                elif medium_user_rank <= int(row["Expected Last Rank"]):
                    last_rank_dataframe.at[index, "Admit Chance"] = "Medium"

                else:
                    last_rank_dataframe.at[index, "Admit Chance"] = "Low"

            if row["2022 Last Rank"] == 0:
                last_rank_dataframe.at[index, "2022 Last Rank"] = "Unavailable"

            if row.empty:
                last_rank_dataframe = last_rank_dataframe.drop(index)

        last_rank_dataframe = last_rank_dataframe.drop(
            "Expected Last Rank", axis="columns"
        )

        return last_rank_dataframe
