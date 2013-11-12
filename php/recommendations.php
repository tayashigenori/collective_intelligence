<?php

/*
expecting this format of data
*/
// A dictionary of movie critics and their ratings of a small
// set of movies
$critics = array(
    'Lisa Rose' => array(
        'Lady in the Water' => 2.5,
        'Snakes on a Plane' => 3.5,
        'Just My Luck' => 3.0,
        'Superman Returns' => 3.5,
        'You, Me and Dupree' => 2.5,
        'The Night Listener' => 3.0
    ),
    'Gene Seymour' => array(
        'Lady in the Water' => 3.0,
        'Snakes on a Plane' => 3.5,
        'Just My Luck' => 1.5,
        'Superman Returns' => 5.0,
        'The Night Listener' => 3.0,
        'You, Me and Dupree' => 3.5
    ),
    'Michael Phillips' => array(
        'Lady in the Water' => 2.5,
        'Snakes on a Plane' => 3.0,
        'Superman Returns' => 3.5,
        'The Night Listener' => 4.0
    ),
    'Claudia Puig' => array(
        'Snakes on a Plane' => 3.5,
        'Just My Luck' => 3.0,
        'The Night Listener' => 4.5,
        'Superman Returns' => 4.0,
        'You, Me and Dupree' => 2.5
    ),
    'Mick LaSalle' => array(
        'Lady in the Water' => 3.0,
        'Snakes on a Plane' => 4.0,
        'Just My Luck' => 2.0,
        'Superman Returns' => 3.0,
        'The Night Listener' => 3.0,
        'You, Me and Dupree' => 2.0
    ),
    'Jack Matthews' => array(
        'Lady in the Water' => 3.0,
        'Snakes on a Plane' => 4.0,
        'The Night Listener' => 3.0,
        'Superman Returns' => 5.0,
        'You, Me and Dupree' => 3.5
    ),
    'Toby' => array(
        'Snakes on a Plane' => 4.5,
        'You, Me and Dupree' => 1.0,
        'Superman Returns' => 4.0
    )
);

function load_tastes_from_file($filepath)
{
    $r = array();
    $file_handle = fopen($filepath, 'r');
    if ($file_handle === false) {
        return array();
    }
    while( ($line = fgets($file_handle)) !== false) {
        $line_parts = explode("\t", $line);
        $person = $line_parts[0];
        $tastes = $line_parts[1];
        $r[$person] = explode(",", $tastes);
    }
    fclose($file_handle);
    return $r;
}
function load_restaurants_from_file($filepath)
{
    $r = array();
    $file_handle = fopen($filepath, 'r');
    if ($file_handle === false) {
        return array();
    }
    while( ($line = fgets($file_handle)) !== false) {
        #$line_eucjp = mb_convert_encoding($line, 'EUC-JP', 'UTF-8');
        $r = explode(",", $line);
    }
    fclose($file_handle);
    return $r;
}

/*
 * distances
 */
// compute similarity score based on the distance between person1 and person2
function sim_distance($prefs, $person1, $person2)
{
    // get list of items for which both persons have scores
    $si = array();
    foreach ($prefs[$person1] as $item => $score) {
        if (array_key_exists($item, $prefs[$person2])) {
            $si[$item] = 1;
        }
    }
    // if person1 and person2 have nothing in common return 0
    if (count($si) == 0) {
        return 0;
    }

    // sum squares of all distances
    $tmp_distances = array();
    foreach ($prefs[$person1] as $item => $score) {
        if (array_key_exists($item, $prefs[$person2])) {
            $tmp_distances[] = pow( ($prefs[$person1][$item] - $prefs[$person2][$item]), 2);
        }
    }

    $sum_of_squares = array_sum($tmp_distances);
    return 1 / (1 + $sum_of_squares);
}

