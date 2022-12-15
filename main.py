#https://medium.com/geekculture/top-4-python-libraries-for-technical-analysis-db4f1ea87e09

import pandas as pd
import requests
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import datetime
import kaleido

# from datetime import datetime
from csv import reader
import bs4 as bs
import requests
import csv
import plotly.graph_objects as go
from ta.trend import MACD
from ta.momentum import StochasticOscillator

from plotly.subplots import make_subplots


# plt.style.use('seaborn')
test_tickers = ['2379.TW', 'A', '1103.TW', 'HDB', 'TFII']
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
              '5608.TW', '5609.TWO', '5701.TWO', '5703.TWO', '5704.TWO', '5706.TW', '5820.TWO', '5864.TWO', '5871.TW',
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
us_tickers = ['AAPL', 'MSFT', 'GOOG', 'GOOGL', 'AMZN', 'TSLA', 'BRK-B', 'UNH', 'XOM', 'JNJ', 'V', 'WMT', 'JPM', 'CVX',
              'NVDA', 'LLY', 'TSM', 'PG', 'MA', 'HD', 'BAC', 'META', 'PFE', 'KO', 'ABBV', 'MRK', 'PEP', 'NVO', 'COST',
              'ORCL', 'MCD', 'SHEL', 'TMO', 'ASML', 'DIS', 'AVGO', 'TM', 'TMUS', 'CSCO', 'DHR', 'AZN', 'ACN', 'WFC',
              'ABT', 'NVS', 'BABA', 'BMY', 'CRM', 'COP', 'NEE', 'SCHW', 'ADBE', 'LIN', 'NKE', 'AMGN', 'TXN', 'UPS',
              'PM', 'CMCSA', 'TTE', 'RTX', 'MS', 'HON', 'QCOM', 'T', 'NFLX', 'ELV', 'RY', 'LMT', 'IBM', 'CVS', 'LOW',
              'UNP', 'INTU', 'BHP', 'DE', 'INTC', 'TD', 'GS', 'UL', 'CAT', 'EQNR', 'MDT', 'SAP', 'HDB', 'AXP', 'SPGI',
              'SNY', 'PLD', 'HSBC', 'BP', 'BUD', 'AMD', 'ADP', 'BLK', 'SBUX', 'PYPL', 'GILD', 'CI', 'DEO', 'AMT', 'C',
              'BTI', 'CB', 'PBR', 'SYK', 'ISRG', 'RIO', 'GE', 'BA', 'NOW', 'NOC', 'MDLZ', 'TJX', 'SONY', 'MO', 'REGN',
              'MMC', 'CNI', 'VRTX', 'ENB', 'INFY', 'EOG', 'IBN', 'AMAT', 'TGT', 'PGR', 'CHTR', 'ADI', 'BKNG', 'EL',
              'DUK', 'SO', 'ZTS', 'SLB', 'HUM', 'MMM', 'BX', 'CNQ', 'GD', 'CP', 'ABNB', 'GSK', 'BDX', 'PDD', 'OXY',
              'ITW', 'BAM', 'PNC', 'FISV', 'WM', 'HCA', 'USB', 'BMO', 'CME', 'CL', 'BSX', 'CSX', 'PXD', 'AON', 'ETN',
              'TFC', 'JD', 'MRNA', 'AMX', 'MU', 'DG', 'SHW', 'MET', 'BNS', 'MUFG', 'D', 'VALE', 'CCI', 'ATVI', 'MCK',
              'MPC', 'APD', 'KDP', 'LRCX', 'GM', 'PSA', 'UBER', 'ITUB', 'EPD', 'ICE', 'NSC', 'F', 'ORLY', 'ABB', 'RELX',
              'ADM', 'MAR', 'EQIX', 'TRI', 'EMR', 'FIS', 'UBS', 'TEAM', 'PANW', 'SNOW', 'PSX', 'DVN', 'VLO', 'MCO',
              'MNST', 'HSY', 'AIG', 'CNC', 'GIS', 'AZO', 'SRE', 'VMW', 'KHC', 'LHX', 'CTVA', 'DXCM', 'ADSK', 'E',
              'ABEV', 'FCX', 'SU', 'AEP', 'KLAC', 'STZ', 'APH', 'SNPS', 'FTNT', 'SAN', 'ECL', 'NTR', 'MELI', 'WDS',
              'TRP', 'EW', 'ROP', 'STLA', 'LNG', 'SYY', 'HES', 'CTAS', 'SHOP', 'PAYX', 'TRV', 'KKR', 'RSG', 'KMB',
              'LULU', 'CMG', 'MSI', 'FDX', 'CDNS', 'ENPH', 'BCE', 'COF', 'A', 'CM', 'AFL', 'BIIB', 'TAK', 'NGG', 'JCI',
              'WDAY', 'KMI', 'BSBR', 'NXPI', 'WMB', 'AJG', 'TEL', 'PRU', 'HMC', 'IQV', 'ET', 'CVE', 'EXC', 'O', 'SMFG',
              'BBD', 'CRWD', 'MSCI', 'PCG', 'PH', 'ING', 'TT', 'ANET', 'HLT', 'ILMN', 'SCCO', 'NTES', 'RACE', 'SQ',
              'XEL', 'SPG', 'EA', 'DLTR', 'MRVL', 'MCHP', 'GPN', 'CMI', 'NUE', 'IMO', 'BK', 'ALL', 'WCN', 'NEM', 'MPLX',
              'CSGP', 'CARR', 'YUM', 'PCAR', 'KR', 'DOW', 'BNTX', 'AMP', 'ROST', 'ABC', 'ALB', 'HAL', 'CTSH', 'VOD',
              'BBDO', 'LYG', 'RMD', 'APO', 'KEYS', 'WBA', 'RIVN', 'TDG', 'BBVA', 'MFC', 'WBD', 'ED', 'VICI', 'GFS',
              'NDAQ', 'CEG', 'IDXX', 'ODFL', 'OTIS', 'ALC', 'TU', 'CPNG', 'AME', 'ROK', 'GWW', 'ON', 'DLR', 'SBAC',
              'MTB', 'STM', 'WEC', 'HLN', 'DFS', 'DD', 'CQP', 'DELL', 'PEG', 'WELL', 'MTD', 'VRSK', 'LVS', 'HPQ',
              'FAST', 'TLK', 'SE', 'CPRT', 'BAX', 'MFG', 'STT', 'CRH', 'BCS', 'FANG', 'RBLX', 'BKR', 'SQM', 'BIDU',
              'DHI', 'GOLD', 'PPG', 'GLW', 'OKE', 'VEEV', 'ES', 'AWK', 'CLR', 'CHT', 'TTD', 'K', 'WIT', 'PUK', 'RJF',
              'GMAB', 'DDOG', 'HRL', 'LYB', 'ORAN', 'NWG', 'FMX', 'GPC', 'ZM', 'SLF', 'NOK', 'TSCO', 'FITB', 'TSN',
              'IFF', 'AVB', 'ALNY', 'APTV', 'TROW', 'WTW', 'SIRI', 'CTRA', 'EXR', 'SGEN', 'ARE', 'FNV', 'LEN', 'IT',
              'LCID', 'ZBH', 'EQR', 'CDW', 'HIG', 'FERG', 'WY', 'BR', 'EIX', 'CBRE', 'FTV', 'HEI', 'DAL', 'EBAY', 'ZS',
              'VMC', 'DTE', 'FRC', 'PFG', 'ETR', 'VRSN', 'HBAN', 'FE', 'URI', 'CAJ', 'CCEP', 'ARGX', 'MBLY', 'LUV',
              'NU', 'ULTA', 'AEE', 'MKC', 'UI', 'RCI', 'MLM', 'CF', 'EFX', 'ACGL', 'EBR', 'LPLA', 'TTWO', 'ROL', 'MOH',
              'AEM', 'PAYC', 'MRO', 'RF', 'IR', 'CFG', 'EC', 'LH', 'CAH', 'PWR', 'EPAM', 'DB', 'TEF', 'GIB', 'INVH',
              'PPL', 'WRB', 'TTM', 'ANSS', 'MT', 'COIN', 'ERIC', 'RPRX', 'FTS', 'ELP', 'CHD', 'TDY', 'HPE', 'DOV',
              'XYL', 'LYV', 'MOS', 'CLX', 'ZI', 'DASH', 'QSR', 'CNP', 'NET', 'WAT', 'PBA', 'MAA', 'TS', 'TPL', 'PLTR',
              'PODD', 'AES', 'NTRS', 'IEP', 'CAG', 'JBHT', 'CNHI', 'AMCR', 'DRI', 'YUMC', 'IX', 'STE', 'STLD', 'BGNE',
              'PKI', 'WAB', 'GRMN', 'KEY', 'IEX', 'CMS', 'PINS', 'BIP', 'HOLX', 'WST', 'CHWY', 'INCY', 'BRO', 'SUI',
              'TECK', 'DGX', 'CINF', 'SYF', 'SNAP', 'MKL', 'ICLR', 'MPWR', 'MGA', 'NIO', 'BMRN', 'SJM', 'SPOT', 'CHKP',
              'EXPD', 'VTR', 'AGR', 'CPB', 'FOXA', 'WPC', 'RTO', 'BALL', 'AZPN', 'RYAAY', 'BBY', 'EXPE', 'TRGP', 'LKQ',
              'NTAP', 'WPM', 'UMC', 'HWM', 'NLOK', 'ATO', 'J', 'TRMB', 'ZBRA', 'FOX', 'FMC', 'CRBG', 'APA', 'OMC',
              'ALGN', 'HZNP', 'JKHY', 'BG', 'TCOM', 'IRM', 'TXT', 'ESS', 'BAH', 'UAL', 'EQT', 'PARAA', 'EVRG', 'FLT',
              'AKAM', 'BILL', 'FSLR', 'MGM', 'SWKS', 'ZTO', 'LSXMA', 'AVY', 'LSXMK', 'HUBS', 'LI', 'LDOS', 'TWLO', 'L',
              'SIVB', 'TYL', 'PTC', 'NVR', 'SPLK', 'COO', 'FWONK', 'SUZ', 'ARES', 'WMG', 'RCL', 'HST', 'SHG', 'LBRDA',
              'LNT', 'KB', 'KOF', 'SSNC', 'FHN', 'TER', 'KIM', 'AER', 'ERIE', 'PKX', 'LBRDK', 'AVTR', 'NDSN', 'FCNCA',
              'BEKE', 'DINO', 'SEDG', 'VIV', 'UDR', 'PEAK', 'MDB', 'GLPI', 'OVV', 'HUBB', 'PCTY', 'GDDY', 'RE', 'POOL',
              'WLK', 'DAR', 'SJR', 'ETSY', 'CSL', 'MTCH', 'PARA', 'LW', 'RPM', 'FICO', 'CPT', 'IP', 'AFG', 'FWONA',
              'NICE', 'VTRS', 'CHRW', 'ENTG', 'RS', 'CTLT', 'DPZ', 'CHK', 'IPG', 'BEN', 'GGG', 'ELS', 'ABMD', 'CAR',
              'SNA', 'EQH', 'CCL', 'SWK', 'TECH', 'WTRG', 'ICL', 'TRU', 'AAP', 'UHAL', 'TOST', 'BAP', 'CNA', 'BXP',
              'TW', 'ASX', 'NFE', 'PKG', 'WDC', 'PHG', 'AMH', 'TTC', 'GL', 'TAP', 'NBIX', 'MMP', 'FNF', 'VFC', 'WES',
              'SSL', 'CRL', 'ACI', 'AR', 'WOLF', 'STX', 'MAS', 'WSO', 'UTHR', 'ACM', 'DOX', 'BIO', 'SNN', 'NI', 'BJ',
              'NRG', 'CCJ', 'CE', 'CG', 'CUK', 'HII', 'CS', 'REG', 'SWAV', 'BSY', 'DT', 'REXR', 'HOOD', 'H', 'RGEN',
              'AXON', 'EWBC', 'SRPT', 'CDAY', 'KMX', 'TFX', 'QGEN', 'SBNY', 'ARCC', 'RGA', 'CFR', 'MORN', 'JNPR', 'WMS',
              'NWS', 'TEVA', 'JHX', 'IHG', 'NMR', 'DOCU', 'GRAB', 'XP', 'NWSA', 'BLDR', 'SCI', 'WPP', 'VST', 'HSIC',
              'LAMR', 'WBS', 'ARMK', 'CZR', 'ZEN', 'LSI', 'BKI', 'CUBE', 'EMN', 'ALLE', 'PLUG', 'CMA', 'AGCO', 'UNM',
              'MKTX', 'DKS', 'LNC', 'PHM', 'RDY', 'DECK', 'BCH', 'WSC', 'BURL', 'GFL', 'QRVO', 'PSTG', 'OKTA', 'AAL',
              'AEG', 'ADT', 'BRKR', 'HAS', 'FLEX', 'JAZZ', 'ESLT', 'HTHT', 'STOR', 'BWA', 'G', 'RRX', 'SNX', 'JBL',
              'LOGI', 'U', 'PSNY', 'MTN', 'WRK', 'FFIV', 'NLY', 'LBTYK', 'CASY', 'GME', 'UHS', 'RHI', 'ALLY', 'NOV',
              'CBSH', 'LII', 'AOS', 'LEGN', 'PAA', 'FIVE', 'AGL', 'IBKR', 'DCP', 'LEA', 'LBTYA', 'PAG', 'WSM', 'PFGC',
              'CCK', 'CGNX', 'DISH', 'LECO', 'DBX', 'GGB', 'PSO', 'BEP', 'FRT', 'OTEX', 'FBHS', 'FND', 'OC', 'GLOB',
              'OLN', 'JEF', 'KEP', 'TFII', 'HR', 'MTDR', 'GTLS', 'JLL', 'FMS', 'SKM', 'TPR', 'PNW', 'ZION', 'MUSA',
              'BBWI', 'CHDN', 'BSMX', 'KNX', 'PAC', 'KRTX', 'WHR', 'SBS', 'LUMN', 'CFLT', 'MIDD', 'OHI', 'ACHC', 'ROKU',
              'TTEK', 'MANH', 'ZG', 'AQN', 'PCOR', 'GNRC', 'Z', 'NNN', 'MUR', 'OGE', 'BOKF', 'UGI', 'RBC', 'NVCR',
              'SWN', 'WAL', 'RBA', 'RCM', 'GTLB', 'GFI', 'SEIC', 'ORI', 'CHH', 'WEX', 'KNSL', 'AIZ', 'CIEN', 'AA',
              'CACI', 'GPK', 'PATH', 'MASI', 'PNR', 'DCI', 'LSCC', 'NXST', 'CLVT', 'IVZ', 'WCC', 'ALV', 'NCLH', 'CLF',
              'MPW', 'CELH', 'SEE', 'MEDP', 'EME', 'XM', 'SGFY', 'CHE', 'WH', 'DXC', 'PDCE', 'SBSW', 'SSB', 'EGP',
              'RNR', 'ASR', 'USFD', 'DKNG', 'VMI', 'KBR', 'HTZ', 'BSAC', 'AMC', 'TIXT', 'HALO', 'VOYA', 'WFG', 'GMED',
              'OGN', 'APLS', 'XRAY', 'CLH', 'WYNN', 'KT', 'HRB', 'ATR', 'TXRH', 'MAT', 'S', 'ARW', 'RRC', 'PB', 'DLB',
              'COLD', 'SF', 'DLO', 'CW', 'HQY', 'APP', 'REYN', 'DVA', 'EDR', 'STWD', 'PEN', 'ELAN', 'CYBR', 'IOT',
              'CPRI', 'ITT', 'IRDM', 'RGLD', 'BRX', 'IONS', 'SON', 'RL', 'HOG', 'CNXC', 'FR', 'PNFP', 'NEP', 'GBCI',
              'CHRD', 'ST', 'NWL', 'TME', 'GNTX', 'HLI', 'NTNX', 'BYD', 'MHK', 'NFG', 'ASND', 'WF', 'EXAS', 'CIB',
              'NVT', 'ESTC', 'CACC', 'CAE', 'RH', 'VLY', 'FLO', 'BERY', 'AYI', 'MTZ', 'LEVI', 'PHI', 'TIMB', 'CIVI',
              'QDEL', 'HCP', 'AN', 'SAIC', 'PII', 'XPEV', 'AFRM', 'AIRC', 'GIL', 'WWE', 'SIGI', 'RLI', 'XPO', 'MDU',
              'SNV', 'EXLS', 'INGR', 'DSGX', 'VAC', 'OSK', 'CHX', 'FYBR', 'ASH', 'CSAN', 'COTY', 'DTM', 'M', 'ONB',
              'STAG', 'OPCH', 'UBSI', 'WTFC', 'PPC', 'TRQ', 'AU', 'VRT', 'ALK', 'CR', 'CCCS', 'MKSI', 'DNB', 'PBF',
              'LTHM', 'LAD', 'ENLC', 'TX', 'WWD', 'FSV', 'DDS', 'ONON', 'STN', 'LFUS', 'SM', 'SITE', 'PRGO', 'AMN',
              'LSTR', 'QLYS', 'BLD', 'ADC', 'CX', 'EHC', 'HUN', 'TREX', 'NVST', 'FFIN', 'POST', 'MGY', 'DOOO', 'FSK',
              'INFA', 'MP', 'WU', 'YMM', 'PYCR', 'PRI', 'BC', 'EXEL', 'PLNT', 'SWCH', 'INSP', 'BEPC', 'FCN', 'DNA',
              'BPOP', 'DRVN', 'IDA', 'GOL', 'FAF', 'SLGN', 'AXTA', 'BWXT', 'SRC', 'CMC', 'LNW', 'SYNH', 'HOMB', 'SKX',
              'HP', 'PENN', 'VVV', 'LNTH', 'TKR', 'THG', 'IAA', 'MSA', 'LHCG', 'CABO', 'NATI', 'LYFT', 'ORA', 'LITE',
              'AMKR', 'DOCS', 'BLCO', 'OZK', 'NOVT', 'SAIA', 'FNB', 'CADE', 'TOL', 'AM', 'KRC', 'RYN', 'LANC', 'GWRE',
              'RYAN', 'FUTU', 'ENSG', 'OSH', 'SWX', 'RHP', 'KNTK', 'AIT', 'WIX', 'GH', 'VAL', 'X', 'AMG', 'BAK', 'ALGM',
              'BIPC', 'MNDY', 'THC', 'DV', 'NYT', 'EXPO', 'WING', 'PSN', 'CALX', 'COLM', 'TDOC', 'ASAI', 'COHR', 'AQUA',
              'KGC', 'WTS', 'HWC', 'OMF', 'SAM', 'CIG', 'FIBK', 'HXL', 'TPX', 'TSEM', 'BZ', 'OLED', 'EXP', 'RUN',
              'SPSC', 'DEN', 'NE', 'NTRA', 'MSM', 'COKE', 'ORCC', 'FTI', 'TGNA', 'CHPT', 'VNO', 'TENB', 'SMAR', 'HGV',
              'AGNC', 'PDI', 'BCPC', 'AXS', 'STVN', 'CERE', 'OWL', 'WEN', 'FCFS', 'UFPI', 'ROG', 'VIPS', 'THO', 'LEG',
              'CROX', 'SOFI', 'CC', 'IPGP', 'LPX', 'ITCI', 'FIZZ', 'ESI', 'PAGS', 'NJR', 'GXO', 'BXMT', 'FIX', 'KNBE',
              'IAC', 'NVEI', 'ASAN', 'UMPQ', 'TRNO', 'ASGN', 'NYCB', 'AUY', 'APPF', 'BKH', 'HAE', 'DAVA', 'UNVR',
              'EEFT', 'MQ', 'SJI', 'GRFS', 'FLR', 'KRG', 'CPG', 'FIVN', 'CRSP', 'ESNT', 'SLM', 'EDU', 'IART', 'ACT',
              'R', 'OGS', 'PINC', 'CIGI', 'CRK', 'ATCO', 'HE', 'CWST', 'FN', 'VIRT', 'MTSI', 'WNS', 'NTLA', 'BHF',
              'IGT', 'CBT', 'UCBI', 'BOX', 'NARI', 'GPS', 'CWEN', 'MTG', 'EVR', 'WK', 'NSP', 'ZWS', 'SFBS', 'SRCL',
              'CYTK', 'MAN', 'GLBE', 'TNET', 'KEX', 'POR', 'CNM', 'PGNY', 'GEF', 'NEWR', 'ALSN', 'CVI', 'TFSL', 'CVBF',
              'SLAB', 'PNM', 'DNLI', 'COUP', 'INDB', 'RITM', 'EVA', 'SEAS', 'BXSL', 'FRSH', 'ERF', 'NSA', 'ALTR',
              'ATKR', 'AIMC', 'AJRD', 'UMBF', 'APLE', 'AL', 'APG', 'ATI', 'WHD', 'ALIT', 'IRTC', 'SNDR', 'W', 'POWI',
              'CRUS', 'MMSI', 'HKD', 'ALKS', 'CWAN', 'JHG', 'ARWR', 'MRTX', 'MMS', 'FELE', 'DNP', 'TRTN', 'PTEN', 'FLS',
              'BSM', 'AEL', 'MSGS', 'PVH', 'AVT', 'FOXF', 'BFAM', 'SYNA', 'IRT', 'FUL', 'ZD', 'ROIV', 'VET', 'SSD',
              'SGML', 'SMPL', 'BECN', 'SR', 'GSAT', 'ABCM', 'ASB', 'NTCO', 'PCH', 'PRVA', 'OLLI', 'AGO', 'SUN', 'CUZ',
              'AB', 'GATX', 'BE', 'TNDM', 'APPN', 'SMCI', 'WTM', 'ABCB', 'TWNK', 'LAZ', 'ICUI', 'EURN', 'MLI', 'KSS',
              'ASO', 'ETRN', 'DY', 'PLTK', 'QS', 'VC', 'GT', 'DOCN', 'AXNX', 'ESGR', 'BILI', 'PECO', 'NCNO', 'DQ',
              'ABG', 'REZI', 'AAON', 'PPBI', 'VIAV', 'OMCL', 'EBC', 'MODG', 'BTU', 'AWI', 'DOC', 'BEAM', 'INST', 'UNF',
              'PAAS', 'STAA', 'GO', 'AZTA', 'BL', 'SKY', 'EVO', 'ATHM', 'LAC', 'AYX', 'LU', 'ADNT', 'NNI', 'RDN', 'HRI',
              'ABCL', 'ONTO', 'UAA', 'ONEM', 'CBU', 'FRHC', 'RMBS', 'NSIT', 'BTG', 'AWR', 'CWT', 'SANM', 'RNG', 'SPT',
              'BMBL', 'GOLF', 'CATY', 'DUOL', 'DIOD', 'CRC', 'BRBR', 'TRIP', 'ESMT', 'BMI', 'JWN', 'IS', 'SID', 'ALE',
              'FHB', 'TDC', 'SEM', 'BNL', 'JXN', 'RUM', 'LOPE', 'CEQP', 'AY', 'GTES', 'FTCH', 'SUM', 'AGI', 'SFM',
              'LPL', 'STNE', 'SBRA', 'BPMC', 'AMED', 'MSTR', 'FHI', 'AVNT', 'TNL', 'BANF', 'VSCO', 'ACA', 'TXG', 'EVH',
              'SPWR', 'SIG', 'SQSP', 'PWSC', 'HRMY', 'VSAT', 'CNX', 'NEA', 'NWE', 'ARLP', 'AHCO', 'OMAB', 'VNT', 'DEI',
              'AMRC', 'PACW', 'IBOC', 'EPRT', 'SPXC', 'HI', 'BDC', 'OUT', 'CORT', 'TMHC', 'FULT', 'GHC', 'BOH', 'ALRM',
              'PEGA', 'ATUS', 'FOLD', 'SFNC', 'HHC', 'KFY', 'VSH', 'PDO', 'YPF', 'VIR', 'TCBI', 'KMPR', 'AVA', 'GLPG',
              'NEU', 'CPA', 'KWR', 'TWKS', 'PI', 'SXT', 'HIW', 'VRNS', 'ABM', 'OFC', 'TV', 'AEIS', 'UA', 'JBT', 'MMYT',
              'CNS', 'EYE', 'GLNG', 'WD', 'FL', 'INMD', 'PK', 'IIPR', 'PRTA', 'FBP', 'EPR', 'LBRT', 'SSRM', 'ENVX',
              'EQC', 'WFRD', 'LFST', 'NCR', 'PFSI', 'AMR', 'CHGG', 'TKC', 'JAMF', 'JJSF', 'LSPD', 'WSFS', 'AAWW',
              'BLKB', 'FSS', 'OTTR', 'PSEC', 'JOBY', 'RARE', 'FRPT', 'MRCY', 'NEOG', 'XMTR', 'TAL', 'THS', 'COOP',
              'MATX', 'KOS', 'SRAD', 'CRVL', 'BRZE', 'WOOF', 'ACIW', 'AIN', 'YETI', 'QRTEA', 'EVEX', 'CVT', 'FWRD',
              'MTH', 'LAZR', 'TR', 'BKU', 'COMM', 'OLPX', 'PR', 'ARCH', 'CALM', 'HL', 'MAIN', 'FRO', 'ZIM', 'ISEE',
              'STNG', 'BCO', 'CVLT', 'PBH', 'PTCT', 'LCII', 'GKOS', 'AZEK', 'GPI', 'PLXS', 'ENV', 'LXP', 'RUSHA',
              'YELP', 'IFS', 'PTON', 'CRI', 'CPE', 'ULCC', 'UGP', 'MC', 'RIG', 'ENOV', 'ARVN', 'RLAY', 'MCW', 'BCC',
              'BB', 'HUBG', 'USM', 'PAYO', 'VERX', 'SMG', 'NOG', 'ENS', 'AVAL', 'ZGN', 'VRRM', 'COLB', 'LESL', 'RPD',
              'FRME', 'CWK', 'SITC', 'ARRY', 'IBTX', 'BCRX', 'ACAD', 'TEX', 'OI', 'DORM', 'IPAR', 'MYOV', 'AUB', 'PDCO',
              'WIRE', 'WB', 'PCVX', 'CBZ', 'FROG', 'CCOI', 'PZZA', 'NTCT', 'CBRL', 'NHI', 'LIVN', 'WMK', 'NOMD', 'HPK',
              'SLG', 'BANR', 'AMBP', 'NGVT', 'WAFD', 'CNO', 'KBH', 'JBLU', 'HBI', 'SHLS', 'IBP', 'BRFS', 'FLNC', 'MXL',
              'NAD', 'VNOM', 'UNFI', 'IMCR', 'MGEE', 'MGPI', 'SGRY', 'WERN', 'IBA', 'FFBC', 'FOUR', 'IOSP', 'KLIC',
              'CNMD', 'VERV', 'PROK', 'CXM', 'SPR', 'ALHC', 'MLCO', 'TPG', 'EQRX', 'PAGP', 'AUR', 'DNUT', 'RKLB', 'RRR',
              'BOWL', 'HEP', 'WSBC', 'PCRX', 'TAC', 'HASI', 'MEOH', 'AGTI', 'BHC', 'EXG', 'FLYW', 'NVG', 'SHO', 'EVTC',
              'GNW', 'PRK', 'DKL', 'MAC', 'SHOO', 'PRMW', 'TCN', 'TOWN', 'NEX', 'ABR', 'MGRC', 'AX', 'SAVE', 'EXTR',
              'FUN', 'ENIC', 'WLY', 'WOR', 'XENE', 'FSR', 'FOCS', 'IBRX', 'SCL', 'YOU', 'PRFT', 'VRNT', 'NUVA', 'BRC',
              'JKS', 'ELF', 'NVEE', 'KW', 'SYBT', 'RXDX', 'MNTK', 'TRN', 'ESAB', 'HELE', 'HLNE', 'URBN', 'JBGS', 'SAGE',
              'PD', 'UTF', 'ICFI', 'CENT', 'AVAV', 'CMTG', 'XRX', 'CPK', 'GBDC', 'DAN', 'NPO', 'VZIO', 'ITRI', 'TRMK',
              'ESE', 'WDFC', 'KD', 'MDC', 'AG', 'FA', 'DBRG', 'RNST', 'MRVI', 'VICR', 'SHAK', 'AMBA', 'PRGS', 'OLK',
              'NVMI', 'RNW', 'CSQ', 'TRMD', 'LGIH', 'CEIX', 'PLMR', 'KMT', 'CENTA', 'RES', 'ATSG', 'CLBK', 'PEB',
              'TTEC', 'LTH', 'JOE', 'MANU', 'AMLX', 'ARNC', 'GDRX', 'SJW', 'FATE', 'AEO', 'LFG', 'HLF', 'LAUR', 'INSM',
              'SLVM', 'LKFN', 'CTKB', 'BLMN', 'RLX', 'HTLF', 'DK', 'SG', 'CSGS', 'ENR', 'KAI', 'CVCO', 'UDMY', 'EPC',
              'ITGR', 'FCPT', 'STEM', 'TASK', 'PAX', 'NAVI', 'CSIQ', 'KEN', 'XPRO', 'FBC', 'TRUP', 'KTB', 'NXE', 'SONO',
              'MFGP', 'BKE', 'CD', 'NOVA', 'CRCT', 'NUS', 'PRCT', 'INSW', 'SES', 'GMS', 'CCU', 'HAYW', 'SITM', 'CSWI',
              'RCUS', 'OR', 'VCTR', 'CRDO', 'KRYS', 'NBTB', 'EXPI', 'PSMT', 'EFSC', 'ZIP', 'ACLS', 'SGHC', 'RLJ', 'IHS',
              'DRH', 'APAM', 'NABL', 'ASZ', 'PACB', 'CIXX', 'SHC', 'PTVE', 'TTGT', 'BROS', 'FBK', 'XHR', 'ATRC', 'SNEX',
              'TDS', 'PLAY', 'STER', 'ODP', 'COUR', 'UPST', 'CERT', 'FORG', 'RXRX', 'RELY', 'HCC', 'BBUC', 'SBCF',
              'TCBK', 'TDCX', 'THRM', 'ATGE', 'ARCB', 'NWBI', 'UTG', 'AKRO', 'CAKE', 'HTH', 'TWST', 'GFF', 'SKT', 'ETY',
              'JACK', 'SI', 'XPEL', 'STEP', 'SUPN', 'NMIH', 'SPB', 'SAH', 'TIGO', 'ADX', 'AMPL', 'WE', 'HLIO', 'SSTK',
              'RVNC', 'BFH', 'GDV', 'SIX', 'WGO', 'GDS', 'CNNE', 'BAMR', 'GOOS', 'RVMD', 'HTGC', 'SABR', 'UNIT', 'VTYX',
              'CTRE', 'MWA', 'WRBY', 'QTWO', 'AXSM', 'SBLK', 'SAFE', 'TROX', 'ERJ', 'IMKTA', 'MTX', 'LNN', 'RVLV',
              'NVAX', 'EMBC', 'ROIC', 'FTDR', 'SIMO', 'GOGO', 'EVT', 'AVDX', 'ZLAB', 'NZF', 'ALG', 'PRME', 'NS', 'SKIN',
              'SMTC', 'TEO', 'BUR', 'IQ', 'BMEZ', 'HMY', 'MTRN', 'BRP', 'PJT', 'USAC', 'LILAK', 'FTAI', 'XNCR', 'LILA',
              'UPWK', 'LZ', 'TPH', 'ADTN', 'CRS', 'DSEY', 'SEMR', 'YY', 'SDGR', 'BIGZ', 'ETWO', 'NUV', 'CTOS', 'KAHC',
              'PIPR', 'GPOR', 'STRA', 'B', 'NAPA', 'CVII', 'BVN', 'EVCM', 'GOGL', 'NUVL', 'BATRA', 'EVRI', 'TALO',
              'ZETA', 'BOOT', 'SILK', 'NTB', 'IRWD', 'VBTX', 'BBU', 'MPLN', 'SEAT', 'GPRE', 'WABC', 'ADUS', 'CLM',
              'OPEN', 'CLFD', 'BATRK', 'PFS', 'HAIN', 'CARG', 'MYGN', 'IVT', 'KAR', 'VSTO', 'NWN', 'MIR', 'ROCC',
              'MAXR', 'MNSO', 'BLDP', 'UE', 'STEL', 'ELME', 'AAT', 'CMP', 'CLDX', 'MSGE', 'MNRL', 'ROAD', 'HLIT', 'RQI',
              'VRTV', 'VGR', 'ARI', 'KYMR', 'BDJ', 'MD', 'TEN', 'GETY', 'FLNG', 'MDRX', 'AMPS', 'GET', 'BBIO', 'ROCK',
              'COHU', 'TLRY', 'LVWR', 'ESTE', 'MARA', 'DCT', 'MCY', 'LMND', 'GOF', 'FGEN', 'RFP', 'TBBK', 'DOOR',
              'DICE', 'HMN', 'NBR', 'OXM', 'HOPE', 'BCAT', 'AIR', 'AMEH', 'LTC', 'FBNC', 'GSBD', 'USA', 'MSEX', 'GAB',
              'VVNT', 'SWTX', 'DH', 'DEA', 'QFIN', 'AGYS', 'NBHC', 'ARCO', 'MLKN', 'AGIO', 'HPP', 'CIM', 'TTMI', 'DAWN',
              'SASR', 'SATS', 'VCSA', 'CSTM', 'HURN', 'BTRS', 'TMDX', 'ALLO', 'ALVO', 'ETV', 'FORM', 'UEC', 'NG',
              'IOVA', 'IRBT', 'CVNA', 'CINC', 'MRTN', 'FREY', 'GCMG', 'AMPH', 'LYEL', 'SWI', 'MNRO', 'CGC', 'CHCO',
              'AMK', 'INT', 'CODI', 'MCRI', 'FNA', 'TDW', 'CLMT', 'MEI', 'RVT', 'TY', 'HCM', 'EAT', 'SAND', 'IDCC',
              'LGND', 'BGCP', 'DVAX', 'NAC', 'HLMN', 'MMI', 'CRTO', 'SAVA', 'TSLX', 'GTY', 'PGRE', 'PTY', 'RYTM', 'PHR',
              'TVTX', 'UCTT', 'APPS', 'CLNE', 'GVA', 'TELL', 'STBA', 'CPRX', 'CCS', 'NKLA', 'CCRN', 'OLO', 'EGBN',
              'DHT', 'MYRG', 'SRCE', 'VRE', 'LOB', 'BTT', 'ZNTL', 'ECAT', 'OPK', 'RCKT', 'EPAC', 'NMRK', 'SOVO', 'LRN',
              'ME', 'AI', 'ERII', 'CVAC', 'GEL', 'MLNK', 'BUSE', 'ALKT', 'TSP', 'ACVA', 'INTA', 'POSH', 'CYRX', 'PAM',
              'DGII', 'ALEX', 'MODN', 'VIVO', 'JPS', 'KTOS', 'CHEF', 'RC', 'SFL', 'PSNYW', 'PARR', 'EVOP', 'LXU',
              'OSIS', 'KDNY', 'PL', 'VCYT', 'TGH', 'JBI', 'CNXN', 'NVRO', 'ECVT', 'ESTA', 'GTN', 'DCOM', 'BSTZ', 'KRNT',
              'DNOW', 'SBH', 'PBFX', 'MODV', 'CLS', 'PCT', 'LADR', 'WWW', 'OMI', 'KFRC', 'FCF', 'SNDX', 'IMGN', 'OII',
              'OFG', 'TMCI', 'HEES', 'PTRA', 'ALGT', 'BXMX', 'AKR', 'OCFC', 'NXGN', 'MATV', 'BHLB', 'SVC', 'CRSR',
              'PDM', 'PAY', 'KROS', 'PLUS', 'SCHL', 'AFYA', 'PGTI', 'EAF', 'CNK', 'MEG', 'JWSM', 'MED', 'PRM', 'MAG',
              'UAN', 'OTLY', 'PRAA', 'EVBG', 'HYT', 'INBX', 'VRTS', 'SAFT', 'TGS', 'SPTN', 'CAAP', 'UTZ', 'GNL', 'PX',
              'SBGI', 'PMT', 'KALU', 'HESM', 'FDP', 'MDGL', 'TBK', 'RAMP', 'AAC', 'ATEN', 'VCEL', 'UVV', 'FCEL', 'KN',
              'OBNK', 'INFN', 'AGM', 'FINV', 'TWO', 'PIII', 'RYI', 'IAS', 'KREF', 'VVX', 'ETG', 'IHRT', 'CASH', 'RCII',
              'AVID', 'SSP', 'OCSL', 'FLGT', 'CXW', 'PLRX', 'NMFC', 'FIGS', 'CTS', 'TARO', 'SBR', 'ECPG', 'WOW', 'GDEN',
              'SPCE', 'TMP', 'KYN', 'FRG', 'STEW', 'ESRT', 'DFIN', 'PUMP', 'LBAI', 'MHO', 'HNI', 'GIC', 'AIV', 'ANDE',
              'DAC', 'STKL', 'ENVA', 'NXRT', 'CWH', 'HTLD', 'BLU', 'RIOT', 'FBRT', 'PRA', 'TH', 'ARKO', 'ARHS', 'FVRR',
              'BGS', 'CRON', 'AVO', 'SXI', 'DDD', 'EIG', 'EVTL', 'MNTV', 'SWIR', 'DCPH', 'USPH', 'HFWA', 'DIN', 'GABC',
              'UUUU', 'SLN', 'OSTK', 'AROC', 'SANA', 'AUPH', 'PSFE', 'BDN', 'IONQ', 'AMSF', 'RILY', 'CMRE', 'PRO',
              'HRT', 'SHEN', 'KRP', 'NIC', 'GGAL', 'MORF', 'INTR', 'CDRE', 'GBX', 'LC', 'CFFN', 'VIST', 'SPNS', 'AXL',
              'TNC', 'WBX', 'PLL', 'CDMO', 'SBSI', 'PFBC', 'KRO', 'GSM', 'DSL', 'CUBI', 'MBUU', 'AMWL', 'RDNT', 'APE',
              'CCSI', 'ADEA', 'LZB', 'RETA', 'EVV', 'ADPT', 'BIGC', 'STC', 'HERA', 'COMP', 'LPI', 'EGO', 'PATK', 'RXT',
              'BALY', 'CPUH', 'ANGI', 'PRIM', 'CDE', 'ASLE', 'ATRI', 'ATEC', 'GRBK', 'PRLB', 'COWN', 'EBS', 'CINT',
              'QQQX', 'USER', 'CSR', 'NFJ', 'GENI', 'KURA', 'SPH', 'ADV', 'USNA', 'ERO', 'CBD', 'CDNA', 'BCOR', 'NSSC',
              'CAMT', 'GEO', 'ARQT', 'EXFY', 'WTI', 'PERI', 'KIND', 'BBN', 'RDWR', 'FSLY', 'BRKL', 'GDOT', 'WTTR',
              'NMZ', 'PFC', 'PAYA', 'CGAU', 'TNK', 'MBIN', 'PLYA', 'HCSG', 'DNN', 'DMLP', 'LICY', 'AVNS', 'SLCA',
              'BORR', 'ASIX', 'EQX', 'RGNX', 'NYMT', 'DFH', 'ACRS', 'HBM', 'APOG', 'MFA', 'NRC', 'ZUO', 'PNT', 'GLP',
              'PLAB', 'MGI', 'HIMX', 'RNP', 'MTTR', 'BANC', 'AMTB', 'IMXI', 'CRNX', 'STGW', 'CAL', 'FWRG', 'BST',
              'BRSP', 'CET', 'MCRB', 'WNC', 'KIDS', 'NEXT', 'SPNT', 'FPF', 'BLFS', 'RGR', 'AZZ', 'ASTE', 'GOSS', 'BYND',
              'BHE', 'TGLS', 'BHVN', 'HLX', 'BFS', 'DBI', 'TRS', 'ENTA', 'BBDC', 'DO', 'AUS', 'MUC', 'VORB', 'VERU',
              'MRUS', 'CNOB', 'PDS', 'ERAS', 'DCBO', 'MGNI', 'DCGO', 'AMCX', 'PTA', 'AZUL', 'SLDP', 'PTLO', 'KAMN',
              'UMH', 'FNKO', 'ACLX', 'WALD', 'JBSS', 'BFLY', 'PBT', 'AMPX', 'AMRS', 'HWKN', 'SSYS', 'AVXL', 'ORLA',
              'VECO', 'NHC', 'SNCY', 'TA', 'MYTE', 'NVGS', 'HOLI', 'VLRS', 'RA', 'INVA', 'NEO', 'CONX', 'OEC', 'BMA',
              'JRVR', 'NTST', 'AGRO', 'HIMS', 'OFLX', 'INDI', 'TWI', 'LWLG', 'RBCAA', 'ANF', 'MOD', 'COGT', 'MOMO',
              'GIII', 'GES', 'LMAT', 'CLBT', 'MERC', 'SCRM', 'AOSL', 'CARS', 'IE', 'BTZ', 'ENFN', 'RTL', 'CANO', 'FFWM',
              'GERN', 'INN', 'IMVT', 'SNPO', 'HOUS', 'STAR', 'CUTR', 'THRD', 'ETW', 'DSGN', 'MNKD', 'BIOX', 'CLB',
              'CBL', 'SKYW', 'SII', 'PDFS', 'SUMO', 'ALLG', 'REPL', 'QURE', 'ACEL', 'PFHC', 'CNDT', 'RADI', 'EXAI',
              'IMTX', 'CCF', 'GAM', 'BY', 'GPRK', 'VREX', 'SA', 'MIRM', 'EDIT', 'MCG', 'GSHD', 'QCRH', 'HQH', 'JELD',
              'IGMS', 'NAAS', 'ARGO', 'ULH', 'EOS', 'HTBK', 'SP', 'LGV', 'NYAX', 'WINA', 'CHCT', 'SLP', 'PNTM', 'GPRO',
              'APGB', 'UTL', 'BKD', 'SCS', 'CTBI', 'PEBO', 'OXLC', 'LPRO', 'OSW', 'CHY', 'WASH', 'MATW', 'BV', 'TGTX',
              'UVSP', 'INNV', 'NRK', 'NRDS', 'PUBM', 'THQ', 'DM', 'SMP', 'STRL', 'HAFC', 'MRC', 'AWF', 'VTOL', 'REVG',
              'BCX', 'FSM', 'RWT', 'BCSF', 'ROVR', 'BOC', 'IDYA', 'PRG', 'ANAB', 'NVX', 'KNSA', 'PRS', 'FVIV', 'DADA',
              'WLKP', 'DOLE', 'HIBB', 'CMCO', 'VTEX', 'NOAH', 'AVPT', 'ORGN', 'TMST', 'DRQ', 'AHH', 'EFC', 'VRDN',
              'WEST', 'FORR', 'SHYF', 'VVI', 'ACCD', 'WETF', 'PRDO', 'HTD', 'RPT', 'CHI', 'RENN', 'AOD', 'ALEC', 'PAR',
              'BRMK', 'VRNA', 'BRLT', 'VRAY', 'FBMS', 'DLX', 'OSCR', 'PLOW', 'MQY', 'LPSN', 'SCSC', 'JPC', 'CII', 'CRF',
              'KRUS', 'RKT', 'BFC', 'RICK', 'TITN', 'FPI', 'PWP', 'BSIG', 'LOMA', 'NFBK', 'AMWD', 'MUI', 'HSKA', 'BJRI',
              'NMM', 'GSBC', 'IMAX', 'PGRU', 'RNA', 'HFRO', 'HGTY', 'EOCW', 'SVFA', 'UBA', 'SBOW', 'ICHR', 'SLRC',
              'AERI', 'SILV', 'PLYM', 'NBXG', 'SCHN', 'JANX', 'MCB', 'HSTM', 'MAXN', 'MOV', 'HONE', 'BCYC', 'CHS', 'OM',
              'OPI', 'VHI', 'CCO', 'NX', 'TLS', 'CAPL', 'FMBH', 'BLNK', 'RSKD', 'HA', 'BTWN', 'ECOM', 'MVST', 'MFIC',
              'VLD', 'CRAI', 'CLW', 'SRNE', 'KRNY', 'MYE', 'THRY', 'IMOS', 'ITOS', 'OBE', 'AVD', 'MLAB', 'AGEN',
              'LMACA', 'SCOA', 'TNGX', 'GGR', 'GRC', 'LGAC', 'PGC', 'AMAL', 'BLTE', 'SLAM', 'CEPU', 'HLVX', 'MXCT',
              'ASTL', 'FFC', 'TRST', 'WKME', 'TRDA', 'FC', 'ARR', 'LPG', 'NKTR', 'RUTH', 'AMRK', 'HZO', 'GDYN', 'IESC',
              'OSBC', 'SYM', 'EE', 'NRGX', 'LAND', 'NNOX', 'BRY', 'UFPT', 'GOOD', 'MRSN', 'NESR', 'RAPT', 'ACHR',
              'HCKT', 'FPAC', 'SGMO', 'CLOV', 'TCPC', 'IAG', 'PAXS', 'CCVI', 'NEXA', 'EIM', 'SCWX', 'SLI', 'GSEV',
              'LEU', 'MYI', 'TIL', 'CFB', 'ANIP', 'JQC', 'BXC', 'IGR', 'ATNI', 'HBNC', 'CHRS', 'SIGA', 'TBI', 'SHCR',
              'IDT', 'BHIL', 'PDT', 'SD', 'FUBO', 'UHT', 'ACRE', 'EGLE', 'SGH', 'TILE', 'TBPH', 'TRTX', 'CRNC', 'NOTE',
              'BNGO', 'DENN', 'UFCS', 'SCVL', 'VNET', 'MOR', 'BTO', 'RPTX', 'CGBD', 'CENX', 'YEXT', 'ATEX', 'EXK',
              'CERS', 'YSG', 'HCCI', 'NGD', 'AUDC', 'CRGY', 'BHG', 'PHK', 'EHAB', 'EB', 'NVTS', 'TSE', 'LAW', 'VTRU',
              'CEVA', 'WDI', 'ZH', 'INVZ', 'NNDM', 'SIBN', 'SNBR', 'GSL', 'LBC', 'ETD', 'GHIX', 'VTNR', 'EFXT', 'DWAC',
              'CFIV', 'IPSC', 'ARCE', 'CLDT', 'NKTX', 'CAC', 'EOI', 'EBIX', 'ALCC', 'MSBI', 'MTLS', 'DLY', 'NAT', 'RGP',
              'ALT', 'GCO', 'PTSI', 'LQDT', 'GWH', 'DOMO', 'YORW', 'KVSC', 'COLL', 'CGEM', 'CSII', 'BFST', 'TRNS',
              'MIT', 'LCA', 'STOK', 'ACQR', 'CATC', 'TTI', 'QNST', 'BBAR', 'CSTL', 'IPI', 'BBSI', 'NXP', 'AMBC', 'CVGW',
              'VMEO', 'KELYA', 'ABST', 'CMAX', 'PGY', 'SLGC', 'NRIX', 'PAHC', 'COCO', 'FFIC', 'EGIO', 'FCBC', 'UIS',
              'KC', 'AEHR', 'VNDA', 'DYN', 'TGI', 'HAYN', 'EWTX', 'CCBG', 'CRBU', 'THR', 'VMO', 'MVIS', 'CASS', 'PMVP',
              'GMRE', 'BOE', 'MBI', 'ICPT']
