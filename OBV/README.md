OBV 能量潮指標
===========================

_相信大家在投資時都會注意到標的物的成交量，成交量所代表的不僅僅是有多少人目前正在關注這隻標的，同時也展現了市場行情動能的變化，一起來看看OBV能在技術指標上展現出怎樣的信號吧！_
## **什麼是 OBV？** ##
On Balance Volume（ 簡稱 OBV ）能量潮指標，屬於一種成交量指標，1963 年在 Joseph Granville 的著作《New Key to Stock Market Profits》中所提出。認為股價的動能最主要是受到成交量所影響，量是價的先行指標，因此依照收盤價的漲跌來累計每日的成交量，並以此累積值當作市場行情動能變化趨勢的指標。
## **OBV 計算方法** ##
>可以使用當日收盤價來計算，也能使用平均收盤價來當作依據。依照收盤價的漲跌可以分為三種情形，並依此得出漲跌雙方動能消長的趨勢變化，其中 t 代表當期，t-1 即代表前一期：  
>
>**1. 當期收盤價 > 前一期收盤價，OBV<sub>t</sub> =OBV<sub>t-1</sub> + 當期成交量**
>
>**2. 當期收盤價 = 前一期收盤價，OBV<sub>t</sub> =OBV<sub>t-1</sub>**
>
>**3. 當期收盤價 < 前一期收盤價，OBV<sub>t</sub> =OBV<sub>t-1</sub> — 當期成交量**
>
>Note：求出的 OBV 值主要應用在線圖的走勢方向，並非 OBV 值本身的大小，因為不同的起始值將會產生不同的 OBV 線圖，但相對的線型走勢是一致的。
>

### ** 常用交易主邏輯 ** ###
>OBV 線圖通常會與價格圖形搭配使用，以利判斷市場行情走勢是否成立。  
>
>**1. 當 OBV 線穩定上升，且股價也同步上漲，表示行情有向上趨勢，可以考慮買進。**
>
>**2. 當 OBV 線穩定下降，且股價也同步下跌，表示行情有向下跌勢，可以考慮賣出。**
>
>**3. 當 OBV 線上升而股價卻反向下跌時，表示雖然股價表現不佳，但市場承接力道意願仍強，可以考慮買進。**
>
>**4. 當 OBV 線下降而股價卻反向上漲時，表示市場的買盤意願不強，股價可能隨時下跌，可以考慮賣出。**
>
>**5. 當 OBV 線急速上升，代表行情上大部分的短期買方能量已經出盡全力，買盤力道可能已達到頂，不太可能持續太久，可以考慮賣出。**
>
>**6. 當 OBV 線急速下跌，代表市場上出現大量賣壓，可以等待 OBV 線止跌回穩後，考慮買進。**
>
>**7. OBV 線長期累積後的大波段的高點（ 低點 ），常成為行情的大阻力區，股價在這附近會有強較強上升壓力（ 下跌支撐 ）。而當股價突破阻力區後，後續漲勢將更加強勁 （ 跌勢更劇烈 ）。**  
>

## ** 使用 Crypto Arsenal 平台實做交易回測 **
>**交易標的：**  
>ETH / USDT
>
>**使用Ｋ棒：**  
>6 小時Ｋ
>
>**交易時長：**  
>2 個月（ 2020–10–01 00:00 至 2020–11–30 00:00 ）
>
>**買入條件：**  
>參考 4 個 K 棒，若 4 個 K 棒的 OBV 值以第 4 日 > 第 2 日 > 第 3 日和第 1 日，形成 OBV 波浪向上突破的型態，則買入 20%。
>
>**賣出條件：**  
>與買入條件相反，若 4 個 K 棒的 OBV 值以第 4 日 < 第 2 日 < 第 3 日和第 1 日，形成 OBV 波浪向下突破的型態，則賣出所有倉位。
>
**回測結果：<font size="5">＋12.57%</font>**
<img alt="" class="ni pm ef es eo ex w c" role="presentation" src="https://miro.medium.com/max/1400/0*Mkufehq4mI3JtTmN" srcset="https://miro.medium.com/max/552/0*Mkufehq4mI3JtTmN 276w, https://miro.medium.com/max/1104/0*Mkufehq4mI3JtTmN 552w, https://miro.medium.com/max/1280/0*Mkufehq4mI3JtTmN 640w, https://miro.medium.com/max/1400/0*Mkufehq4mI3JtTmN 700w" sizes="700px"/>
<font size="1"><center>買賣點位說明</center></font>

### **Step 1 : 選擇策略**
先登入 Crypto Arsenal 交易平台，至左手邊選單選擇我的策略（ My Strategy ），進入後點找到右上角的新增策略（ New Strategy ），最後在選單中選擇 OBV，並按下建立。
<img alt="" class="ni pm ef es eo ex w c"  role="presentation" src="https://miro.medium.com/max/1400/0*_HBmi_j0WtOAsPLQ" srcset="https://miro.medium.com/max/552/0*_HBmi_j0WtOAsPLQ 276w, https://miro.medium.com/max/1104/0*_HBmi_j0WtOAsPLQ 552w, https://miro.medium.com/max/1280/0*_HBmi_j0WtOAsPLQ 640w, https://miro.medium.com/max/1400/0*_HBmi_j0WtOAsPLQ 700w" sizes="700px"/>
<font size="1"><center>Step 1 : 選擇策略</center></font>

