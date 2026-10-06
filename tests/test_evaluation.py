from scripts.evaluate import metrics


def test_failures_and_negative_false_acceptance_are_not_hidden():
    rows = [
        {'expected':'rejected','status':'accepted','elapsed_ms':100},
        {'expected':'uncertain','status':'uncertain','elapsed_ms':200},
        {'expected':'accepted','status':'rejected','elapsed_ms':300},
        {'expected':'rejected','error_type':'HTTPStatusError','elapsed_ms':400},
    ]
    m=metrics(rows)
    assert m['failures']==1 and m['completed']==3
    assert m['negative_cases']==3 and m['false_acceptances']==1
    assert m['false_rejections']==1 and m['uncertainty_count']==1
    assert m['p50_ms_all_requests']==200 and m['p95_ms_all_requests']==400


def test_empty_metrics_do_not_claim_accuracy():
    m=metrics([])
    assert m['false_acceptance_rate_all_negative_cases'] is None
    assert m['p50_ms_all_requests'] is None
