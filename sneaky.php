<?PHP
        unset($log,$log2);
        if ( /* Minor edits with obscenities. */
                (($change['length'] >= -200) and ($change['length'] <= 200))
                and (($d = $wpi->diff($change['title'],$change['old_revid'],$change['revid'])) or true)
                and ((($change['title'] == 'User:VinDieselism/Sandbox') and print_r($rv)) or true)
                and (($s = score($vandalWordsList,$d[0],$log)) or true)
                and (($s -= score($vandalWordsList,$d[1],$log2)) or true)
                and (
                        (
                                ($s < -5) /* Minor edits with likely false positives. */
                                and (($rv = $wpapi->revisions($change['title'],2,'older',true,$change['revid'])) or true)
                                and (!fnmatch('*#REDIRECT*',strtoupper(substr($rv[0]['*'],0,9))))
                                and (!fnmatch('*SEX*',strtoupper($rv[1]['*'])))
                                and (!fnmatch('*BDSM*',strtoupper($rv[1]['*'])))
                                and (score($vandalWordsList,$change['title']) >= 0)
                                and (score($vandalWordsList,$rv[1]['*']) >= 0)
                                and (!preg_match('/(^|\s)([a-z]{1,2}(\*+|\-{3,})[a-z]{0,2}|\*{4}|\-{4}|(\<|\()?censored(\>|\))?)(ing?|ed)?(\s|$)/iS',$rv[1]['*']))
                                and ($heuristic .= '/obscenities')
                                and ($reason = 'making a minor change with obscenities')
                        )
                        or (
                                ($s > 5)
                                and (($rv = $wpapi->revisions($change['title'],2,'older',true,$change['revid'])) or true)
                                and (!fnmatch('*#REDIRECT*',strtoupper(substr($rv[0]['*'],0,9))))
                                and (!preg_match('/(^|\s)([a-z]{1,2}(\*+|\-{3,})[a-z]{0,2}|\*{4}|\-{4}|(\<|\()?censored(\>|\))?)(ing?|ed)?(\s|$)/iS',$rv[1]['*']))
                                and (preg_match('/(^|\s)([a-z]{1,2}(\*+|\-{3,})[a-z]{0,2}|\*{4}|\-{4}|(\<|\()?censored(\>|\))?)(ing?|ed)?(\s|$)/iS',$rv[0]['*']))
                                and ($heuristic .= '/censor')
                                and ($reason = 'making a minor change censoring content ([[WP:CENSOR|Wikipedia is not censored]])')
                        )
                        or (
                                (preg_match('/\!\!\!/S',$d[0]))
                                and (($rv = $wpapi->revisions($change['title'],2,'older',true,$change['revid'])) or true)
                                and (!preg_match('/\!\!\!/S',$rv[1]['*']))
                                and (!fnmatch('*#REDIRECT*',strtoupper(substr($rv[0]['*'],0,9))))
                                and ($heuristic .= '/exclamation')
                                and ($reason = 'making a minor change adding "!!!"')
                        )
                )
        ) { $heuristicret = true; if (isset($log2) and is_array($log2)) foreach ($log2 as $k => $v) $log[$k] -= $v; if (isset($log) and is_array($log)) foreach ($log as $k => $v) if ($v == 0) unset($log[$k]); unset($log2); /* fwrite($irc,'PRIVMSG #wikipedia-BAG/VinDieselism :Would revert http://en.wikipedia.org/w/index.php?title='.urlencode($change['namespace'].$change['title']).'&diff=prev'.'&oldid='.urlencode($change['revid'])." .\n"); */ }
?>
