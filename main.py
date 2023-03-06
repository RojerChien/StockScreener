from pickle import TRUE
# https://medium.com/geekculture/top-4-python-libraries-for-technical-analysis-db4f1ea87e09

import pandas as pd
import webbrowser

pd.options.mode.chained_assignment = None  # 將警告訊息關閉
import requests
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import datetime
import kaleido
import numpy as np

# from datetime import datetime
from csv import reader

import bs4 as bs
import requests
import csv
import plotly.graph_objects as go
from ta.trend import MACD
from ta.momentum import StochasticOscillator
##from yahooquery import Ticker
from plotly.subplots import make_subplots
import webbrowser

########################## 從Firstrade以及老處取得ptp stock tickers #####################
import requests
from bs4 import BeautifulSoup


def get_ptp_tickers(url1, url2):
    # 第一個網站
    response1 = requests.get(url1)
    soup1 = BeautifulSoup(response1.content, "html.parser")

    table1 = soup1.find("table", {"width": "100%"})
    tbody1 = table1.find("tbody")
    rows1 = tbody1.find_all("tr")
    ptp_lists = []

    for row in rows1:
        cols = row.find_all("td")
        if len(cols) == 3:
            symbol = cols[2].get_text().strip()
            ptp_lists.append(symbol)

    # 第二個網站
    response2 = requests.get(url2)
    soup2 = BeautifulSoup(response2.text, 'html.parser')
    table2 = soup2.find('table', {'class': 'table'})
    rows2 = table2.find_all('tr')
    ptp_tickers = []

    for row in rows2:
        code = row.find('td')
        if code:
            ptp_tickers.append(code.text.strip())

    # 合併兩個列表，並取得不重覆的值
    ptp_lists.extend(ptp_tickers)
    ptp_lists = list(set(ptp_lists))

    return ptp_lists
    print(ptp_lists)


url1 = "https://help.zh-tw.firstrade.com/article/841-new-1446-f-regulations"
url2 = 'https://www.itigerup.com/bulletin/ptp'
ptp_lists = get_ptp_tickers(url1, url2)

vcp_test_tickers = ['AAPL', 'ICPT']
test_tickers = ['UFPT', 'IPVF', 'SCU', 'ICD']

tw_tickers = ['1101.TW', '1102.TW', '1103.TW', '1104.TW', '1108.TW', '1109.TW', '1110.TW', '1201.TW', '1203.TW',
              '1210.TW', '1213.TW', '1215.TW', '1216.TW', '1217.TW', '1218.TW', '1219.TW', '1220.TW', '1225.TW',
              '1227.TW', '1229.TW', '1231.TW', '1232.TW', '1233.TW', '1234.TW', '1235.TW', '1236.TW', '1240.TWO',
              '1256.TW', '1258.TWO', '1259.TWO', '1264.TWO', '1268.TWO', '1301.TW', '1303.TW', '1304.TW', '1305.TW',
              '1307.TW', '1308.TW', '1309.TW', '1310.TW', '1312.TW', '1313.TW', '1314.TW', '1315.TW', '1316.TW',
              '1319.TW', '1321.TW', '1323.TW', '1324.TW', '1325.TW', '1326.TW', '1336.TWO', '1337.TW', '1338.TW',
              '1339.TW', '1340.TW', '1341.TW', '1402.TW', '1409.TW', '1410.TW', '1413.TW', '1414.TW', '1416.TW',
              '1417.TW', '1418.TW', '1419.TW', '1423.TW', '1432.TW', '1434.TW', '1435.TW', '1436.TW', '1437.TW',
              '1438.TW', '1439.TW', '1440.TW', '1441.TW', '1442.TW', '1443.TW', '1444.TW', '1445.TW', '1446.TW',
              '1447.TW', '1449.TW', '1451.TW', '1452.TW', '1453.TW', '1454.TW', '1455.TW', '1456.TW', '1457.TW',
              '1459.TW', '1460.TW', '1463.TW', '1464.TW', '1465.TW', '1466.TW', '1467.TW', '1468.TW', '1470.TW',
              '1471.TW', '1472.TW', '1473.TW', '1474.TW', '1475.TW', '1476.TW', '1477.TW', '1503.TW', '1504.TW',
              '1506.TW', '1512.TW', '1513.TW', '1514.TW', '1515.TW', '1516.TW', '1517.TW', '1519.TW', '1521.TW',
              '1522.TW', '1524.TW', '1525.TW', '1526.TW', '1527.TW', '1528.TW', '1529.TW', '1530.TW', '1531.TW',
              '1532.TW', '1533.TW', '1535.TW', '1536.TW', '1537.TW', '1538.TW', '1539.TW', '1540.TW', '1541.TW',
              '1558.TW', '1560.TW', '1565.TWO', '1568.TW', '1569.TWO', '1570.TWO', '1580.TWO', '1582.TW', '1583.TW',
              '1584.TWO', '1586.TWO', '1587.TW', '1589.TW', '1590.TW', '1591.TWO', '1593.TWO', '1595.TWO', '1598.TW',
              '1599.TWO', '1603.TW', '1604.TW', '1605.TW', '1608.TW', '1609.TW', '1611.TW', '1612.TW', '1614.TW',
              '1615.TW', '1616.TW', '1617.TW', '1618.TW', '1626.TW', '1701.TW', '1702.TW', '1707.TW', '1708.TW',
              '1709.TW', '1710.TW', '1711.TW', '1712.TW', '1713.TW', '1714.TW', '1717.TW', '1718.TW', '1720.TW',
              '1721.TW', '1722.TW', '1723.TW', '1725.TW', '1726.TW', '1727.TW', '1730.TW', '1731.TW', '1732.TW',
              '1733.TW', '1734.TW', '1735.TW', '1736.TW', '1737.TW', '1742.TWO', '1760.TW', '1762.TW', '1773.TW',
              '1776.TW', '1777.TWO', '1781.TWO', '1783.TW', '1784.TWO', '1785.TWO', '1786.TW', '1788.TWO', '1789.TW',
              '1795.TW', '1796.TWO', '1799.TWO', '1802.TW', '1805.TW', '1806.TW', '1808.TW', '1809.TW', '1810.TW',
              '1813.TWO', '1815.TWO', '1817.TW', '1903.TW', '1904.TW', '1905.TW', '1906.TW', '1907.TW', '1909.TW',
              '2002.TW', '2006.TW', '2007.TW', '2008.TW', '2009.TW', '2010.TW', '2012.TW', '2013.TW', '2014.TW',
              '2015.TW', '2017.TW', '2020.TW', '2022.TW', '2023.TW', '2024.TW', '2027.TW', '2028.TW', '2029.TW',
              '2030.TW', '2031.TW', '2032.TW', '2033.TW', '2034.TW', '2035.TWO', '2038.TW', '2049.TW', '2059.TW',
              '2061.TWO', '2062.TW', '2063.TWO', '2064.TWO', '2065.TWO', '2066.TWO', '2067.TWO', '2069.TW', '2070.TWO',
              '2101.TW', '2102.TW', '2103.TW', '2104.TW', '2105.TW', '2106.TW', '2107.TW', '2108.TW', '2109.TW',
              '2114.TW', '2115.TW', '2201.TW', '2204.TW', '2206.TW', '2207.TW', '2208.TW', '2221.TWO', '2227.TW',
              '2228.TW', '2230.TWO', '2231.TW', '2233.TW', '2235.TWO', '2236.TW', '2239.TW', '2243.TW', '2301.TW',
              '2302.TW', '2303.TW', '2305.TW', '2308.TW', '2312.TW', '2313.TW', '2314.TW', '2316.TW', '2317.TW',
              '2321.TW', '2323.TW', '2324.TW', '2327.TW', '2328.TW', '2329.TW', '2330.TW', '2331.TW', '2332.TW',
              '2337.TW', '2338.TW', '2340.TW', '2342.TW', '2344.TW', '2345.TW', '2347.TW', '2348.TW', '2349.TW',
              '2351.TW', '2352.TW', '2353.TW', '2354.TW', '2355.TW', '2356.TW', '2357.TW', '2358.TW', '2359.TW',
              '2360.TW', '2362.TW', '2363.TW', '2364.TW', '2365.TW', '2367.TW', '2368.TW', '2369.TW', '2371.TW',
              '2373.TW', '2374.TW', '2375.TW', '2376.TW', '2377.TW', '2379.TW', '2380.TW', '2382.TW', '2383.TW',
              '2385.TW', '2387.TW', '2388.TW', '2390.TW', '2392.TW', '2393.TW', '2395.TW', '2397.TW', '2399.TW',
              '2401.TW', '2402.TW', '2404.TW', '2405.TW', '2406.TW', '2408.TW', '2409.TW', '2412.TW', '2413.TW',
              '2414.TW', '2415.TW', '2417.TW', '2419.TW', '2420.TW', '2421.TW', '2423.TW', '2424.TW', '2425.TW',
              '2426.TW', '2427.TW', '2428.TW', '2429.TW', '2430.TW', '2431.TW', '2433.TW', '2434.TW', '2436.TW',
              '2438.TW', '2439.TW', '2440.TW', '2441.TW', '2442.TW', '2443.TW', '2444.TW', '2449.TW', '2450.TW',
              '2451.TW', '2453.TW', '2454.TW', '2455.TW', '2457.TW', '2458.TW', '2459.TW', '2460.TW', '2461.TW',
              '2462.TW', '2464.TW', '2465.TW', '2466.TW', '2467.TW', '2468.TW', '2471.TW', '2472.TW', '2474.TW',
              '2476.TW', '2477.TW', '2478.TW', '2480.TW', '2481.TW', '2482.TW', '2483.TW', '2484.TW', '2485.TW',
              '2486.TW', '2488.TW', '2489.TW', '2491.TW', '2492.TW', '2493.TW', '2495.TW', '2496.TW', '2497.TW',
              '2498.TW', '2501.TW', '2504.TW', '2505.TW', '2506.TW', '2509.TW', '2511.TW', '2514.TW', '2515.TW',
              '2516.TW', '2520.TW', '2524.TW', '2527.TW', '2528.TW', '2530.TW', '2534.TW', '2535.TW', '2536.TW',
              '2537.TW', '2538.TW', '2539.TW', '2540.TW', '2542.TW', '2543.TW', '2545.TW', '2546.TW', '2547.TW',
              '2548.TW', '2596.TWO', '2597.TW', '2601.TW', '2603.TW', '2605.TW', '2606.TW', '2607.TW', '2608.TW',
              '2609.TW', '2610.TW', '2611.TW', '2612.TW', '2613.TW', '2614.TW', '2615.TW', '2616.TW', '2617.TW',
              '2618.TW', '2630.TW', '2633.TW', '2634.TW', '2636.TW', '2637.TW', '2640.TWO', '2641.TWO', '2642.TW',
              '2643.TWO', '2701.TW', '2702.TW', '2704.TW', '2705.TW', '2706.TW', '2707.TW', '2712.TW', '2718.TWO',
              '2719.TWO', '2722.TW', '2723.TW', '2724.TWO', '2726.TWO', '2727.TW', '2729.TWO', '2731.TW', '2732.TWO',
              '2734.TWO', '2736.TWO', '2739.TW', '2740.TWO', '2745.TWO', '2748.TW', '2752.TWO', '2801.TW', '2809.TW',
              '2812.TW', '2816.TW', '2820.TW', '2832.TW', '2834.TW', '2836.TW', '2838.TW', '2845.TW', '2849.TW',
              '2850.TW', '2851.TW', '2852.TW', '2855.TW', '2867.TW', '2880.TW', '2881.TW', '2882.TW', '2883.TW',
              '2884.TW', '2885.TW', '2886.TW', '2887.TW', '2888.TW', '2889.TW', '2890.TW', '2891.TW', '2892.TW',
              '2897.TW', '2901.TW', '2903.TW', '2904.TW', '2905.TW', '2906.TW', '2908.TW', '2910.TW', '2911.TW',
              '2912.TW', '2913.TW', '2915.TW', '2916.TWO', '2923.TW', '2924.TWO', '2926.TWO', '2929.TW', '2937.TWO',
              '2939.TW', '3002.TW', '3003.TW', '3004.TW', '3005.TW', '3006.TW', '3008.TW', '3010.TW', '3011.TW',
              '3013.TW', '3014.TW', '3015.TW', '3016.TW', '3017.TW', '3018.TW', '3019.TW', '3021.TW', '3022.TW',
              '3023.TW', '3024.TW', '3025.TW', '3026.TW', '3027.TW', '3028.TW', '3029.TW', '3030.TW', '3031.TW',
              '3032.TW', '3033.TW', '3034.TW', '3035.TW', '3036.TW', '3037.TW', '3038.TW', '3040.TW', '3041.TW',
              '3042.TW', '3043.TW', '3044.TW', '3045.TW', '3046.TW', '3047.TW', '3048.TW', '3049.TW', '3050.TW',
              '3051.TW', '3052.TW', '3054.TW', '3055.TW', '3056.TW', '3057.TW', '3058.TW', '3059.TW', '3060.TW',
              '3062.TW', '3064.TWO', '3066.TWO', '3067.TWO', '3071.TWO', '3073.TWO', '3078.TWO', '3081.TWO', '3083.TWO',
              '3085.TWO', '3086.TWO', '3088.TWO', '3089.TWO', '3090.TW', '3093.TWO', '3094.TW', '3095.TWO', '3105.TWO',
              '3114.TWO', '3115.TWO', '3118.TWO', '3122.TWO', '3128.TWO', '3130.TW', '3131.TWO', '3141.TWO', '3147.TWO',
              '3149.TW', '3152.TWO', '3162.TWO', '3163.TWO', '3164.TW', '3167.TW', '3169.TWO', '3171.TWO', '3176.TWO',
              '3178.TWO', '3188.TWO', '3189.TW', '3191.TWO', '3202.TWO', '3205.TWO', '3206.TWO', '3207.TWO', '3209.TW',
              '3211.TWO', '3213.TWO', '3217.TWO', '3218.TWO', '3219.TWO', '3221.TWO', '3224.TWO', '3226.TWO',
              '3227.TWO', '3228.TWO', '3229.TW', '3230.TWO', '3231.TW', '3232.TWO', '3234.TWO', '3236.TWO', '3252.TWO',
              '3257.TW', '3259.TWO', '3260.TWO', '3264.TWO', '3265.TWO', '3266.TW', '3268.TWO', '3272.TWO', '3276.TWO',
              '3284.TWO', '3285.TWO', '3287.TWO', '3288.TWO', '3289.TWO', '3290.TWO', '3293.TWO', '3294.TWO', '3296.TW',
              '3297.TWO', '3303.TWO', '3305.TW', '3306.TWO', '3308.TW', '3310.TWO', '3311.TW', '3312.TW', '3313.TWO',
              '3317.TWO', '3321.TW', '3322.TWO', '3323.TWO', '3324.TWO', '3325.TWO', '3332.TWO', '3338.TW', '3339.TWO',
              '3346.TW', '3354.TWO', '3356.TW', '3360.TWO', '3362.TWO', '3363.TWO', '3372.TWO', '3373.TWO', '3374.TWO',
              '3376.TW', '3379.TWO', '3380.TW', '3388.TWO', '3390.TWO', '3402.TWO', '3406.TW', '3413.TW', '3416.TW',
              '3419.TW', '3426.TWO', '3432.TW', '3434.TWO', '3437.TW', '3438.TWO', '3441.TWO', '3443.TW', '3444.TWO',
              '3450.TW', '3454.TW', '3455.TWO', '3465.TWO', '3466.TWO', '3479.TWO', '3481.TW', '3483.TWO', '3484.TWO',
              '3489.TWO', '3490.TWO', '3491.TWO', '3492.TWO', '3494.TW', '3498.TWO', '3499.TWO', '3501.TW', '3504.TW',
              '3508.TWO', '3511.TWO', '3512.TWO', '3515.TW', '3516.TWO', '3518.TW', '3520.TWO', '3521.TWO', '3522.TWO',
              '3523.TWO', '3526.TWO', '3527.TWO', '3528.TW', '3529.TWO', '3530.TW', '3531.TWO', '3532.TW', '3533.TW',
              '3535.TW', '3536.TW', '3537.TWO', '3540.TWO', '3541.TWO', '3545.TW', '3546.TWO', '3548.TWO', '3550.TW',
              '3551.TWO', '3552.TWO', '3555.TWO', '3556.TWO', '3557.TW', '3558.TWO', '3563.TW', '3564.TWO', '3567.TWO',
              '3570.TWO', '3576.TW', '3577.TWO', '3580.TWO', '3581.TWO', '3583.TW', '3587.TWO', '3588.TW', '3591.TW',
              '3593.TW', '3594.TWO', '3596.TW', '3605.TW', '3607.TW', '3609.TWO', '3611.TWO', '3615.TWO', '3617.TW',
              '3622.TW', '3623.TWO', '3624.TWO', '3625.TWO', '3628.TWO', '3630.TWO', '3631.TWO', '3632.TWO', '3642.TWO',
              '3645.TW', '3646.TWO', '3652.TW', '3653.TW', '3661.TW', '3663.TWO', '3664.TWO', '3665.TW', '3666.TWO',
              '3669.TW', '3672.TWO', '3673.TW', '3675.TWO', '3679.TW', '3680.TWO', '3682.TW', '3684.TWO', '3685.TWO',
              '3686.TW', '3689.TWO', '3691.TWO', '3693.TWO', '3694.TW', '3701.TW', '3702.TW', '3703.TW', '3704.TW',
              '3705.TW', '3706.TW', '3707.TWO', '3708.TW', '3709.TWO', '3710.TWO', '3711.TW', '3712.TW', '4102.TWO',
              '4104.TW', '4105.TWO', '4106.TW', '4107.TWO', '4108.TW', '4109.TWO', '4111.TWO', '4113.TWO', '4114.TWO',
              '4116.TWO', '4119.TW', '4120.TWO', '4121.TWO', '4123.TWO', '4126.TWO', '4127.TWO', '4128.TWO', '4129.TWO',
              '4130.TWO', '4131.TWO', '4133.TW', '4137.TW', '4138.TWO', '4139.TWO', '4142.TW', '4147.TWO', '4148.TW',
              '4153.TWO', '4154.TWO', '4155.TW', '4157.TWO', '4160.TWO', '4161.TWO', '4162.TWO', '4163.TWO', '4164.TW',
              '4167.TWO', '4168.TWO', '4171.TWO', '4173.TWO', '4174.TWO', '4175.TWO', '4183.TWO', '4188.TWO', '4190.TW',
              '4192.TWO', '4198.TWO', '4205.TWO', '4207.TWO', '4303.TWO', '4304.TWO', '4305.TWO', '4306.TW', '4401.TWO',
              '4402.TWO', '4406.TWO', '4413.TWO', '4414.TW', '4416.TWO', '4417.TWO', '4419.TWO', '4420.TWO', '4426.TW',
              '4430.TWO', '4432.TWO', '4433.TWO', '4438.TW', '4439.TW', '4502.TWO', '4503.TWO', '4506.TWO', '4510.TWO',
              '4513.TWO', '4523.TWO', '4526.TW', '4527.TWO', '4528.TWO', '4529.TWO', '4530.TWO', '4532.TW', '4533.TWO',
              '4534.TWO', '4535.TWO', '4536.TW', '4538.TWO', '4540.TW', '4541.TWO', '4542.TWO', '4543.TWO', '4545.TW',
              '4549.TWO', '4550.TWO', '4551.TW', '4552.TW', '4554.TWO', '4555.TW', '4556.TWO', '4557.TW', '4560.TW',
              '4561.TWO', '4562.TW', '4563.TWO', '4564.TW', '4566.TW', '4568.TWO', '4571.TW', '4572.TW', '4576.TW',
              '4609.TWO', '4702.TWO', '4706.TWO', '4707.TWO', '4711.TWO', '4712.TWO', '4714.TWO', '4716.TWO', '4720.TW',
              '4721.TWO', '4722.TW', '4726.TWO', '4728.TWO', '4729.TWO', '4735.TWO', '4736.TWO', '4737.TW', '4739.TW',
              '4741.TWO', '4743.TWO', '4744.TWO', '4745.TWO', '4746.TW', '4747.TWO', '4754.TWO', '4755.TW', '4760.TWO',
              '4763.TW', '4764.TW', '4766.TW', '4767.TWO', '4804.TWO', '4806.TWO', '4807.TW', '4903.TWO', '4904.TW',
              '4905.TWO', '4906.TW', '4907.TWO', '4908.TWO', '4909.TWO', '4911.TWO', '4912.TW', '4915.TW', '4916.TW',
              '4919.TW', '4924.TWO', '4927.TW', '4930.TW', '4931.TWO', '4933.TWO', '4934.TW', '4935.TW', '4938.TW',
              '4939.TWO', '4942.TW', '4943.TW', '4944.TWO', '4946.TWO', '4950.TWO', '4952.TW', '4953.TWO', '4956.TW',
              '4958.TW', '4960.TW', '4961.TW', '4966.TWO', '4967.TW', '4968.TW', '4971.TWO', '4972.TWO', '4973.TWO',
              '4974.TWO', '4976.TW', '4977.TW', '4979.TWO', '4987.TWO', '4989.TW', '4991.TWO', '4994.TW', '4995.TWO',
              '4999.TW', '5007.TW', '5009.TWO', '5011.TWO', '5013.TWO', '5014.TWO', '5015.TWO', '5016.TWO', '5201.TWO',
              '5202.TWO', '5203.TW', '5205.TWO', '5206.TWO', '5209.TWO', '5210.TWO', '5211.TWO', '5212.TWO', '5213.TWO',
              '5215.TW', '5220.TWO', '5223.TWO', '5225.TW', '5227.TWO', '5230.TWO', '5234.TW', '5243.TW', '5245.TWO',
              '5251.TWO', '5258.TW', '5263.TWO', '5269.TW', '5272.TWO', '5274.TWO', '5276.TWO', '5278.TWO', '5281.TWO',
              '5283.TW', '5284.TW', '5285.TW', '5287.TWO', '5288.TW', '5289.TWO', '5291.TWO', '5299.TWO', '5301.TWO',
              '5302.TWO', '5309.TWO', '5310.TWO', '5312.TWO', '5314.TWO', '5315.TWO', '5321.TWO', '5324.TWO',
              '5328.TWO', '5340.TWO', '5344.TWO', '5345.TWO', '5347.TWO', '5348.TWO', '5351.TWO', '5353.TWO',
              '5355.TWO', '5356.TWO', '5364.TWO', '5371.TWO', '5381.TWO', '5383.TWO', '5386.TWO', '5388.TW', '5392.TWO',
              '5398.TWO', '5403.TWO', '5410.TWO', '5425.TWO', '5426.TWO', '5432.TWO', '5434.TW', '5438.TWO', '5439.TWO',
              '5443.TWO', '5452.TWO', '5455.TWO', '5457.TWO', '5460.TWO', '5464.TWO', '5465.TWO', '5468.TWO', '5469.TW',
              '5471.TW', '5474.TWO', '5475.TWO', '5478.TWO', '5483.TWO', '5484.TW', '5487.TWO', '5488.TWO', '5489.TWO',
              '5490.TWO', '5493.TWO', '5498.TWO', '5508.TWO', '5511.TWO', '5512.TWO', '5514.TWO', '5515.TW', '5516.TWO',
              '5519.TW', '5520.TWO', '5521.TW', '5522.TW', '5523.TWO', '5525.TW', '5529.TWO', '5530.TWO', '5531.TW',
              '5533.TW', '5534.TW', '5536.TWO', '5538.TW', '5543.TWO', '5601.TWO', '5603.TWO', '5604.TWO', '5607.TW',
              '5608.TW', '5609.TWO', '5701.TWO', '5703.TWO', '5704.TWO', '5706.TW', '5864.TWO', '5871.TW',
              '5876.TW', '5878.TWO', '5880.TW', '5902.TWO', '5903.TWO', '5904.TWO', '5905.TWO', '5906.TW', '5907.TW',
              '6005.TW', '6015.TWO', '6016.TWO', '6020.TWO', '6021.TWO', '6023.TWO', '6024.TW', '6026.TWO', '6101.TWO',
              '6103.TWO', '6104.TWO', '6108.TW', '6109.TWO', '6111.TWO', '6112.TW', '6113.TWO', '6114.TWO', '6115.TW',
              '6116.TW', '6117.TW', '6118.TWO', '6120.TW', '6121.TWO', '6122.TWO', '6123.TWO', '6124.TWO', '6125.TWO',
              '6126.TWO', '6127.TWO', '6128.TW', '6129.TWO', '6130.TWO', '6133.TW', '6134.TWO', '6136.TW', '6138.TWO',
              '6139.TW', '6140.TWO', '6141.TW', '6142.TW', '6143.TWO', '6144.TWO', '6146.TWO', '6147.TWO', '6148.TWO',
              '6150.TWO', '6151.TWO', '6152.TW', '6153.TW', '6154.TWO', '6155.TW', '6156.TWO', '6158.TWO', '6160.TWO',
              '6161.TWO', '6163.TWO', '6164.TW', '6165.TW', '6166.TW', '6167.TWO', '6168.TW', '6169.TWO', '6170.TWO',
              '6171.TWO', '6173.TWO', '6174.TWO', '6175.TWO', '6176.TW', '6177.TW', '6179.TWO', '6180.TWO', '6182.TWO',
              '6183.TW', '6184.TW', '6185.TWO', '6186.TWO', '6187.TWO', '6188.TWO', '6189.TW', '6190.TWO', '6191.TW',
              '6192.TW', '6194.TWO', '6195.TWO', '6196.TW', '6197.TW', '6198.TWO', '6199.TWO', '6201.TW', '6202.TW',
              '6203.TWO', '6204.TWO', '6205.TW', '6206.TW', '6207.TWO', '6208.TWO', '6209.TW', '6210.TWO', '6212.TWO',
              '6213.TW', '6214.TW', '6215.TW', '6216.TW', '6217.TWO', '6218.TWO', '6219.TWO', '6220.TWO', '6221.TWO',
              '6222.TWO', '6223.TWO', '6224.TW', '6225.TW', '6226.TW', '6227.TWO', '6228.TWO', '6229.TWO', '6230.TW',
              '6231.TWO', '6233.TWO', '6234.TWO', '6235.TW', '6236.TWO', '6237.TWO', '6239.TW', '6240.TWO', '6241.TWO',
              '6242.TWO', '6243.TW', '6244.TWO', '6245.TWO', '6246.TWO', '6247.TWO', '6248.TWO', '6257.TW', '6259.TWO',
              '6261.TWO', '6263.TWO', '6264.TWO', '6265.TWO', '6266.TWO', '6269.TW', '6270.TWO', '6271.TW', '6274.TWO',
              '6275.TWO', '6276.TWO', '6277.TW', '6278.TW', '6279.TWO', '6281.TW', '6282.TW', '6283.TW', '6284.TWO',
              '6285.TW', '6287.TWO', '6288.TW', '6289.TW', '6290.TWO', '6291.TWO', '6292.TWO', '6294.TWO', '6404.TWO',
              '6405.TW', '6409.TW', '6411.TWO', '6412.TW', '6414.TW', '6415.TW', '6416.TW', '6417.TWO', '6418.TWO',
              '6419.TWO', '6425.TWO', '6431.TW', '6432.TWO', '6435.TWO', '6441.TWO', '6442.TW', '6443.TW', '6446.TWO',
              '6449.TW', '6451.TW', '6456.TW', '6457.TWO', '6461.TWO', '6462.TWO', '6464.TW', '6465.TWO', '6469.TWO',
              '6470.TWO', '6472.TWO', '6477.TW', '6482.TWO', '6485.TWO', '6486.TWO', '6488.TWO', '6491.TW', '6492.TWO',
              '6494.TWO', '6496.TWO', '6499.TWO', '6504.TW', '6505.TW', '6506.TWO', '6508.TWO', '6509.TWO', '6510.TWO',
              '6512.TWO', '6514.TWO', '6516.TWO', '6523.TWO', '6525.TW', '6527.TWO', '6530.TWO', '6531.TW', '6532.TWO',
              '6533.TW', '6535.TWO', '6538.TWO', '6541.TW', '6542.TWO', '6547.TWO', '6548.TWO', '6552.TW', '6556.TWO',
              '6558.TW', '6560.TWO', '6561.TWO', '6568.TWO', '6569.TWO', '6570.TWO', '6573.TW', '6574.TWO', '6576.TWO',
              '6577.TWO', '6578.TWO', '6579.TW', '6581.TW', '6582.TW', '6589.TWO', '6590.TWO', '6591.TW', '6592.TW',
              '6593.TWO', '6594.TWO', '6596.TWO', '6603.TWO', '6605.TW', '6609.TWO', '6612.TWO', '6613.TWO', '6615.TWO',
              '6616.TWO', '6624.TWO', '6625.TW', '6629.TWO', '6640.TWO', '6641.TW', '6642.TWO', '6643.TWO', '6649.TWO',
              '6654.TWO', '6655.TW', '6662.TWO', '6664.TWO', '6666.TW', '6667.TWO', '6668.TW', '6669.TW', '6670.TW',
              '6671.TW', '6672.TW', '6674.TW', '6679.TWO', '6680.TWO', '6683.TWO', '6690.TWO', '6697.TWO', '6698.TW',
              '6706.TW', '6715.TW', '6803.TWO', '7402.TWO', '8011.TW', '8016.TW', '8021.TW', '8024.TWO', '8027.TWO',
              '8028.TW', '8032.TWO', '8033.TW', '8034.TWO', '8038.TWO', '8039.TW', '8040.TWO', '8042.TWO', '8043.TWO',
              '8044.TWO', '8046.TW', '8047.TWO', '8048.TWO', '8049.TWO', '8050.TWO', '8054.TWO', '8059.TWO', '8064.TWO',
              '8066.TWO', '8067.TWO', '8068.TWO', '8070.TW', '8072.TW', '8081.TW', '8101.TW', '8103.TW', '8104.TW',
              '8105.TW', '8110.TW', '8112.TW', '8114.TW', '8131.TW', '8150.TW', '8163.TW', '8201.TW', '8210.TW',
              '8213.TW', '8215.TW', '8222.TW', '8249.TW', '8261.TW', '8271.TW', '8341.TW', '8367.TW', '8374.TW',
              '8404.TW', '8411.TW', '8422.TW', '8429.TW', '8442.TW', '8443.TW', '8454.TW', '8462.TW', '8463.TW',
              '8464.TW', '8466.TW', '8467.TW', '8473.TW', '8478.TW', '8480.TW', '8481.TW', '8482.TW', '8488.TW',
              '8499.TW', '8926.TW', '8940.TW', '8996.TW', '9802.TW', '9902.TW', '9904.TW', '9905.TW', '9906.TW',
              '9907.TW', '9908.TW', '9910.TW', '9911.TW', '9912.TW', '9914.TW', '9917.TW', '9918.TW', '9919.TW',
              '9921.TW', '9924.TW', '9925.TW', '9926.TW', '9927.TW', '9928.TW', '9929.TW', '9930.TW', '9931.TW',
              '9933.TW', '9934.TW', '9935.TW', '9937.TW', '9938.TW', '9939.TW', '9940.TW', '9941.TW', '9942.TW',
              '9943.TW', '9944.TW', '9945.TW', '9946.TW', '9955.TW', '9958.TW', '8069.TWO', '8071.TWO', '8074.TWO',
              '8076.TWO', '8077.TWO', '8080.TWO', '8083.TWO', '8084.TWO', '8085.TWO', '8086.TWO', '8087.TWO',
              '8088.TWO', '8089.TWO', '8091.TWO', '8092.TWO', '8093.TWO', '8096.TWO', '8097.TWO', '8099.TWO',
              '8107.TWO', '8109.TWO', '8111.TWO', '8121.TWO', '8147.TWO', '8155.TWO', '8171.TWO', '8176.TWO',
              '8182.TWO', '8183.TWO', '8234.TWO', '8240.TWO', '8255.TWO', '8277.TWO', '8279.TWO', '8284.TWO',
              '8289.TWO', '8291.TWO', '8299.TWO', '8342.TWO', '8349.TWO', '8354.TWO', '8358.TWO', '8383.TWO',
              '8390.TWO', '8401.TWO', '8403.TWO', '8409.TWO', '8410.TWO', '8415.TWO', '8416.TWO', '8418.TWO',
              '8420.TWO', '8421.TWO', '8423.TWO', '8424.TWO', '8426.TWO', '8431.TWO', '8432.TWO', '8433.TWO',
              '8435.TWO', '8436.TWO', '8437.TWO', '8440.TWO', '8444.TWO', '8446.TWO', '8450.TWO', '8455.TWO',
              '8472.TWO', '8476.TWO', '8477.TWO', '8489.TWO', '8905.TWO', '8906.TWO', '8908.TWO', '8916.TWO',
              '8917.TWO', '8921.TWO', '8923.TWO', '8924.TWO', '8927.TWO', '8928.TWO', '8929.TWO', '8930.TWO',
              '8931.TWO', '8932.TWO', '8933.TWO', '8935.TWO', '8936.TWO', '8937.TWO', '8938.TWO', '8941.TWO',
              '8942.TWO']

