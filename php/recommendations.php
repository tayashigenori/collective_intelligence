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

function loadRestaurantsFromFile($filepath)
{
    $r = array();
    $file_handle = fopen($filepath, 'r');
    if ($file_handle === false) {
        return array();
    }
    while( ($line = fgets($file_handle)) !== false) {
        #$line_eucjp = mb_convert_encoding($line, 'EUC-JP', 'UTF-8');
        $r = explode(",", rtrim($line));
    }
    fclose($file_handle);
    return $r;
}
function loadTastesFromFile($filepath, $restaurants = array())
{
    $r = array();
    $file_handle = fopen($filepath, 'r');
    if ($file_handle === false) {
        return array();
    }
    while( ($line = fgets($file_handle)) !== false) {
        $line_parts = explode("\t", rtrim($line));
        $person = $line_parts[0];
        $tastes = explode(",", $line_parts[1]);
        // error
        if (count($tastes) != count($restaurants)) {
            fputs(STDERR, sprintf("Invalid input in %s", $filepath));
            exit(0);
        }
        // add!
        if (empty($restaurants)) {
            $r[$person] = $tastes;
        } else {
            $r[$person] = array();
            foreach(range(0, count($tastes)-1) as $n) {
                $r[$person][$restaurants[$n]] = $tastes[$n];
            }
        }
    }
    fclose($file_handle);
    return $r;
}

/*
 * distances
 */
// compute similarity score based on the distance between person1 and person2
function simDistance($prefs, $person1, $person2)
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
function simPearson($prefs, $p1, $p2)
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
function topMatches($prefs, $person, $n = 5, $similarity = 'simPearson')
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
function getRecommendations($prefs, $person, $similarity = "simPearson")
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
                if ( array_key_exists($item, $totals) == false ) {
                    $totals[$item] = 0;
                }
                $totals[$item] += $prefs[$other][$item] * $sim;
                // sum of similarities
                if ( array_key_exists($item, $sim_sums) == false) {
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

// transform data
function transformPrefs($prefs)
{
    $result = array();
    foreach ($prefs as $person => $items) {
        foreach ($items as $item => $score) {
            if (array_key_exists($item, $result) == false) {
                $result[$item] = array();
            }
            // exchange $item and $person
            $result[$item][$person] = $prefs[$person][$item];
        }
    }
    return $result;
}

// compute item-based similarities
function calculateSimilarItems($prefs, $n = 10)
{
    // create an array with the key as $item and the value as a list of similar items to it
    $result = array();

    // transform prefs marix to item-centric
    $item_prefs = transformPrefs($prefs);
    $c = 0;
    foreach ($item_prefs as $item) {
        // show status in processing huge dataset
        $c += 1;
        if ( $c % 100 == 0) {
            echo sprintf("%d / %d", $c, count($item_prefs));
        }
        // find items most similar to $item
        $scores = topMatches($item_prefs, $item, $n, 'sim_distance');
        $result[$item] = $scores;
    }
    return $result;
}

// compute recommendations by computing item-based similarities
function getRecommendedItems($prefs, $item_match, $user)
{
    $user_ratings = $prefs[$user];
    $scores = array();
    $total_sim = array();

    // loop over items rated by this $user
    foreach($user_ratings as $item => $rating) {

        // loop over items similar to this $item
        foreach ($item_match[$item] as $similarity => $item2) {

            // ignore items $user already rated
            if (array_key_exists($item2, $user_ratings)) {
                continue;
            }

            // compute weighted score of products of similarity and rating
            if (array_key_exists($items, $scores)) {
                $scores[$item2] = 0;
            }
            $scores[$item2] += $similarity * $rating;

            // compute sum of all similarities
            if (array_key_exists($items, $total_sim)) {
                $total_sim[$item2] = 0;
            }
            $total_sim[$item2] += $similarity;
        }
    }

    // for normalization, divide weighted score by sum of similarities
    $rankings = array();
    foreach ($scores as $item => $score) {
        $rankings[] = array(
            $score / $total_sim[$item],
            $item
        );
    }

    // return ranking sorted in descending order
    arsort($rankings);
    return $rankings;
}

/*
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

$restaurants = loadRestaurantsFromFile($options['r']);
$critics = loadTastesFromFile($options['f'], $restaurants);

$user = $options['u'];
switch ($options['t']) {
    case 'similar_person':
        $top_matches = topMatches($critics, $user, 3);
        echo sprintf("[To:%s] Most similar person to you!\n", $user);
        foreach ($top_matches as $other => $score) {
            echo sprintf("similar person: %s, similar score: %s\n", $other, $score);
        }
        break;
    case 'recommendation':
        $recommendations = getRecommendations($critics, $user);
        echo sprintf("[To:%s] Recommendation for you!\n", $user);
        foreach ($recommendations as $item => $score) {
            echo sprintf("recommended item: %s, recommend score: %s\n", $item, $score);
        }
        break;
    case 'transform':
        $transformed_prefs = transformPrefs($critics);
        echo sprintf("Transforming...\n");
        foreach ($transformed_prefs as $item => $critics) {
            echo sprintf("transformed: item: %s, critics: %s\n", $item, implode(",", $critics));
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

