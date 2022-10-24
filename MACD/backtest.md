
MACD 指數平滑移動平均線（ 回測 ）
===========================

_經過之前**<a href="https://medium.com/@mkrt.crypto.arsenal/macd%E5%9B%9E%E6%B8%AC-%E6%89%8B%E6%8A%8A%E6%89%8B%E6%95%99%E5%AD%B8-e5533f62323f">MACD指數平滑移動平均線</a>**的詳細介紹，相信已經對 MACD 指標有徹底的瞭解了，這篇將實際使用 Crypto Arsenal 量化交易平台裡的免費 MACD 指標模板做回測，這篇將教學如何簡單地修改模板程式，更客製化自己的想法和策略。_


## ** 使用 Crypto Arsenal 平台實做交易回測 **
>**交易標的：**  
>ETH / USDT
>
>**使用Ｋ棒：**  
>4 小時Ｋ
>
>**交易時長：**
>6 個月（ 2021–06–23 00:00 至 2021–12–23 00:00 ）
>
>**買入條件：**
>Histogram 底部轉折處且 Histogram < 0，all in all out。
>
>**賣出條件：**
>Histogram 頂部轉折處且 Histogram > 0，all in all out。
>
**回測結果：<font size="5">＋82.9%</font>**

### **Step 1 : 選擇策略**
先登入Crypto Arsenal 交易平台，至左手邊選單選擇我的策略（ My Strategy ），進入後點找到右上角的新增策略（ New Strategy ），最後在選單中選擇 MACD，並按下建立。
<img alt="" class="oh qo ef es eo ex w c" role="presentation" src="https://miro.medium.com/max/1400/0*F5OYYKzkGv_XCuJu" srcset="https://miro.medium.com/max/552/0*F5OYYKzkGv_XCuJu 276w, https://miro.medium.com/max/1104/0*F5OYYKzkGv_XCuJu 552w, https://miro.medium.com/max/1280/0*F5OYYKzkGv_XCuJu 640w, https://miro.medium.com/max/1400/0*F5OYYKzkGv_XCuJu 700w" sizes="700px"/>
<font size="1"><center>Step 1 : 選擇策略</center></font>

### **Step 2 : 選擇多空交易對**
分別輸入各個欄位，我們只以交易現貨只做多為例子，所以 Type 欄選擇「 SPOT 」，Trend 欄選擇「 Long 」。輸入完後點選 Save 儲存，此時畫面不會跳轉，直接選擇 EDITOR 進入回測畫面。
<img alt="" class="oh qo ef es eo ex w c" role="presentation" src="https://miro.medium.com/max/1400/0*Wzba8D3f8UzN0Y2o" srcset="https://miro.medium.com/max/552/0*Wzba8D3f8UzN0Y2o 276w, https://miro.medium.com/max/1104/0*Wzba8D3f8UzN0Y2o 552w, https://miro.medium.com/max/1280/0*Wzba8D3f8UzN0Y2o 640w, https://miro.medium.com/max/1400/0*Wzba8D3f8UzN0Y2o 700w" sizes="700px"/>
<font size="1"><center>Step 2 : 選擇多空交易對</center></font>

### **Step 3：調整回測時段**
先在 Backtesting Interval 選擇回測時間，這裡使用 6 個月，可以點擊月曆的小圖標選取自己喜歡的開始和結束時間或是直接點旁邊的 6M，代表選擇「 最近的 6 個月 」執行回測。其他數值例如 Fee 選項的交易手續費可以依喜好修改，這裡我們直接使用平台默認值。
<img alt="" class="oh qo ef es eo ex w c"  role="presentation" src="https://miro.medium.com/max/1400/0*StHC7jR5dvr6kIc0" srcset="https://miro.medium.com/max/552/0*StHC7jR5dvr6kIc0 276w, https://miro.medium.com/max/1104/0*StHC7jR5dvr6kIc0 552w, https://miro.medium.com/max/1280/0*StHC7jR5dvr6kIc0 640w, https://miro.medium.com/max/1400/0*StHC7jR5dvr6kIc0 700w" sizes="700px"/>
<font size="1"><center>Step 3：調整回測時段</center></font>

### **Step 4：修改程式碼**
接下來看到程式碼，等等，先不要離開～相信小編，真的超級簡單！
回測模板 Crypto Arsenal 已經全部寫好囉，可以只設定我們想要調整的參數就好，這邊也會對所有常用的參數做一一說明。
>#### **使用到的參數說明：**
>**第 9 行 self.period：**<p>設定 K 線區間，單位為秒，可以看到預設為 30 ** 60 代表 30 分Ｋ，這次使用 4 * 60 * 60 的 4 小時Ｋ。</p>
>
>**第 13 行 self.fast_period : **  
>MACD 快線的 EMA 參數。
>
>**第 14 行 self.slow_period : **  
>MACD 慢線的 EMA 參數。
>
>**第 13 行 self.signal_period : **  
>Signal 線的 EMA 參數。
<center><img alt="" class="oh qo ef es eo ex w c" role="presentation" src="https://miro.medium.com/max/1200/0*w1aGaMFUbpPAUb-U" srcset="https://miro.medium.com/max/552/0*w1aGaMFUbpPAUb-U 276w, https://miro.medium.com/max/1104/0*w1aGaMFUbpPAUb-U 552w, https://miro.medium.com/max/1200/0*w1aGaMFUbpPAUb-U 600w" sizes="600px"/></center>
>
>**第 22 行 self.proportion：**  
>每次買入條件被觸發後，想投入多少比例的總資產，這裏使用 0.95 ，也就是 All in all out。