us_tickers = ['MSFT', 'GOOG', 'GOOGL', 'AMZN', 'PCAR', 'BRK-B', 'TSLA', 'NVDA', 'V', 'TSM', 'XOM', 'META', 'UNH', 'JPM',
              'JNJ', 'WMT', 'MA', 'PG', 'NVO', 'CVX', 'LLY', 'HD', 'ABBV', 'MRK', 'BAC', 'KO', 'AVGO', 'ASML', 'PEP',
              'BABA', 'ORCL', 'PFE', 'SHEL', 'COST', 'TMO', 'AZN', 'CSCO', 'MCD', 'CRM', 'TM', 'NKE', 'DHR', 'NVS',
              'DIS', 'ABT', 'WFC', 'LIN', 'TMUS', 'ACN',
              'BHP', 'VZ', 'MS', 'UPS', 'TXN', 'CMCSA', 'TTE', 'PM', 'ADBE', 'HSBC', 'BMY', 'RTX', 'NEE', 'SCHW',
              'NFLX', 'RY',
              'QCOM', 'SAP', 'T', 'COP', 'HON', 'AXP', 'CAT', 'UNP', 'UL', 'AMD', 'DE', 'AMGN', 'HDB', 'BA', 'LMT',
              'BP', 'PDD',
              'BUD', 'RIO', 'TD', 'SNY', 'LOW', 'SBUX', 'GS', 'IBM', 'PLD', 'INTU', 'ELV', 'SPGI', 'MDT', 'INTC', 'CVS',
              'SONY',
              'BLK', 'GILD', 'BKNG', 'DEO', 'C', 'SYK', 'AMAT', 'EQNR', 'GE', 'ADI', 'ADP', 'AMT', 'MDLZ', 'TJX', 'EL',
              'NOW',
              'CB', 'CI', 'BTI', 'MUFG', 'REGN', 'PGR', 'PYPL', 'MO', 'MMC', 'ISRG', 'VALE', 'CNI', 'ENB', 'ZTS', 'SLB',
              'TGT',
              'VRTX', 'INFY', 'CHTR', 'FISV', 'JD', 'ABNB', 'IBN', 'CP', 'DUK', 'ITW', 'NOC', 'USB', 'PBR', 'EOG',
              'GSK', 'ETN',
              'SO', 'HCA', 'BSX', 'AMOV', 'BN', 'UBS', 'BMO', 'AMX', 'CME', 'BX', 'BDX', 'CNQ', 'UBER', 'LRCX', 'SAN',
              'APD',
              'CSX', 'GD', 'EQIX', 'ABB', 'HUM', 'AON', 'WM', 'CL', 'PNC', 'FCX', 'MELI', 'MU', 'TFC', 'ATVI', 'MMM',
              'BNS',
              'MPC', 'SMFG', 'STLA', 'RELX', 'TRI', 'SCCO', 'SHW', 'PANW', 'ICE', 'NTES', 'CCI', 'SNPS', 'OXY', 'MET',
              'GM', 'VLO', 'MNST', 'MRNA', 'MCO', 'CDNS', 'ORLY', 'MAR', 'AIG', 'PSA', 'KLAC', 'FDX', 'NSC', 'BIDU',
              'SHOP',
              'ING', 'F', 'PSX', 'PXD', 'KDP', 'HSY', 'EW', 'RACE', 'MCK', 'TAK', 'DG', 'EMR', 'KHC', 'KKR', 'WDS', 'E',
              'WDAY', 'VMW', 'GIS', 'AZO', 'FTNT', 'SRE', 'APH', 'BBVA', 'ITUB', 'SU', 'NXPI', 'SQ', 'D', 'PH', 'NGG',
              'ECL', 'DXCM', 'LVS', 'ROP', 'CTVA', 'AEP', 'ADM', 'MSI', 'CTAS', 'HMC', 'MCHP', 'NUE', 'ADSK', 'JCI',
              'SNOW',
              'HES', 'KMB', 'TRV', 'TT', 'STM', 'O', 'TEAM', 'ANET', 'PUK', 'AFL', 'A', 'TDG', 'CM', 'LYG', 'DOW',
              'COF',
              'CMG', 'MSCI', 'APO', 'STZ', 'RSG', 'NTR', 'TEL', 'BK', 'TRP', 'LHX', 'BCE', 'LNG', 'PAYX', 'ABEV', 'SPG',
              'EXC', 'MFG', 'LULU', 'BSBR', 'AJG', 'IQV', 'IDXX', 'BIIB', 'KMI', 'HLT', 'MRVL', 'SYY', 'ODFL', 'ROST',
              'CARR',
              'CRH', 'CNC', 'FIS', 'MFC', 'WBD', 'WMB', 'WELL', 'CVE', 'DVN', 'PRU', 'AMP', 'YUM', 'OTIS', 'CMI', 'SE',
              'GFS', 'XEL', 'HLN', 'VICI', 'NEM', 'WCN', 'NWG', 'GWW', 'GEHC', 'HAL', 'DD', 'ROK', 'FMX', 'PCG', 'CPRT',
              'ALL',
              'ALC', 'SGEN', 'BCS', 'AME', 'KR', 'VOD', 'URI', 'DLTR', 'ON', 'MTD', 'ILMN', 'BKR', 'CTSH', 'LYB', 'ABC',
              'PPG',
              'RMD', 'MBLY', 'ED', 'APTV', 'DHI', 'BNTX', 'EA', 'ORAN', 'STT', 'WBA', 'DFS', 'FERG', 'FAST', 'IMO',
              'PEG', 'CHT',
              'OKE', 'ALB', 'DLR', 'GPN', 'GLW', 'CSGP', 'SLF', 'TU', 'ENPH', 'GOLD', 'DELL', 'CRWD', 'HPQ', 'KEYS',
              'VRSK', 'SBAC',
              'WEC', 'NDAQ', 'LEN', 'VEEV', 'TTD', 'CDW', 'ANSS', 'BBD', 'ULTA', 'CBRE', 'ACGL', 'FANG', 'NOK', 'IT',
              'WIT', 'FNV',
              'ZBH', 'ES', 'MTB', 'YUMC', 'TLK', 'AWK', 'CCEP', 'HZNP', 'MT', 'TSCO', 'CPNG', 'WTW', 'BGNE', 'EBAY',
              'ARE', 'TROW',
              'DB', 'CEG', 'EIX', 'EFX', 'DAL', 'FITB', 'HIG', 'LI', 'GMAB', 'TCOM', 'BEKE', 'GPC', 'BBDO', 'SQM',
              'VMC',
              'RCI', 'ALNY', 'TEF', 'ALGN', 'FTV', 'WST', 'DDOG', 'HEI', 'AVB', 'EC', 'IR', 'IFF', 'EQR', 'WY', 'HRL',
              'PWR', 'STLD',
              'RJF', 'MPWR', 'SPOT', 'K', 'NU', 'RBLX', 'MLM', 'CNHI', 'FE', 'EXR', 'FRC', 'CAJ', 'ETR', 'HBAN', 'GIB',
              'RF', 'RYAAY',
              'AEM', 'AEE', 'TECK', 'DOV', 'DASH', 'LH', 'TSN', 'DTE', 'FSLR', 'ZM', 'CHD', 'IX', 'VRSN', 'UMC', 'PFG',
              'LPLA', 'TS',
              'TDY', 'HPE', 'CTRA', 'LUV', 'PPL', 'BAX', 'PODD', 'CFG', 'QSR', 'NET', 'HOLX', 'MKC', 'PKX', 'CLX',
              'NTRS', 'CAH', 'VTR',
              'ARGX', 'ZTO', 'WAB', 'MOS', 'FTS', 'JBHT', 'ZS', 'TTWO', 'HUBS', 'WPM', 'CINF', 'FOXA', 'GRMN', 'PBA',
              'BMRN', 'WAT', 'STE',
              'INVH', 'ICLR', 'OMC', 'BBY', 'ERIC', 'MAA', 'XYL', 'RCL', 'ELP', 'MKL', 'WRB', 'HWM', 'SEDG', 'EPAM',
              'SWKS', 'DRI',
              'CNP', 'SUI', 'TRGP', 'INCY', 'PAYC', 'FOX', 'ROL', 'FICO', 'CAG', 'BALL', 'WPC', 'PINS', 'EXPD', 'CMS',
              'UAL', 'CHWY', 'MGM',
              'IEX', 'CF', 'NVR', 'KEY', 'BR', 'SPLK', 'AMCR', 'AVTR', 'SIRI', 'AES', 'LYV', 'MRO', 'PARAA', 'SIVB',
              'EXPE', 'FWONK', 'WMG',
              'PLTR', 'HTHT', 'FMC', 'UI', 'MGA', 'MOH', 'COO', 'ATO', 'FDS', 'AER', 'SJM', 'SNAP', 'BRO', 'RPRX',
              'PKI', 'ASX', 'FLT', 'TER',
              'CPB', 'CHKP', 'ZBRA', 'COIN', 'RTO', 'WLK', 'SYF', 'DGX', 'LKQ', 'KOF', 'AXON', 'LCID', 'IRM', 'J', 'RE',
              'TXT', 'ETSY',
              'RS', 'KB', 'TW', 'EBR', 'AGR', 'SSNC', 'PTC', 'LW', 'RIVN', 'AVY', 'BG', 'NIO', 'FWONA', 'SHG', 'BEN',
              'SJR', 'ESS', 'L',
              'ARES', 'PHG', 'BURL', 'PARA', 'BIO', 'CBOE', 'AZPN', 'MDB', 'GLPI', 'TPL', 'BAM', 'NTAP', 'UDR', 'IPG',
              'POOL', 'TME', 'CCL',
              'VTRS', 'EVRG', 'HUBB', 'LDOS', 'TYL', 'CE', 'STX', 'CSL', 'MKTX', 'WPP', 'CRBG', 'SNA', 'NICE', 'IP',
              'SRPT', 'PEAK', 'PKG',
              'APA', 'TRMB', 'WYNN', 'LNT', 'BAH', 'OKTA', 'BLDR', 'KIM', 'CTLT', 'H', 'TWLO', 'NDSN', 'SNN', 'TRU',
              'LBRDA', 'UHAL', 'CG',
              'LBRDK', 'ELS', 'ENTG', 'SWK', 'GEN', 'VIV', 'CUK', 'ACM', 'CPT', 'ERIE', 'DT', 'DOCU', 'PHM', 'NMR',
              'HST', 'WDC', 'JKHY',
              'CCJ', 'FHN', 'EQT', 'IHG', 'TECH', 'GRAB', 'SUZ', 'CNA', 'BSY', 'REXR', 'BWA', 'GL', 'WSO', 'U', 'GGG',
              'LSCC', 'TTC', 'MTCH',
              'MAS', 'AFG', 'CHRW', 'GDDY', 'RPM', 'AKAM', 'EQH', 'TAP', 'OVV', 'CRL', 'PSNY', 'CDAY', 'WTRG', 'LSXMB',
              'FIVE', 'JBL', 'EXAS',
              'FMS', 'UTHR', 'CLF', 'DOX', 'TEVA', 'NI', 'CS', 'DECK', 'WSC', 'TFX', 'TFII', 'CHK', 'CZR', 'DKS', 'KMX',
              'REG', 'AMH',
              'DPZ', 'BCH', 'ACI', 'AGCO', 'GFL', 'LAMR', 'PCTY', 'CUBE', 'RRX', 'LSI', 'EWBC', 'FNF', 'BAP', 'QGEN',
              'TPR', 'ARCC', 'DINO',
              'AAL', 'SCI', 'LSXMA', 'EMN', 'CCK', 'AEG', 'FCNCA', 'BRKR', 'LSXMK', 'DAR', 'PAG', 'FLEX', 'XM', 'HSIC',
              'BXP', 'VFC',
              'AOS', 'QRVO', 'JNPR', 'LBTYB', 'ZI', 'BJ', 'ALLE', 'NWS', 'NLY', 'PEN', 'COTY', 'LECO', 'NBIX', 'GGB',
              'NWSA', 'LBTYK', 'PAC',
              'Z', 'RGEN', 'ARMK', 'RGA', 'SSL', 'TOST', 'BZ', 'ZG', 'AGL', 'RNR', 'MASI', 'MTN', 'FND', 'LBTYA', 'ICL',
              'OTEX', 'BSMX',
              'UHS', 'CHDN', 'VIPS', 'JAZZ', 'KNX', 'JHX', 'BBWI', 'WBS', 'SNX', 'PCOR', 'AA', 'CMA', 'MANH', 'IBKR',
              'PNR', 'BKI', 'BILL',
              'PFGC', 'LII', 'RDY', 'ALLY', 'OC', 'UNM', 'NOV', 'MORN', 'YMM', 'TX', 'KEP', 'ROKU', 'G', 'ASR', 'RHI',
              'FRT', 'FFIV',
              'HII', 'IOT', 'CAR', 'OSH', 'VST', 'USFD', 'LOGI', 'WCC', 'WEX', 'CFR', 'JEF', 'PNW', 'MIDD', 'WOLF',
              'ALGM', 'LEA', 'HOOD',
              'DKNG', 'GFI', 'WSM', 'NNN', 'CGNX', 'AAP', 'WRK', 'CBSH', 'JLL', 'BSAC', 'PATH', 'BILI', 'DCI', 'WAL',
              'XRAY', 'SEIC', 'ALV',
              'ORI', 'EME', 'MTZ', 'COLD', 'CASY', 'NVCR', 'IVZ', 'PSO', 'DLB', 'OLN', 'RGLD', 'CHE', 'RL', 'FBIN',
              'CX', 'LEGN', 'XPEV',
              'UGI', 'AR', 'ST', 'ATR', 'BERY', 'CROX', 'INSP', 'IRDM', 'NVT', 'ITT', 'CLVT', 'SKM', 'NRG', 'KBR',
              'HAS', 'GPK', 'SAIA',
              'TTEK', 'HR', 'DBX', 'ESLT', 'WHR', 'PLUG', 'PSTG', 'DVA', 'TPX', 'VOYA', 'KNSL', 'CLH', 'GNRC', 'ZION',
              'EDU', 'AU',
              'CIEN', 'CAE', 'EGP', 'ONON', 'CNXC', 'WMS', 'NFE', 'CELH', 'OGE', 'SF', 'SEE', 'FUTU', 'SKX', 'APLS',
              'LEVI', 'GLOB', 'FR',
              'CACI', 'LAD', 'VMI', 'X', 'IQ', 'TXRH', 'ARW', 'NXST', 'PRI', 'RBC', 'SBS', 'ADT', 'FTI', 'BOKF', 'HOG',
              'CR', 'SWAV',
              'BRX', 'SGFY', 'DOOO', 'CW', 'MNDY', 'SBNY', 'BYD', 'WH', 'RH', 'RBA', 'KRTX', 'AXTA', 'ACHC', 'AIZ',
              'GNTX', 'WF', 'PLNT',
              'FYBR', 'CFLT', 'INGR', 'XP', 'BLD', 'NATI', 'MTDR', 'SITE', 'LSTR', 'OLED', 'CHH', 'LFUS', 'NTNX', 'PII',
              'RRC', 'TOL', 'PB',
              'ASND', 'HLI', 'STN', 'EDR', 'MDU', 'NYT', 'DOCS', 'AN', 'GTLB', 'MHK', 'STVN', 'CHX', 'HALO', 'OHI',
              'ADC', 'DSGX', 'MPW',
              'AMKR', 'NVST', 'FCN', 'PDCE', 'DXC', 'MAT', 'NCLH', 'TKR', 'MUR', 'CPRI', 'RLI', 'WWE', 'BC', 'WFG',
              'CIB', 'MKSI', 'AYI',
              'HXL', 'NTRA', 'OGN', 'M', 'DDS', 'CIVI', 'BBLN', 'MEDP', 'CMC', 'BLCO', 'MLCO', 'ALK', 'VVV', 'SIGI',
              'PBF', 'IPGP', 'AGNC',
              'SSB', 'STAG', 'WWD', 'FSV', 'THC', 'GXO', 'NWL', 'VRT', 'CYBR', 'KT', 'SNV', 'SLGN', 'SAIC', 'MNSO',
              'GIL', 'STWD', 'ROIV',
              'ATKR', 'OSK', 'OPCH', 'HTZ', 'RCM', 'NYCB', 'GRFS', 'FLO', 'SON', 'REYN', 'NE', 'WTS', 'VAC', 'GMED',
              'PVH', 'AQUA', 'SWN',
              'HUN', 'SRC', 'LNW', 'COHR', 'TIXT', 'SBSW', 'DISH', 'GTLS', 'VLY', 'GWRE', 'AMG', 'BWXT', 'CHRD', 'QDEL',
              'SMAR', 'CACC',
              'CRUS', 'TIMB', 'PPC', 'UNVR', 'FAF', 'SLAB', 'NEP', 'RXDX', 'EXEL', 'EHC', 'FSK', 'HRB', 'HQY', 'WTFC',
              'APG', 'MUSA',
              'AIRC', 'ASH', 'CCCS', 'GME', 'PNFP', 'HGV', 'COLM', 'AIT', 'MP', 'ESTC', 'TREX', 'CSAN', 'OWL', 'IAA',
              'EXLS', 'SPSC',
              'IOSP', 'TXG', 'EEFT', 'LU', 'ATI', 'UBSI', 'FLR', 'POST', 'HCP', 'IGT', 'ORCC', 'FIX', 'UFPI', 'MSA',
              'NFG', 'ENLC',
              'EXPO', 'SIM', 'CC', 'LANC', 'ALTR', 'VAL', 'WIX', 'OZK', 'DNB', 'RHP', 'PHI', 'OMF', 'SMCI', 'EXP',
              'NOVT', 'ELAN',
              'LNC', 'COKE', 'AQN', 'IDA', 'TRNO', 'ABG', 'GBCI', 'AXS', 'PRGO', 'SOFI', 'TAL', 'FFIN', 'NEWR', 'AM',
              'EVR', 'IONS',
              'FNB', 'WING', 'ONB', 'LNTH', 'SNDR', 'ENSG', 'APP', 'RIG', 'ESI', 'AUY', 'FOXF', 'BPOP', 'RUN', 'TENB',
              'THG', 'MMS',
              'TNET', 'RYN', 'DTM', 'THO', 'BEPC', 'HOMB', 'CIGI', 'NJR', 'INFA', 'SHC', 'ORA', 'WFRD', 'AAON', 'SID',
              'BIPC', 'MTSI',
              'WU', 'BFAM', 'AL', 'PENN', 'MDGL', 'MSM', 'WEN', 'KRG', 'WB', 'POWI', 'PSN', 'RMBS', 'CADE', 'DRVN',
              'VC', 'WK', 'NSP',
              'DUOL', 'ESNT', 'GPS', 'YPF', 'ASO', 'SMG', 'MSGS', 'APPF', 'RYAN', 'FIVN', 'SSD', 'R', 'SYNA', 'CBT',
              'IART', 'NSIT',
              'ASAI', 'KGC', 'IAC', 'AJRD', 'ITCI', 'DAVA', 'SEB', 'QLYS', 'LEG', 'DLO', 'FLS', 'HP', 'ALIT', 'ALKS',
              'JHG', 'DV', 'AYX',
              'TSEM', 'PDI', 'ALSN', 'FELE', 'KEX', 'ASGN', 'S', 'FN', 'NVEI', 'UAA', 'SRCL', 'HE', 'FIZZ', 'ATCO',
              'PTON', 'MGY',
              'PYCR', 'IPAR', 'CIG', 'MODG', 'MAN', 'GLBE', 'CERE', 'LPX', 'UMBF', 'WNS', 'OGS', 'RITM', 'BECN', 'DEN',
              'FRHC', 'MLI',
              'BCPC', 'FRSH', 'BRBR', 'KRC', 'BE', 'PNM', 'POR', 'DIOD', 'HRI', 'LPL', 'VNT', 'BXSL', 'HHC', 'SYNH',
              'HWC', 'BL', 'LTHM',
              'SEAS', 'TDOC', 'AVT', 'BOX', 'ACLS', 'ONTO', 'FCFS', 'W', 'FL', 'KNTK', 'SGRY', 'ADNT', 'AGI', 'TEX',
              'FRO', 'CNM', 'BKH',
              'XPO', 'ATHM', 'PWSC', 'TDC', 'AIMC', 'ICUI', 'DNP', 'TFSL', 'MTG', 'PECO', 'ACT', 'CWST', 'GTES', 'CPG',
              'BTU', 'CABO',
              'AVNT', 'NEOG', 'ELF', 'MMSI', 'SWX', 'ZWS', 'IRT', 'GEF', 'SAM', 'NSA', 'BHF', 'SKY', 'TRTN', 'KMPR',
              'AMN', 'FOUR',
              'SFBS', 'UA', 'MTH', 'NTLA', 'HAE', 'APLE', 'MAXR', 'GATX', 'TMHC', 'ESGR', 'CYTK', 'TGNA', 'BTG', 'PINC',
              'PEGA',
              'FUL', 'CRSP', 'EURN', 'QS', 'SM', 'NTCO', 'CUZ', 'CHPT', 'GOLF', 'OMAB', 'VNO', 'UCBI', 'EPRT', 'DNLI',
              'SMPL', 'ENS',
              'SFM', 'MEOH', 'PCH', 'WTM', 'UNF', 'CPA', 'SR', 'ZD', 'GDS', 'AFRM', 'DQ', 'ERF', 'FOLD', 'ESAB', 'LIFW',
              'BDC', 'CWEN',
              'AGO', 'LYFT', 'TKC', 'FIBK', 'SRAD', 'SGML', 'LITE', 'AZEK', 'EVH', 'INST', 'KD', 'LOPE', 'KWR', 'WIRE',
              'INDB', 'BXMT',
              'OLLI', 'IRTC', 'OI', 'STNG', 'SPR', 'BMI', 'JBT', 'QFIN', 'FHI', 'NCR', 'AEL', 'SANM', 'ARWR', 'SUM',
              'ALE', 'AWI',
              'CVT', 'ALVO', 'AEIS', 'PLTK', 'KOS', 'LTH', 'ASB', 'CNS', 'LAC', 'PI', 'JXN', 'MANU', 'FOCS', 'FSS',
              'NWE', 'DOC', 'TNL',
              'ENV', 'ATAT', 'RLX', 'PGNY', 'FHB', 'CRK', 'DRS', 'SPT', 'NEU', 'HI', 'NNI', 'CVI', 'ABCM', 'VIRT',
              'SEM', 'IBP', 'RDN',
              'SLM', 'BNL', 'PR', 'CVBF', 'TWNK', 'CERT', 'YETI', 'TIGO', 'ACAD', 'RUSHB', 'CALX', 'PACW', 'BHC',
              'LUMN', 'PCVX',
              'SIG', 'SPXC', 'ABCB', 'HL', 'ENIC', 'PRVA', 'MAIN', 'GOL', 'PTCT', 'AMBA', 'FLNC', 'GPI', 'LAZR', 'GT',
              'COOP',
              'ISEE', 'PAAS', 'NEA', 'ZGN', 'ABM', 'CBU', 'CRC', 'RNG', 'SXT', 'SQSP', 'AWR', 'PK', 'RARE', 'GH',
              'CRVL', 'BMBL',
              'ASAN', 'RUSHA', 'RETA', 'NWTN', 'TCBI', 'CCOI', 'HPK', 'MRCY', 'DOCN', 'EVO', 'JWN', 'AIN', 'GNW',
              'ESMT', 'AMC', 'AY',
              'KSS', 'CWAN', 'CWT', 'NGVT', 'OLPX', 'BAK', 'BCO', 'ENOV', 'CATY', 'PTEN', 'NOMD', 'HUBG', 'APPN',
              'PFSI', 'TR', 'WOR',
              'PPBI', 'EPR', 'LXP', 'HCM', 'KLIC', 'AXNX', 'AVA', 'VSCO', 'VSH', 'AZTA', 'WHD', 'PBH', 'PZZA', 'VIR',
              'IBOC', 'GHC',
              'FRPT', 'ACA', 'KFY', 'WSFS', 'BLKB', 'NARI', 'TRIP', 'TRMD', 'BOH', 'OTTR', 'WERN', 'BRZE', 'CCU',
              'HLNE', 'BANF', 'CNMD',
              'PSEC', 'KTB', 'CNO', 'TV', 'ROG', 'NCNO', 'VRNS', 'KBH', 'MSTR', 'ACIW', 'LCII', 'DORM', 'CRI', 'FLYW',
              'OFC', 'AMED',
              'DY', 'OLK', 'WD', 'AAWW', 'FULT', 'SHOO', 'INMD', 'CXM', 'ARRY', 'SSRM', 'SITM', 'AXSM', 'ARCH', 'CWK',
              'HIW', 'MCW',
              'RPD', 'SITC', 'ZIM', 'CALM', 'LBRT', 'SHLS', 'FWRD', 'HASI', 'AX', 'THS', 'SFNC', 'ARNC', 'OUT', 'AUB',
              'TFPM', 'JKS',
              'BRC', 'DNA', 'PRTA', 'AMBP', 'AEO', 'IFS', 'UGP', 'JJSF', 'PAGS', 'SBRA', 'BCC', 'AVAL', 'MMYT', 'NOG',
              'EBC', 'WOOF',
              'BEAM', 'MC', 'PROK', 'IBA', 'JOBY', 'INSM', 'PAGP', 'REZI', 'MXL', 'STAA', 'HELE', 'AMR', 'ZLAB', 'ABR',
              'SSTK', 'JBLU',
              'ETRN', 'MDC', 'SPB', 'GO', 'CSIQ', 'PLXS', 'CNX', 'PD', 'VRRM', 'MYOV', 'BKU', 'ENR', 'NAD', 'DADA',
              'RVNC', 'CVLT', 'TPG', 'SPWR', 'PDCO', 'STNE', 'CD', 'TMDX', 'FBP', 'XRX', 'NVMI', 'MAC', 'BPMC', 'FTDR',
              'JAMF', 'VVNT',
              'RRR', 'INTA', 'MRTX', 'MATX', 'URBN', 'MGEE', 'BOWL', 'HRMY', 'INSW', 'OMCL', 'ITRI', 'ITGR', 'DCT',
              'VTYX', 'IHS',
              'ALRM', 'PRFT', 'XPRO', 'CBZ', 'PRGS', 'KAI', 'RELY', 'IMCR', 'SONO', 'AGTI', 'UNFI', 'SBCF', 'SAGE',
              'WLY', 'CVCO',
              'CBRL', 'VRNT', 'MQ', 'NVG', 'OR', 'WLYB', 'TROX', 'DEI', 'LIVN', 'HAYW', 'TDW', 'CPE', 'GLNG', 'JOE',
              'CRS', 'MGRC', 'GLPG',
              'ULCC', 'ESE', 'PRMW', 'SBLK', 'YOU', 'ARCB', 'ERJ', 'GETY', 'EVTC', 'GMS', 'IIPR', 'TWKS', 'TPH', 'VSAT',
              'TNDM',
              'LGIH', 'FRME', 'TRUP', 'PSNYW', 'XENE', 'VIAV', 'BLMN', 'CSTM', 'RXO', 'WDFC', 'PAYO', 'MTRN', 'EXG',
              'SIX', 'GKOS', 'GBDC',
              'AMRC', 'UTF', 'EQC', 'VERX', 'FCPT', 'NHI', 'FFBC', 'SCL', 'AMK', 'EXTR', 'YY', 'NAVI', 'PAX', 'AI',
              'IBTX', 'FORM', 'ABCL',
              'ODP', 'FROG', 'KW', 'KMT', 'HSAI', 'BOOT', 'TEO', 'NPO', 'TGTX', 'COLB', 'LESL', 'CLBK', 'WAFD', 'LSPD',
              'SJW', 'DAN',
              'HLIO', 'APAM', 'RUM', 'TRN', 'CPK', 'TOWN', 'BB', 'VET', 'AMLX', 'SHO', 'FSR', 'SHAK', 'NUVA', 'ALG',
              'DNUT', 'NABL', 'EPC',
              'PACB', 'VNOM', 'SIMO', 'TAC', 'CENT', 'NEX', 'CSQ', 'HIMS', 'MGPI', 'CSWI', 'VCTR', 'AKRO', 'CLDX',
              'PSMT', 'IDCC',
              'BTE', 'OII', 'SLG', 'MWA', 'AVAV', 'WMK', 'GDRX', 'BANR', 'CORT', 'NEO', 'TCN', 'SDRL', 'CRCT', 'B',
              'SNEX', 'THRM', 'BVN',
              'KRYS', 'ZETA', 'CARG', 'WSBC', 'ITCB', 'MSGE', 'SUPN', 'GSAT', 'HCC', 'HTH', 'SAH', 'RVMD', 'FA', 'VICR',
              'NXE',
              'GFF', 'CENTA', 'YELP', 'QRTEB', 'HTLF', 'HTGC', 'SLVM', 'FGEN', 'VGR', 'GPRE', 'STRA', 'PRK', 'GOGL',
              'AHCO', 'GOGO', 'ICFI',
              'EFSC', 'AGYS', 'TALO', 'HBI', 'MYRG', 'LTRPB', 'PTVE', 'BFH', 'UTG', 'NUS', 'RKLB', 'MTX', 'NOVA',
              'CEIX', 'MRVI', 'HEES',
              'RVLV', 'RES', 'LGND', 'DOOR', 'PIPR', 'NTCT', 'SMTC', 'USM', 'CAKE', 'PCRX', 'HLF', 'CHGG', 'GOOS',
              'SKT', 'NMIH', 'RNST',
              'BKE', 'VRTV', 'CTRE', 'SAVE', 'WGO', 'RLAY', 'DBRG', 'PHR', 'DSEY', 'JBGS', 'PLAY', 'GDV', 'TTEC', 'GVA',
              'SGHC', 'NZF',
              'TBBK', 'ARHS', 'LILA', 'MIR', 'NG', 'LILAK', 'AIR', 'GGAL', 'HMY', 'TGLS', 'GOF', 'PEB', 'EVCM', 'PJT',
              'XNCR', 'DHT',
              'BGCP', 'CRTO', 'BROS', 'SWTX', 'ETWO', 'ACVA', 'VZIO', 'FTCH', 'ATUS', 'ZIP', 'CCS', 'FLNG', 'ENLT',
              'OXM', 'ALGT', 'RLJ',
              'ADX', 'STR', 'TDCX', 'ETY', 'QTWO', 'NUV', 'EMBC', 'LRN', 'MCY', 'JACK', 'BATRA', 'PAM', 'LAUR', 'DRH',
              'DK', 'SILK', 'PLRX',
              'CMTG', 'SVC', 'STEP', 'BORR', 'ATRC', 'MYGN', 'MRTN', 'UE', 'LFST', 'LKFN', 'MLKN', 'BATRK', 'MEI',
              'BUR', 'EYE', 'SAFE',
              'CSGS', 'BMEZ', 'NTB', 'ADUS', 'ROIC', 'BIGZ', 'TRMK', 'MOMO', 'COHU', 'SDGR', 'AVDX', 'EXPI', 'CVAC',
              'PARR', 'TASK',
              'ESTA', 'XPEL', 'ATGE', 'AMPH', 'GET', 'FORG', 'CTOS', 'EGO', 'IRWD', 'SSU', 'CVII', 'NWBI', 'KYMR',
              'IMKTA',
              'PFS', 'CRSR', 'EAT', 'EVT', 'ARCO', 'NAPA', 'GAB', 'CNNE', 'FBK', 'AROC', 'NBTB', 'AG', 'AMEH', 'BRP',
              'SBH', 'LNN',
              'VCYT', 'INT', 'TGS', 'BDJ', 'TCBK', 'HLMN', 'FSLY', 'SYBT', 'RQI', 'FBNC', 'XHR', 'VIST', 'NWN', 'SATS',
              'BCRX',
              'BCAT', 'SKIN', 'NVEE', 'EVRI', 'EVEX', 'ROCK', 'GSBD', 'PRAA', 'AUR', 'PATK', 'CLM', 'MORF', 'SNDX',
              'NUVL', 'BBIO',
              'PTY', 'PRCT', 'FCF', 'ATEC', 'USA', 'MHO', 'IVT', 'HURN', 'IAS', 'CNK', 'VSTO', 'CPRX', 'KTOS', 'HAIN',
              'ELME',
              'SABR', 'VRNA', 'COUR', 'CMP', 'BLDP', 'GTY', 'RNW', 'TNK', 'MDRX', 'MSC', 'SCHL', 'RCKT', 'OEC', 'ARI',
              'COMM',
              'CLS', 'MNRO', 'EPAC', 'NRDS', 'OSIS', 'ARVN', 'INFN', 'NAC', 'RAMP', 'ATSG', 'AGM', 'LZ', 'PRME', 'OCSL',
              'UPWK', 'TWO',
              'CAAP', 'TSLX', 'ANDE', 'RVT', 'KN', 'ENVA', 'SAND', 'JBI', 'FDP', 'STEL', 'CRDO', 'BNRE', 'ECAT', 'KROS',
              'ERO', 'GCMG', 'NBHC', 'PLYA', 'AAT',
              'PERI', 'KAR', 'PLMR', 'RXRX', 'HOPE', 'PDO', 'AMPL', 'VVX', 'RNA', 'BTT', 'ESTE', 'GPOR', 'HKD', 'HMN',
              'PRIM', 'SEAT', 'WABC', 'UTZ', 'DICE',
              'JPS', 'LOB', 'GNL', 'VRTS', 'TH', 'TY', 'PLUS', 'KEN', 'SUMO', 'NXT', 'LVWR', 'ROAD', 'TGH', 'LTC',
              'FINV', 'FVRR', 'BRFS', 'RYTM', 'KDNY',
              'SWI', 'RYI', 'CODI', 'NBR', 'UCTT', 'CIM', 'CHCO', 'EAF', 'SFL', 'GRBK', 'STBA', 'FNA', 'DNOW', 'VCEL',
              'SASR', 'ETV', 'VRE', 'BBUC',
              'MATV', 'OFG', 'HLIT', 'CGAU', 'WRBY', 'VBTX', 'ANF', 'MGNI', 'SXI', 'TVTX', 'ALHC', 'EVOP', 'CTS',
              'MNTK', 'IE', 'MCRI', 'BSTZ', 'LADR',
              'RADI', 'NMRK', 'PDFS', 'BXMX', 'ALKT', 'DDD', 'UPST', 'AVTA', 'LZB', 'AKR', 'OCFC', 'MODV', 'TFIN',
              'DEA', 'ENVX', 'MSEX', 'TTMI', 'IMVT',
              'ALEX', 'TDS', 'VLRS', 'PRM', 'CASH', 'DAWN', 'EGBN', 'AGIO', 'SPCE', 'EVBG', 'HBM', 'UEC', 'MMI', 'TNC',
              'RDNT', 'WWW', 'ECVT', 'SOVO',
              'ACLX', 'ORLA', 'BUSE', 'WNC', 'USPH', 'UDMY', 'HIMX', 'AVNS', 'MOD', 'KRO', 'GB', 'MBIN', 'JWSM', 'KFRC',
              'HNI', 'CMRE', 'OTLY',
              'KALU', 'HTLD', 'VRDN', 'NMFC', 'ADTN', 'MD', 'PGTI', 'INDI', 'FCEL', 'AAC', 'CHEF', 'DVAX', 'MBC',
              'BHLB', 'MLNK', 'BMA', 'SLN', 'HPP',
              'TMCI', 'STER', 'COMP', 'HYT', 'DO', 'HLX', 'GERN', 'OLO', 'TRS', 'UVV', 'MODN', 'RCUS', 'AVID', 'CARS',
              'PX', 'CTKB', 'AUPH', 'REPL', 'MNKD',
              'MAG', 'STEM', 'STRL', 'ERII', 'LBAI', 'TA', 'CAMT', 'PRG', 'KYN', 'DSL', 'TLRY', 'ANGI', 'MBUU', 'ECPG',
              'SRCE', 'UNIT', 'PL',
              'RC', 'ETG', 'STEW', 'NOAH', 'DGII', 'DH', 'OMI', 'DAC', 'PRO', 'MED', 'SCLX', 'OFLX', 'EIG', 'ZUO',
              'DFIN', 'WDH', 'FREY', 'NXRT',
              'USNA', 'CLB', 'ESRT', 'SAFT', 'NXGN', 'SBSI', 'MATW', 'VERV', 'ADPT', 'GES', 'NSSC', 'DCOM', 'SPNS',
              'EVV', 'PBT', 'MEG', 'IRBT', 'FIGS', 'SPNT', 'DCBO', 'DRQ', 'CNXN', 'SNCY', 'DFH', 'NVRO', 'OBNK', 'PMT',
              'DIN', 'DOLE', 'BGS', 'GABC', 'AIV', 'DAO', 'TARO', 'EQX', 'SEMR', 'GDEN', 'MCG', 'LMAT', 'LXU', 'IOVA',
              'SBR', 'PDM', 'PLL', 'FRG', 'STC', 'PSFE', 'BRKL', 'NFJ', 'CFFN', 'TTGT', 'GSHD', 'NRC', 'NMZ', 'ASIX',
              'CLBT', 'DCPH', 'ALTI', 'BYND', 'PGRE', 'RILY', 'IAG', 'ASTE', 'HERA', 'CXW', 'NTST', 'ATEN', 'PAY',
              'GEO', 'JELD', 'CGC', 'HOLI', 'GRND', 'CENX', 'VECO', 'PTLO', 'NIC', 'FBRT', 'HUYA', 'QQQX', 'ALX',
              'SBGI', 'TMP', 'NKLA', 'FPF', 'CRNC', 'OM', 'GOTU', 'PLAB', 'CYRX', 'ALLG', 'ME', 'TBLA', 'ZNTL', 'PTA',
              'CMCO', 'NAAS', 'JBSS', 'NAMS', 'PRA', 'ACDC', 'PUMP', 'OSCR', 'EQRX', 'GIC', 'MFA', 'NVGS', 'AXL', 'MGI',
              'APPS', 'FORTY', 'MUC', 'NEXT', 'CLNE', 'AMPS', 'MLTX', 'GTN', 'CRNX', 'DNN', 'BBN', 'IMAX', 'INNV',
              'ASLE', 'GBX', 'OSW', 'AFYA', 'SAVA', 'MNTV', 'TWST', 'AMSF', 'TITN', 'ADEA', 'SHIP', 'BSIG', 'WINA',
              'KC', 'RGNX', 'APOG', 'UUUU', 'ARKO', 'BBAR', 'KIDS', 'RGR', 'ARGO', 'AZZ', 'LMND', 'CHCT', 'ENTA', 'BST',
              'BANC', 'INBX', 'SES', 'ATRI', 'RNP', 'RIOT', 'RAPT', 'KRNT', 'GDOT', 'ARR', 'BDN', 'PFBC', 'SSP', 'BTZ',
              'SKYW', 'DDL', 'FLGT', 'YEXT', 'CET', 'STGW', 'LICY', 'LC', 'PWP', 'QURE', 'GENI', 'NWLI', 'CDMO', 'CUBI',
              'BHVN', 'HCSG', 'CCRN', 'SLCA', 'BLFS', 'AMCX', 'BFS', 'GSM', 'KREF', 'IMXI', 'SHEN', 'ZH', 'FSM', 'SPTN',
              'OXLC', 'HFWA', 'ARQT', 'PCT', 'RA', 'BLU', 'DCGO', 'BALY', 'CVNA', 'RKT', 'CNOB', 'CONX', 'FBMS', 'KRP',
              'SCRM', 'RDWR', 'GGR', 'CLFD', 'AMTB', 'PAR', 'CCF', 'MRC', 'MLAB', 'NAT', 'WBX', 'COCO', 'CEPU', 'PLYM',
              'SCHN', 'NYMT', 'ICHR', 'JRVR', 'APE', 'USLM', 'AMYT', 'RTL', 'PERF', 'MOND', 'CWH', 'RSKD', 'UMH', 'WOW',
              'PTRA', 'BY', 'CSR', 'BBDC', 'RPT', 'IMGN', 'CHY', 'AVPT', 'CAL', 'CDE', 'IBRX', 'FWRG', 'ALBO', 'IONQ',
              'PRDO', 'STKL', 'SHYF', 'GAM', 'CMPR', 'HSKA', 'NVTS', 'QNST', 'SA', 'THR', 'EGLE', 'OPK', 'SYM', 'SII',
              'SG', 'BCX', 'SSYS', 'EB', 'COLL', 'PRLB', 'AMWD', 'LPG', 'HIBB', 'SCS', 'VKTX', 'NRK', 'UFPT', 'AGRO',
              'ALLO', 'ACCD', 'QCRH', 'SNPO', 'MRUS', 'PNTM', 'COGT', 'IGMS', 'RBCAA', 'WT', 'IESC', 'EFXT', 'APGB',
              'KNSA', 'PEBO', 'HWKN', 'PFC', 'VTLE', 'ETW', 'YSG', 'CHI', 'NX', 'AHH', 'HRT', 'CDNA', 'MIRM', 'BTAI',
              'WALD', 'DSGR', 'WTTR', 'AWF', 'OSTK', 'IMOS', 'ASTL', 'SPRY', 'SNBR', 'UTL', 'HQH', 'PLOW', 'CNDT',
              'NHC', 'WEST', 'XMTR', 'AOD', 'SMP', 'BCSF', 'MQY', 'RWT', 'PRS', 'EFC', 'TMST', 'OPEN', 'HCCI', 'BHE',
              'TSE', 'EWCZ', 'ADV', 'CBL', 'TUYA', 'FFWM', 'ARCE', 'MUI', 'AMRN', 'WTI', 'BFC', 'CSII', 'MFIC', 'SLRC',
              'ACEL', 'INN', 'SXC', 'IDYA', 'NUTX', 'UVSP', 'AVO', 'GNK', 'BRSP', 'NEXA', 'TELL', 'EOS', 'TWI', 'ICPT',
              'ACRS', 'GPRO', 'WKME', 'MTTR', 'VALN', 'CDRE', 'NMM', 'THRY', 'SGH', 'OPI', 'HTD', 'ROCC', 'PNT', 'OPRA',
              'SCSC', 'CRAI', 'SILV', 'LPRO', 'PHAR', 'TGI', 'INTR', 'BLTE', 'CGBD', 'LOMA', 'CII', 'CRON', 'INVA',
              'CYH', 'MAXN', 'CCSI', 'SHCR', 'NBXG', 'VRAY', 'RICK', 'ULH', 'KARO', 'KURA', 'HSTM', 'GIII', 'LANV',
              'PDS', 'KOP', 'AC', 'DLX', 'PBI', 'ROVR', 'ADMA', 'VTRU', 'THQ', 'JPC', 'RDFN', 'IDT', 'EOCW', 'SLP',
              'NNDM', 'GRNT', 'GPRK', 'VTOL', 'SKWD', 'FFC', 'ANIP', 'MOV', 'VTNR', 'HCAT', 'BXC', 'CHS', 'AMBC',
              'EXAI', 'CBAY', 'PGRU', 'ASC', 'BJRI', 'RTC', 'PRTC', 'CTBI', 'IHRT', 'PTGX', 'AEHR', 'MYE', 'WE', 'THCH',
              'HY', 'AMWL', 'ETD', 'CBD', 'IGR', 'HGTY', 'GSL', 'CRF', 'AVXL', 'MEGI', 'MYI', 'SLAM', 'TXO', 'VSEC',
              'MARA', 'PRVB', 'CCO', 'MSDA', 'HZO', 'EHAB', 'XPOF', 'HTBK', 'CEVA', 'GMBL', 'OSBC', 'JQC', 'WDI',
              'VTEX', 'OFIX', 'BIOX', 'AOSL', 'BRY', 'MERC', 'GRC', 'DYN', 'EIM', 'EXFY', 'GHLD', 'UFCS', 'SLI', 'WASH',
              'KAMN', 'HAYN', 'HBT', 'CINT', 'UHT', 'RPAY', 'FPAC', 'AMAL', 'SCVL', 'MYTE', 'RBBN', 'HAFC', 'VREX',
              'BASE', 'FOR', 'LPSN', 'REVG', 'ENFN', 'GSBC', 'BOC', 'MBI', 'KIND', 'BMR', 'WPCB', 'VHI', 'ACHR', 'SP',
              'ASPN', 'ALEC', 'ANAB', 'MHUA', 'TRST', 'CTIC', 'CCVI', 'BLBD', 'PHK', 'NFBK', 'MLYS', 'AMRK', 'NRGX',
              'SANA', 'BIGC', 'MGIC', 'DX', 'AMOT', 'SIBN', 'MTW', 'MPLN', 'TWOU', 'UBA', 'TBPH', 'DENN', 'NXP', 'ETNB',
              'TNP', 'BLX', 'GNUS', 'INDT', 'DCO', 'TCPC', 'HSII', 'BCYC', 'PAXS', 'TRNS', 'DLY', 'BTO', 'QSG', 'SRG',
              'FAX', 'BRMK', 'ORGN', 'CFB', 'KRNY', 'CHUY', 'PGC', 'JANX', 'HSC', 'IMTX', 'OSPN', 'GHIX', 'HONE',
              'LGST', 'VITL', 'NFGC', 'CASS', 'HBNC', 'FC', 'CFIV', 'FLWS', 'PAHC', 'SCWX', 'ALCC', 'JOUT', 'VMEO',
              'CUTR', 'CLW', 'CSWC', 'EH', 'ATNI', 'NDMO', 'PTSI', 'MCRB', 'PUBM', 'GMRE', 'BBSI', 'BVH', 'BOE', 'HFRO',
              'FMBH', 'FSNB', 'KVSC', 'FORR', 'ACQR', 'DRD', 'TRTX', 'MAX', 'REPX', 'VMO', 'STAR          ', 'LWLG',
              'RUTH', 'BKD', 'PDT', 'EOI', 'ZEUS', 'PCN', 'DBI', 'LEU', 'AVD', 'KELYB', 'KRUS', 'OIS', 'KELYA', 'KE',
              'TK', 'MCB', 'CSTL', 'UBP', 'SBOW', 'MHD', 'SRI', 'VVR', 'MCFT', 'YORW', 'EGHT', 'ALTG', 'VCSA', 'BROG',
              'ACRE', 'VECT', 'TBI', 'HIFS', 'CCBG', 'YALA', 'LAND', 'CLDT', 'NMCO', 'RMGC', 'RGP', 'MUJ', 'EWTX',
              'NYAX', 'CATC', 'ACMR', 'EDIT', 'HVT', 'VPG', 'ITOS', 'GDYN', 'CPF', 'PFN', 'CAC', 'NESR', 'BAER', 'OBE',
              'CCB', 'QRTEA', 'CION', 'HOUS', 'AMLI', 'AIO', 'BV', 'NID', 'IIIN', 'ALT', 'EBS', 'HCKT', 'LBC', 'FDMT',
              'AGEN', 'NVAX', 'LYEL', 'CCD', 'MSBI', 'LDP', 'REX', 'CIR', 'FATE', 'ARDX', 'FPI', 'MOR', 'PML', 'AVDL',
              'UVE', 'VNET', 'CVGW', 'DM', 'TRVG', 'IIIV', 'BW', 'BHK', 'MRSN', 'GCO', 'FMNB', 'VAQC', 'LANDM', 'CALT',
              'ZING', 'TIPT', 'TIGR', 'WRLD', 'ATEX', 'CRGY', 'FFIC', 'BIT', 'IIM', 'BME', 'PRPC', 'SVM', 'GGN', 'EBF',
              'GRRR', 'EE', 'AVTE', 'RERE', 'IAUX', 'BH', 'BGY', 'DXPE', 'HA', 'WIW', 'EVC', 'NKX', 'TYRA', 'CMBM',
              'CRMT', 'DIAX', 'EXK', 'RYAM', 'HROW', 'MBWM', 'SKYT', 'PEO', 'EMD', 'NIE', 'IRS', 'SLDP', 'SD', 'SOUN',
              'TRMR', 'TRAQ', 'YTPG', 'TILE', 'AORT', 'ECC', 'VINP', 'KALA', 'DWAC', 'HLVX', 'DGNU', 'EBIX', 'PFLT',
              'RWAY', 'LX', 'ANZU', 'GOOD', 'HHLA', 'INVZ', 'CECO', 'CARA', 'DHIL', 'AGX', 'AGAC', 'VTS', 'SGHT',
              'ARTNA', 'VLD', 'ACCO', 'THFF', 'EGY', 'VGM', 'THW', 'POWL', 'SFIX', 'PLCE', 'ETJ', 'TCVA', 'AMPX',
              'GHRS', 'PDOT', 'BOOM', 'VKQ', 'BLUE', 'SMR', 'DPG', 'DOMO', 'NSTD', 'SNRH', 'NTGR', 'FTHY', 'SMBC',
              'AUDC', 'CHRS', 'TRC', 'TGB', 'TLGA', 'MBAC', 'FRPH', 'LND', 'SJT', 'GTX', 'NSTC', 'ATRO', 'ERAS', 'FCBC',
              'MTLS', 'EOLS', 'FDUS', 'LASR', 'VVI', 'BLNK', 'MCBS', 'IONR', 'BLE', 'GUT', 'COOL', 'DGICA', 'CLOV',
              'BFST', 'CCNE', 'NVX', 'PACK', 'ALLK', 'SMRT', 'NPK', 'FARO', 'TERN', 'SOHU', 'NSTB', 'IQI', 'BGB',
              'HTBI', 'XPER', 'BUI', 'PLPC', 'CSV', 'IBEX', 'SMWB', 'AROW', 'SWBI', 'VALU', 'EZPW', 'MCS', 'DGICB',
              'MYD', 'LEGH', 'GBTG', 'SIGA', 'BMRC', 'HYLN', 'ANGO', 'TETC', 'LHC', 'TBLD', 'ZYME', 'MYPS', 'SGMO',
              'MMD', 'PGY', 'GUG', 'IRMD', 'CCAP', 'JFR', 'BELFA', 'MPB', 'LEV', 'BLW', 'TPIC', 'OPY', 'OABI', 'OLP',
              'SLGC', 'CERS', 'DDI', 'APEN', 'CVLG', 'HPS', 'RXT', 'RMR', 'NBB', 'FSBC', 'LQDA', 'GHY', 'HMST', 'CMPX',
              'NXJ', 'COOK', 'TRIN', 'MESO', 'MDXG', 'MOFG', 'GCBC', 'ATLC', 'IRON', 'BZH', 'CEM', 'WSR', 'AMSWA',
              'BRLT', 'ATCX', 'EQBK', 'ESPR', 'MXCT', 'SNDL', 'FSRX', 'IBCP', 'BHIL', 'HDSN', 'ITRN', 'PROC', 'ANIK',
              'AZUL', 'HCVI', 'SMBK', 'ONL', 'BELFB', 'OCUL', 'OSUR', 'CMTL', 'HCI', 'GAIN', 'DSU', 'ZUMZ', 'SGU',
              'PNTG', 'BHB', 'ICNC', 'VCV', 'NOA', 'METC', 'VLN', 'TWLV', 'NXDT', 'IVCB', 'CPAA', 'FNKO', 'BFAC', 'SB',
              'TTI', 'JPI', 'CAN', 'TNGX', 'BFLY', 'LOCO', 'PSPC', 'PSTX', 'GHG', 'BFK', 'NSTG', 'SRRK', 'MTVC', 'CGEM',
              'FACT', 'EDAP', 'SPFI', 'RMNI', 'FRXB', 'CPSI', 'HPI', 'RXST', 'ROSS', 'RONI', 'LEGA', 'NFYS', 'GIM',
              'TRTL', 'SSTI', 'TIOA', 'CRESY', 'MVF', 'FMIV', 'PTOC', 'VORB', 'ZTR', 'TPC', 'MMU', 'EBTC', 'BBCP',
              'UWMC', 'ACRO', 'LITT', 'LXFR', 'PRPL', 'MPX', 'ACAH', 'GFX', 'RPTX', 'EVER', 'CPAC', 'ZT', 'TPVG', 'RMT',
              'NPFD', 'TWNI', 'IPI', 'NRGV', 'ABST', 'AMRS', 'TSVT', 'IVR', 'BRDG', 'ACRV', 'ABUS', 'SLAC', 'NRIX',
              'GEVO', 'MX', 'STK', 'RDIB', 'ALDX', 'AKYA', 'BIRD', 'SENEA', 'DTOC', 'LOVE', 'LUNG', 'BCSA', 'FRA',
              'ORC', 'BYTS', 'ARL', 'IGD', 'IFN', 'DOYU', 'LYTS', 'NVTA', 'VCXB', 'SLQT', 'BIG', 'CLAA', 'GCI', 'NR',
              'RSVR', 'CTLP', 'EVLV', 'VIGL', 'TPB', 'INSE', 'SCWO', 'AVK', 'CARE', 'NQP', 'SENEB', 'ISD', 'LGO',
              'ARCT', 'NEWP', 'MITK', 'OUST', 'CYXT', 'LQDT', 'BAND', 'LXRX', 'DESP', 'TARS', 'TREE', 'NETI', 'KVSA',
              'DFP', 'PLMI', 'FANH', 'SKE', 'CMAX', 'GSRM', 'NUVB', 'AVNW', 'HCMA', 'CTO', 'DJCO', 'NMAI', 'EVTL',
              'ASTS', 'BRT', 'NGMS', 'BWB', 'CNCE', 'PMTS', 'EAD', 'HCNE', 'DHCA', 'EVGO', 'DSX', 'MUA', 'ENTF', 'HOV',
              'TG', 'MVIS', 'EDN', 'CSTA', 'BMEA', 'ALRS', 'PETS', 'EVN', 'AGGR', 'ONEW', 'NML', 'BRKH', 'ESM', 'RRAC',
              'SCPL', 'IGIC', 'GPAC', 'SST', 'BBAI', 'PMO', 'KRNL', 'AHRN', 'MYN', 'GRVY', 'CHW', 'QTRX', 'AEVA',
              'DMRC', 'ACAB', 'NWPX', 'EMO', 'JUN', 'ETB', 'MBSC', 'BWMN', 'NEWT', 'TSP', 'SWIM', 'DXLG', 'BNGO',
              'BZUN', 'CIFR', 'LEO', 'FG', 'FSD', 'BWMX', 'DISA', 'GNLX', 'HIO', 'ONTF', 'KZR', 'AAN', 'PUYI', 'HIPO',
              'GXII', 'LAW', 'FF', 'SDHY', 'TRDA', 'RBB', 'MVST', 'FULC', 'FLIC', 'REI', 'FISI', 'GOGN', 'AMPY', 'VKI',
              'AURA', 'PWUP', 'ESQ', 'TCI', 'ALVR', 'GBAB', 'MCBC', 'HORI', 'PEPG', 'CXAC', 'ATXS', 'IPVI', 'CSTR',
              'GLDD', 'APTM', 'GLAD', 'XPDB', 'NVEC', 'GNTY', 'SPKB', 'PHAT', 'PNNT', 'ESAC', 'CVEO', 'LCAA', 'MGTX',
              'TYG', 'FLME', 'NGM', 'TDF', 'DSGN', 'ARRW', 'PPT', 'ARIS', 'BGR', 'ALPN', 'LGVC', 'GGAA', 'RRBI', 'MGNX',
              'HPF', 'WPCA', 'DSKE', 'EGRX', 'WLFC', 'HQL', 'CRBU', 'RGC', 'NETC', 'API', 'NNOX', 'ATEK', 'EVE', 'VOR',
              'STRE', 'WVE', 'AURC', 'NFNT', 'FWAC', 'ADER', 'JMSB', 'ETO', 'KCGI', 'FEI           ', 'BMAC', 'PACI',
              'ADEX', 'FMAO', 'WSBF', 'AWP', 'INGN', 'MSB', 'ATRA', 'CNDA', 'THRX', 'KPTI', 'CASA', 'VNDA', 'VGAS',
              'JUGG', 'NL', 'SMTI', 'PFIS', 'EM', 'PRTS', 'BLEU', 'BLUA', 'AMNB', 'IMAB', 'BACA', 'MRNS', 'EFT', 'EMLD',
              'EFR', 'WTBA', 'FTEV', 'KMF', 'BLND', 'PMGM', 'STOK', 'CLAR', 'GAMB', 'FTPA', 'CNSL', 'VMD', 'BRW',
              'CZNC', 'LVRA', 'IRAA', 'CMPS', 'HIX', 'WEAV', 'SPWH', 'BFZ', 'AXGN', 'ACAQ', 'STIX', 'CIVB', 'RKTA',
              'IVCA', 'SPCM', 'CIO', 'MVBF', 'RFI', 'SHBI', 'PKE', 'JRO', 'PEGR', 'SLND', 'BRCC', 'FLL', 'MTAL', 'PUCK',
              'NIU', 'KTF', 'NINE', 'DOUG', 'LLAP', 'RFMZ', 'BLFY', 'IPVF', 'NCV', 'HT', 'MHLD', 'CZFS', 'NBN', 'STRO',
              'FFA', 'MUX', 'RCEL', 'DHC', 'RAIN', 'UTMD', 'PFTA', 'GFGD', 'RANI', 'JRI', 'BNR', 'UIS', 'RMAX', 'VLGEA',
              'INO', 'FCUV', 'MIY', 'VPCB', 'ARBE', 'CYD', 'GILT', 'RKDA', 'SAR', 'NRDY', 'FUBO', 'HBCP', 'PMM', 'FINS',
              'CNTA', 'LUNA', 'UONE', 'ORGO', 'BYN', 'DNAD', 'GLRE', 'KOD', 'BLDE', 'ODV', 'DNAB', 'NAN', 'VSTA',
              'NPAB', 'SMMF', 'OOMA', 'ARLO', 'DZSI', 'MIN', 'CLIN', 'VERA', 'FNLC', 'OIA', 'RBOT', 'LDI', 'QUOT',
              'LUNR', 'LOKM', 'AUTL', 'JGGC', 'CAF', 'RCLF', 'SFST', 'CPZ', 'AFCG', 'MLR', 'SVII', 'AFTR', 'LPTV',
              'SLVR', 'OBIO', 'SOR', 'SCAQ', 'MHN', 'OSG', 'HWEL', 'SBT', 'CPUH', 'JMIA', 'NATH', 'KRT', 'ACNB', 'PETQ',
              'NPCT', 'STET', 'ZFOX', 'TIG', 'HUMA', 'ICVX', 'GROY', 'FOF', 'SRDX', 'AIRS', 'CNGL', 'OPRX', 'HUT',
              'VMGA', 'WHF', 'NRAC', 'HRZN', 'DMYS', 'CDXS', 'PFL', 'INAQ', 'VEL', 'BSRR', 'SOI', 'BHR', 'HZON', 'THCP',
              'BIOS', 'OBT', 'GATO', 'VRCA', 'GNE', 'NMG', 'HLTH', 'USCT', 'MEKA', 'TOAC', 'FEAM', 'CITE', 'SMHI',
              'HQI', 'RMM', 'CORS', 'PLAO', 'RENE', 'PANL', 'VERU', 'TGR', 'FET', 'RLYB', 'AMTD', 'BTWN', 'GPMT',
              'WNNR', 'SVFB', 'FIP', 'BGRY', 'IRRX', 'MPRA', 'SOL', 'BBW', 'AFRI', 'DSAQ', 'RCFA', 'TLGY', 'AFB',
              'FRON', 'KNSW', 'CVCY', 'GWRS', 'CMCA', 'DPCS', 'SVNA', 'NRIM', 'ITIC', 'CBRG', 'SCUA', 'CANO', 'EDD',
              'UTAA', 'RELL', 'OMGA', 'XFIN', 'FIAC', 'PORT', 'AEAE', 'BRD', 'VII', 'WWAC', 'TRIS', 'IXAQ', 'SCM',
              'LCW', 'FBIZ', 'BYM', 'HYZN', 'VLAT', 'WKHS', 'RM', 'TROO', 'WRAC', 'ASG', 'GLUE', 'LDHA', 'FTCI', 'PGSS',
              'NODK', 'PBFS', 'AMRX', 'VMCA', 'MASS', 'BCBP', 'IVCP', 'QD', 'FRGE', 'VAXX', 'NN', 'TCMD', 'MLEC', 'SY',
              'MCR', 'MEC', 'PRTH', 'ARDC', 'CBNK', 'FRST', 'EGGF', 'SVRA', 'NCA', 'RJAC', 'RDVT', 'CURV', 'EP', 'PSTL',
              'LMDX', 'ASA', 'AVIR', 'FZT', 'ASRT', 'FRSG', 'PHVS', 'KODK', 'PGEN', 'NKTR', 'SKYA', 'MGU', 'PRLD',
              'MCI', 'TWOA', 'HAIA', 'XPAX', 'UNTY', 'NC', 'JILL', 'LMNR', 'GRIN', 'TGAA', 'CREC', 'DSM', 'ROC', 'VYGR',
              'LSAK', 'FDBC', 'NWFL', 'EU', 'CDZI', 'LSEA', 'HRTX', 'EOT', 'UP', 'SIFY', 'VCXA', 'STKS', 'HYI', 'FSBW',
              'SPXX', 'ERC', 'JGH', 'WAVC', 'CPS', 'TSBK', 'CVGI', 'CNTY', 'RLGT', 'RIGL', 'IFIN', 'DBVT', 'RNGR',
              'ARAY', 'VOXX', 'CCRD', 'NDLS', 'NAUT', 'TRCA', 'MMT', 'SKGR', 'BKCC', 'AVAC', 'CDAQ', 'ASUR', 'BGH',
              'BSVN', 'SHAP', 'EGIO', 'WINT', 'ODC', 'KALV', 'PCB', 'NREF', 'SATL', 'AEF', 'OTLK', 'PIII', 'PMVP',
              'OCFT', 'ENER', 'FEN', 'IQMD', 'ADAP', 'TMC', 'IQMDU', 'QUAD', 'PMX', 'AADI', 'LRMR', 'BITE', 'ADCT',
              'HNST', 'PHYT', 'DBD', 'ASCB', 'BKT', 'PMF', 'NOTE', 'ILPT', 'APAC', 'TLS', 'WW', 'GTAC', 'GVCI', 'IPSC',
              'ALXO', 'LE', 'GEEX', 'FRBA', 'BCML', 'ATAK', 'GTACU', 'SMIH', 'MLAI', 'EEX', 'BGT', 'SCPH', 'CRZN',
              'PRLH', 'ARTE', 'ATAI', 'GRWG', 'DCFC', 'ATNM', 'MKFG', 'DALS', 'TUSK', 'FTF', 'FCT', 'PROF', 'PLM',
              'SILC', 'TLYS', 'FUND', 'SEDA', 'SAMG', 'SEER', 'EVI', 'MPAA', 'OPA', 'ANNX', 'ORIA', 'SKYX', 'TBSA',
              'FICV', 'HNRG', 'QSI', 'HPLT', 'DTC', 'REFI', 'III', 'MXF', 'BWC', 'BGSX', 'BNY', 'RSI', 'LOCC', 'NECB',
              'HLLY', 'RCS', 'USCB', 'APLD', 'PINE', 'CGNT', 'VUZI', 'REAX', 'SUPV', 'CELC', 'KLTR', 'KBAL', 'EGAN',
              'WEYS', 'NUW', 'THRN', 'TEI', 'UTI', 'SSBK', 'WRN', 'PSF', 'NHIC', 'NVAC', 'FLJ', 'BYNO', 'NGVC', 'BOCN',
              'XOMA', 'GWH', 'NKSH', 'AGS', 'UONEK', 'CSLM', 'IMMR', 'PLBC', 'PKBK', 'FSP', 'TCBX', 'HOFT', 'SELB',
              'INBK', 'XFLT', 'URG', 'ORRF', 'URGN', 'CMCL', 'FENC', 'AMAM', 'CCCC', 'AKTS', 'SWKH', 'DNMR', 'CWCO',
              'IPHA', 'CVLY', 'CFFS', 'MYFW', 'RGCO', 'PANA', 'RIDE', 'OB', 'VZLA', 'VATE', 'WLDN', 'FHTX', 'CABA',
              'UROY', 'VPV', 'TSI', 'RDW', 'BARK', 'JRS', 'NCZ', 'VERI', 'OPAL', 'GBIO', 'FVCB', 'PFMT', 'TCX', 'DBL',
              'CHMG', 'EHTH', 'OCN', 'FOSL', 'ALOR', 'KFS', 'BWFG', 'SI', 'SKIL', 'BRBS', 'CPSS', 'SWSS', 'OMER',
              'DRTS', 'OCEA', 'CIX', 'MQT', 'KIO', 'OXUS', 'BKSY', 'OPT', 'BPT', 'SEPA', 'MVT', 'YRD', 'BIVI', 'FIF',
              'HIVE', 'SCU', 'AXAC', 'APCA', 'POWW', 'FNVT', 'TCS', 'PPTA', 'PDLB', 'CTRN', 'APXI', 'NUO', 'TWCB',
              'GBBK', 'TTSH', 'JYNT', 'QIPT', 'MNTN', 'OVLY', 'CVRX', 'BRIV', 'BOAC', 'YI', 'CAAS', 'KNOP', 'TCFC',
              'ITAQ', 'EPM', 'AGIL', 'TOUR', 'KNTE', 'KSI', 'WNEB', 'MUE', 'PTMN', 'RENT', 'GNFT', 'TCOA', 'CRGO',
              'AVAH', 'IVA', 'ALTO', 'OCGN', 'NGC', 'BPRN', 'HGLB', 'VFL', 'MNSB', 'ANTX', 'AZRE', 'CLBR', 'ATLO',
              'MOLN', 'CBAN', 'GFOR', 'FGBI', 'NKTX', 'ABOS', 'RIV', 'LVOX', 'EMX', 'PEPL', 'HMPT', 'SLNA', 'BSAQ',
              'EVM', 'SCD', 'COFS', 'FUSN', 'IIF', 'RCAC', 'DC', 'HFFG', 'TNYA', 'GLO', 'PBPB', 'AENZ', 'CALB', 'ACV',
              'SAMA', 'CTR', 'EVBN', 'LMST', 'VABK', 'BCOV', 'RAD', 'BKN', 'AACI', 'JSPR', 'GENC', 'MTA', 'TBNK',
              'LCTX', 'NPV', 'AFT', 'FRGI', 'CTV', 'PRQR', 'MFM', 'PCYO', 'GER', 'GRPN', 'CONN', 'JAQC', 'TGAN', 'SPOK',
              'CCAI', 'JCE', 'PHT', 'FDEU', 'CFFI', 'DHX', 'FXLV', 'EOD', 'VBNK', 'TRUE', 'TELA', 'ESSA', 'ROSE', 'GCT',
              'WIA', 'DLTH', 'DMB', 'ITI', 'OPTN', 'LCNB', 'BNNR', 'GHL', 'CLOE', 'LGI', 'ATAQ', 'CLPT', 'TWN', 'APEI',
              'PRCH', 'NTG', 'HURC', 'ACIU', 'ARYD', 'NATR', 'CATO', 'DHY', 'HIE', 'ELA', 'IHIT', 'MFIN', 'LIAN',
              'KMDA', 'OPRT', 'INFU', 'VTN', 'CLSK', 'RCKY', 'ARYE', 'ALPA', 'ISTR', 'GRTS', 'PAYS', 'MHI', 'NBH',
              'IVH', 'PCK', 'ETX           ', 'PDSB', 'GLSI', 'ALCO', 'MIXT', 'CLMB', 'JOF', 'PCQ', 'XERS', 'BGFV',
              'MITA', 'STXS', 'INOD', 'MCAA', 'PEBK', 'KVHI', 'ACTG', 'MAV', 'APMI', 'SGC', 'IVVD', 'JWAC', 'PWOD',
              'ABSI', 'NSL', 'CANG', 'AOMR', 'AJX', 'ERES', 'UFI', 'BZFD', 'BLZE', 'GDO', 'KRMD', 'JAKK', 'GLTA',
              'LTRX', 'NOTV', 'POET', 'AIF', 'GSQB', 'HBB', 'ACP', 'WPRT', 'DAKT', 'EMF', 'AXTI', 'MRBK', 'VBF', 'BYRN',
              'BBBY', 'IVAC', 'STTK', 'GTHX', 'DIBS', 'ETAO', 'MLP', 'MIO', 'JATT', 'BGXX', 'FT', 'MBCN', 'HPX', 'PBYI',
              'IGI', 'MTRX', 'UPLD', 'OXSQ', 'CRMD', 'RRGB', 'EBAC', 'MRCC', 'STRS', 'AKA', 'BSL', 'BVS', 'XAIR',
              'ORIC', 'YMAB', 'PNRG', 'DFLI', 'TEAF', 'OVID', 'GRX', 'KITT', 'AIP', 'FLC', 'PKOH', 'ESCA', 'ZIMV',
              'ALYA', 'OPBK', 'SAL', 'WILC', 'KNDI', 'SMMT', 'GLDG', 'DLHC', 'THRD', 'LATG', 'LION', 'HWBK', 'CTGO',
              'VRA', 'PZC', 'NBST', 'NVCT', 'LFCR', 'OPP', 'EHI', 'MCN', 'WMPN', 'INSI', 'BSET', 'INMB', 'KLXE', 'CSTE',
              'CRGE', 'FRBN', 'SOPH', 'IH', 'ZVIA', 'CCTS', 'GLT', 'AHT', 'GOSS', 'GF', 'PTRS', 'INTT', 'ENX', 'LCUT',
              'GOCO', 'TRHC', 'NUBI', 'STBX', 'HYW', 'DHF', 'BEEM', 'MG', 'NHS', 'PIM', 'SEVN', 'GGT', 'UCL', 'CTXR',
              'TUP', 'NIQ', 'ELLO', 'OLMA', 'OHAA', 'RWOD', 'CBH', 'PVBC', 'CAMP', 'ARQQ', 'FNCB', 'AGFS', 'HYB', 'SUP',
              'INVE', 'ENCP', 'IDE', 'TETE', 'NNY', 'FTII', 'PTWO', 'MACK', 'RMBI', 'SAGA', 'TOP', 'GRPH', 'SMAP',
              'PIAI', 'NRO', 'EVGR', 'LIBY', 'PRAX', 'XYF', 'BMAQ', 'LINC', 'JFIN', 'KYCH', 'FORA', 'ASGI', 'OXAC',
              'FNWD', 'GLLI', 'BGI', 'RMBL', 'SRT', 'GMFI', 'UEIC', 'RNLX', 'ALSA', 'ZTEK', 'BDSX', 'SACH', 'CNF',
              'MSSA', 'MRDB', 'GHM', 'AMSC', 'BURU', 'TWIN', 'ROCL', 'CMT', 'EFHT', 'CMRX', 'WINV', 'MACA', 'AFAR',
              'FEXD', 'YOTA', 'TDUP', 'FATP', 'FCCO', 'PFD', 'CHEA', 'MPA', 'ANIX', 'WEL', 'ADRT', 'BSBK', 'LVAC',
              'TGVC', 'RFAC', 'ACET', 'SMLR', 'BGSF', 'RVSB', 'RDCM', 'AGBA', 'CIA', 'CRNT', 'FCRD', 'FPH', 'PLBY',
              'SNFCA', 'IMMP', 'IXHL', 'INTE', 'FPL', 'CHEK', 'TRVI', 'PFSW', 'ATOM', 'SPIR', 'CIK', 'KULR', 'RCMT',
              'PLG', 'STIM', 'BGX', 'SGA', 'CDLX', 'LAB', 'STG', 'ECBK', 'MVO', 'FRAF', 'OMIC', 'HEQ', 'OIIM', 'SJ',
              'SHUA', 'MHH', 'TKNO', 'HNVR', 'IGA', 'LMB', 'AE', 'YTRA', 'REVE', 'IKNA', 'AREN', 'EOSE', 'JMAC', 'MRAM',
              'OPOF', 'ADSE', 'EVG', 'CTMX', 'BCAB', 'EBMT', 'ESEA', 'GSD', 'REAL', 'MHF', 'ARC', 'IREN', 'MPV', 'CHMI',
              'ISSC', 'CTSO', 'NYXH', 'ADTH', 'JOAN', 'AOGO', 'VOC', 'GRCL', 'FNWB', 'BRAC', 'VSAC', 'ANVS', 'FFNW',
              'FSTR', 'FSFG', 'MOBV', 'QRHC', 'MLVF', 'FRLA', 'BANX', 'MNMD', 'LITB', 'OFED', 'GNSS', 'CFBK', 'BWG',
              'CHN', 'NGS', 'ASYS', 'IMRX', 'EPSN', 'AVHI', 'BATL', 'CWBC', 'OFS', 'IGTA', 'MSD', 'FLFV', 'LL', 'DHHC',
              'BFIN', 'SPE', 'MYNA', 'AKLI', 'MITT', 'FUNC', 'LIVB', 'EML', 'PRPH', 'UBFO', 'FREE', 'HEAR', 'NAZ',
              'LAZY', 'RMMZ', 'SGHL', 'GLST', 'KORE', 'CZWI', 'IOAC', 'GLG', 'XTNT', 'CDTX', 'LOOP', 'PXS', 'DMF',
              'BTA', 'DMO', 'CPHC', 'MVLA', 'PRE', 'JHS', 'MESA', 'GALT', 'AOUT', 'UXIN', 'ALTU', 'GMDA', 'TRON',
              'PSNL', 'DTIL', 'AREC', 'GNTA', 'AMTX', 'CUE', 'YELL', 'TBCP', 'OVBC', 'JSD', 'CBFV', 'TSQ', 'EAR', 'WEA',
              'GGE', 'FSTX', 'FRBK', 'CLLS', 'NBTX', 'KOPN', 'XNET', 'CAPR', 'LVLU', 'CTRM', 'FAT', 'LARK', 'NTIC',
              'VHC', 'FINW', 'HNRA', 'FMN', 'CDXC', 'BLI', 'PFO', 'RVLP', 'LNKB', 'MCAC', 'ASPS', 'PCYG', 'SQNS', 'AGD',
              'IAF', 'QMCO', 'AIB', 'CTG', 'BRID', 'DMTK', 'VACC', 'PCF', 'GENQ', 'WHG', 'ATHA', 'SBFG', 'SRL', 'PBHC',
              'UNB', 'ECF', 'INZY', 'VERY', 'LBPH', 'CDRO', 'ARAV', 'ACAX', 'PHD', 'NPCE', 'NIM', 'FATBB', 'FXNC',
              'MNP', 'VNRX', 'PAI', 'CRT', 'DRRX', 'TSAT', 'GLQ', 'MNK', 'CMCT', 'FLNT', 'MIST', 'GASS', 'DECA', 'DCF',
              'JHI', 'INCR', 'ONYX', 'CLGN', 'ELMD', 'ACAC', 'CURO', 'AKU', 'NRT', 'BCTX', 'MDWD', 'SLGL', 'IDBA',
              'HBIO', 'DBTX', 'SCOR', 'LEE', 'FONR', 'SZZL', 'VBOC', 'CPTK', 'EYEN', 'SONX', 'LFT', 'RGF', 'PCM', 'GIA',
              'STRM', 'GGZ', 'SBI', 'DRIO', 'KF', 'PRST', 'OPNT', 'APPH', 'TAST', 'LAKE', 'MNOV', 'GMGI', 'CXE', 'FLXS',
              'SSBI', 'GDL', 'SLDB', 'HOLO', 'LIFE', 'QFTA', 'BKKT', 'RMI', 'PHX', 'SERA', 'MGF', 'APYX', 'PIRS', 'BCV',
              'FGMC', 'VOXR', 'SCTL', 'ALLT', 'RBKB', 'CFFE', 'VCIF', 'SSSS', 'FLUX', 'CLPR', 'BNED', 'AFBI', 'WTMA',
              'DIT', 'CVM', 'ALPS', 'SUNL', 'SANG', 'PRSR', 'SRTS', 'HOWL', 'ACNT', 'SFBC', 'NEON', 'CLRC', 'ZEPP',
              'SKYH', 'HYPR', 'CMPO', 'SWZ', 'SMID', 'SATX', 'FLAG', 'XBIT', 'NKG', 'NXG', 'HITI', 'MNTX', 'TOI',
              'EMCG', 'PROV', 'WIMI', 'BTBT', 'MYNZ', 'RLMD', 'EVF', 'IHD', 'EARN', 'CHAA', 'BYFC', 'BNIX', 'NMT',
              'PWFL', 'PLSE', 'EYPT', 'HMNF', 'PLX', 'PRTK', 'ARMP', 'WRAP', 'ISDR', 'MDXH', 'ERH', 'NCAC', 'ANPC',
              'RFM', 'PRDS', 'INTG', 'EMBK', 'AAMC', 'LVO', 'CGO', 'KRON', 'IPA', 'DAVE', 'FOA', 'EXD', 'RZLT', 'MIMO',
              'LBBB', 'GNT', 'LIVE', 'CMLS', 'ETON', 'PESI', 'SNCR', 'ATY', 'HSPO', 'EPIX', 'ALOT', 'NEOV', 'NMI',
              'SND', 'ONCY', 'HMAC', 'GCV', 'HGBL', 'ELYM', 'CODX', 'KSM', 'DLA', 'DARE', 'MAYS', 'VWE', 'JLS', 'MAQC',
              'MDV', 'BKSC', 'BCAN', 'MAPS', 'ATER', 'OSI', 'VIA', 'VGI', 'BWEN', 'MLGO', 'GWII', 'FRD', 'IMAQ', 'XLO',
              'ATMC', 'LWAY', 'IMUX', 'FCAP', 'UBCP', 'CEN', 'FARM', 'CMU', 'ATLX', 'ORN', 'FTK', 'VBFC', 'PNAC', 'NXC',
              'HNW', 'PXLW', 'EAC', 'CIZN', 'SOTK', 'PYXS', 'CULL', 'UPXI', 'EMAN', 'FIXX', 'PED', 'CURI', 'PCCT',
              'CLNN', 'IFRX', 'GLU', 'AAIC', 'ACHV', 'BRAG', 'AQMS', 'EDF', 'MGYR', 'PCTI', 'ACU', 'TENK', 'STRT',
              'RPHM', 'ACR', 'ORMP', 'PET', 'MCHX', 'AUBN', 'PNI', 'AMST', 'VNCE', 'ONDS', 'PVL', 'USAP', 'TALS',
              'MTAC', 'BHM', 'GEOS', 'IPX', 'PGP', 'BWAC', 'PRT', 'USX', 'DEX', 'OSA', 'KINZ', 'FTHM', 'JPT', 'TPZ',
              'CJJD', 'SCX', 'NNBR', 'BSGA', 'NVCN', 'GLYC', 'TCRX', 'TZOO', 'AEYE', 'AIRG', 'ANEB', 'LTRPA', 'BCLI',
              'RDI', 'UIHC', 'REKR', 'RCAT', 'ARBK', 'BEDU', 'GDST', 'PPIH', 'HHS', 'ADAG', 'GAN', 'HOUR', 'MCAF',
              'SANW', 'WFCF', 'FATH', 'SNDA', 'AAOI', 'SPRO', 'ADES', 'EIGR', 'STCN', 'CODA', 'PLTN', 'SRV', 'SURG',
              'DTF', 'GLV', 'BAFN', 'CVV', 'CRDF', 'PFX', 'HYFM', 'CZOO', 'SMSI', 'VIRC', 'LNZA', 'IAE', 'LGVN', 'DPRO',
              'QUIK', 'MYMD', 'VIOT', 'VHAQ', 'LYRA', 'SYRS', 'PGZ', 'GECC', 'TCBC', 'OCUP', 'EPOW', 'HVBC', 'JHAA',
              'KTCC', 'VIAO', 'PBAX', 'CMCM', 'MKUL', 'JEQ', 'CLSD', 'AQU', 'HUIZ', 'TANH', 'NCNA', 'TACT', 'QUBT',
              'LUXH', 'ICAD', 'VLT', 'JZ', 'IHTA', 'AXR', 'CEV', 'MKTW', 'IPWR', 'CDIO', 'HSON', 'HEXO', 'CLST', 'HRTG',
              'ELBM', 'MFD', 'INKT', 'PNF', 'ASRV', 'BDTX', 'GEG', 'PASG', 'ASMB', 'NMS', 'PETZ', 'ATNF', 'LSBK',
              'CNTB', 'LPTH', 'CULP', 'DKDCA', 'ROOT', 'MMMB', 'BCOW', 'ALGS', 'GIFI', 'ACBA', 'VIRX', 'HNNA', 'CXH',
              'BSGM', 'SIEB', 'RGS', 'MURF', 'OESX', 'HCWB', 'AZYO', 'TSHA', 'NM', 'ARKR', 'LOAN', 'ULBI', 'GAIA',
              'IDR', 'LRFC', 'OMEX', 'HUGE', 'PRTG', 'RVP', 'RAIL', 'AVRO', 'SELF', 'FCO', 'UPTD', 'AIRT', 'CSBR',
              'AUGX', 'SNTI', 'RAM', 'REFR', 'AWIN', 'SLNG', 'SFR', 'NTZ', 'NHTC', 'BOLT', 'UBX', 'DMA', 'SSIC', 'MGLD',
              'AACG', 'RSSS', 'ICD', 'HUDI', 'DRCT', 'BOTJ', 'FEIM', 'ROCG', 'ISPO', 'LVTX', 'TAYD', 'MDWT', 'EEA',
              'NCSM', 'FAM', 'IROQ', 'WMC', 'NBW', 'ASPI', 'RGT', 'CFSB', 'RBT', 'DPSI', 'QLI', 'CCM', 'ICMB', 'KA',
              'JNCE', 'OSS', 'TTP', 'LTRN', 'LINK', 'GNS', 'JRSH', 'FKWL', 'BKTI', 'DDF', 'SNAL', 'HTY', 'SCYX', 'CGA',
              'MBTC', 'MIRO', 'HOFV', 'CEE', 'NSTS', 'CRWS', 'GRFX', 'FUSB', 'ENZ', 'FNGR', 'KFFB', 'ENOB', 'JMM',
              'EMKR', 'GLTO', 'EDI', 'IMNM', 'LFMD', 'PMCB', 'BYSI', 'NVNO', 'CYT', 'INDO', 'VRAR', 'TURN', 'PGRW',
              'CCLD', 'CADL', 'EVTV', 'VANI', 'CACO', 'PDEX', 'SPRB', 'DUNE', 'HFBL', 'AP', 'DSP', 'GNPX', 'ESP',
              'NAII', 'HHGC', 'LUCD', 'BDL', 'NLS', 'PFIE', 'YQ', 'CSPI', 'RSF', 'ENLV', 'TEDU', 'NDP', 'APT', 'SBEV',
              'MTRY', 'NTIP', 'ADOC', 'AAME', 'GRTX', 'BTMD', 'AZ', 'FSEA', 'BCEL', 'ICCM', 'GP', 'INKA', 'TATT',
              'TCBS', 'LTBR', 'BREZ', 'CKPT', 'RFL', 'AGAE', 'OKYO', 'TBIO', 'RFIL', 'CSSE', 'USEG', 'NLSP', 'IOBT',
              'SFE', 'ANGH', 'UG', 'MAIA', 'CXDO', 'TCRR', 'ZENV', 'MPU', 'MOVE', 'LFVN', 'AGMH', 'INTZ', 'IOR', 'STRW',
              'FMY', 'SNSE', 'DCTH', 'ICCH', 'CGTX', 'FGB', 'CVU', 'DSWL', 'SRAX', 'DMAC', 'LYLT', 'NBO', 'IDN', 'VTSI',
              'KACL', 'KRKR', 'GANX', 'TXMD', 'NICK', 'GROW', 'NXN', 'HTOO', 'PIXY', 'MNDO', 'DMS', 'PPBT', 'KSCP',
              'MEOA', 'KOSS', 'RPID', 'DHAC', 'RNXT', 'SOHO', 'CHCI', 'SYPR', 'ATXG', 'ACHL', 'USIO', 'ICCC', 'SGTX',
              'MXE', 'SEED', 'FGH', 'EBON', 'ALR', 'MMV', 'TESS', 'RENN', 'NXTC', 'CPSH', 'PNBK', 'MLAC', 'TKLF',
              'FTEK', 'TARA', 'EDRY', 'DYAI', 'KEQU', 'BCDA', 'EUCR', 'AIH', 'LICN', 'ZDGE', 'ACER', 'WAVS', 'OMQS',
              'COYA', 'EVOJ', 'LASE', 'KIRK', 'UTSI', 'ADXN', 'AINC', 'BMTX', 'PMN', 'JT', 'AFIB', 'ISO', 'XGN', 'EGF',
              'WTT', 'POCI', 'NSYS', 'ACXP', 'VLCN', 'GSIT', 'WKEY', 'ABEO', 'PBBK', 'INAB', 'ESOA', 'SSKN', 'ATTO',
              'DAIO', 'SPI', 'LITM', 'FSI', 'ICU', 'AIU', 'GBRG', 'DXR', 'BMRA', 'TLF', 'ICLK', 'VMAR', 'MSVB', 'CLRO',
              'AWRE', 'SALM', 'RAND', 'PALI', 'AMAO', 'DWSN', 'EVAX', 'UGRO', 'GSUN', 'CYN', 'ADN', 'IRIX', 'DGHI',
              'PYN', 'ACGN', 'CIF', 'MEGL', 'MBRX', 'USAU', 'COE', 'GURE', 'PTN', 'GTIM', 'UPH', 'NOVN', 'SRZN', 'EDTX',
              'COSM', 'BFI', 'SDPI', 'TCON', 'MIGI', 'LNSR', 'XPON', 'AVTX', 'MTC', 'SWAG', 'OCC', 'HAPP', 'EZGO',
              'SNT', 'DUOT', 'IMPL', 'CPIX', 'GRF', 'TISI', 'OCCI', 'EDUC', 'MTR', 'CCEL', 'PHCF', 'ELDN', 'TTCF',
              'MFV', 'MTEX', 'ABIO', 'HUSA', 'ORGS', 'TMPO', 'CLPS', 'WVVI', 'CLAY', 'ZIVO', 'PMD', 'BWAY', 'RMCF',
              'NTRB', 'GBNH', 'YGMZ', 'APWC', 'NTWK', 'SLS', 'PETV', 'SUNW', 'BBGI', 'APCX', 'CGRN', 'MNPR', 'CTIB',
              'XIN', 'CNTG', 'OPFI', 'SGRP', 'MRM', 'CVR', 'IMMX', 'CEI', 'JEWL', 'BTCM', 'DTSS', 'SOS', 'PATI', 'RAYA',
              'WKSP', 'MPTI', 'LUMO', 'GAME', 'SPCB', 'WLMS', 'EDSA', 'ELEV', 'DERM', 'GTEC', 'ISRL', 'TGL', 'RVSN',
              'SAI', 'MXC', 'BIOR', 'BON', 'BTTX', 'SVT', 'PPSI', 'IPDN', 'EUDA', 'OPHC', 'ILAG', 'CUBA', 'CMRA',
              'NMTC', 'CASI', 'GBNY', 'FENG', 'TNON', 'BEAT', 'AMPG', 'FTFT', 'LSDI', 'LXEH', 'FGF', 'ATHX', 'CYAD',
              'MGOL', 'LGL', 'NVVE', 'NFTG', 'CORR', 'SOBR', 'DALN', 'GLBZ', 'BNRG', 'SHPH', 'ZCMD', 'JFU', 'MODD',
              'NOM', 'TBLT', 'RVPH', 'BSQR', 'USEA', 'GLBS', 'ASST', 'VINC', 'YOSH', 'CVKD', 'BRN', 'SGMA', 'PXMD',
              'MSGM', 'FPAY', 'LCI', 'NH', 'LSTA', 'DOMH', 'RGLS', 'SRGA', 'WHLM', 'NYC', 'TAIT', 'MBOT', 'RAVE',
              'ALBT', 'BNOX', 'ATIF', 'ATNX', 'ISUN', 'NMTR', 'FBRX', 'EQS', 'AFGC', 'NXPL', 'CNFR', 'ASTC', 'MRAI',
              'HTCR', 'MOGU', 'NRSN', 'KZIA', 'GRCY', 'FEDU', 'POLA', 'AEY', 'BQ', 'CMMB', 'CKX', 'SIF', 'BRLI', 'SLNO',
              'VIVK', 'WAVE', 'ERNA', 'ZVSA', 'PALT', 'RMTI', 'GENE', 'DLPN', 'HALL', 'BTCS', 'ADD', 'ONVO', 'EKSO',
              'EDTK', 'CARV', 'JCTCF', 'MDJH', 'VEEE', 'AMS', 'ENTX', 'APDN', 'AGRI', 'CHRA', 'BHV', 'TRT', 'ELTK',
              'GCTK', 'AEI', 'WYY', 'IBIO', 'TSRI', 'FGI', 'LEXX', 'BWV', 'LMNL', 'BLPH', 'IINN', 'MRKR', 'MRIN',
              'EEIQ', 'TPST', 'BRFH', 'PFIN', 'GEHI', 'PEGY', 'VJET', 'ISIG', 'MOXC', 'CING', 'BLBX', 'LEJU', 'CLRB',
              'ELSE', 'AIRI', 'IHT', 'AEZS', 'MARPS', 'VRME', 'COHN', 'BFRG', 'COCP', 'GRIL', 'SCKT', 'SSNT', 'NNVC',
              'SIEN', 'MARK', 'GIGM', 'ECOR', 'FRZA', 'KINS', 'PW', 'BNSO', 'YTEN', 'AUUD', 'WHLR', 'BPTH', 'STSS',
              'BIAF', 'INDP', 'APRE', 'GIPR', 'CYTH', 'RCON', 'BRTX', 'ALIM', 'SQFT', 'LMFA', 'ISPC', 'NURO', 'ATHE',
              'MITQ', 'VINE', 'CFMS', 'FEMY', 'ITRM', 'BTBD', 'SGBX', 'DGLY', 'LUCY', 'DTST', 'CRBP', 'HILS', 'PULM',
              'LIPO', 'CREG', 'MF', 'DFFN', 'GWAV', 'APM', 'RCG', 'NDRA', 'NXTP', 'JVA', 'FORD', 'OXBR', 'FUV', 'LEDS',
              'GFAI', 'IMNN', 'HSCS', 'IMRN', 'NERV', 'APVO', 'NEPH', 'ACRX', 'SWVL', 'GRNQ', 'BLIN', 'SECO', 'ARTW',
              'CNET', 'AWX', 'BOSC', 'CLWT', 'WAFU', 'KWE', 'BREA', 'BTB', 'EVOK', 'NCRA', 'COMS', 'NSPR', 'VYNE',
              'LSF', 'ANTE', 'CANF', 'OGEN', 'LCFY', 'JFBR', 'COEP', 'AYTU', 'QH', 'ONFO', 'ARTL', 'HIHO', 'MICS',
              'MTEK', 'GHSI', 'SSY', 'NUZE', 'TRVN', 'KTRA', 'NXGL', 'REVB', 'AVGR', 'SNGX', 'WISA', 'MDGS', 'KPRX',
              'RIBT', 'SVRE', 'CMND', 'MDIA', 'DYNT', 'TMBR', 'CYAN', 'RSLS', 'SNPX', 'XTLB', 'ONCS', 'ELOX', 'ALRN',
              'NCPL', 'SINT', 'RMED', 'RHE', 'NAOV', 'SILO', 'ALAR', 'DBGI', 'GBR', 'CETX', 'RELI', 'GDC', 'PHIO',
              'STAF', 'ATXI', 'TIRX', 'SNTG', 'UUU', 'INBS', 'UNAM', 'XCUR', 'CWBR', 'FRTX', 'EDBL', 'SNOA', 'NBRV',
              'SLRX', 'SVFD', 'JAN', 'QLGN', 'ADTX', 'PSHG', 'VINO', 'GMVD', 'NUWE', 'BIMI', 'INM', 'NBY', 'BVXV',
              'OBLG', 'ENVB', 'KAL', 'HOTH', 'PTPI', 'NVIV', 'HTGM', 'OPGN', 'FWBI', 'JAGX', 'CYTO', 'TCBP', 'THMO',
              'MYSZ', 'CNSP', 'MOB', 'CFRX', 'SNES', 'BXRX', 'NEGG', 'AEPPZ', 'AESC', 'AQNA', 'AQNB', 'AQNU', 'CDZIP',
              'CHRB', 'CMSA', 'CMSC', 'CMSD', 'DTB', 'DTG', 'DTW', 'DUKB', 'ENJ', 'NIMC', 'PCGU', 'PCTTU', 'PCTTW',
              'SOJC', 'SOJD', 'SOJE', 'TVC', 'TVE', 'UGIC', 'VIASP', 'UZD', 'UZE', 'UZF', 'ARBKL', 'BEEMW', 'GEGGL',
              'INDIW', 'LIFWZ', 'PAYOW', 'RUMBW', 'SLNHP', 'SNCRL', 'SURGW', 'XELAP', 'AGNCL', 'AGNCM', 'AGNCN',
              'AGNCO', 'AGNCP', 'AIC', 'AJXA', 'BNH', 'BNJ', 'DHCNI', 'DHCNL', 'GOODN', 'GOODO', 'HCDIP', 'HTIA',
              'HTIBP', 'LANDO', 'MDRRP', 'NYMTL', 'NYMTM', 'NYMTN', 'NYMTZ', 'OPINL', 'RCA', 'RTLPO', 'RTLPP', 'SACC',
              'SCCB', 'SCCC', 'SCCD', 'SCCE', 'SCCF', 'SCCG', 'SOHOB', 'SOHON', 'SOHOO', 'SQFTP', 'TPTA', 'WHLRD',
              'WHLRL', 'WHLRP', 'FRGAP', 'LFMDP', 'ACABU', 'ACACU', 'ACAHU', 'ADERU', 'AEAEU', 'ALPAU', 'ALTUU',
              'AMAOU', 'ANZUU', 'APMIU', 'ARRWU', 'AVHIU', 'BLNGU', 'BMAQU', 'BNNRU', 'BRIVU', 'BRKHU', 'BWACU', 'BWNB',
              'BWSN', 'BYNOU', 'CCAIU', 'CETUU', 'CFIVU', 'CIIGU', 'CMPOW', 'CNGLU', 'CONXU', 'DMYY', 'DUNEU', 'DWACU',
              'DWACW', 'EMLDU', 'FGMCU', 'FIACU', 'FLFVU', 'FMIVU', 'FRLAU', 'FTIIU', 'FTPAU', 'GAMCU', 'GATEU',
              'GMFIU', 'GXIIU', 'HCNEU', 'HCVIU', 'HPLTU', 'HUDAU', 'IIVI', 'INTEU', 'IPVIU', 'JAQCU', 'JMACU', 'LFACU',
              'LIBYU', 'LIONU', 'LITTU', 'MCAFU', 'MINDP', 'MLAIU', 'MPRAU', 'MTCN', 'MTRYU', 'NBSTU', 'NHICU', 'NPABU',
              'OHAAU', 'PGRWU', 'PMGMU', 'PNACU', 'POWWP', 'PPYAU', 'PTOCU', 'PUCKU', 'QOMOU', 'RBCP', 'RCLFU', 'REVEU',
              'RFACU', 'ROCGU', 'RWODU', 'SAMAU', 'SCAQU', 'SDACU', 'SEATW', 'SGHLU', 'SMAPU', 'TBCPU', 'TETCU',
              'TGVCU', 'THCPU', 'TWCBU', 'TWLVU', 'UPTDU', 'VIIAU', 'WAVSU', 'XFINU', 'XPDBU', 'ZTAQU', 'ALVOW',
              'BCTXW', 'BDXB', 'BIPH', 'BKDT', 'CCLDO', 'CCLDP', 'CYCCP', 'FBIOP', 'GMVDW', 'HROWL', 'HROWM', 'IMTXW',
              'NAMSW', 'ROIVW', 'RVPHW', 'STRRP', 'XOMAO', 'XOMAP', 'AAIN', 'ACGLN', 'ACGLO', 'ACQRU', 'AFARU', 'AFGB',
              'AFGD', 'AGGRU', 'AIBBU', 'AIMBU', 'AIZN', 'ALSAU', 'ARGD', 'ATAKU', 'ATLCL', 'ATLCP', 'AURCU', 'BANFP',
              'BCSAU', 'BHFAL', 'BHFAM', 'BHFAN', 'BHFAO', 'BHFAP', 'BIOSU', 'BLACU', 'BMN', 'BOCNU', 'BPOPM', 'BRLIU',
              'BTWNU', 'BWBBP', 'BYTSU', 'CCNEP', 'CCTSU', 'CDAQU', 'CHEAU', 'CNFRL', 'CNOBP', 'CRECU', 'CUBB', 'DCOMP',
              'DECAU', 'DHCAU', 'DISAU', 'DISTU', 'DPCSU', 'EBACU', 'ECCC', 'ECCV', 'ECCW', 'ECCX', 'EFSCP', 'EIC',
              'EICA', 'EMCGU', 'ENTFU', 'ESGRO', 'ESGRP', 'EUCRU', 'EVGRU', 'FCNCO', 'FCNCP', 'FGBIP', 'FGFPP', 'FICVU',
              'FITBI', 'FITBO', 'FITBP', 'FNVTU', 'FRMEP', 'FRONU', 'FSCO', 'FULTP', 'GAINN', 'GAINZ', 'GBRGU', 'GECCN',
              'GECCO', 'GGAAU', 'GJH', 'GJO', 'GJP', 'GJS', 'GJT', 'GREEL', 'GSRMR', 'GVCIU', 'HAIAU', 'HBANM', 'HBANP',
              'HCXY', 'HERAU', 'HNNAZ', 'HTFB', 'HTFC', 'HTLFP', 'HWCPZ', 'INBKZ', 'IVCAU', 'IVCBU', 'IVCPU', 'IXAQU',
              'JSM', 'KMPB', 'KRNLU', 'KTH', 'KYCHU', 'LATGU', 'LCAAU', 'LGSTU', 'LVRAU', 'MACAU', 'MARXU', 'MBINM',
              'MBINN', 'MBINO', 'MBINP', 'MBNKP', 'MCAAU', 'MGR', 'MGRB', 'MGRD', 'MHLA', 'MHNC', 'MITAU', 'MLACU',
              'MNSBP', 'MSBIP', 'MSSAU', 'NEWTL', 'NRACU', 'NTRSO', 'OCCIN', 'OCCIO', 'OCFCP', 'OFSSH', 'ONBPO',
              'ONBPP', 'ONYXU', 'ORIAU', 'OXLCL', 'OXLCM', 'OXLCN', 'OXLCO', 'OXLCP', 'OXLCZ', 'OXSQZ', 'OZKAP',
              'PEGRU', 'PFH', 'PLAOU', 'PLMIU', 'PNFPP', 'PRH', 'PRLHU', 'PRSRU', 'PTHRU', 'PWUPU', 'RAMMU', 'RCC',
              'RENEU', 'RILYL', 'RILYP', 'RLTY', 'RMGCU', 'RZB', 'RZC', 'SAJ', 'SAT', 'SAY', 'SBNYP', 'SCRMU', 'SFB',
              'SHUAU', 'SIGIP', 'SIVBP', 'SKYAU', 'SLAMU', 'SLMBP', 'SMIHU', 'SPKBU', 'SSSSL', 'SVIIU', 'TCBIO',
              'TECTP', 'TGAAU', 'TRINL', 'TRONU', 'UCBIO', 'UNMA', 'UTAAU', 'VCXAU', 'VLYPO', 'VLYPP', 'VMCAU', 'VPCBU',
              'WAFDP', 'WSBCP', 'WTFCM', 'WTFCP', 'XPAXU', 'ZIONL', 'ZIONO', 'ZIONP', 'ARKOW', 'CHKEL', 'CHKEW', 'ENBA',
              'HPKEW', 'METCL', 'TANNI', 'TANNL', 'TANNZ', 'TELZ', 'CHSCL', 'CHSCM', 'CHSCN', 'CHSCO', 'CHSCP', 'WESTW',
              'WVVIP', 'ACBAU', 'AIRTP', 'ASTSW', 'CCV', 'CCZ', 'COMSP', 'CSSEN', 'CSSEP', 'DBGIW', 'DDT', 'FATBP',
              'FOSLL', 'GMBLP', 'GTXAP', 'HOVNP', 'HTZWW', 'IMBIL', 'IMPPP', 'INVZW', 'LBRDP', 'OXSQG', 'OXSQL',
              'PARAP', 'PXSAP', 'PXSAW', 'QRTEP', 'RILYG', 'RILYK', 'RILYM', 'RILYN', 'RILYO', 'RILYT', 'RILYZ',
              'RSVRW', 'SABRP', 'SBBA', 'SREA', 'TBB', 'TBC', 'THWWW', 'ATCOL', 'AEFC', 'AFGE', 'APTMU', 'ASTLW',
              'ATMCU', 'ATMV', 'ATMVU', 'AUVIP', 'BEPH', 'BEPI', 'BIPI', 'CGABL', 'CTBB', 'CTDD', 'EAI', 'ECX', 'ELC',
              'EMP', 'ENO', 'FCRX', 'GFLU', 'GPCR', 'GPJA', 'ISRLU', 'JUGGU', 'KKRS', 'KTN', 'LCFYW', 'LGVCU', 'NEWTZ',
              'NRUC', 'NSS', 'PACWP', 'QVCC', 'QVCD', 'RCB', 'RWAYL', 'RWAYZ', 'TFSA', 'INLX', 'UPBD', 'ELVN', 'ZVRA',
              'LVRO', 'MCVT', 'QDRO', 'QDROU', 'TFINP', 'HHRS', 'HUBC', 'HUDA', 'IMCI', 'SCLXW']

