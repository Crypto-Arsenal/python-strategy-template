DMI 動向指標
===========================


上星期六比特幣大跌，整個加密貨幣市場都跟著下盪，市場的恐慌指數也隨之上漲，越在這種人心惶惶的時刻，你越需要數據上的客觀數字來幫助你穩定心態！今天我們要討論的是DMI，一個判斷趨勢的好指標 。

## **DMI 是什麼？**

DMI（Directional Movement Index）動向指標，又稱動向指數，是由美國機械工程師 J. Welles Wilder 所提出的方法，DMI 利用股價創新高或破新低的動能大小和震盪的真實波幅去計算整體趨勢的強弱，主要用來判斷股價是否具有趨勢以及趨勢的強弱變化。

## **DMI 計算方法**

### **_前置計算_**
----------

> **_Step 1 ：取得趨勢 ＋DM 與 - DM（ Directional Movement，DM ）_**

若（ 今日 High（ 最高價 ）- 昨日 High ）> （昨日 Low（ 最低價 ）- 今日 Low ），則 ＋DM ＝（ 今日 High - 昨日 High 與 0 ）取二者中最大值，若不為 0 代表股價高點持續走高，為上漲趨勢。

若（ 昨日 Low - 今日 Low ）> （ 今日 High - 昨日 High ），則 - DM ＝（ 昨日 Low 今日 Low 與 0 ）取二者中最大值，若不為 0 代表股價低點持續走低，為下跌趨勢。

注意這裡的正負並不是「數值」的正負，而是代表往上或往下的「趨勢方向」！！！

> **_Step 2：取得真實波幅（ True Range，TR ）_**

波幅相對簡單，只需要今日的 High 和 Low 以及昨日的收盤價（ Close ）。

TR = （ 今日 High - 今日Low，今日 High - 昨日 Close，昨日 Close - 今日Low）三組中的最大值。

> **_Step 3：對3組資料分別取移動平均值，這裡時間長度以最常見的 14 為例子_**

<img alt="" class="ef es eo ex w" src="https://miro.medium.com/max/522/1*xXIdhVzlgF4mIcK-sXWPlQ.png" sizes="560px" role="presentation"/>

### **指標計算**
--------

> **_Step 1 : 計算方向指標 ＋DI 與 - DI（ Directional Indicator，DI ）_**

<img alt="" class="ef es eo ex w" src="https://miro.medium.com/max/570/1*sqkAXHS66LSfnfDdv_J28A.png" sizes="386px" role="presentation"/>

兩者求出的值皆會介於 0 至 100 之間，代表過去 14 天趨勢向上與向下的比例，其餘則代表沒有趨勢。

> **_Step 2：取得趨向指數（ Directional Movement Index，DX ）與平均趨向指數（ Average Directional Movement Index，ADX ）_**

DX：分子為 (＋DI14 減 - DI14 ) 分母為 (＋DI14 加 - DI14 ) 最後再取絕對值就可以得出 DX。

ADX：對 DX 取移動平均值

<img alt="" class="ef es eo ex w" src="https://miro.medium.com/max/1080/1*UD6CqMd696tO4QxH8AZbiQ.png" width="540" height="126" sizes="540px" role="presentation"/>

## **懶人包記憶**

講了那麼多公式，相信大家還是會有些地方搞不清楚，如果只想知道這指標大致怎麼使用的話，這裡用更簡單易懂的方式介紹 DMI 指標帶大家入門！

組成DMI指標共有3條線，分別為**正負的 DI** 再加上 **ADX**。正負的 DI 值用於判斷「 **趨勢的方向** 」，而 ADX 用於判斷 「 **趨勢的強弱** 」。

若 ＋DI 大於 - DI ，代表設定的期間內（ 前面以 14 作為例子 ）上漲趨勢較空頭趨勢明顯，而 ADX 一般以大於 20 或 25 做為有趨勢存在的判斷，而大於 30 代表趨勢強烈，另外 ADX 過高代表趨勢非常強烈，可能是趨勢即將反轉的訊號。

## **DMI 交易實例**

參考下圖當藍線 ＋DI 向上穿越橘線 - DI 可視為買入訊號，反之，＋DI 向下突破 - DI 視為賣出訊號。另外圖中的紅線為 ADX。

並不是每次的訊號都會有明顯的行情，建議投資者須參考其他指標做最終的交易判斷。

<img alt="" class="ef es eo ex w" src="https://miro.medium.com/max/1400/0*XZaCVV-4Aiqu80qz" width="700" height="608" sizes="700px" role="presentation"/>

> _關於Crypto-Arsenal_

Crypto-Arsenal致力於建構加密貨幣量化程式交易平台，打造新一代智能交易機器人開發、媒合與自動執行跟投的雲端服務，對接各大加密貨幣交易所，支援雲端或本地端策略開發環境、即時回測、實時模擬、實盤交易、計算績效指標與視覺化圖表等功能。

> _Crypto-Arsenal 社群平台_

Facebook [https://www.facebook.com/cryptoarsenal](https://www.facebook.com/cryptoarsenal)  
Instagram [https://www.instagram.com/crypto\_arsenal/](https://www.instagram.com/crypto_arsenal/)  
LinkedIn [https://www.linkedin.com/company/crypto-arsenal](https://www.linkedin.com/company/crypto-arsenal)  
Telegram 官方頻道 [https://t.me/TG\_Crypto\_Arsenal](https://t.me/TG_Crypto_Arsenal)  
Telegram 中文官方社群 [https://t.me/joinchat/-r64ASMb6A8zODdl](https://t.me/joinchat/-r64ASMb6A8zODdl)

喜歡我們文章的話，請追蹤我們的Medium並在下面給我們幾個掌聲  
我們會持續為您帶來交易相關的資訊！