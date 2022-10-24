MFI 資金流量指標
===========================

_MFI 通常被認為是領先指標，通常用來預測市場走勢，透過 MFI 觀察出的超買、超賣訊號，可以幫你識別潛在的逆轉，在大盤隨時上下震盪、方向不明的現在， MFI 或許能成為指引你下一步操作的明燈！_
## **什麼是 MFI？** ##
Money Flow Index（ 簡稱 MFI ）資金流量指標，也稱為成交量加權相對強弱指標（ Volume Relative Strength Index , VRSI ）。MFI 是從前幾篇介紹過的 **<a href= "https://medium.com/@mkrt.crypto.arsenal/%E8%A9%B2%E8%B2%B7-%E8%A9%B2%E8%B3%A3-%E4%BE%86%E5%95%8F%E6%8A%80%E8%A1%93%E6%8C%87%E6%A8%99-4-f31274e6abe8">RSI（ Relative Strength Index ）</a>** 優化改良而來，它不像 RSI 只考慮價格因素，MFI 同時分析了價格以及成交量，屬於衡量買賣雙方壓力的指標。
## **MFI 計算方法** ##
MFI 的計算公式較複雜，以下將拆解為四個步驟，其中時間頻率設為 n（ 大多設定為 14 ）。  
>
><img alt="" class="nv py ef es eo ex w c" role="presentation" src="https://miro.medium.com/max/1400/1*H-jmq-XLG-xjzrbMu8gfAw.png" srcset="https://miro.medium.com/max/552/1*H-jmq-XLG-xjzrbMu8gfAw.png 276w, https://miro.medium.com/max/1104/1*H-jmq-XLG-xjzrbMu8gfAw.png 552w, https://miro.medium.com/max/1280/1*H-jmq-XLG-xjzrbMu8gfAw.png 640w, https://miro.medium.com/max/1400/1*H-jmq-XLG-xjzrbMu8gfAw.png 700w" sizes="700px"/>
>

**NOTE :**  
計算出來的 MFI 值可以解釋為買方佔買賣雙方總力道的比例，因此會介於 0 至 100 之間，通常當 MFI 上升代表買入壓力增加，反之 MFI 下降則表示賣出壓力增加。

### ** 常用交易主邏輯 ** ###
常用的 MFI 交易邏輯和前面介紹過的 RSI 指標相似，可以用來做為判斷超買與超賣的情況，比較好的是 MFI 額外地將成交量考量在內。

>
>**1. 當 MFI 低於 20 時，代表短期欠缺資金流動，等到 MFI 反轉向上突破 20 時，可以視為買入訊號。**
>
>**2. 當 MFI 高於 80 時，代表短期資金過熱，等到 MFI 反轉向下跌破 80 時，可以視為賣出訊號。**
>
>**3. 當股價和 MFI 同步上升時，且 MFI 高於 80 以上，代表行情超買，可以視為賣出訊號。**
>
>**4. 當股價和 MFI 同步下降時，且 MFI 低於 20 以下，代表行情超賣，可以視為買入訊號。**
>
>**5. 當股價和 MFI 反向背離時，股價出現新低點，而 MFI 出現較高點，代表買方力道逐漸增強，可以視為買入訊號。**
>
>**6. 當股價和 MFI 反向背離時，股價出現新高點，而 MFI 出現較低點，代表賣方力道逐漸增強，可以視為賣出訊號。**
>


## ** 使用 Crypto Arsenal 平台實做交易回測 **
>**交易標的：**  
>ETH / USDT
>
>**使用Ｋ棒：**  
>2 小時Ｋ
>
>**交易時長：**  
>2 個月（ 2020–07–01 00:00 至 2020–08–31 00:00 ）
>
>**買入條件：**  
>若前一個 K 棒的 MFI 值在 20 以上，且現在 K 棒的 MFI 跌破 20，就判斷行情為超賣，則買入 20%。
>
>**賣出條件：**  
>若前一個 K 棒的 MFI 值在 80 以下，且現在 K 棒的 MFI 突破 80，就判斷行情為超買，則賣出所有倉位。
>
**回測結果：<font size="5">＋19.74%</font>**