etf_tickers = ['AAAU', 'AAPD', 'AAPU', 'AAXJ', 'ABEQ', 'ACES', 'ACWI', 'ACWV', 'ACWX', 'AGG', 'AGGY', 'AGQ', 'AGZ',
               'AGZD', 'AIA', 'AIRR', 'ALTL', 'AMZD', 'AMZU', 'ANGL', 'AOA', 'AOK', 'AOM', 'AOR',
               'ARKF', 'ARKG', 'ARKK', 'ARKQ', 'ARKW', 'ASHR', 'AVDE', 'AVDV', 'AVEM', 'AVES', 'AVIG', 'AVIV', 'AVLV',
               'AVRE', 'AVSD', 'AVUS', 'AVUV', 'BAB', 'BALT', 'BAR', 'BBAX', 'BBCA', 'BBEU', 'BBH', 'BBIN', 'BBJP',
               'BBRE', 'BBSA', 'BBUS', 'BCI', 'BERZ', 'BIB', 'BIBL', 'BIL', 'BILS', 'BITI', 'BITO', 'BIV', 'BIZD',
               'BKLC', 'BKLN', 'BLCN', 'BLOK', 'BLV', 'BMAR', 'BMEZ', 'BND', 'BNDW', 'BNDX', 'BNOV', 'BOIL',
               'BOND', 'BOTZ', 'BRZU', 'BSCM', 'BSCN', 'BSCO', 'BSCP', 'BSCQ', 'BSCR', 'BSCS', 'BSJM', 'BSJN', 'BSJO',
               'BSJP', 'BSJQ', 'BSMN', 'BSMT', 'BSTZ', 'BSV', 'BTAL', 'BTF', 'BUCK', 'BUFD', 'BUFR', 'BUG', 'BULZ',
               'BWX', 'BYTE', 'CALF', 'CATH', 'CCOR', 'CDC', 'CDL', 'CEMB', 'CFO', 'CGCP', 'CGDV', 'CGGO', 'CGGR',
               'CGUS', 'CGW', 'CGXU', 'CHAU', 'CHIE', 'CHIQ', 'CIBR', 'CLOU', 'CLSC', 'CLTL', 'CMBS', 'CMDY', 'CMF',
               'CNCR', 'CNRG', 'COM', 'COMB', 'COMT', 'COPX', 'CORP', 'COWZ', 'CQQQ', 'CRBN', 'CSB',
               'CSTNL', 'CTA', 'CURE', 'CWB', 'CWEB', 'CWI', 'CXSE', 'CYA', 'DAPR', 'DAUG',
               'DBEF', 'DBJP', 'DBMF', 'DDM', 'DEF', 'DEM', 'DES', 'DFAC', 'DFAE', 'DFAI', 'DFAR', 'DFAS',
               'DFAT', 'DFAU', 'DFAX', 'DFCF', 'DFEB', 'DFEM', 'DFEN', 'DFEV', 'DFIC', 'DFIP', 'DFIS', 'DFIV', 'DFNM',
               'DFSD', 'DFSV', 'DFUS', 'DFUV', 'DGRO', 'DGRW', 'DGS', 'DHS', 'DIA', 'DIAL', 'DIG', 'DIHP', 'DISV',
               'DIV', 'DIVB', 'DIVO', 'DJD', 'DJIA', 'DJUL', 'DLN', 'DLS', 'DLY', 'DMXF', 'DNL', 'DOCT', 'DOG', 'DOL',
               'DON', 'DPST', 'DRIP', 'DRIV', 'DRLL', 'DRN', 'DRSK', 'DRV', 'DSEP', 'DSI', 'DSTL', 'DTD', 'DTH', 'DUG',
               'DUHP', 'DUSL', 'DUST', 'DVY', 'DVYE', 'DWAS', 'DWM', 'DWX', 'DXD', 'DXJ', 'EAGG', 'EBND', 'ECH', 'EDC',
               'EDOG', 'EDV', 'EDZ', 'EELV', 'EEM', 'EEMS', 'EEMV', 'EES', 'EFA', 'EFAV', 'EFAX', 'EFG', 'EFV', 'EFZ',
               'EIDO', 'EMB', 'EMGF', 'EMHY', 'EMLC', 'EMLP', 'EMQQ', 'EMXC', 'EPHE', 'EPI', 'EPOL', 'EPP',
               'EPS', 'EPV', 'ERX', 'ERY', 'ESGD', 'ESGE', 'ESGU', 'ESGV', 'ESML', 'ESPO', 'ETHE', 'EUFN', 'EUM', 'EUO',
               'EUSA', 'EUSB', 'EWA', 'EWC', 'EWD', 'EWG', 'EWH', 'EWI', 'EWJ', 'EWL', 'EWM', 'EWN', 'EWP', 'EWQ',
               'EWS', 'EWSC', 'EWT', 'EWU', 'EWW', 'EWX', 'EWY', 'EWZ', 'EXI', 'EZA', 'EZU', 'FAAR', 'FAB', 'FALN',
               'FAN', 'FAS', 'FAUG', 'FAZ', 'FBCG', 'FBND', 'FBT', 'FCG', 'FCOM', 'FCOR', 'FCPI', 'FCTR', 'FCVT',
               'FDHY', 'FDIS', 'FDL', 'FDLO', 'FDN', 'FDRR', 'FDT', 'FDVV', 'FEM', 'FEMS', 'FENY', 'FEX', 'FEZ', 'FGD',
               'FGRO', 'FHLC', 'FIDU', 'FINX', 'FIVG', 'FIW', 'FIXD', 'FJUN', 'FLDR', 'FLGB', 'FLJH', 'FLJP', 'FLOT',
               'FLRN', 'FLTR', 'FLUD', 'FMAT', 'FMAY', 'FMB', 'FMF', 'FMHI', 'FNCL', 'FNDA', 'FNDB', 'FNDC', 'FNDE',
               'FNDF', 'FNDX', 'FNOV', 'FNX', 'FOCT', 'FPE', 'FPEI', 'FPX', 'FPXI', 'FRDM', 'FREL', 'FRI', 'FSEP',
               'FSMB', 'FSTA', 'FTA', 'FTC', 'FTCS', 'FTEC', 'FTGC', 'FTHI', 'FTLS', 'FTRI', 'FTSL', 'FTSM', 'FTXG',
               'FTXL', 'FTXN', 'FUMB', 'FUTY', 'FV', 'FVAL', 'FVD', 'FXB', 'FXC', 'FXE', 'FXG', 'FXH', 'FXI', 'FXL',
               'FXN', 'FXO', 'FXP', 'FXR', 'FXU', 'FXY', 'FXZ', 'FYC', 'FYT', 'FYX', 'GBF', 'GBIL', 'GBTC', 'GCC',
               'GCOR', 'GCOW', 'GDX', 'GDXJ', 'GDXU', 'GEM', 'GGLL', 'GHYB', 'GHYG', 'GIGB', 'GLD', 'GLDM', 'GLL',
               'GLTR', 'GMF', 'GMOM', 'GNMA', 'GNR', 'GOVT', 'GQRE', 'GRES', 'GRID', 'GSEW', 'GSIE', 'GSLC',
               'GSSC', 'GSST', 'GSUS', 'GSY', 'GTO', 'GUNR', 'GUSH', 'GVI', 'GWX', 'GXC', 'HACK', 'HAUZ', 'HDEF',
               'HDGE', 'HDV', 'HEDJ', 'HEFA', 'HEQT', 'HFXI', 'HIBL', 'HIBS', 'HIGH', 'HLAL', 'HMOP', 'HNDL', 'HTRB',
               'HYBB', 'HYD', 'HYDB', 'HYEM', 'HYG', 'HYGH', 'HYGV', 'HYLB', 'HYLS', 'HYMB', 'HYS', 'HYZD', 'IAGG',
               'IAI', 'IAK', 'IAT', 'IAU', 'IAUM', 'IBB', 'IBDD', 'IBDN', 'IBDO', 'IBDP', 'IBDQ', 'IBDR', 'IBDS',
               'IBDT', 'IBHD', 'IBHE', 'IBMK', 'IBML', 'IBMM', 'IBMN', 'IBMO', 'IBMQ', 'IBTB', 'IBTD', 'IBTE', 'IBTF',
               'IBTG', 'IBUY', 'ICF', 'ICLN', 'ICOW', 'ICSH', 'ICVT', 'IDEV', 'IDLV', 'IDRV', 'IDU', 'IDV', 'IEF',
               'IEFA', 'IEI', 'IEMG', 'IEO', 'IEUR', 'IEV', 'IEZ', 'IFRA', 'IGE', 'IGF', 'IGIB', 'IGLB', 'IGM', 'IGOV',
               'IGRO', 'IGSB', 'IGV', 'IHAK', 'IHDG', 'IHE', 'IHF', 'IHI', 'IHY', 'IJH', 'IJJ', 'IJK', 'IJR', 'IJS',
               'IJT', 'IJUL', 'ILCG', 'ILF', 'ILTB', 'IMCG', 'IMCV', 'IMSEF', 'IMTB', 'IMTM', 'INDA', 'INDL', 'INDS',
               'INDY', 'INFL', 'INTF', 'IOO', 'IPAC', 'IPAY', 'IPO', 'IQDF', 'IQDG', 'IQLT', 'ISCF', 'ISHG', 'ISHUF',
               'ISTB', 'ISVVF', 'ISZXF', 'ITA', 'ITB', 'ITEQ', 'ITM', 'ITOT', 'IUS', 'IUSB', 'IUSG', 'IUSV', 'IVE',
               'IVLU', 'IVOL', 'IVOO', 'IVOV', 'IVV', 'IVVPF', 'IVW', 'IWB', 'IWC', 'IWD', 'IWF', 'IWL', 'IWM', 'IWN',
               'IWO', 'IWP', 'IWR', 'IWS', 'IWV', 'IWX', 'IWY', 'IXC', 'IXG', 'IXJ', 'IXN', 'IXP', 'IXUS', 'IYC', 'IYE',
               'IYF', 'IYG', 'IYH', 'IYJ', 'IYK', 'IYM', 'IYR', 'IYT', 'IYW', 'IYY', 'IYZ', 'JAAA', 'JAGG', 'JAVA',
               'JCPB', 'JCPI', 'JDST', 'JEPI', 'JEPQ', 'JETS', 'JHEM', 'JHML', 'JHMM', 'JHSC', 'JIG', 'JMBS', 'JMST',
               'JMUB', 'JNK', 'JNUG', 'JPEM', 'JPHY', 'JPIB', 'JPIE', 'JPIN', 'JPME', 'JPSE', 'JPST', 'JQUA', 'JVAL',
               'KBA', 'KBE', 'KBWB', 'KBWD', 'KBWY', 'KIE', 'KJAN', 'KMLM', 'KNG', 'KOCT', 'KOLD', 'KOMP', 'KRBN',
               'KRE', 'KSA', 'KWEB', 'KXI', 'LABD', 'LABU', 'LDUR', 'LEMB', 'LGLV', 'LIT', 'LMBS', 'LQD', 'LQDH',
               'LRGE', 'LRGF', 'LTPZ', 'LVHD', 'LVHI', 'MBB', 'MCHI', 'MDY', 'MDYG', 'MDYV', 'MEAR', 'METV', 'MGC',
               'MGK', 'MGV', 'MIDU', 'MINT', 'MJ', 'MLN', 'MLPA', 'MLPX', 'MMIN', 'MMIT', 'MNA', 'MOAT', 'MOO', 'MRGR',
               'MSOS', 'MTUM', 'MUB', 'MUNI', 'MUST', 'NAIL', 'NANR', 'NBCM', 'NEAR', 'NETZ', 'NFLT', 'NFRA', 'NJAN',
               'NJUL', 'NOBL', 'NOCT', 'NOPE', 'NTSI', 'NTSX', 'NUDM', 'NUEM', 'NUGO', 'NUGT', 'NULG', 'NULV', 'NUMG',
               'NUMV', 'NUSC', 'NUSI', 'NVDS', 'NXTG', 'NYF', 'OEF', 'OIH', 'OILK', 'OILU', 'OMFL', 'ONEQ', 'ONEY',
               'ONG', 'ONLN', 'OUNZ', 'OUSA', 'OUSM', 'PALC', 'PALL', 'PAVE', 'PAWZ', 'PBJ', 'PBTP', 'PBW', 'PCEF',
               'PCY', 'PDBC', 'PDN', 'PDP', 'PEJ', 'PEY', 'PFEB', 'PFF', 'PFFA', 'PFFD', 'PFFV', 'PFIX', 'PFM', 'PFXF',
               'PGF', 'PGJ', 'PGX', 'PHB', 'PHDG', 'PHO', 'PICK', 'PID', 'PIE', 'PIN', 'PJP', 'PJUL', 'PKW', 'PMAY',
               'PNOV', 'PNQI', 'POCT', 'PPA', 'PPH', 'PPLT', 'PREF', 'PRF', 'PRFZ', 'PSCE', 'PSEP', 'PSI', 'PSK', 'PSP',
               'PSQ', 'PST', 'PTBD', 'PTLC', 'PTMC', 'PTNQ', 'PULS', 'PVI', 'PWB', 'PWV', 'PWZ', 'PXE', 'PXF', 'PXH',
               'PXI', 'PXJ', 'PZA', 'QABA', 'QAI', 'QCLN', 'QCON', 'QDF', 'QEFA', 'QID', 'QLC', 'QLD', 'QLTA', 'QMOM',
               'QQEW', 'QQQ', 'QQQE', 'QQQJ', 'QQQM', 'QQXT', 'QTEC', 'QUAL', 'QUS', 'QYLD', 'RAVI', 'RDIV', 'RDVY',
               'REET', 'REGL', 'REK', 'REM', 'REMX', 'RETL', 'REW', 'REZ', 'RFV', 'RGI', 'RHS', 'RINF', 'RING', 'RLY',
               'ROBO', 'RODM', 'ROM', 'ROUS', 'RPAR', 'RPG', 'RPV', 'RSP', 'RTH', 'RVNU', 'RWJ', 'RWL', 'RWM', 'RWO',
               'RWR', 'RWX', 'RXI', 'RYE', 'RYF', 'RYH', 'RYLD', 'RYT', 'RYU', 'SAMT', 'SARK', 'SCHA', 'SCHB', 'SCHC',
               'SCHD', 'SCHE', 'SCHF', 'SCHG', 'SCHH', 'SCHI', 'SCHJ', 'SCHK', 'SCHM', 'SCHO', 'SCHP', 'SCHQ', 'SCHR',
               'SCHV', 'SCHX', 'SCHY', 'SCHZ', 'SCMB', 'SCO', 'SCZ', 'SDG', 'SDIV', 'SDOG', 'SDOW', 'SDS', 'SDVY',
               'SDY', 'SECT', 'SEF', 'SFY', 'SGOL', 'SGOV', 'SH', 'SHM', 'SHV', 'SHY', 'SHYD', 'SHYG', 'SIL', 'SILJ',
               'SIVR', 'SJB', 'SJNK', 'SKF', 'SKOR', 'SKYY', 'SLQD', 'SLV', 'SLX', 'SLY', 'SLYG', 'SLYV', 'SMB', 'SMDV',
               'SMH', 'SMIG', 'SMIN', 'SMLF', 'SMMD', 'SMMU', 'SMMV', 'SNPE', 'SOXL', 'SOXQ', 'SOXS', 'SOXX', 'SPAB',
               'SPBO', 'SPD', 'SPDN', 'SPDW', 'SPEM', 'SPGM', 'SPGP', 'SPHB', 'SPHD', 'SPHQ', 'SPHY', 'SPIB', 'SPIP',
               'SPLB', 'SPLG', 'SPLV', 'SPMB', 'SPMD', 'SPSB', 'SPSM', 'SPTI', 'SPTL', 'SPTM', 'SPTS', 'SPUS', 'SPUU',
               'SPXL', 'SPXS', 'SPXU', 'SPY', 'SPYC', 'SPYD', 'SPYG', 'SPYV', 'SPYX', 'SQQQ', 'SRLN', 'SRS', 'SRTY',
               'SRVR', 'SSO', 'SSUS', 'STIP', 'STPZ', 'STRV', 'SUB', 'SUSA', 'SUSB', 'SUSC', 'SUSL', 'SVIX', 'SVOL',
               'SVXY', 'SWAN', 'SYLD', 'TACK', 'TAIL', 'TAN', 'TARK', 'TBF', 'TBIL', 'TBLD', 'TBT', 'TBX', 'TCHP',
               'TDIV', 'TDSC', 'TDTF', 'TDTT', 'TECL', 'TECS', 'TFI', 'TFLO', 'THD', 'THLV', 'TILT', 'TIP', 'TIPX',
               'TLH', 'TLT', 'TLTD', 'TLTE', 'TMF', 'TMFC', 'TMV', 'TNA', 'TOLZ', 'TOTL', 'TPYP', 'TQQQ', 'TSLL',
               'TSLQ', 'TSLS', 'TTT', 'TUR', 'TWM', 'TYO', 'TZA', 'UCO', 'UCON', 'UDOW', 'UGL', 'UITB',
               'UJAN', 'UMAR', 'UOCT', 'UPAR', 'UPRO', 'URA', 'URNM', 'URTH', 'URTY', 'USD', 'USDU',
               'USFR', 'USHY', 'USIG', 'USMF', 'USMV', 'USRT', 'USTB', 'USVM', 'USXF', 'UTSL', 'UTWO',
               'UVIX', 'UVXY', 'UWM', 'UYLD', 'VAMO', 'VAW', 'VB', 'VBK', 'VBR', 'VCIT', 'VCLT', 'VCR', 'VCSH', 'VDC',
               'VDE', 'VEA', 'VEGI', 'VEU', 'VFH', 'VFVA', 'VGDTF', 'VGIT', 'VGK', 'VGLT', 'VGSH', 'VGT', 'VHT', 'VIG',
               'VIGI', 'VIOG', 'VIOO', 'VIOV', 'VIS', 'VIXM', 'VIXY', 'VLU', 'VLUE', 'VMBS', 'VNGUF', 'VNLA', 'VNM',
               'VNQ', 'VNQI', 'VO', 'VOE', 'VONE', 'VONG', 'VONV', 'VOO', 'VOOG', 'VOOV', 'VOT', 'VOTE', 'VOX', 'VPL',
               'VPU', 'VRIG', 'VRP', 'VSGX', 'VSS', 'VT', 'VTC', 'VTEB', 'VTHR', 'VTI', 'VTIP', 'VTV', 'VTWG', 'VTWO',
               'VTWV', 'VUG', 'VUSB', 'VV', 'VWO', 'VWOB', 'VXF', 'VXUS', 'VYM', 'VYMI', 'WANT', 'WCLD', 'WEBL',
               'WEBS', 'WFHY', 'WIP', 'XAR', 'XBI', 'XBJL', 'XBOC', 'XCEM', 'XDEC', 'XES', 'XHB', 'XHE', 'XHS', 'XJH',
               'XJUN', 'XLB', 'XLC', 'XLE', 'XLF', 'XLG', 'XLI', 'XLK', 'XLP', 'XLRE', 'XLU', 'XLV', 'XLY', 'XME',
               'XMHQ', 'XMLV', 'XMMO', 'XNTK', 'XOP', 'XRT', 'XSD', 'XSEP', 'XSLV', 'XSOE', 'XSVM', 'XSW', 'XT', 'XTL',
               'XTN', 'XYLD', 'YANG', 'YCL', 'YCS', 'YINN', 'YXI', 'YYY', 'ZROZ', 'ZSL']


