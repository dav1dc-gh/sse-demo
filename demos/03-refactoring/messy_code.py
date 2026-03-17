"""Data processing utilities — inherited from legacy codebase."""

import json
from datetime import datetime


EMPTY_STATISTICS = {'sum': 0, 'count': 0, 'avg': 0, 'min': 0, 'max': 0, 'range': 0}

TAX_MULTIPLIER = 1.1
DISCOUNT_MULTIPLIER = 0.9


def _is_valid_item(item):
    return item.get('name') and item.get('name') != '' and item.get('value') is not None


def _parse_numeric_value(raw_value):
    if isinstance(raw_value, str):
        try:
            return float(raw_value)
        except ValueError:
            return 0
    return raw_value


def _stamp_processed(item, processed=True):
    item['processed'] = processed
    item['timestamp'] = str(datetime.now())


def _apply_price_adjustments(value, include_tax=True, include_discount=False, surcharge=None):
    if include_tax:
        value *= TAX_MULTIPLIER
    if include_discount:
        value *= DISCOUNT_MULTIPLIER
    if surcharge is not None:
        value += surcharge
    return value


def _process_price(item, include_tax, include_discount, surcharge):
    value = _parse_numeric_value(item['value'])
    if value > 0:
        value = _apply_price_adjustments(value, include_tax, include_discount, surcharge)
        item['value'] = round(value, 2)
        _stamp_processed(item)
    else:
        item['value'] = 0
        _stamp_processed(item, processed=False)
        item['error'] = 'negative value'
    return item


def _normalize_name(item):
    name = item['name'].strip().lower().replace(' ', '_')
    name = ''.join(char for char in name if char.isalnum() or char == '_')
    item['name'] = name
    _stamp_processed(item)
    return item


def _deduplicate_tags(item):
    if 'tags' in item:
        tags = item['tags']
        if isinstance(tags, str):
            tags = tags.split(',')
        seen = []
        for tag in tags:
            tag = tag.strip().lower()
            if tag and tag not in seen:
                seen.append(tag)
        item['tags'] = seen
    _stamp_processed(item)
    return item


PROCESS_TYPE_PRICE = 1
PROCESS_TYPE_NAME = 2
PROCESS_TYPE_TAGS = 3


def process_items(items, process_type, include_tax=True, include_discount=False, surcharge=None):
    processed_items = []
    for item in items:
        if not _is_valid_item(item):
            continue
        if process_type == PROCESS_TYPE_PRICE:
            processed_items.append(_process_price(item, include_tax, include_discount, surcharge))
        elif process_type == PROCESS_TYPE_NAME:
            processed_items.append(_normalize_name(item))
        elif process_type == PROCESS_TYPE_TAGS:
            processed_items.append(_deduplicate_tags(item))
    return processed_items


def compute_statistics(named_value_lists):
    statistics = {}
    for category, values in named_value_lists.items():
        if values is None:
            statistics[category] = dict(EMPTY_STATISTICS)
            continue

        if not isinstance(values, list):
            statistics[category] = {
                'sum': values, 'count': 1, 'avg': values,
                'min': values, 'max': values, 'range': 0,
            }
            continue

        numeric_values = [v for v in values if v is not None and isinstance(v, (int, float))]
        if not numeric_values:
            statistics[category] = dict(EMPTY_STATISTICS)
            continue

        total = sum(numeric_values)
        count = len(numeric_values)
        minimum = min(numeric_values)
        maximum = max(numeric_values)
        statistics[category] = {
            'sum': total,
            'count': count,
            'avg': total / count,
            'min': minimum,
            'max': maximum,
            'range': maximum - minimum,
        }
    return statistics


def _format_item_status(item):
    return 'Active' if item.get('processed') else 'Inactive'


def _generate_text_report(items):
    lines = [
        '=== REPORT ===',
        f'Generated: {datetime.now()}',
        '==============',
        '',
    ]
    for item in items:
        lines.append(f"Name: {item.get('name', 'Unknown')}")
        lines.append(f"Value: {item.get('value', 'N/A')}")
        lines.append(f"Status: {_format_item_status(item)}")
        if item.get('error'):
            lines.append(f"Error: {item['error']}")
        lines.append('---')

    processed_count = sum(1 for item in items if item.get('processed'))
    lines.append(f'\nTotal items: {len(items)}')
    lines.append(f'Processed: {processed_count}')
    lines.append(f'Failed: {len(items) - processed_count}')
    return '\n'.join(lines) + '\n'


def _generate_csv_report(items):
    lines = ['name,value,status,error']
    for item in items:
        name = item.get('name', 'Unknown')
        value = item.get('value', 'N/A')
        status = _format_item_status(item)
        error = item.get('error', '')
        lines.append(f'{name},{value},{status},{error}')
    return '\n'.join(lines) + '\n'


def generate_report(items, output_format):
    if output_format == 'text':
        return _generate_text_report(items)
    elif output_format == 'csv':
        return _generate_csv_report(items)
    elif output_format == 'json':
        return json.dumps(items, indent=2)
    return ''


def merge_records_by_key(primary_records, secondary_records, merge_key):
    merged = {}
    for record in primary_records:
        record_id = record.get(merge_key)
        if record_id:
            merged[record_id] = dict(record)

    for record in secondary_records:
        record_id = record.get(merge_key)
        if record_id:
            if record_id in merged:
                for field, value in record.items():
                    if field != merge_key:
                        merged[record_id][field] = value
            else:
                merged[record_id] = dict(record)

    return list(merged.values())
