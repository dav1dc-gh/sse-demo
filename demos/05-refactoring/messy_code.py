"""
Messy Code — Refactoring Demo

This file contains intentionally BAD code that works but is poorly structured,
uses bad naming conventions, has code smells, and violates clean code principles.

DEMO INSTRUCTIONS:
==================
1. Select the entire file (or individual functions)
2. Open Copilot Chat and ask: "Refactor this code to follow clean code principles"
3. Or try more specific prompts:
   - "Refactor this to use proper naming conventions"
   - "Extract this into smaller, well-named functions"
   - "Apply the Single Responsibility Principle to this code"
   - "Convert this to use modern Python idioms"
4. Try the inline chat (Cmd+I): "Fix the code smells in this function"
5. Show the /fix command to address potential bugs

BONUS: Ask Copilot "What are the code smells in this file?" and watch it
enumerate everything that's wrong.
"""

import json
import os
from datetime import datetime


# Bad: God function that does everything
def do_stuff(d, t, flag1=True, flag2=False, x=None):
    r = []
    for i in range(len(d)):
        item = d[i]
        # check if valid
        if item.get('n') and item.get('n') != '' and item.get('v') is not None:
            if t == 1:
                # process type 1
                val = item['v']
                if isinstance(val, str):
                    try:
                        val = float(val)
                    except:
                        val = 0
                if val > 0:
                    if flag1:
                        val = val * 1.1  # add tax
                    if flag2:
                        val = val * 0.9  # discount
                    if x is not None:
                        val = val + x
                    item['v'] = round(val, 2)
                    item['processed'] = True
                    item['ts'] = str(datetime.now())
                    r.append(item)
                else:
                    item['v'] = 0
                    item['processed'] = False
                    item['error'] = 'negative value'
                    r.append(item)
            elif t == 2:
                # process type 2
                n = item['n']
                n = n.strip()
                n = n.lower()
                n = n.replace(' ', '_')
                n = ''.join(c for c in n if c.isalnum() or c == '_')
                item['n'] = n
                item['processed'] = True
                item['ts'] = str(datetime.now())
                r.append(item)
            elif t == 3:
                # process type 3
                if 'tags' in item:
                    tags = item['tags']
                    if isinstance(tags, str):
                        tags = tags.split(',')
                    new_tags = []
                    for tag in tags:
                        tag = tag.strip().lower()
                        if tag and tag not in new_tags:
                            new_tags.append(tag)
                    item['tags'] = new_tags
                item['processed'] = True
                item['ts'] = str(datetime.now())
                r.append(item)
    return r


# Bad: Deeply nested conditionals, magic numbers, no error handling
def calc(data):
    result = {}
    for k in data:
        v = data[k]
        if v is not None:
            if isinstance(v, list):
                if len(v) > 0:
                    s = 0
                    c = 0
                    mn = 999999999
                    mx = -999999999
                    for i in v:
                        if i is not None:
                            if isinstance(i, (int, float)):
                                s = s + i
                                c = c + 1
                                if i < mn:
                                    mn = i
                                if i > mx:
                                    mx = i
                    if c > 0:
                        result[k] = {
                            'sum': s,
                            'count': c,
                            'avg': s / c,
                            'min': mn,
                            'max': mx,
                            'range': mx - mn
                        }
                    else:
                        result[k] = {'sum': 0, 'count': 0, 'avg': 0, 'min': 0, 'max': 0, 'range': 0}
                else:
                    result[k] = {'sum': 0, 'count': 0, 'avg': 0, 'min': 0, 'max': 0, 'range': 0}
            else:
                result[k] = {'sum': v, 'count': 1, 'avg': v, 'min': v, 'max': v, 'range': 0}
        else:
            result[k] = {'sum': 0, 'count': 0, 'avg': 0, 'min': 0, 'max': 0, 'range': 0}
    return result


# Bad: Duplicated logic, poor separation of concerns
def make_report(data, fmt):
    output = ''
    if fmt == 'text':
        output = output + '=== REPORT ===\n'
        output = output + 'Generated: ' + str(datetime.now()) + '\n'
        output = output + '==============\n\n'
        for item in data:
            output = output + 'Name: ' + str(item.get('n', 'Unknown')) + '\n'
            output = output + 'Value: ' + str(item.get('v', 'N/A')) + '\n'
            output = output + 'Status: ' + ('Active' if item.get('processed') else 'Inactive') + '\n'
            if item.get('error'):
                output = output + 'Error: ' + str(item.get('error')) + '\n'
            output = output + '---\n'
        output = output + '\nTotal items: ' + str(len(data)) + '\n'
        processed_count = 0
        for item in data:
            if item.get('processed'):
                processed_count = processed_count + 1
        output = output + 'Processed: ' + str(processed_count) + '\n'
        output = output + 'Failed: ' + str(len(data) - processed_count) + '\n'
    elif fmt == 'csv':
        output = output + 'name,value,status,error\n'
        for item in data:
            output = output + str(item.get('n', 'Unknown')) + ','
            output = output + str(item.get('v', 'N/A')) + ','
            output = output + ('Active' if item.get('processed') else 'Inactive') + ','
            output = output + str(item.get('error', '')) + '\n'
    elif fmt == 'json':
        output = json.dumps(data, indent=2)
    return output


# Bad: Using index-based iteration, unclear variable names, no type hints
def merge(l1, l2, k):
    r = {}
    for i in range(len(l1)):
        id = l1[i].get(k)
        if id:
            r[id] = dict(l1[i])
    for i in range(len(l2)):
        id = l2[i].get(k)
        if id:
            if id in r:
                for key in l2[i]:
                    if key != k:
                        r[id][key] = l2[i][key]
            else:
                r[id] = dict(l2[i])
    return list(r.values())