def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code


def lineNotifyImage(token, message, image):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + token}
    data = {'message': message}
    image = open(image, 'rb')
    imageFile = {'imageFile': image}
    r = requests.post(url, headers=headers, data=data, files=imageFile)
    if r.status_code == requests.codes.ok:
        return '圖片發送成功！'
    else:
        return f'圖片發送失敗: {r.status_code}'
    image.close()


token = 'YuvfgED98JDWMvATPEAnDu3u9Ge0R2B9BkrOvCwHZId'


def plotly_chart(dfin, ticker, number):
    # Reference: https://python.plainenglish.io/a-simple-guide-to-plotly-for-plotting-financial-chart-54986c996682
    plot_period = -155  # 只保留特定天數的資料
    df = dfin[plot_period:]
    # df = dfin[-266:]
    # df = yf.download(ticker, period='1y', interval='1d')

    # first declare an empty figure
    fig = go.Figure()
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        vertical_spacing=0.01,
                        row_heights=[0.5, 0.1, 0.1])

    # removing all empty dates
    # build complete timeline from start date to end date
    dt_all = pd.date_range(start=df.index[0], end=df.index[-1])
    # retrieve the dates that ARE in the original datset
    dt_obs = [d.strftime("%Y-%m-%d") for d in pd.to_datetime(df.index)]
    # define dates with missing values
    dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]
    fig.update_xaxes(rangebreaks=[dict(values=dt_breaks)])
    # MACD
    macd = MACD(close=df['Close'],
                window_slow=26,
                window_fast=12,
                window_sign=9)
    # stochastic
    stoch = StochasticOscillator(high=df['High'],
                                 close=df['Close'],
                                 low=df['Low'],
                                 window=14,
                                 smooth_window=3)
    # add OHLC
    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df['Open'],
                                 high=df['High'],
                                 low=df['Low'],
                                 close=df['Close'],
                                 showlegend=False)
                  )

    # add moving averages to df
    # df['MA20'] = df['Close'].rolling(window=20).mean()
    # df['MA5'] = df['Close'].rolling(window=5).mean()

    # add VCMA to df
    df['total_price'] = df['Close'] * df['Volume']
    # df.loc[df['total_price']] = df['Close'] * df['Volume']

    windows = [233, 144, 55, 21, 5]
    for w in windows:
        rolling_total_price = df['total_price'].rolling(window=w).sum()
        rolling_volume = df['Volume'].rolling(window=w).sum()
        df[f'vcma{w}'] = rolling_total_price / rolling_volume
    # df['vcma233'] = df['total_price'].rolling(window=233).sum() / df['Volume'].rolling(window=233).sum()
    # df['vcma144'] = df['total_price'].rolling(window=144).sum() / df['Volume'].rolling(window=144).sum()
    # df['vcma55'] = df['total_price'].rolling(window=55).sum() / df['Volume'].rolling(window=55).sum()
    # df['vcma21'] = df['total_price'].rolling(window=21).sum() / df['Volume'].rolling(window=21).sum()
    # df['vcma5'] = df['total_price'].rolling(window=5).sum() / df['Volume'].rolling(window=5).sum()

    # add moving average traces
    fig.add_trace(go.Scatter(x=df.index,
                             y=df['vcma5'],
                             opacity=0.7,
                             line=dict(color='blue', width=2),
                             name='VCMA 5'))
    fig.add_trace(go.Scatter(x=df.index,
                             y=df['vcma21'],
                             opacity=0.7,
                             line=dict(color='green', width=2),
                             name='VCMA 21'))
    fig.add_trace(go.Scatter(x=df.index,
                             y=df['vcma55'],
                             opacity=0.7,
                             line=dict(color='red', width=2),
                             name='VCMA 55'))
    fig.add_trace(go.Scatter(x=df.index,
                             y=df['vcma144'],
                             opacity=0.7,
                             line=dict(color='magenta', width=2),
                             name='VCMA 144'))
    fig.add_trace(go.Scatter(x=df.index,
                             y=df['vcma233'],
                             opacity=0.7,
                             line=dict(color='goldenrod', width=2),
                             name='VCMA 233'))

    # hide dates with no values
    fig.update_xaxes(rangebreaks=[dict(values=dt_breaks)])
    # remove rangeslider
    fig.update_layout(xaxis_rangeslider_visible=False)
    # add chart title
    fig.update_layout(title=ticker)
    fig.update_layout(width=1920, height=1080,
                      xaxis_title='Date',
                      yaxis_title='Price',
                      font=dict(family='Arial', size=24),
                      title_font=dict(family='Arial', size=36))

    # Set MACD color
    colors = ['green' if val >= 0
              else 'red' for val in macd.macd_diff()]
    # MACD_name = ['Positive MACD' if val >= 0
    #  else 'Negative MACD' for val in macd.macd_diff()]

    # Add MACD trace
    fig.add_trace(go.Bar(x=df.index,
                         y=macd.macd_diff(),
                         marker_color=colors, name="MACD"
                         ), row=3, col=1)
    fig.add_trace(go.Scatter(x=df.index,
                             y=macd.macd(),
                             line=dict(color='blue', width=2),
                             name='MACD Fast'
                             ), row=3, col=1)

    fig.add_trace(go.Scatter(x=df.index,
                             y=macd.macd_signal(),
                             line=dict(color='red', width=2),
                             name='MACD Signal'
                             ), row=3, col=1)
    fig.update_yaxes(title_text="MACD", showgrid=False, row=3, col=1)

    # Set Volume color
    colors = ['red' if row['Open'] - row['Close'] >= 0
              else 'green' for index, row in df.iterrows()]
    # Add volume trace
    fig.add_trace(go.Bar(x=df.index,
                         y=df['Volume'],
                         marker_color=colors, name="Volume"
                         ), row=2, col=1)
    # 添加 AvgVol 軌跡
    fig.add_trace(
        go.Scatter(x=df.index, y=df['AvgVol'], name="Average Volume"),
        row=2, col=1
    )
    fig.update_yaxes(title_text="Volume", row=2, col=1)

    # removing white space
    fig.update_layout(margin=go.layout.Margin(
        l=60,  # left margin
        r=60,  # right margin
        b=60,  # bottom margin
        t=100  # top margin
    ))

    fig.show()
    fig.write_image(str(number) + ".jpg")

    # plt.savefig(str(true_number) +
    # fig.to_image(format="png", engine="kaleido")


