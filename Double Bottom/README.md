 Double Bottom 雙底
===========================

_量化交易雖然是一個省心省力省時間還護眼睛的交易方法，但也是需要在判斷趨勢的基礎上去做交易策略的選用才能發揮出最大的效益！在大盤震盪的時候不想看盤就一起來看看技術指標吧 ：）_
## **什麼是 Double Bottom ?**
雙底是技術分析上非常實用的分析方法，因為價格形狀與英文字母 W 相似，故俗稱 Ｗ 底。底部是由兩次下跌後的反彈所形成，兩底部是強力的價格支撐位。
在技術分析上雙底是空頭轉多頭的底部型態，若後低略高於前低形成 Higher Low，且價格帶量突破頸線被視為空頭減弱多頭強勢的信號，但因為通常價格突破頸線時已經從第二次底部上漲一段時間，所以如果在突破後入場，在遇到假突破時常會被套在高點，更穩健的方法可以等待突破後的回檔，踩穩頸線時入場。  
另外與 W 相反的線型是 M 頂，在技術分析上屬於多頭觸頂的轉空訊號！
<img alt="" class="oe ql ef es eo ex w c" role="presentation" src="https://miro.medium.com/max/1400/0*WPAvcGsGCRQKQXBc" srcset="https://miro.medium.com/max/552/0*WPAvcGsGCRQKQXBc 276w, https://miro.medium.com/max/1104/0*WPAvcGsGCRQKQXBc 552w, https://miro.medium.com/max/1280/0*WPAvcGsGCRQKQXBc 640w, https://miro.medium.com/max/1400/0*WPAvcGsGCRQKQXBc 700w" sizes="700px"/>
<font size="1"><center>圖形解釋</center></font>

## **常用交易主邏輯**
>若價格向上突破頸線，則買入。  
>若價格向下跌破頸線，則賣出。

## **使用 Crypto Arsenal 平台實做交易回測**
>交易標的：ETH / USDT
>
>使用Ｋ棒：1 小時Ｋ
>
>交易時長：6 個月（ 2021–06–15 00:00 至 2021–12–15 00:00 ）
>
>買入條件：收盤價突破 W 型態頸線，則買入，單次為總資產 30%。
>
>賣出條件：收盤價跌破頸線則賣出。
>
**回測結果：<font size="5">＋41.41%</font>**

### **Step 1 : 選擇策略**
先登入Crypto Arsenal 交易平台，至左手邊選單選擇我的策略（ My Strategy ），進入後點找到右上角的新增策略（ New Strategy ），最後在選單中選擇 Double Bottom，並按下建立。
<img alt="" class="oe ql ef es eo ex w c" role="presentation" src="https://miro.medium.com/max/1400/0*prN-tdW-5V5rNziO" srcset="https://miro.medium.com/max/552/0*prN-tdW-5V5rNziO 276w, https://miro.medium.com/max/1104/0*prN-tdW-5V5rNziO 552w, https://miro.medium.com/max/1280/0*prN-tdW-5V5rNziO 640w, https://miro.medium.com/max/1400/0*prN-tdW-5V5rNziO 700w" sizes="700px"/>
<font size="1"><center>Step 1 : 選擇策略</center></font>

### **Step 2 : 選擇多空交易對**
分別輸入各個欄位，我們以交易現貨只做多為例子，所以 Type 欄選擇 「 SPOT 」，Trend 欄選擇「 Long 」。輸入完後點選 Save 儲存，此時畫面不會跳轉，直接選擇 EDITOR 進入回測畫面。
<img alt="" class="oe ql ef es eo ex w c" role="presentation" src="https://miro.medium.com/max/1400/0*iBOP6Zo5Njkh6xhX" srcset="https://miro.medium.com/max/552/0*iBOP6Zo5Njkh6xhX 276w, https://miro.medium.com/max/1104/0*iBOP6Zo5Njkh6xhX 552w, https://miro.medium.com/max/1280/0*iBOP6Zo5Njkh6xhX 640w, https://miro.medium.com/max/1400/0*iBOP6Zo5Njkh6xhX 700w" sizes="700px"/>
<font size="1"><center>Step 2 : 選擇多空交易對</center></font>

### **Step 3：調整回測時段**
先在 Backtesting Interval 選擇回測時間，這裡使用 6 個月，可以點擊月曆的小圖標選取自己喜歡的開始和結束時間或是直接點旁邊的 6M，代表選擇「 最近的 6 個月 」執行回測。其他數值例如 Fee 選項的交易手續費可以依喜好修改，這裡我們直接使用平台默認值。
<img alt="" class="oe ql ef es eo ex w c" role="presentation" src="https://miro.medium.com/max/1400/0*0QZ0COALmAKHr5J6" srcset="https://miro.medium.com/max/552/0*0QZ0COALmAKHr5J6 276w, https://miro.medium.com/max/1104/0*0QZ0COALmAKHr5J6 552w, https://miro.medium.com/max/1280/0*0QZ0COALmAKHr5J6 640w, https://miro.medium.com/max/1400/0*0QZ0COALmAKHr5J6 700w" sizes="700px"/>
<font size="1"><center>Step 3：調整回測時段</center></font>

