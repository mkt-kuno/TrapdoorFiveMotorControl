import pandas
import matplotlib.pyplot as plt

MAXCH = 25

df = pandas.read_csv('20221113_i2j4k6l4m2.csv')
# 鉛直方向のデータを落とす
df = df.drop(df.columns[[i for i in range(8,58,2)]], axis=1)
df = df.drop(df.columns[[0,1,7]], axis=1)

# ラベルを着け直す
df.columns = ["I","J","K","L","M",
"19","18","17","16","15",
"04","03","02","01","00",
"14","13","12","11","10",
"09","08","07","06","05",
"24","23","22","21","20"]

# ラベル順に並べ直す
df = df.reindex(["I","J","K","L","M"]+["%02d" % ch for ch in range(0,25)], axis=1)

## キャリブレーション値の作成と補正

cal=[
    0.1586, 0.1718, 0.166,  0.1601, 0.1475,
    0.1517, 0.1648, 0.1648,   0.1609, 0.1648,
    None, 0.1706, 0.1624, 0.1505, 0.1699,
    0.1633, 0.1567, 0.132,  0.1601, 0.1611,
    0.1648, 0.1637, 0.1549, 0.1714, 0.1531
]
con=[
    17.471,  -0.3595, -0.0919, -0.6789, -2.0629,
    30.342,  2.9226 , 0      , 2.5426 ,       0,
    None, 0.0213 , 0.806  , 1.2446 , -0.4462,
    -1.3548, -6.2407, 1.8187 , -6.528 , -30.895,
    -3.2287, -1.4843, -0.5295, 0.3416 , -19.253  
]
col = ["19","18","17","16","15",
"04","03","02","01","00",
"14","13","12","11","10",
"09","08","07","06","05",
"24","23","22","21","20"]
diccal = {}
diccon = {}
for ch in range(MAXCH):
    diccal[col[ch]] = cal[ch]
    diccon[col[ch]] = con[ch]
# キャリブレーション値を掛けて補正
for ch in range(MAXCH):
    if diccal["%02d" % ch] is None:
        continue
    df["%02d" % ch] = (df["%02d" % ch] + diccon["%02d" % ch]) / diccal["%02d" % ch] * 9.81 / 1000
df['K'] = df["K"] * (-1)

df_diff = df.copy()
df_dist = df.copy()

# # カット位置の指定
# cut = [0, 366, 438, 837, 1235, 1635, -1]
# data = [0]*4

# # データを適切な位置でカット
# df = df.iloc[cut[1]:cut[5], :]
# data[0] = df.iloc[cut[1]:cut[3], :]
# data[1] = df.iloc[cut[3]:cut[4], :]
# data[2] = df.iloc[cut[4]:cut[5], :]
# data[3] = df.iloc[cut[5]:cut[6], :]

# cut[0]の場所をオフセットとして、配列全体から引く
# ->ゼロからの変化として捉えられる
for ch in range(MAXCH):
    try:
        df_diff["%02d" % ch] = df_diff["%02d" % ch] - df_diff["%02d" % ch][0]
    except:
        pass

df_dist = df_dist.drop(df.columns[[0,1,2,3,4,19]], axis=1)

df_dist = df_dist.T

# 個別のデータを見る場合
# for d in data:
#     d.plot(x="Date Time")
#     plt.show()
#     plt.cla()
#     plt.clf()
#     plt.close()

## ここからプロット
# fig = plt.figure()
# fig.add_subplot(1, 3, 1)
# df_diff.plot(ax=plt.gca(), x="K", y=["%02d" % ch for ch in range(1,25,5)])
# plt.ylim([-30,30])
# plt.xlim([0,6])
# plt.rcParams["xtick.direction"] = "in"      
# plt.rcParams["ytick.direction"] = "in"
# fig.add_subplot(1, 3, 2)
# df_diff.plot(ax=plt.gca(), x="K", y=["%02d" % ch for ch in range(2,25,5)])
# plt.ylim([-30,30])
# plt.xlim([0,6])
# plt.rcParams["xtick.direction"] = "in"      
# plt.rcParams["ytick.direction"] = "in"
# fig.add_subplot(1, 3, 3)
# df_diff.plot(ax=plt.gca(), x="K", y=["%02d" % ch for ch in range(3,25,5)])
# plt.ylim([-30,30])
# plt.xlim([0,6])
# plt.rcParams["xtick.direction"] = "in"      
# plt.rcParams["ytick.direction"] = "in"
#df_dist.plot(ax=plt.gca(), x=df_dist.columns[0], y=df_dist.columns[185])
plt.rcParams["font.family"] = "serif"       # 使用するフォント
plt.rcParams["font.serif"] = "MS Gothic"
plt.rcParams['font.size'] = 10 #フォントの大きさ（基準）
plt.rcParams["xtick.direction"] = "in"      
plt.rcParams["ytick.direction"] = "in"
fig = plt.figure()
fig.add_subplot(1, 3, 1)
df_diff.plot(ax=plt.gca(), x="K", y=["%02d" % 11, "%02d" % 12, "%02d" % 13])
plt.ylim([-30,30])
plt.xlim([0,6])
plt.xlabel('降下量(中央)(mm)')
plt.ylabel('せん断荷重変化(kN)')
plt.rcParams["xtick.direction"] = "in"      
plt.rcParams["ytick.direction"] = "in"

fig.add_subplot(1, 3, 2)
df_diff.plot(ax=plt.gca(), x="K", y=["%02d" % 6, "%02d" % 7, "%02d" % 8, "%02d" % 16, "%02d" % 17, "%02d" % 18])
plt.ylim([-30,30])
plt.xlim([0,6])
plt.xlabel('降下量(中央)(mm)')
plt.ylabel('せん断荷重変化(kN)')
plt.rcParams["xtick.direction"] = "in"      
plt.rcParams["ytick.direction"] = "in"
fig.add_subplot(1, 3, 3)
df_diff.plot(ax=plt.gca(), x="K", y=["%02d" % 1, "%02d" % 2, "%02d" % 3, "%02d" % 21, "%02d" % 22, "%02d" % 23])
plt.ylim([-30,30])
plt.xlim([0,6])
plt.xlabel('降下量(中央)(mm)')
plt.ylabel('せん断荷重変化(kN)')
plt.rcParams["xtick.direction"] = "in"      
plt.rcParams["ytick.direction"] = "in"

fig = plt.figure()
df_dist.plot(ax=plt.gca(), y=[df_dist.columns[0],df_dist.columns[185],df_dist.columns[310],df_dist.columns[435]])
plt.ylim([-40,40])
plt.xlabel('降下量(中央)(mm)')
plt.ylabel('せん断荷重変化(kN)')
plt.rcParams["xtick.direction"] = "in"      
plt.rcParams["ytick.direction"] = "in"

plt.show()
plt.cla()
plt.clf()
plt.close()

## 未使用コード
# data[0].to_csv('output/data_00100.csv')
# data[1].to_csv('output/data_01110.csv')
# data[2].to_csv('output/data_11111.csv')
# data[3].to_csv('output/data_freerun_after_11111.csv')
df.to_csv('output/all_shear.csv')

# plt.savefig("image.png")