def plot_chart(stock_data, true_number):
    plt.rc('figure', figsize=(15, 10))
    fig, axes = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})
    fig.tight_layout(pad=3)
    print(stock_data)
    close = stock_data.Close
    vol = stock_data.Volume
    date = stock_data.index
    plot_price = axes[0]
    plot_price.plot(date, close, color='blue',
                    linewidth=2, label='Price')
    ohlc = stock_data.loc[:, [stock_data.index, stock_data.Open, stock_data.High, stock_data.Low, stock_data.Close]]
    ohlc.date = pd.to_datetime(ohlc.index)
    fig, ax = plt.subplots()
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    fig.suptitle('Daily Candlestick Chart of NIFTY50')
    ohlc.date = ohlc.index.apply(mpl_dates.date2num)
    ohlc = ohlc.astype(float)
    date_format = mpl_dates.DateFormatter('%d-%m-%Y')
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.savefig(str(true_number) + ".jpg")  # 將圖存成 JPEG 檔


def VCMA_history(vcma_values):
    pattern = np.array([False] * 20 + [True])
    return np.array_equal(vcma_values[-21:-1], pattern[:-1]) and vcma_values[-1] == pattern[-1]


import yfinance as yf
import pandas as pd


def detect_vcp(tickers, start, ptp_list):
    true_number = 0
    run_number = 0
    today = str(datetime.datetime.now().date())
    lineNotifyMessage(token, "Start VCP: " + today + " ")
    for row in tickers[start:]:
        ptp_no = 0
        ptp = "False"
        for row2 in ptp_list:  # for row2 in ptp_list[start:]:
            # print (row,row2)
            if (row == row2):
                ptp = "True"
                ptp_no += 1
                lineNotifyMessage(token, row + " is PTP stock!")
                print(row, " is PTP stock, skip analysis!")

        if (ptp != "True"):
            # print ("Start　analysis!")
            start += 1
            print(" " + str(start), str(row))
            # print(row)
            # df = yf.download(row, start=start, end=end)
            try:
                data = yf.download(row, period="2y", progress=False)
                data['AvgVol'] = data['Volume'].rolling(55).mean()  # 55為平均的天數
                last_close_price = round(data["Close"][-1], 2)

            except:
                lineNotifyMessage(token, row + " is not exist!")
                # pass
            # print(df)

            plot_title = "{} {} {} {}".format(row, today, last_close_price, scenario)

    data['Pct Change'] = data['Close'].pct_change()
    data['Trend'] = 0
    Trend = 0
    for i in range(1, len(data)):
        if data['Close'][i] > data['Close'][i - 1]:
            if Trend == -1:
                data['Trend'][i - 1] = -1
                Trend = 0
            else:
                Trend = 1
        elif data['Close'][i] < data['Close'][i - 1]:
            if Trend == 1:
                data['Trend'][i - 1] = 1
                Trend = 0
            else:
                Trend = -1

    data['Consolidation'] = 0
    Consolidation = 0
    for i in range(1, len(data)):
        if data['Trend'][i] == 0:
            Consolidation += 1
            if Consolidation >= 5:
                data['Consolidation'][i] = 1
        else:
            Consolidation = 0

    cons_data = data[data['Consolidation'] == 1]
    cons_data = cons_data[cons_data['Volume'] < cons_data['Volume'].shift()]

    for i in range(1, len(cons_data)):
        if data['Close'][cons_data.index[i]] > data['Close'][cons_data.index[i - 1]]:
            if data['Volume'][cons_data.index[i]] > data['Volume'][cons_data.index[i - 1]]:
                print("VCP pattern found!")
                plotly_chart(data, plot_title, 0)
                lineNotifyImage(token, "Meet VCP Criteria", str(true_number) + ".jpg")