etf_tickers = ['AAAU', 'AAPD', 'AAPU', 'AAXJ', 'ABEQ', 'ACES', 'ACWI', 'ACWV', 'ACWX', 'AGG', 'AGGY', 'AGQ', 'AGZ',
               'AGZD', 'AIA', 'AIRR', 'ALTL', 'AMLP', 'AMZA', 'AMZD', 'AMZU', 'ANGL', 'AOA', 'AOK', 'AOM', 'AOR',
               'ARKF', 'ARKG', 'ARKK', 'ARKQ', 'ARKW', 'ASHR', 'AVDE', 'AVDV', 'AVEM', 'AVES', 'AVIG', 'AVIV', 'AVLV',
               'AVRE', 'AVSD', 'AVUS', 'AVUV', 'BAB', 'BALT', 'BAR', 'BBAX', 'BBCA', 'BBEU', 'BBH', 'BBIN', 'BBJP',
               'BBRE', 'BBSA', 'BBUS', 'BCI', 'BERZ', 'BIB', 'BIBL', 'BIL', 'BILS', 'BITI', 'BITO', 'BIV', 'BIZD',
               'BKLC', 'BKLN', 'BLCN', 'BLOK', 'BLV', 'BMAR', 'BMEZ', 'BND', 'BNDW', 'BNDX', 'BNO', 'BNOV', 'BOIL',
               'BOND', 'BOTZ', 'BRZU', 'BSCM', 'BSCN', 'BSCO', 'BSCP', 'BSCQ', 'BSCR', 'BSCS', 'BSJM', 'BSJN', 'BSJO',
               'BSJP', 'BSJQ', 'BSMN', 'BSMT', 'BSTZ', 'BSV', 'BTAL', 'BTF', 'BUCK', 'BUFD', 'BUFR', 'BUG', 'BULZ',
               'BWX', 'BYTE', 'CALF', 'CATH', 'CCOR', 'CDC', 'CDL', 'CEMB', 'CFO', 'CGCP', 'CGDV', 'CGGO', 'CGGR',
               'CGUS', 'CGW', 'CGXU', 'CHAU', 'CHIE', 'CHIQ', 'CIBR', 'CLOU', 'CLSC', 'CLTL', 'CMBS', 'CMDY', 'CMF',
               'CNCR', 'CNRG', 'COM', 'COMB', 'COMT', 'COPX', 'CORN', 'CORP', 'COWZ', 'CPER', 'CQQQ', 'CRBN', 'CSB',
               'CSTNL', 'CTA', 'CURE', 'CWB', 'CWEB', 'CWI', 'CXSE', 'CYA', 'DAPR', 'DAUG', 'DBA', 'DBB', 'DBC', 'DBE',
               'DBEF', 'DBJP', 'DBMF', 'DBO', 'DDM', 'DEF', 'DEM', 'DES', 'DFAC', 'DFAE', 'DFAI', 'DFAR', 'DFAS',
               'DFAT', 'DFAU', 'DFAX', 'DFCF', 'DFEB', 'DFEM', 'DFEN', 'DFEV', 'DFIC', 'DFIP', 'DFIS', 'DFIV', 'DFNM',
               'DFSD', 'DFSV', 'DFUS', 'DFUV', 'DGRO', 'DGRW', 'DGS', 'DHS', 'DIA', 'DIAL', 'DIG', 'DIHP', 'DISV',
               'DIV', 'DIVB', 'DIVO', 'DJD', 'DJIA', 'DJUL', 'DLN', 'DLS', 'DLY', 'DMXF', 'DNL', 'DOCT', 'DOG', 'DOL',
               'DON', 'DPST', 'DRIP', 'DRIV', 'DRLL', 'DRN', 'DRSK', 'DRV', 'DSEP', 'DSI', 'DSTL', 'DTD', 'DTH', 'DUG',
               'DUHP', 'DUSL', 'DUST', 'DVY', 'DVYE', 'DWAS', 'DWM', 'DWX', 'DXD', 'DXJ', 'EAGG', 'EBND', 'ECH', 'EDC',
               'EDOG', 'EDV', 'EDZ', 'EELV', 'EEM', 'EEMS', 'EEMV', 'EES', 'EFA', 'EFAV', 'EFAX', 'EFG', 'EFV', 'EFZ',
               'EIDO', 'EMB', 'EMGF', 'EMHY', 'EMLC', 'EMLP', 'EMQQ', 'EMXC', 'ENFR', 'EPHE', 'EPI', 'EPOL', 'EPP',
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
               'GLTR', 'GMF', 'GMOM', 'GNMA', 'GNR', 'GOVT', 'GQRE', 'GRES', 'GRID', 'GSEW', 'GSG', 'GSIE', 'GSLC',
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
               'TSLQ', 'TSLS', 'TTT', 'TUR', 'TWM', 'TYO', 'TZA', 'UCO', 'UCON', 'UDN', 'UDOW', 'UGA', 'UGL', 'UITB',
               'UJAN', 'UMAR', 'UNG', 'UOCT', 'UPAR', 'UPRO', 'URA', 'URNM', 'URTH', 'URTY', 'USCI', 'USD', 'USDU',
               'USFR', 'USHY', 'USIG', 'USMF', 'USMV', 'USO', 'USRT', 'USTB', 'USVM', 'USXF', 'UTSL', 'UTWO', 'UUP',
               'UVIX', 'UVXY', 'UWM', 'UYLD', 'VAMO', 'VAW', 'VB', 'VBK', 'VBR', 'VCIT', 'VCLT', 'VCR', 'VCSH', 'VDC',
               'VDE', 'VEA', 'VEGI', 'VEU', 'VFH', 'VFVA', 'VGDTF', 'VGIT', 'VGK', 'VGLT', 'VGSH', 'VGT', 'VHT', 'VIG',
               'VIGI', 'VIOG', 'VIOO', 'VIOV', 'VIS', 'VIXM', 'VIXY', 'VLU', 'VLUE', 'VMBS', 'VNGUF', 'VNLA', 'VNM',
               'VNQ', 'VNQI', 'VO', 'VOE', 'VONE', 'VONG', 'VONV', 'VOO', 'VOOG', 'VOOV', 'VOT', 'VOTE', 'VOX', 'VPL',
               'VPU', 'VRIG', 'VRP', 'VSGX', 'VSS', 'VT', 'VTC', 'VTEB', 'VTHR', 'VTI', 'VTIP', 'VTV', 'VTWG', 'VTWO',
               'VTWV', 'VUG', 'VUSB', 'VV', 'VWO', 'VWOB', 'VXF', 'VXUS', 'VYM', 'VYMI', 'WANT', 'WCLD', 'WEAT', 'WEBL',
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


if __name__ == "__main__":
    token = 'YuvfgED98JDWMvATPEAnDu3u9Ge0R2B9BkrOvCwHZId'
    # message = '基本功能測試'


# lineNotifyMessage(token, message)

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


# 需加入均線在上升的條件(今天VCMA需大於昨日VCMA)
# start = datetime.datetime(2021,2,10)
# start = ("2021-02-10")
# end = datetime.datetime.now()
# end = datetime.now().date().strftime("$Y-$m-$d")
# delta = datetime.timedelta(days = 500)
#
# print (start)
# print (end)
# end = datetime.datetime(2022,8,18)
# def genImage (tickers,df,)
# plt.rcParams["font.family"]=["Microsoft JhengHei"]   # 中文字型
# plt.title('Stock Price')
# df = yf.download("TSLA", period="60d")
# stock2330=twstock.Stock('2330')
# plt.plot(df.Close)      # 取得近 31 日股價串列
##plt.grid(True)
# plt.savefig('stock.jpg')       # 將圖存成 JPEG 檔
# for row in range(start,tickers):
token = 'YuvfgED98JDWMvATPEAnDu3u9Ge0R2B9BkrOvCwHZId'


def plotly_chart(dfin, ticker, number):
    # Reference: https://python.plainenglish.io/a-simple-guide-to-plotly-for-plotting-financial-chart-54986c996682
    # ticker = 'AAPL'
    # df = yf.download(symbol, start='2020-01-01')

    df = dfin[-266:]
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
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA5'] = df['Close'].rolling(window=5).mean()

    # add VCMA to df
    df['total_price'] = df['Close'] * df['Volume']
    df['vcma233'] = df['total_price'].rolling(window=233).sum() / df['Volume'].rolling(window=233).sum()
    df['vcma144'] = df['total_price'].rolling(window=144).sum() / df['Volume'].rolling(window=144).sum()
    df['vcma55'] = df['total_price'].rolling(window=55).sum() / df['Volume'].rolling(window=55).sum()
    df['vcma21'] = df['total_price'].rolling(window=21).sum() / df['Volume'].rolling(window=21).sum()
    df['vcma5'] = df['total_price'].rolling(window=5).sum() / df['Volume'].rolling(window=5).sum()

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

    # Set MACD color
    colors = ['green' if val >= 0
              else 'red' for val in macd.macd_diff()]
    # Add MACD trace
    fig.add_trace(go.Bar(x=df.index,
                         y=macd.macd_diff(),
                         marker_color=colors
                         ), row=3, col=1)
    fig.add_trace(go.Scatter(x=df.index,
                             y=macd.macd(),
                             line=dict(color='black', width=2)
                             ), row=3, col=1)
    fig.add_trace(go.Scatter(x=df.index,
                             y=macd.macd_signal(),
                             line=dict(color='blue', width=1)
                             ), row=3, col=1)
    fig.update_yaxes(title_text="MACD", showgrid=False, row=3, col=1)

    # Set Volume color
    colors = ['green' if row['Open'] - row['Close'] >= 0
              else 'red' for index, row in df.iterrows()]
    # Add volume trace
    fig.add_trace(go.Bar(x=df.index,
                         y=df['Volume'],
                         marker_color=colors
                         ), row=2, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)

    # removing white space
    fig.update_layout(margin=go.layout.Margin(
        l=20,  # left margin
        r=20,  # right margin
        b=20,  # bottom margin
        t=40  # top margin
    ))

    # fig.write_image(str(number) +".jpg")
    # layout = go.layout(
    #    autosize=False,
    #    width=1080,
    #    height=960,
    # )
    # fig = go.Figure(layout=layout)
    # img_bytes = fig.to_image(format="jpg",width=1080,height=960)
    # Image()
    fig.show()
    fig.write_image(str(number) + ".jpg")

    # plt.savefig(str(true_number) +
    # fig.to_image(format="png", engine="kaleido")


def plot_chart(stock_data, true_number):
    plt.rc('figure', figsize=(15, 10))
    fig, axes = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})
    fig.tight_layout(pad=3)
    # plt.plot(df.Close)
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
    # plot_vol = axes[1]
    # plot_vol.bar(date, vol, width=15, color='darkgrey')
    # plt.grid(True)
    # Formatting Date
    date_format = mpl_dates.DateFormatter('%d-%m-%Y')
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.savefig(str(true_number) + ".jpg")  # 將圖存成 JPEG 檔


