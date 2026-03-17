"""Legacy data processing pipeline for financial transaction records."""

import re
from collections import defaultdict
from datetime import datetime, timedelta
from functools import reduce
from itertools import groupby
from operator import itemgetter


def proc_txn_batch(raw_data: list[str], cfg: dict) -> dict:
    """
    Process a batch of transactions and calculate financial risk metrics per account.
    
    This function takes raw transaction data, parses it, normalizes amounts to USD,
    and generates a risk assessment for each account based on transaction patterns.
    
    **ELI5 (Explain Like I'm 5):**
    Imagine you're a bank looking at customer transactions. This function:
    1. Reads messy transaction records (like "TXN123|20240101120000|ACC001|PUR|100|USD|...")
    2. Cleans them up and organizes the data nicely
    3. Converts all money to USD if it's in a different currency
    4. Groups transactions by account
    5. Calculates suspicious activity scores by checking:
       - Too many transactions in 24 hours? ⚠️
       - Too much money spent? ⚠️
       - API transactions over $5000? ⚠️
       - Lots of international transfers? ⚠️
       - Suspicious patterns (like making lots of transactions just under $10k)? ⚠️
    6. Returns a report for each account with total spending, risk level (LOW/MEDIUM/HIGH), 
       and whether it should be flagged for review.
    
    Args:
        raw_data: List of pipe-delimited transaction strings
        cfg: Configuration dict with keys: fx_rates, velocity_window_hrs, velocity_threshold,
             high_value_threshold, structuring_threshold, flag_threshold
    
    Returns:
        Dictionary mapping account IDs to risk analysis results including totals, 
        risk scores, and transaction metadata
    """
    parsed = []
    for line in raw_data:
        if not line.strip() or line.startswith('#'):
            continue
        parts = line.split('|')
        if len(parts) < 7:
            continue
        rec = {
            'tid': parts[0].strip(),
            'ts': datetime.strptime(parts[1].strip(), '%Y%m%d%H%M%S'),
            'acct': parts[2].strip(),
            'type': parts[3].strip().upper(),
            'amt': float(parts[4].strip()),
            'ccy': parts[5].strip().upper(),
            'meta': dict(kv.split('=') for kv in parts[6].strip().split(';') if '=' in kv)
        }
        if rec['amt'] < 0 and rec['type'] != 'REV':
            rec['type'] = 'ADJ'
            rec['meta']['auto_adjusted'] = 'true'
        parsed.append(rec)

    fx = cfg.get('fx_rates', {})
    normalized = []
    for r in parsed:
        if r['ccy'] != 'USD':
            rate = fx.get(r['ccy'], 1.0)
            r['amt_usd'] = round(r['amt'] * rate, 2)
            r['fx_applied'] = True
        else:
            r['amt_usd'] = r['amt']
            r['fx_applied'] = False
        normalized.append(r)

    sorted_data = sorted(normalized, key=lambda x: (x['acct'], x['ts']))
    grouped = defaultdict(list)
    for rec in sorted_data:
        grouped[rec['acct']].append(rec)

    results = {}
    for acct, txns in grouped.items():
        debits = [t for t in txns if t['type'] in ('PUR', 'WDR', 'FEE')]
        credits = [t for t in txns if t['type'] in ('DEP', 'REF', 'REV')]
        adjustments = [t for t in txns if t['type'] == 'ADJ']

        total_deb = reduce(lambda a, t: a + t['amt_usd'], debits, 0.0)
        total_cred = reduce(lambda a, t: a + t['amt_usd'], credits, 0.0)
        total_adj = reduce(lambda a, t: a + t['amt_usd'], adjustments, 0.0)

        velocity = len([
            t for t in txns
            if t['ts'] > (datetime.now() - timedelta(hours=cfg.get('velocity_window_hrs', 24)))
        ])

        risk_score = 0
        if velocity > cfg.get('velocity_threshold', 10):
            risk_score += 30
        if total_deb > cfg.get('high_value_threshold', 10000):
            risk_score += 25
        if any(t.get('meta', {}).get('channel') == 'API' and t['amt_usd'] > 5000 for t in txns):
            risk_score += 20
        cross_border = [t for t in txns if t.get('fx_applied')]
        if len(cross_border) > len(txns) * 0.5:
            risk_score += 15
        pattern = detect_structuring(txns, cfg.get('structuring_threshold', 9500))
        if pattern:
            risk_score += 40

        results[acct] = {
            'account': acct,
            'transaction_count': len(txns),
            'total_debits': round(total_deb, 2),
            'total_credits': round(total_cred, 2),
            'total_adjustments': round(total_adj, 2),
            'net_position': round(total_cred - total_deb + total_adj, 2),
            'velocity_24h': velocity,
            'risk_score': min(risk_score, 100),
            'risk_level': 'HIGH' if risk_score >= 70 else 'MEDIUM' if risk_score >= 40 else 'LOW',
            'flagged': risk_score >= cfg.get('flag_threshold', 50),
            'cross_border_pct': round(len(cross_border) / len(txns) * 100, 1) if txns else 0,
            'first_txn': min(t['ts'] for t in txns),
            'last_txn': max(t['ts'] for t in txns),
        }

    return results


def detect_structuring(txns: list[dict], threshold: float) -> bool:
    """Detect potential transaction structuring (smurfing)."""
    amts = sorted([t['amt_usd'] for t in txns if t['type'] in ('PUR', 'WDR', 'DEP')])
    if len(amts) < 3:
        return False
    near_threshold = [a for a in amts if threshold * 0.85 <= a <= threshold]
    if len(near_threshold) >= 3:
        timestamps = [
            t['ts'] for t in txns
            if t['amt_usd'] in near_threshold
        ]
        if timestamps:
            span = (max(timestamps) - min(timestamps)).total_seconds() / 3600
            if span <= 72:
                return True
    return False


def validate_account_id(acct_id: str) -> bool:
    return bool(re.match(
        r'^(?:(?:(?:[A-Z]{2}\d{2})(?:\s?[A-Z0-9]{4}){2,7}(?:\s?[A-Z0-9]{1,4})?)|'
        r'(?:\d{9}(?:\d{3,9})?)|'
        r'(?:[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}(?:[A-Z0-9]{3})?))$',
        acct_id.strip().upper()
    ))


def find_related_transactions(txns: list[dict], target_tid: str, depth: int = 3) -> list[dict]:
    target = next((t for t in txns if t['tid'] == target_tid), None)
    if not target:
        return []

    related = set()
    queue = [(target, 0)]

    while queue:
        current, d = queue.pop(0)
        if d >= depth:
            continue
        for t in txns:
            if t['tid'] in related or t['tid'] == current['tid']:
                continue
            if (t['acct'] == current['acct'] and
                abs((t['ts'] - current['ts']).total_seconds()) < 3600):
                related.add(t['tid'])
                queue.append((t, d + 1))
            elif (abs(t['amt_usd'] - current['amt_usd']) < 0.01 and
                  t['type'] != current['type'] and
                  abs((t['ts'] - current['ts']).total_seconds()) < 86400):
                related.add(t['tid'])
                queue.append((t, d + 1))

    return [t for t in txns if t['tid'] in related]