start = 0
true_number = 0
run_number = 0
today = str(datetime.datetime.now().date())
#start += 1


# unique_tickers = list(set(un_unique_tickers))
# for ticker in unique_tickers[start:]:
#    process_data(ticker)
#    run_number += 1
def detect_vcp_20230304(ticker_in, data):
    lineNotifyMessage(token, "Start VCP: " + today + " ")
    data['AvgVol'] = data['Volume'].rolling(55).mean()  # 55為平均的天數
    last_close_price = round(data["Close"][-1], 2)

    plot_title = "{} {} {} {}".format(ticker_in, today, last_close_price, scenario)

    data['Pct Change'] = data['Close'].pct_change()
    data['Trend'] = 0
    Trend = 0
    for i in range(1, len(data)):
        if data['Close'][i] > data['Close'][i - 1]:
            if Trend == -1:
                data['Trend'][i - 1] = -1
                Trend = 0
            else:
                Trend = 1
        elif data['Close'][i] < data['Close'][i - 1]:
            if Trend == 1:
                data['Trend'][i - 1] = 1
                Trend = 0
            else:
                Trend = -1

    data['Consolidation'] = 0
    Consolidation = 0
    for i in range(1, len(data)):
        if data['Trend'][i] == 0:
            Consolidation += 1
            if Consolidation >= 5:
                data['Consolidation'][i] = 1
        else:
            Consolidation = 0

    cons_data = data[data['Consolidation'] == 1]
    cons_data = cons_data[cons_data['Volume'] < cons_data['Volume'].shift()]

    for i in range(1, len(cons_data)):
        if data['Close'][cons_data.index[i]] > data['Close'][cons_data.index[i - 1]]:
            if data['Volume'][cons_data.index[i]] > data['Volume'][cons_data.index[i - 1]]:
                print("VCP pattern found!")
                plotly_chart(data, plot_title, 0)
                lineNotifyImage(token, "Meet VCP Criteria", str(true_number) + ".jpg")