### **Step 1 : 選擇策略**
先登入 Crypto Arsenal 交易平台，至左手邊選單選擇我的策略（ My Strategy ），進入後點找到右上角的新增策略（ New Strategy ），最後在選單中選擇 MFI，並按下建立。
<img alt="" class="lp abo fl fw ft gc v c" role="presentation" src="https://miro.medium.com/max/1400/1*ji6g0uFtrmWsDukkem-Djg.png" srcset="https://miro.medium.com/max/552/1*ji6g0uFtrmWsDukkem-Djg.png 276w, https://miro.medium.com/max/1104/1*ji6g0uFtrmWsDukkem-Djg.png 552w, https://miro.medium.com/max/1280/1*ji6g0uFtrmWsDukkem-Djg.png 640w, https://miro.medium.com/max/1400/1*ji6g0uFtrmWsDukkem-Djg.png 700w" sizes="700px"/>
<font size="1"><center>Step 1 : 選擇策略</center></font>

### **Step 2 : 選擇多空交易對**
分別輸入各個欄位，我們只以交易現貨且只做多為例子，所以 Type 欄位選擇 「 SPOT 」，Trend 欄選擇「 Long 」。輸入完後點選 Save 儲存，此時畫面不會跳轉，直接選擇 EDITOR 進入回測畫面。
<img alt="" class="lp abo fl fw ft gc v c" role="presentation" src="https://miro.medium.com/max/1400/1*0ZYMpqyBqE4QrlGaEpxtEA.png" srcset="https://miro.medium.com/max/552/1*0ZYMpqyBqE4QrlGaEpxtEA.png 276w, https://miro.medium.com/max/1104/1*0ZYMpqyBqE4QrlGaEpxtEA.png 552w, https://miro.medium.com/max/1280/1*0ZYMpqyBqE4QrlGaEpxtEA.png 640w, https://miro.medium.com/max/1400/1*0ZYMpqyBqE4QrlGaEpxtEA.png 700w" sizes="700px"/>
<font size="1"><center>Step 2 : 選擇多空交易對</center></font>

### **Step 3：調整回測時段**
先在 Backtesting Interval 選擇回測時間，右邊可以迅速選擇平台已經設定好的回測期間，1Y 代表「 最近1年 」，也可以點選月曆的小圖示選取自己喜歡的開始和結束時間，這裡使用 2020/10/01 至 2020/11/30 為例。其他數值例如 Spread（ 買賣價差 ）、Fee（ 交易手續費 ）等都可以依喜好修改，這裡我們直接使用平台默認值。
<img alt="" class="lp abo fl fw ft gc v c" role="presentation" src="https://miro.medium.com/max/1400/1*SDx8vrj8S8U2na9LoiL8gA.png" srcset="https://miro.medium.com/max/552/1*SDx8vrj8S8U2na9LoiL8gA.png 276w, https://miro.medium.com/max/1104/1*SDx8vrj8S8U2na9LoiL8gA.png 552w, https://miro.medium.com/max/1280/1*SDx8vrj8S8U2na9LoiL8gA.png 640w, https://miro.medium.com/max/1400/1*SDx8vrj8S8U2na9LoiL8gA.png 700w" sizes="700px"/>
<font size="1"><center>Step 3：調整回測時段</center></font>

### **Step 4：修改程式碼**
接下來看程式碼，先不要離開～回測模板 Crypto Arsenal 已經全部寫好囉，只要設定我們自己想要調整的參數就可以了，這邊也會對所有用得到的參數一一做說明。
>#### **使用到的參數說明：** 
>**第 9 行 self.period：**<p>設定 K 線區間，單位為秒，若為 60 * 60 代表小時 Ｋ，這次使用 2 小時 Ｋ。</p>
>
>**第 13 行 self.proportion：**  
>每次買入條件被觸發後，想投入多少比例的總資產，這裏使用 0.2 ，也就是單次買入 20 %，最多買至 100 %。
>
>**第 14 行 self.mfi_period：**  
>在計算現金流量時的 K 線頻率（等同於前面介紹計算方法的時間頻率 n ），單位為 self.period 設定的時間區間，這邊使用 14 個 2 小時 Ｋ。
>
>**第 15 行 self.overbought：**  
>設定 MFI 值的上界，這邊設定為 80。
>
>**第 16 行 self.oversold：**  
>設定 MFI 值的下界，這邊設定為 20。
>

