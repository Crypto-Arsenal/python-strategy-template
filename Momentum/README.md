Mom 動量指標
===========================

## **什麼是 MOM？**
Momentum（ 簡稱 MOM 或 MTM ）動量指標，由 H. M. Gartley 在 1935 年著作《 Porfits in the Stock Market 》首次提出，運算上十分簡單，由今日收盤價扣除 n 日前的收盤價即可得出當日的 MOM，主要用來判斷股價是否具有動能，若具有上漲的動能，MOM 勢必要比 n 日前來得高，也就是 MOM 會大於零。
## **MOM 計算方法**
MOM 的計算方法是所有指標中數一數二容易的，輕輕鬆鬆就能上手！
### **公式：**
>**今日的 MOM = 今日的 Close（ 收盤價 ）- n 日前的 Close  **

假設今日的收盤價為 4000 點，10 日前的收盤價為 3900，那麼今天的 MOM（ 10 ）就是等於 100。  
## **常用交易主邏輯**
>連續 5 日 MOM > 0，則買入。  
>連續 5 日 MOM < 0，則賣出。  

## **使用 Crypto-Arsenal 平台實做交易回測**
>**交易標的：**  
>ETH / USDT  
>
>**使用Ｋ棒：**  
>4 小時Ｋ  
>
>**交易時長：**  
>3 個月（ 2021–09–08 00:00 至 2021–12–08 00:00 ）  
>
>**買入條件：**  
>連續 5 日的 MOM（ 10 ）都大於零，每次觸發只買入總資產 20%，也就是如果 MOM 連續 9 日 > 0，將於第 6 , 7 , 8 , 9 , 10 根Ｋ線開盤價分別買入 20%。  
>
>**賣出條件：**  
>連續 5 日的 MOM（ 10 ）都小於零，每次觸發賣出所有倉位。  
>
**回測結果：<font size="5">＋27.23%</font>**

### **Step 1 : 選擇策略**
先登入 Crypto-Arsenal 交易平台，至左手邊選單選擇我的策略（ My Strategy ），進入後點找到右上角的新增策略（ New Strategy ），最後在選單中選擇 Momentum，並按下建立。
<img alt="" class="oe qu ef es eo ex w c"  role="presentation" src="https://miro.medium.com/max/1400/0*1VFTrqoBwhue1jo2" srcset="https://miro.medium.com/max/552/0*1VFTrqoBwhue1jo2 276w, https://miro.medium.com/max/1104/0*1VFTrqoBwhue1jo2 552w, https://miro.medium.com/max/1280/0*1VFTrqoBwhue1jo2 640w, https://miro.medium.com/max/1400/0*1VFTrqoBwhue1jo2 700w" sizes="700px"/>
<font size="1"><center>Step 1 : 選擇策略</center></font>

### **Step 2 : 選擇多空交易對**
分別輸入各個欄位，我們只以交易現貨只做多為例子，所以 Type 欄選擇 「 SPOT 」，Trend 欄選擇 「 Long 」。輸入完後點選 Save 儲存，此時畫面不會跳轉，直接選擇 EDITOR 進入回測畫面。
<img alt="" class="oe qu ef es eo ex w c" role="presentation" src="https://miro.medium.com/max/1400/0*YS3hg0fTQEUklkHS" srcset="https://miro.medium.com/max/552/0*YS3hg0fTQEUklkHS 276w, https://miro.medium.com/max/1104/0*YS3hg0fTQEUklkHS 552w, https://miro.medium.com/max/1280/0*YS3hg0fTQEUklkHS 640w, https://miro.medium.com/max/1400/0*YS3hg0fTQEUklkHS 700w" sizes="700px"/>
<font size="1"><center>Step 2 : 選擇多空交易對</center></font>

### **Step 3：調整回測時段**
先在 Backtesting Interval 選擇回測時間，這裡使用 3 個月，可以點擊月曆的小圖標選取自己喜歡的開始和結束時間或是直接點旁邊的 3M，代表選擇「 最近的 3 個月 」執行回測。其他數值例如 Fee 選項的交易手續費可以依喜好修改，這裡我們直接使用平台默認值。
<img alt="" class="oe qu ef es eo ex w c" role="presentation" src="https://miro.medium.com/max/1400/1*KcImapkAp5aG9SbmTUfSxA.png" srcset="https://miro.medium.com/max/552/1*KcImapkAp5aG9SbmTUfSxA.png 276w, https://miro.medium.com/max/1104/1*KcImapkAp5aG9SbmTUfSxA.png 552w, https://miro.medium.com/max/1280/1*KcImapkAp5aG9SbmTUfSxA.png 640w, https://miro.medium.com/max/1400/1*KcImapkAp5aG9SbmTUfSxA.png 700w" sizes="700px"/>
<font size="1"><center>Step 3：調整回測時段</center></font>

