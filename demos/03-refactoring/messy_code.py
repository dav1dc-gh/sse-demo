"""Data processing utilities — inherited from legacy codebase."""

import json
import os
from datetime import datetime


def process_items(items, processing_type, apply_tax=True, apply_discount=False, adjustment=None):
    """Process a list of item dicts based on the specified processing type.

    Args:
        items: List of dicts, each with 'n' (name) and 'v' (value) keys.
        processing_type: 1 = calculate pricing, 2 = normalize names, 3 = deduplicate tags.
        apply_tax: If True, applies 10% tax to values (type 1 only).
        apply_discount: If True, applies 10% discount to values (type 1 only).
        adjustment: Optional flat amount added to each value (type 1 only).

    Returns:
        List of processed item dicts with 'processed' and 'ts' fields added.
    """
    processed_items = []

    for item in items:
        # Skip items missing a name or value
        if not item.get('n') or item.get('v') is None:
            continue

        if processing_type == 1:
            # --- Pricing calculation: coerce value to float, apply tax/discount/adjustment ---
            value = item['v']
            if isinstance(value, str):
                try:
                    value = float(value)
                except (ValueError, TypeError):
                    value = 0

            if value > 0:
                if apply_tax:
                    value = value * 1.1   # 10% tax markup
                if apply_discount:
                    value = value * 0.9   # 10% discount
                if adjustment is not None:
                    value = value + adjustment

                item['v'] = round(value, 2)
                item['processed'] = True
                item['ts'] = str(datetime.now())
            else:
                item['v'] = 0
                item['processed'] = False
                item['error'] = 'negative value'

            processed_items.append(item)

        elif processing_type == 2:
            # --- Name normalization: lowercase, replace spaces, strip non-alphanumeric ---
            normalized_name = item['n'].strip().lower().replace(' ', '_')
            normalized_name = ''.join(
                char for char in normalized_name if char.isalnum() or char == '_'
            )
            item['n'] = normalized_name
            item['processed'] = True
            item['ts'] = str(datetime.now())
            processed_items.append(item)

        elif processing_type == 3:
            # --- Tag deduplication: split if string, normalize, and remove duplicates ---
            if 'tags' in item:
                tags = item['tags']
                if isinstance(tags, str):
                    tags = tags.split(',')

                unique_tags = []
                for tag in tags:
                    cleaned_tag = tag.strip().lower()
                    if cleaned_tag and cleaned_tag not in unique_tags:
                        unique_tags.append(cleaned_tag)
                item['tags'] = unique_tags

            item['processed'] = True
            item['ts'] = str(datetime.now())
            processed_items.append(item)

    return processed_items


def calculate_statistics(data):
    """Compute summary statistics (sum, count, avg, min, max, range) for each key in data.

    Args:
        data: Dict mapping category names to either a single numeric value,
              a list of numeric values, or None.

    Returns:
        Dict mapping each key to a stats dict with sum, count, avg, min, max, range.
    """
    empty_stats = {'sum': 0, 'count': 0, 'avg': 0, 'min': 0, 'max': 0, 'range': 0}
    statistics = {}

    for category, values in data.items():
        if values is None:
            statistics[category] = dict(empty_stats)
            continue

        # Single scalar value — treat as a one-element dataset
        if not isinstance(values, list):
            statistics[category] = {
                'sum': values, 'count': 1, 'avg': values,
                'min': values, 'max': values, 'range': 0
            }
            continue

        if len(values) == 0:
            statistics[category] = dict(empty_stats)
            continue

        # Accumulate stats across all valid numeric entries in the list
        total = 0
        count = 0
        minimum = float('inf')
        maximum = float('-inf')

        for number in values:
            if number is not None and isinstance(number, (int, float)):
                total += number
                count += 1
                if number < minimum:
                    minimum = number
                if number > maximum:
                    maximum = number

        if count > 0:
            statistics[category] = {
                'sum': total,
                'count': count,
                'avg': total / count,
                'min': minimum,
                'max': maximum,
                'range': maximum - minimum
            }
        else:
            statistics[category] = dict(empty_stats)

    return statistics


def generate_report(data, output_format):
    """Generate a formatted report from a list of processed item dicts.

    Args:
        data: List of item dicts (expects 'n', 'v', 'processed', and optional 'error' keys).
        output_format: One of 'text', 'csv', or 'json'.

    Returns:
        The formatted report as a string.
    """
    output = ''

    if output_format == 'text':
        # --- Plain-text report with header, item details, and summary ---
        output += '=== REPORT ===\n'
        output += 'Generated: ' + str(datetime.now()) + '\n'
        output += '==============\n\n'

        for item in data:
            output += 'Name: ' + str(item.get('n', 'Unknown')) + '\n'
            output += 'Value: ' + str(item.get('v', 'N/A')) + '\n'
            output += 'Status: ' + ('Active' if item.get('processed') else 'Inactive') + '\n'
            if item.get('error'):
                output += 'Error: ' + str(item.get('error')) + '\n'
            output += '---\n'

        # Summary counts
        processed_count = sum(1 for item in data if item.get('processed'))
        output += '\nTotal items: ' + str(len(data)) + '\n'
        output += 'Processed: ' + str(processed_count) + '\n'
        output += 'Failed: ' + str(len(data) - processed_count) + '\n'

    elif output_format == 'csv':
        # --- CSV with header row ---
        output += 'name,value,status,error\n'
        for item in data:
            output += str(item.get('n', 'Unknown')) + ','
            output += str(item.get('v', 'N/A')) + ','
            output += ('Active' if item.get('processed') else 'Inactive') + ','
            output += str(item.get('error', '')) + '\n'

    elif output_format == 'json':
        output = json.dumps(data, indent=2)

    return output


def merge_lists_by_key(primary_list, secondary_list, merge_key):
    """Merge two lists of dicts by a shared key, with secondary values overriding on conflict.

    Items from primary_list are indexed first. For each item in secondary_list,
    if the merge_key already exists the secondary fields are merged in (overriding
    duplicates); otherwise the secondary item is added as a new entry.

    Args:
        primary_list: Base list of dicts.
        secondary_list: List of dicts to merge into the primary.
        merge_key: The dict key used to match items across both lists.

    Returns:
        A merged list of dicts.
    """
    merged = {}

    # Index all primary items by their merge key
    for item in primary_list:
        item_id = item.get(merge_key)
        if item_id:
            merged[item_id] = dict(item)

    # Merge secondary items: update existing entries or add new ones
    for item in secondary_list:
        item_id = item.get(merge_key)
        if item_id:
            if item_id in merged:
                for field, value in item.items():
                    if field != merge_key:
                        merged[item_id][field] = value
            else:
                merged[item_id] = dict(item)

    return list(merged.values())