### **Step 4：修改程式碼**
接下來看到程式碼，先不要離開！回測模板 Crypto Arsenal 已經全部寫好囉，只要設定我們自己想要調整的參數就可以了，這邊也會對所有常用的參數做一一說明。  
>#### **使用到的參數說明：** 
>**第 10 行 self.period：**<p>設定 K 線區間，單位為秒，可以看到預設為 30 * 60 代表 30 分Ｋ，這次使用 60 * 60 的 1 小時Ｋ。</p>
>
>**第 14 行 self.range_val :**  
>利用中心點前後多少根 K 棒來決定價格轉折點，例如 21 代表如果前後各 10 根 K 棒都沒有比中間第 11 根低或高，那中間點就是最低點或最高點的轉折處，用來找出 W 的雙底和頸線。
>
>**第 22 行 self.proportion：**  
>每次買入條件被觸發後，想投入多少比例的總資產，這裏使用 0.3 ，也就是單次買入 30 %，最多買至原來總資產的 90 %。  

以上就是我們在 Double Bottom 策略回測上常會使用到的參數，主要也就 3 個，是不是很簡單呢？可以自己輸入其他數值玩玩看哦！最後按下藍色的 Run and Debug 按鈕開始回測！
<img alt="" class="oe ql ef es eo ex w c" role="presentation" src="https://miro.medium.com/max/1400/0*A4syesw-wA_nOLUk" srcset="https://miro.medium.com/max/552/0*A4syesw-wA_nOLUk 276w, https://miro.medium.com/max/1104/0*A4syesw-wA_nOLUk 552w, https://miro.medium.com/max/1280/0*A4syesw-wA_nOLUk 640w, https://miro.medium.com/max/1400/0*A4syesw-wA_nOLUk 700w" sizes="700px"/>
<font size="1"><center>Step 4：修改程式碼</center></font>

稍等一下就可以看到這 6 個月的資產變化情形和最大回撤狀況！
<img alt="" class="oe ql ef es eo ex w c" role="presentation" src="https://miro.medium.com/max/1400/0*JnDPGUxG7qAs8cvp" srcset="https://miro.medium.com/max/552/0*JnDPGUxG7qAs8cvp 276w, https://miro.medium.com/max/1104/0*JnDPGUxG7qAs8cvp 552w, https://miro.medium.com/max/1280/0*JnDPGUxG7qAs8cvp 640w, https://miro.medium.com/max/1400/0*JnDPGUxG7qAs8cvp 700w" sizes="700px"/>
<font size="1"><center>回測 6 個月資產曲線</center></font>

回測過去 6 個月就有 41% 獲利，不但完全躲掉了 9 月的大跌，總體的資產曲線也走得很漂亮呢～資產有持續再創高，回撤也都在可控範圍內，是個非常棒的量化策略！
看到資產曲線代表程式執行上沒問題，那如果對交易點位有疑問的話，可以在右下方的 Log 欄位找到所有買賣的進出場點，藉此與程式做比對去做修正。
<img alt="" class="oe ql ef es eo ex w c" role="presentation" src="https://miro.medium.com/max/1400/0*S4N50lLgMBlfywt7" srcset="https://miro.medium.com/max/552/0*S4N50lLgMBlfywt7 276w, https://miro.medium.com/max/1104/0*S4N50lLgMBlfywt7 552w, https://miro.medium.com/max/1280/0*S4N50lLgMBlfywt7 640w, https://miro.medium.com/max/1400/0*S4N50lLgMBlfywt7 700w" sizes="700px"/>

以上就是平台內 Double Bottom 策略模板的簡易使用教學，程式的參數設定也出乎意料的簡單呢！有任何策略使用上的問題都可以加入 Telegram 群組，內有開發者為您解答。  
  
**<font size="3" color="#FF0000"><center>提醒讀者，任何投資都有風險，回測績效都有經過篩選，請謹慎評估後再使用。</center></font>**
**<font size="3" color="#FF0000"><center>提醒讀者，任何投資都有風險，回測績效都有經過篩選，請謹慎評估後再使用。</center></font>**
**<font size="3" color="#FF0000"><center>提醒讀者，任何投資都有風險，回測績效都有經過篩選，請謹慎評估後再使用。</center></font>**
  
Double Bottom 策略在Crypto Arsenal 平台屬於 Elite 等級或以上的會員專屬策略，另外也提供一般使用者免費建立自己的策略還有支持跟單功能，趕快來註冊使用吧！
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