// return Pearson correlation of p1 and p2
function sim_pearson($prefs, $p1, $p2)
{
    // get list of items for which both persons have scores
    $si = array();
    foreach ($prefs[$p1] as $item => $score) {
        if (array_key_exists($item, $prefs[$p2])) {
            $si[$item] = 1;
        }
    }

    // length of the elements
    $n = count($si);

    // if p1 and p2 have nothing in common return 0
    if ($n == 0) {
        return 0;
    }

    $tmp_sum1 = array();
    $tmp_sum2 = array();
    $tmp_sum1_sq = array();
    $tmp_sum2_sq = array();
    $tmp_psum = array();
    foreach ($si as $it => $sc) {
        $tmp_sum1[] = $prefs[$p1][$it];
        $tmp_sum2[] = $prefs[$p2][$it];
        $tmp_sum1_sq[] = pow($prefs[$p1][$it], 2);
        $tmp_sum2_sq[] = pow($prefs[$p2][$it], 2);
        $tmp_psum[] = $prefs[$p1][$it] * $prefs[$p2][$it];
    }
    // sum all prefs
    $sum1 = array_sum($tmp_sum1);
    $sum2 = array_sum($tmp_sum2);

    // sum of squares
    $sum1_sq = array_sum($tmp_sum1_sq);
    $sum2_sq = array_sum($tmp_sum2_sq);

    // sum of products
    $psum = array_sum($tmp_psum);

    // compute Pearson score
    $num = $psum - ($sum1 * $sum2 / $n);
    $den = sqrt(($sum1_sq - pow($sum1,2) / $n) * ($sum2_sq - pow($sum2, 2) / $n));
    if ($den == 0) {
        return 0;
    }

    $r = $num / $den;

    return $r;
}

/*
 * Recommendations
 */
// return someone in prefs that matches $person best
// number of results and similarity are optinal parameter
function top_matches($prefs, $person, $n = 5, $similarity = 'sim_pearson')
{
    $scores = array();
    foreach ($prefs as $other => $item_arr) {
        if ($other != $person) {
            $scores[$other] = call_user_func_array($similarity, array($prefs, $person, $other));
        }
    }
    // sort scores so that higher scores come first
    arsort($scores);
    return $scores;
    //return array_slice($scores, 0, $n);
}


