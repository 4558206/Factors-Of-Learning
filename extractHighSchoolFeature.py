# -*- coding: UTF-8 -*-
import pandas as pd
#####################数据提取##########################
base_info_columns = ['id','time_submit','time_spend','source','source_detail','IP','name','sex','date_born','ss_id',
                     'subject_advicer','rank_advicer','grade_exam1','rank_exam1','grade_exam2','rank_exam2','grade_exam3',
                     'rank_exam3','type_grade_change','date_zhongkao','grade_zhongkao','rank_zhongkao']
whole_question_columns = list(range(15,324))
high_school_columns = base_info_columns + whole_question_columns

fugou_data = pd.read_csv('data/sourceData/fugou_data.csv',header=0,encoding='GBK')
fugou_data.columns = high_school_columns
fugou_data['school_name'] = 'fugou'
fugou_data['area_high_school'] = 2
fugou_data['type_high_school'] = 1
# print(fugou_data.info())
huaiyang_data = pd.read_csv('data/sourceData/huaiyang_data.csv',header=0,encoding='GBK')
huaiyang_data.columns = high_school_columns
huaiyang_data['school_name'] = 'huaiyang'
huaiyang_data['area_high_school'] = 1
huaiyang_data['type_high_school'] = 1
# print(huaiyang_data.info())
luyi_data = pd.read_csv('data/sourceData/luyi_data.csv',header=0,encoding='GBK')
luyi_data.columns = high_school_columns
luyi_data['school_name'] = 'luyi'
luyi_data['area_high_school'] = 2
luyi_data['type_high_school'] = 1
# print(luyi_data.info())
taikang_data = pd.read_csv('data/sourceData/taikang_data.csv',header=0,encoding='GBK')
taikang_data.columns = high_school_columns
taikang_data['school_name'] = 'taikang'
taikang_data['area_high_school'] = 2
taikang_data['type_high_school'] = 1
# print(taikang_data.info())
high_school_columns.remove('ss_id')
shangshui_data = pd.read_csv('data/sourceData/shangshui_data.csv',header=0,encoding='GBK')
shangshui_data.columns = high_school_columns
shangshui_data['ss_id'] = 0
shangshui_data['school_name'] = 'shangshui'
shangshui_data['area_high_school'] = 2
shangshui_data['type_high_school'] = 2
# print(shangshui_data.info())

high_school_data = pd.concat([fugou_data,huaiyang_data],axis=0)
high_school_data = pd.concat([high_school_data,luyi_data],axis=0)
high_school_data = pd.concat([high_school_data,shangshui_data],axis=0)
high_school_data = pd.concat([high_school_data,taikang_data],axis=0)
###############数据预处理#######################
##########基本信息整理#########
"""
    Base Information
    1.高中地区
    2.高中类型
    3.高三班主任任教科目
    4.高三班主任任教职称
    5.一练排名
    6.二练排名
    7.三练排名
    8.高中变化趋势
    9.复读年限
    10.中考成绩
"""
base_info = high_school_data.iloc[:,0:22].copy()
base_info['school_name'] = high_school_data['school_name'].copy()
base_info['type_high_school'] = high_school_data['type_high_school'].copy()
base_info['area_high_school'] = high_school_data['area_high_school'].copy()
base_info['date_zhongkao'] = base_info['date_zhongkao'].astype('int')
base_info['id'] = base_info['name'].astype('str') + '-' + base_info['school_name'].astype('str') + '-' + base_info['ss_id'].astype('str')
BI = base_info[['id','area_high_school','type_high_school','subject_advicer','rank_advicer','rank_exam1',
                'rank_exam2','rank_exam3','type_grade_change']].copy()
BI['reschool'] = 8 - base_info['date_zhongkao']
BI['reschool'] = BI['reschool'].apply(lambda x:x-3 if x>3 else 0)
BI['grade_zhongkao'] = base_info['grade_zhongkao']
test_data_high_school = BI.copy()
# print(test_data_college.info())
# print(test_data_college[:5])



#
##########问卷整理部分###########
questionnaire_info = high_school_data.iloc[:,22:-4]
print(questionnaire_info[:5])
"""
    1. 自我效能感（Self Efficacy）
    - 问卷位置： 15-24
    - 选项计分方式：4-3-2-1
    - 共10题
    - 无分量表
"""
SE = questionnaire_info.iloc[:,:10].copy()
SE.replace("1",4,inplace=True)
SE.replace("2",3,inplace=True)
SE.replace("3",2,inplace=True)
SE.replace("4",1,inplace=True)
SE['SE_points'] = SE.apply(lambda x: x.sum(),axis=1)
test_data_high_school["SE_points"] = SE.loc[:,['SE_points']]
# print(SE.info())
# print(test_data_high_school[:5])


