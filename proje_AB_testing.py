#H0: M1 =M2 average bidding ve maximum bidding dönüşümlerinin ortalamaları arasında anlamlı fark yoktur.
#H1: ... anlanmlı bir fark vardır.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, pearsonr, spearmanr, kendalltau, \
    f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df = pd.read_excel("ab_testing.xlsx")
Control_df = pd.read_excel("ab_testing.xlsx", sheet_name="Control Group")
Test_df = pd.read_excel("ab_testing.xlsx", sheet_name="Test Group")

Control_df.describe().T
Test_df.describe().T

sms.DescrStatsW(Control_df["Purchase"]).tconfint_mean()
sms.DescrStatsW(Test_df["Purchase"]).tconfint_mean()

Control_df["Purchase"].mean()
Test_df["Purchase"].mean()

#H0: M1 =M2 average bidding ve maximum bidding dönüşümlerinin ortalamaları arasında anlamlı fark yoktur.
#H1: ... anlanmlı bir fark vardır.

#İlk olarak normallik varsayımı için shapiro-wilk testi yapılır.

test_stat, pvalue = shapiro(Control_df["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#p-value>0.05 olduğundan HO Reddedilemez, anlamlı fark yoktur

test_stat, pvalue = shapiro(Test_df["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#p-value>0.05 olduğundan HO Reddedilemez, anlamlı fark yoktur.

# Varyans Homojenligi Varsayımı
# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

test_stat, pvalue = levene(Control_df["Purchase"],
                           Test_df["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#p-value>0.05 olduğundan HO reddedilemez. Varyanslar homojendir.

# Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)

test_stat, pvalue = ttest_ind(Control_df["Purchase"],
                           Test_df["Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#p-value>0.05 olduğundan H0 reddedilemez. %95 güven aralığında Average bidding ve maximum bidding dönüşümlerinin ortalamaları
#arasında anlamlı fark yoktur.


######## KULLANILAN TESTLER #########
# İlk olarak normallik varsayımı için Shapiro-Wilk testini her iki grup için de ayrı ayrı kullandık.
# Ardından bu test sonuçları H0 reddedilemez çıkınca yani normal dağılıma uygun olduğu görüldü.
# Eğer H0 red çıksaydı veriler normal dağılıma uygun değil diyip non-parametrik testlerden mann-whitney'e geçecektik.
# Ancak normal dağılıma uygun olduğundan varyansların homojenliği için levene testi kullanıldı.
# levene testinde varyanslar homojen çıktı.
# En son bağımsız iki örneklem t testini yaparak H0 hipotezi reddedilemez sonucuna ulaştık. Burada equal_var=True
# yani varyanslar eşit seçildi, eğer levene testinde H0 red çıksaydı equal_var=False olarak yine t testi yapılacaktı.


######## YORUMLAR ##########
# %95 güven aralığı ile average bidding ve maximum bidding satınalınan ürün sayıları arasında istatistiksel olarak
#anlamlı bir fark yoktur. Yeni yöntemin uygulandığında elimizdeki mevcut verilerle bu yöntemin satınalma sayısını artırdığından
#söz edemeyiz. Güven aralıkları değerlerine baktığımızda %95 güven aralığında test veri setindeki purchase değerlerinin 530-633 arasında
#olduğunu, control veri seti purchase değerlerinin 508-593 değerleri arasında olduğunu söyleyebiliriz. Bu değerlere
#bakıldığında test veri setindeki purchase değerlerinin daha yüksek olduğunu söyleyebiliriz ancak bu sette standart sapma da, aralık da
#daha yüksektir. Bu sebeple yeni yöntemin fazla satınalma getirmesini istatistiki açıdan destekleyen bir kanıt yoktur,
#tesadufi olabilir, daha uzun süre daha fazla veri ile tekrar gözlemlenebilir.

