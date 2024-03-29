
#データベースからメニューを取得する
#仮のダミーデータを記述


def Recipe():
	total_recipe_state_list = ["S1","S2","S3","S4","S5","S6","S7","S8","S9","S10","S11","S12","S13","S14","S15","S16","SS1","SS2","SS3","SS4","SS5"]
	first_recipe_state_list = ["S1","S2","S3","S4","S5","S6","S7","S8","S9","S10","S11","S12","S13","S14","S15","S16"]
	second_recipe_state_list = ["SS1","SS2","SS3","SS4","SS5"]

	first_recipe_flow_edges_list = [("S2","S3"),("S4","S5"),("S7","S8"),("S9","S10"),
					  ("S6","S11"),("S8","S11"),("S11","S12"),("S12","S13"),
					  ("S1","S13"),("S3","S13"),("S5","S13"),("S13","S14"),("S10","S14"),
					  ("S14","S15"),("S15","S16")]

	second_recipe_flow_edges_list = [("SS1","SS2"),("SS2","SS3"),("SS3","SS4"),("SS5","SS4")]

	cost_time = {"S1":2,"S2":1,"S3":1,"S4":1,"S5":1,"S6":4,"S7":1,"S8":3,"S9":17,"S10":20,
			  "S11":1,"S12":11,"S13":20,"S14":1,"S15":4,"S16":1,"SS1":15,"SS2":20,"SS3":2,"SS4":1,"SS5":16}

	use_resource ={"work":["S1","S2","S3","S4","S5","S6","S7","S8","SS3","SS5","SS4"],"IH":["S9","S10","S11","S12","S13","S14","S15","S16","SS1","SS2"]}

	multitasking ={"Multitasking":["S9","S10","SS1","SS2"]}
	#multitasking ={"Multitasking":["S9","SS1"]}
	#multitasking ={"Multitasking":[]}
	return total_recipe_state_list,first_recipe_state_list,second_recipe_state_list,first_recipe_flow_edges_list,second_recipe_flow_edges_list,cost_time,use_resource,multitasking



def Recipe_Text():
	total,first_receipe_s,second_receipe_s,first_receipe_f,second_receipe_f,cost_time,use_resource,multitasking = Recipe()

	recipe_text_list = ["舞茸を細かくほぐす","しめじの石突きを切り落とし","しめじを細かくほぐす","椎茸の石突きと軸を切り落とす",
					 "椎茸を５m幅に切る","ニンニクを３ｍにスライスする","赤唐辛子の種を取り除く","赤唐辛子を4等分に輪切り","鍋に水を入れ，沸騰させる",
					 "鍋の熱湯に塩とオリーブオイルを加え，スパゲッティを規定時間ゆでる","フライパンにオリーブオイルを入れる","フライパンにニンニクと赤唐辛子を加え，香りが出るまで加熱する",
					 "フライパンに舞茸，しめじ，椎茸，塩を加えてしんなりするまで炒める","フライパンに茹でたスパゲッティと和風粉末だし，ゆで汁を加える","フライパン内の食材を満遍なく強火で混ぜ合わせる","お皿に盛り付ける"]
	recipe_d ={}
	
	if len(first_receipe_s) == len(recipe_text_list):
		for num in range(0,len(first_receipe_s)):
			recipe_d.update([(first_receipe_s[num],recipe_text_list[num])])

	#print(recipe_d)

	return recipe_d
Recipe_Text()