### **Step 4：修改程式碼**
接下來看到程式碼，先不要離開 ! 回測模板 Crypto-Arsenal 已經全部寫好囉，只要設定我們自己想要調整的參數就可以了，這邊也會對所有用得到的參數做一一說明。
>#### **使用到的參數說明:**
>**第 9 行 self.period：**<p>設定 K 線區間，單位為秒，若為 60 * 60 代表小時Ｋ，這次使用 4 小時Ｋ。  </p>
>
>**第 13 行 self.proportion：**  
>每次買入條件被觸發後，想投入多少比例的總資產，這裏使用 0.2 ，也就是單次買入總資產的 20 %，最多買至 100 %。  
>
>**第 15 行 self.mom_period：**  
>也就是我們上面介紹提到 MOM 的 n ，看使用者希望與多少根Ｋ棒之前的收盤價做比較，這次設定為 n = 10。  

以上就是我們在 MOM 策略回測上常會使用到的參數，是不是很簡單呢？可以自己輸入其他數值玩玩看哦！最後按下藍色的 Run and Debug 按鈕後即可開始回測！
<img alt="" class="oe qu ef es eo ex w c" role="presentation" src="https://miro.medium.com/max/1400/1*Egc3PWi99IaCfMpBpxMhtw.png" srcset="https://miro.medium.com/max/552/1*Egc3PWi99IaCfMpBpxMhtw.png 276w, https://miro.medium.com/max/1104/1*Egc3PWi99IaCfMpBpxMhtw.png 552w, https://miro.medium.com/max/1280/1*Egc3PWi99IaCfMpBpxMhtw.png 640w, https://miro.medium.com/max/1400/1*Egc3PWi99IaCfMpBpxMhtw.png 700w" sizes="700px"/>
<font size="1"><center>Step 4：修改程式碼</center></font>

稍等一下就可以看到這 3 個月的資產變化情形和最大回測狀況。
<img alt="" class="oe qu ef es eo ex w c"  role="presentation" src="https://miro.medium.com/max/1400/0*phNO67M5b3MN5p5z" srcset="https://miro.medium.com/max/552/0*phNO67M5b3MN5p5z 276w, https://miro.medium.com/max/1104/0*phNO67M5b3MN5p5z 552w, https://miro.medium.com/max/1280/0*phNO67M5b3MN5p5z 640w, https://miro.medium.com/max/1400/0*phNO67M5b3MN5p5z 700w" sizes="700px"/>
<font size="1"><center>回測畫面</center></font>

看到資產曲線代表程式執行上沒問題，那如果對交易點位有疑問的話，可以在右下方的 Logs欄位找到所有買賣的進出場點，藉此與程式做比對。
<img alt="" class="oe qu ef es eo ex w c" role="presentation" src="https://miro.medium.com/max/1400/0*C6pPML21n8YwpwHT" srcset="https://miro.medium.com/max/552/0*C6pPML21n8YwpwHT 276w, https://miro.medium.com/max/1104/0*C6pPML21n8YwpwHT 552w, https://miro.medium.com/max/1280/0*C6pPML21n8YwpwHT 640w, https://miro.medium.com/max/1400/0*C6pPML21n8YwpwHT 700w" sizes="700px"/>
<font size="1"><center>logs欄</center></font>

回測過去兩個月就有 27% 獲利，量化交易的快樂就是這樣樸實無華。  
  
**<font size="3" color="#FF0000"><center>提醒讀者，任何投資都有風險，回測績效都有經過篩選，請謹慎評估後再使用。</center></font>**
**<font size="3" color="#FF0000"><center>提醒讀者，任何投資都有風險，回測績效都有經過篩選，請謹慎評估後再使用。</center></font>**
**<font size="3" color="#FF0000"><center>提醒讀者，任何投資都有風險，回測績效都有經過篩選，請謹慎評估後再使用。</center></font>**
   
目前 Momentum 策略在 Crypto-Arsenal 平台可以免費使用，不要再和輕鬆躺賺的機會擦身而過了，快來 Crypto-Arsenal 註冊使用吧！  
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





