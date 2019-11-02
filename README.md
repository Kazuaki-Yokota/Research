# Nav_System

スケジュール作成プログラム
python Prototype4.py

関連プログラム
	Recipe_Mode.py
		テストで使用するタスク内容を細分化した状態遷移と作業内容を記述。
		今後は別の方法でデータを記述する必要がある
	State_Flow.py
		Recipe_Mode.pyからのモデル情報を基にフローグラフを作成。フローグラフに各種属性を付加する。
		フローグラフの初期化から可視化、状態Sでの次の状態S+1の算出を行う関数を持つ

ナビゲーションプログラム
プログラムは大きく二つに分かれる。起動順番は以下の通り
1．python Connect.py
2. python Main.py

Connect.py
TCP通信を行うための関数を持つ。テスト段階ではセンシングデータをナビゲーションに飛ばす役目を担っている。

Main.py
ナビゲーションプログラムを動かすための統合プログラム。機能ごとにスレッド動作している。
機能としては、以下の通り
１．ナビゲーションGUIを動かす
２．フローグラフを基に作業記録と作業内容をやり取りする
３．センシングデータをやり取りする
４．フローグラフから受け取ったデータをナビゲーションに渡す

関連プログラム
	Nav_GUI.py
		ナビゲーション本体。（未完成）
	State_Flow.py
		Recipe_Mode.pyからのモデル情報を基にフローグラフを作成。フローグラフに各種属性を付加する。
		フローグラフの初期化から可視化、状態Sでの次の状態S+1の算出を行う関数を持つ。
	Connect.py
		TCP通信を行うための関数を持つ