# lineNotifyImage(token,'台積電 2330','stock.jpg')
# start = 5000
def gogogo(start, tickers, catgory):
    # i = 0

    true_number = 0
    run_number = 0
    today = str(datetime.datetime.now().date())
    token = 'YuvfgED98JDWMvATPEAnDu3u9Ge0R2B9BkrOvCwHZId'
    lineNotifyMessage(token, "Start: " + today + " " + catgory)
    for row in tickers[start:]:
        start += 1
        print(catgory + " " + str(start), str(row))
        # print(row)
        # df = yf.download(row, start=start, end=end)
        df = yf.download(row, period="2y")
        volatility_H = df['High'].max() / df['Close'].mean()
        volatility_L = df['Low'].min() / df['Close'].mean()
        volatility = volatility_H - volatility_L
        # print (str(len(df.index)) + " " + str(volatility_H) + " " + str(volatility_L) + " " + str(volatility))
        if (len(df.index) > 377 and volatility > 0.1):  # 過濾資料筆數少於377筆的股票，確保上市時間夠久並且判斷2年內的波動率，像死魚一樣不動的股票就不分析
            run_number += 1
            # print (df.head())
            # print (df.tail())
            # period = "ytd"
            # print (df.shape[0])
            df['total_price'] = df['Close'] * df['Volume']
            vcma = pd.DataFrame()
            vcma['vcma233'] = df['total_price'].rolling(window=233).sum() / df['Volume'].rolling(window=233).sum()
            vcma['vcma144'] = df['total_price'].rolling(window=144).sum() / df['Volume'].rolling(window=144).sum()
            vcma['vcma55'] = df['total_price'].rolling(window=55).sum() / df['Volume'].rolling(window=55).sum()
            vcma['vcma21'] = df['total_price'].rolling(window=21).sum() / df['Volume'].rolling(window=21).sum()
            vcma['vcma5'] = df['total_price'].rolling(window=5).sum() / df['Volume'].rolling(window=5).sum()
            vcma['Result'] = (vcma['vcma5'] > vcma['vcma21']) & (vcma['vcma21'] > vcma['vcma55']) & (
                        vcma['vcma55'] > vcma['vcma144']) & (vcma['vcma144'] > vcma['vcma233'])
            if (TEST == 1):
                # year = df[-200:]
                plotly_chart(df, row, true_number)
                linemessage = (
                    f"{start} - https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A{row} - ")
                # f"{start} - https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A{row2} - {info_sector}")
                lineNotifyImage(token, linemessage, str(true_number) + ".jpg")
            if (vcma['Result'].values[-1] == True) \
                    and (vcma['Result'].values[-2] == False) \
                    and (vcma['Result'].values[-3] == False) \
                    and (vcma['Result'].values[-4] == False) \
                    and (vcma['Result'].values[-5] == False) \
                    and (vcma['Result'].values[-6] == False) \
                    and (vcma['Result'].values[-7] == False) \
                    and (vcma['Result'].values[-8] == False) \
                    and (vcma['Result'].values[-9] == False) \
                    and (vcma['Result'].values[-10] == False) \
                    and (vcma['Result'].values[-11] == False) \
                    and (vcma['Result'].values[-12] == False) \
                    and (vcma['Result'].values[-13] == False) \
                    and (vcma['Result'].values[-14] == False) \
                    and (vcma['Result'].values[-15] == False) \
                    and (vcma['Result'].values[-16] == False) \
                    and (vcma['Result'].values[-17] == False) \
                    and (vcma['Result'].values[-18] == False) \
                    and (vcma['Result'].values[-19] == False) \
                    and (vcma['Result'].values[-20] == False) \
                    and (vcma['vcma5'].values[-1] > vcma['vcma5'].values[-2]) \
                    and (vcma['vcma21'].values[-1] > vcma['vcma21'].values[-2]) \
                    and (vcma['vcma55'].values[-1] > vcma['vcma55'].values[-2]) \
                    and (vcma['vcma144'].values[-1] > vcma['vcma144'].values[-2]):
                # and (vcma['vcma233'].values[-1] > vcma['vcma233'].values[-2]) :
                # filename = str(row) + ".jpg"
                # print (filename)
                # plot_df = df
                # ticker = yf.Ticker(row)
                # info = ticker.info
                # info_sector = info['sector']
                # plt.figure().clear()
                # print (row,"TRUE")
                ##plt.rcParams["font.family"]=["Microsoft JhengHei"]   # 中文字型
                # plot_title = str(row) + str(info_sector)
                print(row, "TRUE")

                if (catgory != "ETF"):
                    ticker = yf.Ticker(row)
                    info = ticker.info
                    info_sector = info['sector']
                    # info_sector = ""
                else:
                    info_sector = ""
                # plt.figure().clear()
                # plt.title(row)
                # df = yf.download("TSLA", period="60d")
                # stock2330=twstock.Stock('2330')
                # print(info_sector)
                # plt.plot(df.Close)  # 取得近 31 日股價串列
                # plt.grid(True)
                # plt.savefig(str(true_number) + ".jpg")  # 將圖存成 JPEG 檔
                # plot_chart(df)
                plotly_chart(df, row, true_number)
                if (catgory != "TW"):

                    linemessage = (
                        f"{start} - https://www.tradingview.com/chart/sWFIrRUP/?symbol={row} - {info_sector}")
                else:
                    if (row[-1] == "W"):
                        row2 = row[:4]
                        linemessage = (
                            f"{start} - https://www.tradingview.com/chart/sWFIrRUP/?symbol=TWSE%3A{row2} - {info_sector}")
                    else:
                        row2 = row[:4]
                        linemessage = (
                            f"{start} - https://www.tradingview.com/chart/sWFIrRUP/?symbol=TPEX%3A{row2} - {info_sector}")

                # lineNotifyImage(token,str(start) + " - " + row+" - " + info_sector,str(true_number)+".jpg")
                lineNotifyImage(token, linemessage, str(true_number) + ".jpg")

                # lineNotifyMessage(token, row)
                true_number += 1
                if (catgory == "ETF" and catgory != "TEST"):
                    t = Ticker(row)
                    etf_weighting = t.fund_sector_weightings
                    print(etf_weighting)

                    # lineNotifyMessage(token,etf_weighting)
    print("Finished")
    lineNotifyMessage(token, "Finished: " + today + " " + catgory + "\nScanned " + str(run_number) + " of " + str(
        start) + " Stocks in " + catgory + " Market\n" + str(true_number) + " Meet Criteria")
    # sector weightings, returns pandas DataFrame

    # else:
    # row_str = ''.join(str(row))
    # print (row_str)
    # print (row)
    # string out = String.Join(delimiter, row);
    # out = "https://tw.tradingview.com/chart/aHk3who2/?symbol="row
    # lineNotifyMessage(token,result)
    # lineNotifyMessage(token, row)
    #    print ("FALSE")

    # US = "1"
TEST = 0
ETF = 0
TW = 1
US = 0
test_start = 0
us_start = 0
tw_start = 0
etf_start = 0
# import csv
# ticker_file = "test.csv"
# ticker_file = "russell_2000_stocklist_test.csv"
# ticker_file = "tw_all_stocklist.csv"
# ticker_file = "E:\Rojer\Desktop\\sp500_stocklist_test.csv"
# with open(ticker_file, newline='') as f:          # Read lines separately
#    reader = csv.reader(f, delimiter='t')
#    tickers = list(reader)
# print(tickers)
# country = "TW"
# country = "US"


if (TEST == 1):
    gogogo(test_start, test_tickers, "TEST")


else:
    if (US == 1):
        gogogo(us_start, us_tickers, "US")
    if (TW == 1):
        gogogo(tw_start, tw_tickers, "TW")
    if (ETF == 1):
        gogogo(etf_start, etf_tickers, "ETF")
# gogogo (us_tickers,"USTW")

