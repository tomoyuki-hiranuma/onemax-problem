# NK-model-GA
NKランドスケープをGAで最適解を求めるプログラム
## メイン
GA.py
### 評価関数
NK ランドスケープ
### 交叉方法
1点交叉
### 世代交代方法
集団から２個体親を選択  
交叉をし、子供2体親2体の合計４個体内で1体エリート、１体は残りでランダムに選択。  
洗濯した親と交換  
### 突然変異率
1%  