以上就是我們在 MFI 策略回測上常會使用到的參數，可以自己輸入其他數值玩玩看哦！最後按下右上角藍色的 Run and Debug 按鈕開始回測！
<img alt="" class="lp abo fl fw ft gc v c" role="presentation" src="https://miro.medium.com/max/1400/1*rDzvVkot2Nos7xFDqPDV5w.png" srcset="https://miro.medium.com/max/552/1*rDzvVkot2Nos7xFDqPDV5w.png 276w, https://miro.medium.com/max/1104/1*rDzvVkot2Nos7xFDqPDV5w.png 552w, https://miro.medium.com/max/1280/1*rDzvVkot2Nos7xFDqPDV5w.png 640w, https://miro.medium.com/max/1400/1*rDzvVkot2Nos7xFDqPDV5w.png 700w" sizes="700px"/>
<font size="1"><center>Step 4：修改程式碼</center></font>

稍等一下就可以看到這 2 個月的資產變化情形和最大回撤狀況！
<img alt="" class="lp abo fl fw ft gc v c" role="presentation" src="https://miro.medium.com/max/1400/1*RXp4xQEe4mXQ9ZZeYG44VQ.png" srcset="https://miro.medium.com/max/552/1*RXp4xQEe4mXQ9ZZeYG44VQ.png 276w, https://miro.medium.com/max/1104/1*RXp4xQEe4mXQ9ZZeYG44VQ.png 552w, https://miro.medium.com/max/1280/1*RXp4xQEe4mXQ9ZZeYG44VQ.png 640w, https://miro.medium.com/max/1400/1*RXp4xQEe4mXQ9ZZeYG44VQ.png 700w" sizes="700px"/>
<font size="1"><center>資產曲線</center></font>

看到資產曲線代表程式執行上沒問題，那如果對交易點位有疑問的話，可以在右下方的 Log 欄位找到所有買賣的進出場點，藉此與程式做比對。

最後為此交易策略的 Performance Metrics 基本績效表現：
<img alt="" class="lp abo fl fw ft gc v c" width="700" height="352" role="presentation" src="https://miro.medium.com/max/1400/1*FT-m6DfOxi5HUjbNBl853w.png" srcset="https://miro.medium.com/max/552/1*FT-m6DfOxi5HUjbNBl853w.png 276w, https://miro.medium.com/max/1104/1*FT-m6DfOxi5HUjbNBl853w.png 552w, https://miro.medium.com/max/1280/1*FT-m6DfOxi5HUjbNBl853w.png 640w, https://miro.medium.com/max/1400/1*FT-m6DfOxi5HUjbNBl853w.png 700w" sizes="700px"/>
<font size="1"><center>Performance Metrics</center></font>

回測期間兩個月就有 19.74% 獲利 ( ROI )，一直想要量化交易卻遲遲不知道如何下手嗎，只要利用此平台選擇自己想要交易策略，就能輕鬆實現囉～

**<font size="3" color="#FF0000"><center>提醒讀者，任何投資都有風險，回測績效都有經過篩選，請謹慎評估後再使用。</center></font>**
**<font size="3" color="#FF0000"><center>提醒讀者，任何投資都有風險，回測績效都有經過篩選，請謹慎評估後再使用。</center></font>**
**<font size="3" color="#FF0000"><center>提醒讀者，任何投資都有風險，回測績效都有經過篩選，請謹慎評估後再使用。</center></font>**
  
MFI 策略在 Crypto Arsenal 平台屬於 Premium 等級的會員專屬策略，此外也有提供一般使用者許多免費策略模板和建立個人策略的功能，平台也支持跟單服務，趕快來註冊使用吧！
## **關於 Crypto-Arsenal**
Crypto-Arsenal 致力於建構加密貨幣量化程式交易平台，打造新一代智能交易機器人開發、媒合與自動執行跟投的雲端服務，對接各大加密貨幣交易所，支援雲端或本地端策略開發環境、即時回測、實時模擬、實盤交易、計算績效指標與視覺化圖表等功能。
#### **Crypto-Arsenal 社群平台**
Facebook https://www.facebook.com/cryptoarsenal  
Instagram https://www.instagram.com/crypto_arsenal/  
LinkedIn https://www.linkedin.com/company/crypto-arsenal  
Telegram 官方頻道 https://t.me/TG_Crypto_Arsenal  
Telegram 中文官方社群 https://s.crypto-arsenal.io/CADiscussionGroup  

喜歡我們文章的話，請追蹤我們的Medium並在下面給我們幾個掌聲  
我們會持續為您帶來交易相關的資訊！