def gogogo_20230304(tickers_in, df, true_number, catgory):
    global scenario
    df['AvgVol'] = df['Volume'].rolling(55).mean()  # 55為平均的天數
    last_close_price = round(df["Close"][-1], 2)

    plot_title = "{} {} {} {}".format(tickers_in, today, last_close_price, scenario)
    # plot_tile = (row + today + last_close_price)
    volatility_H = df['High'].max() / df['Close'].mean()
    volatility_L = df['Low'].min() / df['Close'].mean()
    volatility = volatility_H - volatility_L
    # print (str(len(df.index)) + " " + str(volatility_H) + " " + str(volatility_L) + " " + str(volatility))
    if (len(df.index) > 144 and volatility > 0.1):  # 過濾資料筆數少於144筆的股票，確保上市時間有半年並且判斷半年內的波動率，像死魚一樣不動的股票就不分析
        #print ("meet volume or volatility, start analysis!")
        # run_number += 1
        # print (df.head())
        # print (df.tail())
        # period = "ytd"
        # print (df.shape[0])
        df['total_price'] = df['Close'] * df['Volume']
        vcma = pd.DataFrame()
        # vcma['vcma233'] = df['total_price'].ewm(span=233, adjust=False).mean()
        # vcma['vcma144'] = df['total_price'].ewm(span=144, adjust=False).mean()
        # vcma['vcma89'] = df['total_price'].ewm(span=89, adjust=False).mean()
        # vcma['vcma55'] = df['total_price'].ewm(span=55, adjust=False).mean()
        # vcma['vcma21'] = df['total_price'].ewm(span=21, adjust=False).mean()
        # vcma['vcma5'] = df['total_price'].ewm(span=5, adjust=False).mean()
        vcma['vcma233'] = df['total_price'].rolling(window=233).sum() / df['Volume'].rolling(window=233).sum()
        vcma['vcma144'] = df['total_price'].rolling(window=144).sum() / df['Volume'].rolling(window=144).sum()
        vcma['vcma89'] = df['total_price'].rolling(window=89).sum() / df['Volume'].rolling(window=89).sum()
        vcma['vcma55'] = df['total_price'].rolling(window=55).sum() / df['Volume'].rolling(window=55).sum()
        vcma['vcma21'] = df['total_price'].rolling(window=21).sum() / df['Volume'].rolling(window=21).sum()
        vcma['vcma5'] = df['total_price'].rolling(window=5).sum() / df['Volume'].rolling(window=5).sum()
        # vcma['Result'] = (vcma['vcma5'] > vcma['vcma21']) & (vcma['vcma21'] > vcma['vcma55']) & (
        #            vcma['vcma55'] > vcma['vcma144']) & (vcma['vcma144'] > vcma['vcma233'])

        if (ForcePLOT == 1):
            # year = df[-200:]
            plotly_chart(df, plot_title, true_number)
            # plotly_chart(df, row, true_number)
            url = f'https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A{tickers_in}'
            linemessage = (
                f"{true_number} - url - ")
            # f"{start} - https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A{row2} - {info_sector}")
            lineNotifyImage(token, linemessage, str(true_number) + ".jpg")
            webbrowser.open(url)

        # vcma['VCMA89_Result'] = (vcma['vcma5'] > vcma['vcma21']) & (vcma['vcma21'] > vcma['vcma55']) & (vcma['vcma55'] > vcma['vcma89'])
        # vcma['VCMA21_Result'] = (vcma['vcma5'] > vcma['vcma21']) & (vcma['vcma21'] > vcma['vcma55'])
        vcma['VCMA55_Result'] = (vcma['vcma5'] > vcma['vcma21']) & (vcma['vcma21'] > vcma['vcma55'])
        vcma['VCMA89_Result'] = (vcma['vcma5'] > vcma['vcma21']) & (vcma['vcma21'] > vcma['vcma55']) & (
                vcma['vcma55'] > vcma['vcma89'])
        vcma['VCMA144_Result'] = (vcma['vcma5'] > vcma['vcma21']) & (vcma['vcma21'] > vcma['vcma55']) & (
                vcma['vcma55'] > vcma['vcma89']) & (vcma['vcma89'] > vcma['vcma144'])
        vcma['VCMA233_Result'] = (vcma['vcma5'] > vcma['vcma21']) & (vcma['vcma21'] > vcma['vcma55']) & (
                vcma['vcma55'] > vcma['vcma89']) & (vcma['vcma89'] > vcma['vcma144']) & (
                                         vcma['vcma144'] > vcma['vcma233'])

        VCMA5_inc = (vcma['vcma5'].iloc[-1] > vcma['vcma5'].iloc[-2])
        VCMA21_inc = (vcma['vcma5'].iloc[-1] > vcma['vcma5'].iloc[-2]) and (
                vcma['vcma21'].iloc[-1] > vcma['vcma21'].iloc[-2])
        VCMA55_inc = (vcma['vcma5'].iloc[-1] > vcma['vcma5'].iloc[-2]) and (
                vcma['vcma21'].iloc[-1] > vcma['vcma21'].iloc[-2]) and (
                             vcma['vcma55'].iloc[-1] > vcma['vcma55'].iloc[-2])
        VCMA89_inc = (vcma['vcma5'].iloc[-1] > vcma['vcma5'].iloc[-2]) and (
                vcma['vcma21'].iloc[-1] > vcma['vcma21'].iloc[-2]) and (
                             vcma['vcma55'].iloc[-1] > vcma['vcma55'].iloc[-2]) and (
                             vcma['vcma89'].iloc[-1] > vcma['vcma89'].iloc[-2])
        VCMA144_inc = (vcma['vcma5'].iloc[-1] > vcma['vcma5'].iloc[-2]) and (
                vcma['vcma21'].iloc[-1] > vcma['vcma21'].iloc[-2]) and (
                              vcma['vcma55'].iloc[-1] > vcma['vcma55'].iloc[-2]) and (
                              vcma['vcma89'].iloc[-1] > vcma['vcma89'].iloc[-2]) and (
                              vcma['vcma144'].iloc[-1] > vcma['vcma144'].iloc[-2])
        VCMA233_inc = (vcma['vcma5'].iloc[-1] > vcma['vcma5'].iloc[-2]) and (
                vcma['vcma21'].iloc[-1] > vcma['vcma21'].iloc[-2]) and (
                              vcma['vcma55'].iloc[-1] > vcma['vcma55'].iloc[-2]) and (
                              vcma['vcma89'].iloc[-1] > vcma['vcma89'].iloc[-2]) and (
                              vcma['vcma144'].iloc[-1] > vcma['vcma144'].iloc[-2]) and (
                              vcma['vcma233'].iloc[-1] > vcma['vcma233'].iloc[-2])

        vcma_values_233 = vcma['VCMA233_Result'].values
        pattern_233 = np.array([False] * 20 + [True])
        VCMA233_history = np.array_equal(vcma_values_233[-21:-1], pattern_233[:-1]) and vcma_values_233[-1] == \
                          pattern_233[-1]

        vcma_values_144 = vcma['VCMA144_Result'].values
        pattern_144 = np.array([False] * 20 + [True])
        VCMA144_history = np.array_equal(vcma_values_144[-21:-1], pattern_144[:-1]) and vcma_values_144[-1] == \
                          pattern_144[-1]

        vcma_values_89 = vcma['VCMA89_Result'].values
        pattern_89 = np.array([False] * 20 + [True])
        VCMA89_history = np.array_equal(vcma_values_89[-21:-1], pattern_89[:-1]) and vcma_values_89[-1] == pattern_89[
            -1]

        vcma_values_55 = vcma['VCMA55_Result'].values
        pattern_55 = np.array([False] * 20 + [True])
        VCMA55_history = np.array_equal(vcma_values_55[-21:-1], pattern_55[:-1]) and vcma_values_55[-1] == pattern_55[
            -1]

        FinalResult = "FALSE"
        scenario = 55
        if (scenario == 55) and (VCMA55_history == True) and (VCMA55_inc == True):
            FinalResult = "TRUE"
        elif (scenario == 89) and (VCMA89_history == True) and (VCMA89_inc == True):
            FinalResult = "TRUE"
        elif (scenario == 144) and (VCMA144_history == True) and (VCMA144_inc == True):
            FinalResult = "TRUE"
        elif (scenario == 233) and (VCMA233_history == True) and (VCMA233_inc == True):
            FinalResult = "TRUE"
        else:
            # print ("No Scenario")
            return 1
        # print(FinalResult)
        if (FinalResult == 'TRUE'):

            info_sector = ""

            # plotly_chart(df, tickers_in, true_number)
            plotly_chart(df, plot_title, true_number)
            if (catgory != "TW"):
                linemessage = (
                    f"{true_number} - https://www.tradingview.com/chart/sWFIrRUP/?symbol={tickers_in}")
                url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=" + tickers_in)
                webbrowser.open(url)

            else:
                if (tickers_in[-1] == "W"):
                    row2 = tickers_in[:4]
                    linemessage = (
                        f"{true_number} - https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A{row2}")
                    url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A" + row2)
                    webbrowser.open(url)

                else:
                    row2 = tickers_in[:4]
                    linemessage = (
                        f"{true_number} - https://www.tradingview.com/chart/sWFIrRUP/?symbol=TPEX%3A{row2}")
                    url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=TPEX%3A" + row2)
                    webbrowser.open(url)

            # open_web(url)
            # lineNotifyImage(token,str(start) + " - " + row+" - " + info_sector,str(true_number)+".jpg")
            lineNotifyImage(token, linemessage, str(true_number) + ".jpg")

        print("gogogo Finished")
    else:
        print ("Volume or volatility not meet, skip analysis!")
    # lineNotifyMessage(token, "Finished: " + today + " " + catgory + "\nScanned " + str(run_number) + " of " + str(
    #    start) + " Stocks in " + catgory + " Market\n" + str(true_number) + " Meet Criteria")