### **Step 2 : 選擇多空交易對**
分別輸入各個欄位，我們只以交易現貨且只做多為例子，所以 Type 欄位選擇「 SPOT 」，Trend 欄選擇「 Long 」。輸入完後點選 Save 儲存，此時畫面不會跳轉，直接選擇 EDITOR 進入回測畫面。
<img alt="" class="ni pm ef es eo ex w c" role="presentation" src="https://miro.medium.com/max/1400/0*ETb_0LLfiQ-MQz89" srcset="https://miro.medium.com/max/552/0*ETb_0LLfiQ-MQz89 276w, https://miro.medium.com/max/1104/0*ETb_0LLfiQ-MQz89 552w, https://miro.medium.com/max/1280/0*ETb_0LLfiQ-MQz89 640w, https://miro.medium.com/max/1400/0*ETb_0LLfiQ-MQz89 700w" sizes="700px"/>
<font size="1"><center>Step 2 : 選擇多空交易對</center></font>

### **Step 3：調整回測時段**
先在 Backtesting Interval 選擇回測時間，右邊可以迅速選擇平台已經設定好的回測期間，1Y 代表「 最近1年 」，也可以點選月曆的小圖示選取自己喜歡的開始和結束時間，這裡使用 2020/10/01 至 2020/11/30 為例。其他數值例如 Spread（ 買賣價差 ）、Fee（ 交易手續費 ）等都可以依喜好修改，這裡我們直接使用平台默認值。
<img alt="" class="ni pm ef es eo ex w c"  role="presentation" src="https://miro.medium.com/max/1400/0*ayd541nKS0Fy_Ven" srcset="https://miro.medium.com/max/552/0*ayd541nKS0Fy_Ven 276w, https://miro.medium.com/max/1104/0*ayd541nKS0Fy_Ven 552w, https://miro.medium.com/max/1280/0*ayd541nKS0Fy_Ven 640w, https://miro.medium.com/max/1400/0*ayd541nKS0Fy_Ven 700w" sizes="700px"/>
<font size="1"><center>Step 3：調整回測時段</center></font>

### **Step 4：修改程式碼**
接下來看程式碼，先不要離開～回測模板 Crypto Arsenal 已經全部寫好囉，只要設定我們自己想要調整的參數就可以了，這邊也會對所有用得到的參數一一做說明。
>#### **使用到的參數說明：** 
>**第 9 行 self.period：**<p>設定 K 線區間，單位為秒，若為 60 * 60 代表小時Ｋ，這次使用 6 小時Ｋ。</p>
>
>**第 14 行 self.proportion：**  
>每次買入條件被觸發後，想投入多少比例的總資產，這裏使用 0.2，也就是單次買入 20 %，最多買至 100 %。
>

以上就是我們在 OBV 策略模板上可以調整的參數，可以自己輸入其他數值玩玩看哦！最後按下右上角藍色的 Run and Debug 按鈕開始回測！
<img alt="" class="ni pm ef es eo ex w c"  role="presentation" src="https://miro.medium.com/max/1400/0*kUpLGiXaNsxlxN6S" srcset="https://miro.medium.com/max/552/0*kUpLGiXaNsxlxN6S 276w, https://miro.medium.com/max/1104/0*kUpLGiXaNsxlxN6S 552w, https://miro.medium.com/max/1280/0*kUpLGiXaNsxlxN6S 640w, https://miro.medium.com/max/1400/0*kUpLGiXaNsxlxN6S 700w" sizes="700px"/>
<font size="1"><center>Step 4：修改程式碼</center></font>

稍等一下就可以看到這 2個月的資產變化情形和最大回撤狀況！
<img alt="" class="ni pm ef es eo ex w c"  role="presentation" src="https://miro.medium.com/max/1400/0*QXtXRjmbjZu5m8eR" srcset="https://miro.medium.com/max/552/0*QXtXRjmbjZu5m8eR 276w, https://miro.medium.com/max/1104/0*QXtXRjmbjZu5m8eR 552w, https://miro.medium.com/max/1280/0*QXtXRjmbjZu5m8eR 640w, https://miro.medium.com/max/1400/0*QXtXRjmbjZu5m8eR 700w" sizes="700px"/>
<font size="1"><center>資產曲線</center></font>

看到資產曲線代表程式執行上沒問題，那如果對交易點位有疑問的話，可以在右下方的 Log 欄位找到所有買賣的進出場點，藉此與程式做比對。
以下為此交易策略的 Performance Metrics 基本績效表現：
<img alt="" class="ni pm ef es eo ex w c"  role="presentation" src="https://miro.medium.com/max/1400/0*VGC8sFoy4FQDxDuL" srcset="https://miro.medium.com/max/552/0*VGC8sFoy4FQDxDuL 276w, https://miro.medium.com/max/1104/0*VGC8sFoy4FQDxDuL 552w, https://miro.medium.com/max/1280/0*VGC8sFoy4FQDxDuL 640w, https://miro.medium.com/max/1400/0*VGC8sFoy4FQDxDuL 700w" sizes="700px"/>
<font size="1"><center>Performance Metrics</center></font>

回測過去兩個月就有 12.57% 獲利（ ROI ），一直想要量化交易卻遲遲不知道如何下手嗎，只要利用此平台選擇自己想要交易策略，就能輕鬆實現囉!

**<font size="3" color="#FF0000"><center>提醒讀者，任何投資都有風險，回測績效都有經過篩選，請謹慎評估後再使用。</center></font>**
**<font size="3" color="#FF0000"><center>提醒讀者，任何投資都有風險，回測績效都有經過篩選，請謹慎評估後再使用。</center></font>**
**<font size="3" color="#FF0000"><center>提醒讀者，任何投資都有風險，回測績效都有經過篩選，請謹慎評估後再使用。</center></font>**
  
OBV 策略在 Crypto Arsenal 平台屬於 Starter 等級或以上的會員專屬策略，此外也有提供一般使用者許多免費策略模板和建立個人策略的功能，平台也支持跟單服務，趕快來註冊使用吧！
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