// compute recommendations using weighted average of scores of all users but $person
function get_recommendations($prefs, $person, $similarity = "sim_pearson")
{
    $totals = array();
    $rankings = array();
    $sim_sums = array();
    foreach ($prefs as $other => $item_arr) {
        // don't compare with self
        if ($other == $person) {
            continue;
        }
        $sim = call_user_func_array( $similarity, array($prefs, $person, $other));

        // ignore scores less than 0
        if ($sim <= 0) {
            continue;
        }

        foreach ($prefs[$other] as $item => $score) {
            // compute scores for items $person has not yet watched
            if ( (array_key_exists ($item, $prefs[$person]) == false) || $prefs[$person][$item] == 0 ) {
                // similarity * score
                if ( isset($totals[$item]) == false ) {
                    $totals[$item] = 0;
                }
                $totals[$item] += $prefs[$other][$item] * $sim;
                // sum of similarities
                if ( isset( $sim_sums[$item]) == false) {
                    $sim_sums[$item] = 0;
                }
                $sim_sums[$item] += $sim;
            }
        }
    }

    // normalize list
    foreach ( $totals as $item => $total ) {
        $rankings[$item] = ($total / $sim_sums[$item] );
    }

    // return sorted list
    arsort($rankings);
    return $rankings;
}
/*
"""
データを変換
"""
def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            # itemとpersonを入れ替える
            result[item][person]=prefs[person][item]
    return result

"""
アイテムベースの類似度を算出
"""
def calculateSimilarItems(prefs,n=10):
    # アイテムをキーとして持ち、それぞれのアイテムに似ている
    # アイテムのリストを値として持つディクショナリを作る。
    result={}

    # 嗜好の行列をアイテム中心な形に反転させる
    itemPrefs=transformPrefs(prefs)
    c=0
    for item in itemPrefs:
        # 巨大なデータセット用にステータスを表示
        c+=1
        if c%100==0: print "%d / %d" % (c,len(itemPrefs))
        # このアイテムにもっとも似ているアイテムたちを探す
        scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
        result[item]=scores
    return result

"""
アイテムベースの類似度を算出した上で推薦を算出する
"""
def getRecommendedItems(prefs,itemMatch,user):
    userRatings=prefs[user]
    scores={}
    totalSim={}

    # このユーザに評価されたアイテムをループする
    for (item,rating) in userRatings.items():

        # このアイテムに似ているアイテムたちをループする
        for (similarity,item2) in itemMatch[item]:

            # このアイテムに対してユーザがすでに評価を行なっていれば無視する
            if item2 in userRatings: continue

            # 評点と類似度を掛け合わせたものの合計で重み付けする
            scores.setdefault(item2,0)
            scores[item2]+=similarity*rating

            # すべての類似度の合計
            totalSim.setdefault(item2,0)
            totalSim[item2]+=similarity

    # 正規化のため、それぞれの重み付けしたスコアを類似度の合計で割る
    rankings=[(score/totalSim[item],item) for item,score in scores.items()]

    # 降順に並べたランキングを返す
    rankings.sort()
    rankings.reverse()
    return rankings

"""
movielensデータ
"""
function loadMovieLens(path='./data/ml-100k') {

    # 映画のタイトルを得る
    movies={}
    for line in open(path+'/u.item'):
        (id,title)=line.split('|')[0:2]
        movies[id]=title

    # データの読み込み
    prefs={}
    for line in open(path+'/u.data'):
        (user,movieid,rating,ts)=line.split('\t')
        prefs.setdefault(user,{})
        prefs[user][movies[movieid]]=float(rating)
    return prefs
}
*/

// main
$options = getopt("t:u:f:r:");
if (!is_array($options) ) {
    print "There was a problem reading in the options.\n\n";
    exit(1);
}
if (!isset($options['t']) || !isset($options['u']) || !isset($options['f']) || !isset($options['r'])) {
    print "t,u,f,r options are mandatory options.\n\n";
    exit(1);
}

$critics = load_tastes_from_file($options['f']);
$restaurants = load_restaurants_from_file($options['r']);

$user = $options['u'];
switch ($options['t']) {
    case 'similar_person':
        $top_matches = top_matches($critics, $user, 3);
        echo sprintf("[To:%s] Most similar person to you!\n", $user);
        foreach ($top_matches as $other => $score) {
            echo sprintf("similar person: %s, similar score: %s\n", $other, $score);
        }
        break;
    case 'recommendation':
        $recommendations = get_recommendations($critics, $user);
        echo sprintf("[To:%s] Recommendation for you!\n", $user);
        foreach ($recommendations as $item => $score) {
            echo sprintf("recommended item: %s (%d banme), recommend score: %s\n", $restaurants[$item], $item, $score);
        }
        break;
    default:
        # do nothing
        echo "unknown type\n\n";
}

/*
echo sim_distance($critics, 'Lisa Rose', 'Gene Seymour');
echo "\n";
echo sim_pearson($critics, 'Lisa Rose', 'Gene Seymour');
echo "\n";
foreach (top_matches($critics, 'Toby', 3) as $other => $score) {
    echo sprintf("similar person: %s, similar score: %s", $other, $score);
    echo "\n";
}
echo "\n";


foreach (get_recommendations($critics, 'Toby') as $item => $score) {
    echo sprintf("recommended item: %s, recommend score: %s", $item, $score);
    echo "\n";
}
echo "\n";

foreach (get_recommendations($critics, 'Toby', 'sim_distance') as $item => $score) {
    echo sprintf("recommended item: %s, recommend score: %s", $item, $score);
    echo "\n";
}
echo "\n";
*/

