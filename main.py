import pandas as pd
import numpy as np


if __name__ == '__main__':
    # read endowment_insurance.xlsx
    df_endowment_insurance_pre = pd.read_excel('endowment_insurance.xlsx', sheet_name='Sheet2')  # 可以通过sheet_name来指定读取的表单
    data_endowment_insurance_pre = df_endowment_insurance_pre.head()  # 默认读取前5行的数据
    print("前五行endowment_insurance:\n{0}".format(data_endowment_insurance_pre))  # 格式化输出

    # read research_cost.xlsx
    df_research_cost = pd.read_excel('research_cost.xlsx')  # 可以通过sheet_name来指定读取的表单
    data_research_cost = df_research_cost.head()  # 默认读取前5行的数据
    print("前五行research_cost:\n{0}".format(data_research_cost))  # 格式化输出

    # pre_implement endowment_insurance
    row_endowment_insurance_pre = df_endowment_insurance_pre.shape[0]
    company_cur_endowment_pre = None  # int(df_endowment_insurance_pre.loc[0, 'Stkcd'])
    date_cur_endowment_pre = None  # df_endowment_insurance_pre.loc[0, 'Accper']
    num_1 = False
    num_2 = False
    df_endowment_insurance = pd.DataFrame(columns=['Stkcd', 'Accper', 'Fn03201',
                                           '本期增加额', 'Fn03204'])
    for i in range(row_endowment_insurance_pre):
        if df_endowment_insurance_pre.loc[i, 'Stkcd'] == company_cur_endowment_pre:
            if df_endowment_insurance_pre.loc[i, 'Accper'] == data_endowment_insurance_pre:
                if not num_1 and df_endowment_insurance_pre.loc[i, 'Fn03201'] == '短期薪酬其中：工资、奖金、津贴和补贴':
                    num_1 = True
                    df_endowment_insurance = df_endowment_insurance.append(df_endowment_insurance_pre.loc[i], ignore_index=True)
                if not num_2 and df_endowment_insurance_pre.loc[i, 'Fn03201'] == '离职后福利（设定提存计划）其中：基本养老保险':
                    num_2 = True
                    df_endowment_insurance = df_endowment_insurance.append(df_endowment_insurance_pre.loc[i], ignore_index=True)


            else:
                data_endowment_insurance_pre = df_endowment_insurance_pre.loc[i, 'Accper']
                num1, num_2 = False, False
                if df_endowment_insurance_pre.loc[i, 'Fn03201'] == '短期薪酬其中：工资、奖金、津贴和补贴':
                    num_1 = True
                    df_endowment_insurance = df_endowment_insurance.append(df_endowment_insurance_pre.loc[i], ignore_index=True)
                elif df_endowment_insurance_pre.loc[i, 'Fn03201'] == '离职后福利（设定提存计划）其中：基本养老保险':
                    num_2 = True
                    df_endowment_insurance = df_endowment_insurance.append(df_endowment_insurance_pre.loc[i], ignore_index=True)

        else:
            company_cur_endowment_pre = df_endowment_insurance_pre.loc[i, 'Stkcd']
            data_endowment_insurance_pre = df_endowment_insurance_pre.loc[i, 'Accper']
            num1, num_2 = False, False
            if df_endowment_insurance_pre.loc[i, 'Fn03201'] == '短期薪酬其中：工资、奖金、津贴和补贴':
                num_1 = True
                df_endowment_insurance = df_endowment_insurance.append(df_endowment_insurance_pre.loc[i], ignore_index=True)
            elif df_endowment_insurance_pre.loc[i, 'Fn03201'] == '离职后福利（设定提存计划）其中：基本养老保险':
                num_2 = True
                df_endowment_insurance = df_endowment_insurance.append(df_endowment_insurance_pre.loc[i], ignore_index=True)
    df_endowment_insurance.to_excel("merged_data_after_implement.xlsx")





    # get the maximum column number
    row_endowment_insurance = df_endowment_insurance.shape[0]
    row_research_cost = df_research_cost.shape[0]
    print("hi", row_endowment_insurance)
    print("hi", row_research_cost)

    # generate new DataFrame
    df_merged_data = pd.DataFrame(columns=['Stkcd', 'Accper', 'Fn03201',
                                           '本期增加额', 'Fn03204', 'RDPerson',
                                           'RDSpendSum', 'RDSpendSumRatio'])

    # merge data in this new DataFrame: merged_data
    row_cur_endowment = 0  # because true data in endowment starts from row0
    row_cur_research = 2  # because true data in endowment starts from row2

    company_cur_endowment = int(df_endowment_insurance.loc[row_cur_endowment, 'Stkcd'])
    company_cur_research = int(df_research_cost.loc[row_cur_research, 'Symbol'])
    date_cur_endowment = df_endowment_insurance.loc[row_cur_endowment, 'Accper']
    date_cur_research = df_research_cost.loc[row_cur_research, 'EndDate']

    while row_cur_research < row_research_cost - 1 and row_cur_endowment < row_endowment_insurance:
        if company_cur_endowment == 12:
            print("here")
        df_merged_data.to_excel("merged_data.xlsx")
        while company_cur_endowment > company_cur_research:
            df_merged_data = df_merged_data.append(df_endowment_insurance.loc[row_cur_endowment])
            row_cur_research += 1
            company_cur_research = int(df_research_cost.loc[row_cur_research, 'Symbol'])
        while company_cur_endowment < company_cur_research:
            df_merged_data = df_merged_data.append(df_endowment_insurance.loc[row_cur_endowment])
            row_cur_endowment += 1
            company_cur_endowment = int(df_endowment_insurance.loc[row_cur_endowment, 'Stkcd'])
        if company_cur_research != company_cur_endowment:
            raise ArithmeticError

        cur_company = company_cur_endowment
        # implement the equal company situation
        while cur_company == company_cur_endowment == company_cur_research:
            date_cur_endowment = df_endowment_insurance.loc[row_cur_endowment, 'Accper']
            date_cur_research = df_research_cost.loc[row_cur_research, 'EndDate']
            while date_cur_endowment > date_cur_research and company_cur_endowment is cur_company:
                df_merged_data = df_merged_data.append(df_endowment_insurance.loc[row_cur_endowment])
                row_cur_endowment += 1
                date_cur_endowment = df_endowment_insurance.loc[row_cur_endowment, 'Accper']
                company_cur_endowment = int(df_endowment_insurance.loc[row_cur_endowment, 'Stkcd'])
            while date_cur_endowment < date_cur_research and company_cur_research is cur_company:
                df_merged_data = df_merged_data.append(df_research_cost.loc[row_cur_research])
                row_cur_research += 1
                date_cur_research = df_research_cost.loc[row_cur_research, 'EndDate']
                company_cur_research = int(df_research_cost.loc[row_cur_research, 'Symbol'])

            if company_cur_endowment != company_cur_research:
                print("here")
                continue

            # implement the equal company and equal date situation
            if date_cur_research != date_cur_endowment:
                raise ArithmeticError
            while date_cur_endowment == date_cur_research and company_cur_endowment == company_cur_research == cur_company:
                merge_tmp = df_endowment_insurance.loc[row_cur_endowment].append(df_research_cost.loc[row_cur_research])
                df_merged_data = df_merged_data.append(merge_tmp, ignore_index=True)
                row_cur_endowment += 1
                date_cur_endowment = df_endowment_insurance.loc[row_cur_endowment, 'Accper']
                company_cur_endowment = int(df_endowment_insurance.loc[row_cur_endowment, 'Stkcd'])
            row_cur_research += 1
            date_cur_research = df_research_cost.loc[row_cur_research, 'EndDate']
            company_cur_research = int(df_research_cost.loc[row_cur_research, 'Symbol'])


    print(df_merged_data)
    df_merged_data.to_excel("merged_data.xlsx")




