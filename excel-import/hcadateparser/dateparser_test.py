from dateparser import parseDate, validateResult
from sys import stderr
from dateData import rawDates, miniRawDates

total = 0
numPassthrough = 0
numFailedValidation = 0
missing = 0
matched = 0
single = 0
parsed = dict()

for date in miniRawDates:
    result = parseDate(date)
    result, problems = validateResult(result, date)

    if len(problems) != 0:
        numFailedValidation += 1
        print(problems)

    total += 1
    if result is not None:
        matched += 1
        if result['verbatim']:
            numPassthrough += 1
        
        if len(result['dates']) == 0:
            missing += 1

        if len(result['dates']) == 1:
            single += 1

        parsed[date] = result
    else:
        print(f'parser problem: parser did not understand date "{date}". Talk to a developer!')

print('%d dates had out of range values and need manual fixing' % numFailedValidation, file=stderr)
print('%d dates are known-missing' % missing, file=stderr)
print('%d dates are have extra data and will be displayed verbatim' % numPassthrough, file=stderr)
print('Accuracy: %.1f%% (%d / %d) -- %d unhandled' % (100 * matched / total, matched, total, total - matched), file=stderr)
print('Single dates: %.1f%% (%d / %d) -- %d multiple' % (100 * single / matched, single, matched, matched - single), file=stderr)

with open("parsedDates.json", "w") as outFile:
    import json
    json.dump(parsed, outFile, indent=4)