"""
    2. 成就动机（Achievement Motivation）
    - 问卷位置： 25-54
    - 选项计分方式：4-3-2-1
    - 共30题
    - 成功动机分量表：MS(motivation-of-success)、1-15题
    - 失败动机分量表：MF(motivation-of-failure)、16-30题
"""
AM = questionnaire_info.iloc[:,10:40].copy()
AM.columns=list(range(1,31))
AM.replace("1",4,inplace=True)
AM.replace("2",3,inplace=True)
AM.replace("3",2,inplace=True)
AM.replace("4",1,inplace=True)
AM_MS = AM.loc[:,0:15].copy()
AM_MF = AM.loc[:,15:30].copy()
AM_MS['AM_MS_points'] = SE.apply(lambda x: x.sum(),axis=1)
AM_MF['AM_MF_points'] = SE.apply(lambda x: x.sum(),axis=1)
test_data_high_school['AM_MS_points'] = AM_MS.loc[:,['AM_MS_points']]
test_data_high_school['AM_MF_points'] = AM_MF.loc[:,['AM_MF_points']]
# print(AM.info())
# print(test_data_high_school[:5])


"""
    3. 学习策略（Learning Strategy）
    - 问卷位置： 55-99
    - 选项计分方式：4-3-2-1
    - 反向计分题号：2,6,15,18,22,26,30,36,38,40
    - 共45题
    - 认知策略分量表：CS(cognitive strategy)、题号：4,6,9,12,19,22,26,28,32,34,37,39,42,44,45
    - 元认知分策略量表：MS(metacognitive strategy)、题号：1,3,7,14,15,17,18,20,21,24,27,29,36,41
    - 资源管理利用策略分量表：RM(Resource management)、题号：2,5,8,10,11,13,16,23,25,30,31,33,35,38,40,43
"""
LS = questionnaire_info.iloc[:,40:85].copy()
LS = LS.astype('int')
LS.columns = list(range(1,46))
LS_reverse = LS[[2,6,15,18,22,26,30,36,38,40]].copy()
LS.drop([2,6,15,18,22,26,30,36,38,40],axis=1,inplace=True)
LS_reverse.replace("1",5,inplace=True)
LS_reverse.replace("2",4,inplace=True)
LS_reverse.replace("3",3,inplace=True)
LS_reverse.replace("4",2,inplace=True)
LS_reverse.replace("5",1,inplace=True)
LS = pd.concat([LS,LS_reverse],axis=1)
LS_CS = LS[[4,6,9,12,19,22,26,28,32,34,37,39,42,44,45]].copy()
LS_MS = LS[[1,3,7,14,15,17,18,20,21,24,27,29,36,41]].copy()
LS_RM = LS[[2,5,8,10,11,13,16,23,25,30,31,33,35,38,40,43]].copy()
LS_CS['LS_CS_points'] = LS_CS.apply(lambda x: x.sum(),axis=1)
LS_MS['LS_MS_points'] = LS_MS.apply(lambda x: x.sum(),axis=1)
LS_RM['LS_RM_points'] = LS_RM.apply(lambda x: x.sum(),axis=1)
test_data_high_school['LS_CS_points'] = LS_CS.loc[:,['LS_CS_points']]
test_data_high_school['LS_MS_points'] = LS_MS.loc[:,['LS_MS_points']]
test_data_high_school['LS_RM_points'] = LS_RM.loc[:,['LS_RM_points']]
# print(LS.info())
# print(test_data_high_school[:5])


"""
    4. 考试焦虑（Examination Anxiety）
    - 问卷位置： 100-136
    - 选项计分方式：1-0
    - 反向计分题号：3,15,26,27,29,33
    - 共37题
    - 无分量表
"""
EA = questionnaire_info.iloc[:,85:122].copy()
EA = EA.astype('int')
EA.columns = list(range(1,38))
EA_reverse = EA[[3,15,26,27,29,33]].copy()
EA.drop([3,15,26,27,29,33],axis=1,inplace=True)
EA_reverse.replace(1,0,inplace=True)
EA_reverse.replace(2,1,inplace=True)
EA.replace(2,0,inplace=True)
EA = pd.concat([EA,EA_reverse],axis=1)
EA['EA_points'] = EA.apply(lambda x:x.sum(),axis=1)
test_data_high_school['EA_points'] = EA.loc[:,['EA_points']]
# print(EA.info())
# print(test_data_high_school[:5])