<img alt="" class="oh qo ef es eo ex w c"  role="presentation" src="https://miro.medium.com/max/1400/0*OTZmM-7huZR8k542" srcset="https://miro.medium.com/max/552/0*OTZmM-7huZR8k542 276w, https://miro.medium.com/max/1104/0*OTZmM-7huZR8k542 552w, https://miro.medium.com/max/1280/0*OTZmM-7huZR8k542 640w, https://miro.medium.com/max/1400/0*OTZmM-7huZR8k542 700w" sizes="700px"/>
<font size="1"><center>Step 4：修改程式碼</center></font>  

以上就是我們在 MACD 策略回測上常會使用到的參數，是不是很簡單呢？可以自己輸入其他數值玩玩看哦！

### **修改模板代碼，個人化自己的策略**
在 50 多行的地方，可以看到有進場條件的判斷。  
**原模板的買賣條件是：**
>Histogram 由負轉正，則買入。
>
>Histogram 由正轉負，則賣出。
>

**我們將邏輯改為：**
>Histogram 在負的時候，Histogram 轉折，則買入。  
>
>Histogram 在正的時候，Histogram 轉折，則賣出。  
>

使用前一篇 MACD 指標介紹的圖做新策略買賣點位的說明。
<img alt="" class="oh qo ef es eo ex w c"  role="presentation" src="https://miro.medium.com/max/1400/0*YTCzE2sYlWaSze14" srcset="https://miro.medium.com/max/552/0*YTCzE2sYlWaSze14 276w, https://miro.medium.com/max/1104/0*YTCzE2sYlWaSze14 552w, https://miro.medium.com/max/1280/0*YTCzE2sYlWaSze14 640w, https://miro.medium.com/max/1400/0*YTCzE2sYlWaSze14 700w" sizes="700px"/>
<font size="1"><center>新策略買賣點位說明</center></font>

對比程式碼，紅色框是我們新增的，藍色框是原模板條件，可以刪除或用＃字號註解掉。
<img alt="" class="oh qo ef es eo ex w c"  role="presentation" src="https://miro.medium.com/max/1400/0*IK_rN3FHQf2eZzMV" srcset="https://miro.medium.com/max/552/0*IK_rN3FHQf2eZzMV 276w, https://miro.medium.com/max/1104/0*IK_rN3FHQf2eZzMV 552w, https://miro.medium.com/max/1280/0*IK_rN3FHQf2eZzMV 640w, https://miro.medium.com/max/1400/0*IK_rN3FHQf2eZzMV 700w" sizes="700px"/>
<font size="1"><center>新策略買賣程式修改</center></font>
修改完成後按下藍色的 Run and Debug 按鈕開始回測！
稍等一下就可以看到這 6 個月的資產變化情形和最大回撤狀況！
<img alt="" class="oh qo ef es eo ex w c"  role="presentation" src="https://miro.medium.com/max/1400/0*ouC1rw3rEyxQx-XH" srcset="https://miro.medium.com/max/552/0*ouC1rw3rEyxQx-XH 276w, https://miro.medium.com/max/1104/0*ouC1rw3rEyxQx-XH 552w, https://miro.medium.com/max/1280/0*ouC1rw3rEyxQx-XH 640w, https://miro.medium.com/max/1400/0*ouC1rw3rEyxQx-XH 700w" sizes="700px"/>
<font size="1"><center>資產曲線</center></font>

回測過去 6 個月就有 82.9% 獲利，資產有持續再創高，回撤可能有些劇烈，大跌段沒有避掉，但總體來說還是個不錯的的量化策略，歡迎高手再自行加入濾網強化！  
看到資產曲線代表程式執行上沒問題，那如果對交易點位有疑問的話，可以在右下方的 Log 欄位找到所有買賣的進出場點，藉此與程式做比對去做修正。最後附上策略表現評估表。
<img alt="" class="oh qo ef es eo ex w c" role="presentation" src="https://miro.medium.com/max/1400/0*ldHNHN57hpaFeyh3" srcset="https://miro.medium.com/max/552/0*ldHNHN57hpaFeyh3 276w, https://miro.medium.com/max/1104/0*ldHNHN57hpaFeyh3 552w, https://miro.medium.com/max/1280/0*ldHNHN57hpaFeyh3 640w, https://miro.medium.com/max/1400/0*ldHNHN57hpaFeyh3 700w" sizes="700px"/>
<font size="1"><center>Performance Metrics</center></font>

以上就是平台內 MACD 策略模板的使用教學，程式的參數設定也出乎意料的簡單呢！有任何策略使用上的問題都可以加入 Telegram 群組，內有開發者為您解答。

**<font size="3" color="#FF0000"><center>提醒讀者，任何投資都有風險，回測績效都有經過篩選，請謹慎評估後再使用。</center></font>**
**<font size="3" color="#FF0000"><center>提醒讀者，任何投資都有風險，回測績效都有經過篩選，請謹慎評估後再使用。</center></font>**
**<font size="3" color="#FF0000"><center>提醒讀者，任何投資都有風險，回測績效都有經過篩選，請謹慎評估後再使用。</center></font>**

MACD 策略在 Crypto Arsenal 平台屬於 **Free** 等級策略，此外還提供一般使用者免費建立自己的策略還有支持跟單功能，趕快來註冊使用吧！
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