def remove_ptp_list(ptp_tickers, tickers):
    us_non_ptp_tickers = [x for x in tickers if x not in ptp_tickers]
    us_ptp_tickers = [x for x in tickers if x in ptp_tickers]
    print("PTP US stocks:", us_ptp_tickers)
    print("Non-PTP US stocks:", us_non_ptp_tickers)
    return us_non_ptp_tickers


# for ticker in unique_tickers[start:]:
#    process_data(ticker)
#    run_number += 1


def get_data(ticker_in):
    try:
        data_org = yf.download(ticker_in, period="2y", progress=False)
    except Exception as e:
        lineNotifyMessage(token, f"{ticker_in} download failed: {str(e)}")
        data_org = pd.DataFrame()  # 返回一個空的數據帧
        print("Get Data Fail")
    return data_org


"""
if (VCP == 1):
    for ticker in us_tickers[start:]:
        get_data(ticker)
        run_number += 1
    detect_vcp_20230304(us_tickers, vcp_start)

if (TEST == 1):
    gogogo(test_start, test_tickers, "TEST", ptp_lists)



else:
"""


def vcma_and_volume_screener_old(tickers_in, df, true_number, catgory, day):
    # print ("Start Screener")
    global scenario
    df['AvgVol'] = df['Volume'].rolling(5).mean()  # 55為平均的天數
    df['total_price'] = df['Close'] * df['Volume']
    last_close_price = round(df["Close"][-1], 2)
    plot_title = "{} {} {} {}".format(tickers_in, today, last_close_price, scenario)
    df['vcma{day}'] = df['total_price'].rolling(window=day).sum() / df['Volume'].rolling(window=day).sum()
    # 获取vcma列的最后两个值
    last_vcma = df['vcma{day}'].tail(1).iloc[0]
    second_last_vcma = df['vcma{day}'].tail(2).iloc[0]
    last_volume = df['Volume'].tail(1).iloc[0]
    second_last_volume = df['AvgVol'].tail(1).iloc[0]

    # 检查最后一个值是否大于最后第二个值的1.03倍
    if last_vcma > second_last_vcma * 1.03 and last_volume > second_last_volume * 2:
        plotly_chart(df, plot_title, true_number)
        linemessage = (
            f"{true_number} - https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A{tickers_in} - ")
        # f"{start} - https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A{row2} - {info_sector}")

        lineNotifyImage(token, linemessage, str(true_number) + ".jpg")


def vcma_and_volume_screener_no_comment(tickers_in, df, true_number, catgory, day):
    df = df.tail(21)  # 只留最後的資料
    df['AvgVol'] = df['Volume'].rolling(5).mean()
    df['total_price'] = df['Close'] * df['Volume']
    last_close_price = round(df["Close"].iloc[-1], 2)
    plot_title = f"{tickers_in} {today} {last_close_price} {scenario}"
    df[f'vcma{day}'] = df['total_price'].rolling(window=day).sum() / df['Volume'].rolling(window=day).sum()
    last_vcma = df[f'vcma{day}'].iloc[-1]
    second_last_vcma = df[f'vcma{day}'].iloc[-2]
    last_volume = df['Volume'].iloc[-1]
    second_last_volume = df['AvgVol'].iloc[-1]
    if last_vcma > second_last_vcma * 1.03 and last_volume > second_last_volume * 2:
        plotly_chart(df, plot_title, true_number)
        if (catgory != "TW"):
            linemessage = (
                f"{true_number} - https://www.tradingview.com/chart/sWFIrRUP/?symbol={tickers_in}")
            url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=" + tickers_in)
            webbrowser.open(url)

        else:
            if (tickers_in[-1] == "W"):
                row2 = tickers_in[:4]
                linemessage = (
                    f"{true_number} - https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A{row2}")
                url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A" + row2)
                webbrowser.open(url)
            else:
                row2 = tickers_in[:4]
                linemessage = (
                    f"{true_number} - https://www.tradingview.com/chart/sWFIrRUP/?symbol=TPEX%3A{row2}")
                url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=TPEX%3A" + row2)
                webbrowser.open(url)
        lineNotifyImage(token, linemessage, str(true_number) + ".jpg")

def vcma_and_volume_screener(tickers_in, df, true_number, catgory, day):
    # 只取最後144筆資料
    # df = df.tail(144)

    # 計算10天平均成交量和總成交金額
    df['AvgVol'] = df['Volume'].rolling(day).mean()
    #df['SMA'] = df['Close'].rolling(day).mean()
    df['total_price'] = df['Close'] * df['Volume']
    df['total_price_day'] = df['total_price'].rolling(day).mean()

    ## 最後day個交易金額大於100萬的話，才進行分析，避免掉一些太小的股票
    last_data = int(round(df['total_price_day'].tail(1).iloc[0] / 1000000)) # 使用iloc[0]取得最後一筆資料，並計算成以百萬為單位
    print(last_data)
    if last_data > 1:
        # 取得最後一天的收盤價格，用於畫圖標題
        last_close_price = round(df["Close"].iloc[-1], 2)
        plot_title = f"{tickers_in} {today} {last_close_price} {scenario} screener"

        # 計算vcma
        df[f'vcma{day}'] = df['total_price'].rolling(window=day).sum() / df['Volume'].rolling(window=day).sum()

        # 取得vcma列的最後兩個值
        last_vcma = df[f'vcma{day}'].iloc[-1]
        second_last_vcma = df[f'vcma{day}'].iloc[-2]

        # 取得最後一天的成交量和5天平均成交量的最後一個值
        last_volume = df['Volume'].iloc[-1]
        second_last_volume = df['AvgVol'].iloc[-1]

        # 如果最後一天的vcma大於最後第二天的vcma的1.03倍，並且最後一天的成交量大於5天平均成交量的最後一天的2倍，則畫圖並傳送Line通知
        if last_vcma > second_last_vcma * 1.03 and last_volume > second_last_volume * 2:
            plotly_chart(df, plot_title, true_number)
            if (catgory != "TW"):
                linemessage = (
                    f"{true_number} - https://www.tradingview.com/chart/sWFIrRUP/?symbol={tickers_in} - screener")
                url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=" + tickers_in)
                webbrowser.open(url)

            else:
                if (tickers_in[-1] == "W"):
                    row2 = tickers_in[:4]
                    linemessage = (
                        f"{true_number} - https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A{row2} - screener")
                    url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A" + row2)
                    webbrowser.open(url)

                else:
                    row2 = tickers_in[:4]
                    linemessage = (
                        f"{true_number} - https://www.tradingview.com/chart/sWFIrRUP/?symbol=TPEX%3A{row2} - screener")
                    url = ("https://www.tradingview.com/chart/sWFIrRUP/?symbol=TPEX%3A" + row2)
                    webbrowser.open(url)

            lineNotifyImage(token, linemessage, str(true_number) + ".jpg")


def party(ticker_type, tickers_in, start):
    run_number = start
    lineNotifyMessage(token, "Start: " + str(today) + " " + str(ticker_type))
    # print ("US LOOP")
    new_tickers = remove_ptp_list(ptp_lists, tickers_in)
    # new_tickers = remove_ptp_list(ptp_lists, test_tickers)
    # print (new_tickers)
    for ticker in new_tickers[start:]:
        print(ticker_type, run_number, " ", ticker)
        data = get_data(ticker)
        # print (data)
        run_number += 1
        # print ("before gogogo")
        # print (ticker)
        if (gogogo_run == 1):
            gogogo_20230304(ticker, data, run_number, ticker_type)
        if (VCP == 1):
            detect_vcp_20230304(ticker, data)
        if (VCMA_SCREENER == 1):
            vcma_and_volume_screener(ticker, data, run_number, ticker_type, screener_day)


scenario = 55
VCP = 0
VCP_TEST = 0
ForcePLOT = 0
TEST = 0
ETF = 0
TW = 1
US = 0
VCMA_SCREENER = 1
vcp_start = 0
test_start = 0
us_start = 0
tw_start = 0
etf_start = 0
ptp = 0
screener_day = 10
gogogo_run = 0

if (TEST == 1):
    party("TEST", test_tickers, test_start)
if (US == 1):
    party("US", us_tickers, us_start)
if (TW == 1):
    party("TW", tw_tickers, tw_start)
if (ETF == 1):
    party("ETF", etf_tickers, etf_start)

"""
if (US == 1):
    lineNotifyMessage(token, "Start: " + str(today) + " US")
    #print ("US LOOP")
    new_tickers = remove_ptp_list(ptp_lists, us_tickers)
    #new_tickers = remove_ptp_list(ptp_lists, test_tickers)

    #print (new_tickers)
    for ticker in new_tickers:
        print ("US" , run_number," ", ticker)
        data = get_data(ticker)
        #print (data)
        run_number += 1
        #print ("before gogogo")
        #print (ticker)
        gogogo_20230304(ticker, data, run_number, "US")
        if (VCP == 1):
            detect_vcp_20230304(ticker, data)
        #print("after gogogo")
if (TW == 1):
    gogogo(tw_start, tw_tickers, "TW", ptp_lists)
if (ETF == 1):
    gogogo(etf_start, etf_tickers, "ETF", ptp_lists)
"""