"""
    5.家庭环境(Home Environment)
    - 问卷位置：137-226
    - 选项计分方式：1-2
    - 计正分题号：11,41,61,2,22,52,72,13,33,63,4,54,55,65,16,36,46,76,7,27,57,87,18,38,88,9,29,49,79,10,20,60,70
    - 共90道题
    - 10个分量表
    - 亲密度：11,41,61,1,21,31,51,71,81
    - 情感表达：2,22,52,72,12,32,42,62,82
    - 矛盾性：13,33,63,3,23,43,53,73,83
    - 独立性：4,54,14,24,34,44,64,74,84
    - 成功性：55,65m,5,15,25,35,45,75,85
    - 知识性：16,36,46,76,6,26,56,66,86
    - 娱乐性：7,27,57,87,17,37,47,67,77
    - 道德宗教观：18,38,88,8,28,48,58,68,78
    - 组织性：9,29,49,79,19,39,59,69,89
    - 控制性：10,20,60,70,30,40,50,80,90
"""
HE = questionnaire_info.iloc[:,122:212].copy()
HE = HE.astype('int')
HE.columns = list(range(1,91))
HE_normal = HE[[11,41,61,2,22,52,72,13,33,63,4,54,55,65,16,36,46,76,7,27,57,87,18,38,88,9,29,49,79,10,20,60,70]].copy()
HE.drop([11,41,61,2,22,52,72,13,33,63,4,54,55,65,16,36,46,76,7,27,57,87,18,38,88,9,29,49,79,10,20,60,70],axis=1,inplace=True)
HE.replace(1,-1,inplace=True)
HE.replace(2,-2,inplace=True)
HE = pd.concat([HE,HE_normal],axis=1)
HE_QM = HE[[11,41,61,1,21,31,51,71,81]].copy()
HE_BD = HE[[2,22,52,72,12,32,42,62,82]].copy()
HE_MD = HE[[13,33,63,3,23,43,53,73,83]].copy()
HE_DL = HE[[4,54,14,24,34,44,64,74,84]].copy()
HE_CG = HE[[55,65,5,15,25,35,45,75,85]].copy()
HE_ZS = HE[[16,36,46,76,6,26,56,66,86]].copy()
HE_YL = HE[[7,27,57,87,17,37,47,67,77]].copy()
HE_ZJ = HE[[18,38,88,8,28,48,58,68,78]].copy()
HE_ZZ = HE[[9,29,49,79,19,39,59,69,89]].copy()
HE_KZ = HE[[10,20,60,70,30,40,50,80,90]].copy()
HE_QM['HE_QM_points'] = HE_QM.apply(lambda x:x.sum(),axis=1)
HE_BD['HE_BD_points'] = HE_BD.apply(lambda x:x.sum(),axis=1)
HE_MD['HE_MD_points'] = HE_MD.apply(lambda x:x.sum(),axis=1)
HE_DL['HE_DL_points'] = HE_DL.apply(lambda x:x.sum(),axis=1)
HE_CG['HE_CG_points'] = HE_CG.apply(lambda x:x.sum(),axis=1)
HE_ZS['HE_ZS_points'] = HE_ZS.apply(lambda x:x.sum(),axis=1)
HE_YL['HE_YL_points'] = HE_YL.apply(lambda x:x.sum(),axis=1)
HE_ZJ['HE_ZJ_points'] = HE_ZJ.apply(lambda x:x.sum(),axis=1)
HE_ZZ['HE_ZZ_points'] = HE_ZZ.apply(lambda x:x.sum(),axis=1)
HE_KZ['HE_KZ_points'] = HE_KZ.apply(lambda x:x.sum(),axis=1)
test_data_high_school['HE_QM_points'] = HE_QM.loc[:,['HE_QM_points']]
test_data_high_school['HE_BD_points'] = HE_BD.loc[:,['HE_BD_points']]
test_data_high_school['HE_MD_points'] = HE_MD.loc[:,['HE_MD_points']]
test_data_high_school['HE_DL_points'] = HE_DL.loc[:,['HE_DL_points']]
test_data_high_school['HE_CG_points'] = HE_CG.loc[:,['HE_CG_points']]
test_data_high_school['HE_ZS_points'] = HE_ZS.loc[:,['HE_ZS_points']]
test_data_high_school['HE_YL_points'] = HE_YL.loc[:,['HE_YL_points']]
test_data_high_school['HE_ZJ_points'] = HE_ZJ.loc[:,['HE_ZJ_points']]
test_data_high_school['HE_ZZ_points'] = HE_ZZ.loc[:,['HE_ZZ_points']]
test_data_high_school['HE_KZ_points'] = HE_KZ.loc[:,['HE_KZ_points']]
# print(HE.info())
# print(test_data_high_school[:5])


"""
    6.家庭教养方式(Parenting Pattern)
    - 问卷位置：227-292
    - 问卷计分方式：1-2-3-4
    - 共66题
    - 共分量表
    - 温暖理解：2,4,6,7,9,15,20,25,29,30,31,32,33,37,42,54,60,61,66,44,63
    - 惩罚严厉：13,17,43,51,52,53,55,58,62,5,18,49
    - 过分干涉：1,10,11,14,27,36,48,50,56,57,12,16,19,24,35,41,59
    - 偏爱被试：3,8,22,64,65,32
    - 拒绝否认：21,23,28,34,35,45,26,38,39,47
    - 干涉保护：1,10,11,14,27,36,48,50,56,57,12,16,19,24,35,41,59
"""
PP = questionnaire_info.iloc[:,212:278].copy()
PP = PP.astype('int')
PP.columns = list(range(1,67))
PP_WN = PP[[2,4,6,7,9,15,20,25,29,30,31,32,33,37,42,54,60,61,66,44,63]].copy()
PP_CF = PP[[13,17,43,51,52,53,55,58,62,5,18,49]].copy()
PP_GF = PP[[1,10,11,14,27,36,48,50,56,57,12,16,19,24,35,41,59]].copy()
PP_PA = PP[[3,8,22,64,65,32]].copy()
PP_JJ = PP[[21,23,28,34,35,45,26,38,39,47]].copy()
PP_GS = PP[[1,10,11,14,27,36,48,50,56,57,12,16,19,24,35,41,59]].copy()
PP_WN['PP_WN_points'] = PP_WN.apply(lambda x:x.sum(),axis=1)
PP_CF['PP_CF_points'] = PP_CF.apply(lambda x:x.sum(),axis=1)
PP_GF['PP_GF_points'] = PP_GF.apply(lambda x:x.sum(),axis=1)
PP_PA['PP_PA_points'] = PP_PA.apply(lambda x:x.sum(),axis=1)
PP_JJ['PP_JJ_points'] = PP_JJ.apply(lambda x:x.sum(),axis=1)
PP_GS['PP_GS_points'] = PP_GS.apply(lambda x:x.sum(),axis=1)
test_data_high_school['PP_WN_points'] = PP_WN.loc[:,['PP_WN_points']]
test_data_high_school['PP_CF_points'] = PP_CF.loc[:,['PP_CF_points']]
test_data_high_school['PP_GF_points'] = PP_GF.loc[:,['PP_GF_points']]
test_data_high_school['PP_PA_points'] = PP_PA.loc[:,['PP_PA_points']]
test_data_high_school['PP_JJ_points'] = PP_JJ.loc[:,['PP_JJ_points']]
test_data_high_school['PP_GS_points'] = PP_GS.loc[:,['PP_GS_points']]
# print(PP.info())
# print(test_data_high_school[:5])


"""
    7.家庭亲密性和适应性（Familial Intimacy and Adaptability.）
    - 问卷位置： 293-323
    - 选项计分方式：1-2-3-4-5
    - 计负分题号：3,9,19,29,24,28
    - 共30题
    - 亲密度分量表：初始分36 + 1,5,7,11,13,15,17,21,23,25,27,30,3,9,19,29
    - 适应性分量表：初始分12 + 2,4,6,8,10,12,14,16,18,20,22,26,24,28
"""
FIA = questionnaire_info.iloc[:,278:].copy()
FIA = FIA.astype('int')
FIA.columns = list(range(1,31))
FIA_reverse = FIA[[3,9,19,29,24,28]].copy()
FIA.drop([3,9,19,29,24,28],axis=1,inplace=True)
FIA_reverse.replace(1,-1,inplace=True)
FIA_reverse.replace(2,-2,inplace=True)
FIA_reverse.replace(3,-3,inplace=True)
FIA_reverse.replace(4,-4,inplace=True)
FIA_reverse.replace(5,-5,inplace=True)
FIA = pd.concat([FIA,FIA_reverse],axis=1)
FIA_I = FIA[[1,5,7,11,13,15,17,21,23,25,27,30,3,9,19,29]].copy()
FIA_A = FIA[[2,4,6,8,10,12,14,16,18,20,22,26,24,28]].copy()
FIA_I['FIA_I_points'] = FIA_I.apply(lambda x:x.sum(),axis=1)
FIA_I['FIA_I_points'] = FIA_I['FIA_I_points'] + 36
FIA_A['FIA_A_points'] = FIA_A.apply(lambda x:x.sum(),axis=1)
FIA_A['FIA_A_points'] = FIA_A['FIA_A_points'] + 12
test_data_high_school['FIA_I_points'] = FIA_I.loc[:,['FIA_I_points']]
test_data_high_school['FIA_A_points'] = FIA_A.loc[:,['FIA_A_points']]
# print(FIA.info())
# print(test_data_high_school.info())
# print(test_data_high_school[:5])

test_data_high_school.to_csv('data/midData/test_data_high_school.csv',index=None,encoding='GBK')
