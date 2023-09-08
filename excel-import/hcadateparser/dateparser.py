import re

months = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
]

monthNumbers = {}
for idx, month in enumerate(months):
    monthNumbers[month] = idx + 1

# Map abbreviated months to their full name
monthMap = {
    'Jan': 'January',
    'Feb': 'February',
    'Mar': 'March',
    'Apr': 'April',
    'May': 'May',
    'Jun': 'June',
    'Jul': 'July',
    'Aug': 'August',
    'Sep': 'September',
    'Sept': 'September',
    'Oct': 'October',
    'Nov': 'November',
    'Dec': 'December',
}

# Map typos in months to their correct, full names
typoMonthMap = {
    'Janary':     'January',
    'Janruary':   'January',
    'Janaury':    'January',
    'Januaey':    'January',
    'Januray':    'January',
    'Janurary':   'January',
    'Febrary':    'February',
    'Fabruary':   'February',
    'Febraury':   'February',
    'Feburary':   'February',
    'Febuary':    'February',
    'Juy':        'July',
    'Jule':       'July',
    'Auguest':    'August',
    'Augudt':     'August',
    'Spet':       'September',
    'Septmeber':  'September',
    'Sepember':   'September',
    'Septemer':   'September',
    'Spetember':  'September',
    'Septmber':   'September',
    'Septemeber': 'September',
    'Ooctober':   'October',
    'Ovtober':    'October',
    'Octobeer':   'October',
    'Ocyober':    'October',
    'Novermber':  'November',
    'Novemebr':   'November',
    'Novemver':   'November',
    'Decemeber':  'December',
    'Decmber':    'December',
    'Decemer':    'December',
    'Deceber':    'December',
    'Dece,ber':   'December',
}

# Explicit markers of unreadable / missing data
missingDataMarkers = {
    '(Month Illegible)',
    '(illegible)',
    '[illegible]',
}

# Jam all of that data together into a proper matcher
shortMonths = set(monthMap.keys())
longMonths = set(monthMap.values())
typoMonths = set(typoMonthMap.keys())
baseMonths = shortMonths | longMonths | typoMonths | missingDataMarkers
lowerMonths = set()

for month in baseMonths:
    lowerMonths.add(month.lower())

allMonths = baseMonths | lowerMonths

# Match dates in the range:
# - 1-9
# - 10-29
# - 30 or 31
dayPattern = '(?:(?:[1-2][0-9]?)|(?:[1-9])|(?:30|31))|' + re.escape('(illegible)') + '|' + re.escape('[illegible]')
# NOTE: Out-of-range days will be flagged during validation.
permissiveDayPattern = '(?:[1-2][0-9][0-9])|(?:[3][2-9])' 
monthPattern = '|'.join([re.escape(m) for m in allMonths])

# NOTE: 19 is probably wrong. It will fail validation later.
yearPattern = '(?:17|18|19)[0-9][0-9]'
# NOTE: A lot of 3-digit years... This makes the last digit optional
# NOTE: And a 5-digit one too!!!
permissiveYearPattern = f'(?:{yearPattern}?|(?:{yearPattern}[0-9]))'

ignoreThNd = 'th|nd|st|rd?\\.?'
anyWhitespace = '(?:\\s*)'

def capture(pattern):
    return f'({pattern})'

def namedCapture(name, pattern):
    return f'(?P<{name}>{pattern})'

def ignoreIfPresent(pattern):
    return f'(?:{pattern})?'

namedCapturePattern = re.compile('%s([a-z]*)%s' % (re.escape('P<'), re.escape('>')))
def removeNamedCaptures(pat):
    return re.sub(pattern=namedCapturePattern, repl=':', string=pat)

def removeSpecificNamedCapture(pat, name):
    return pat.replace(f'P<{name}>', ':')

dmPattern = anyWhitespace.join([
    namedCapture('day', dayPattern),
        ignoreIfPresent('th|nd|st|rd'),
        ignoreIfPresent('\\.'),
        ignoreIfPresent('of'),
    namedCapture('month', monthPattern),
        ignoreIfPresent('\\.|,'),
])

dmyPattern = anyWhitespace.join([
    dmPattern,
    namedCapture('year', permissiveYearPattern),
        ignoreIfPresent('\\.'),
])

mdyPattern = anyWhitespace.join([
    namedCapture('month', monthPattern),
        ignoreIfPresent('\\.'),
        ignoreIfPresent(','),
    namedCapture('day', dayPattern),
        ignoreIfPresent('th|nd|st|rd'),
        ignoreIfPresent('\\.'),
        ignoreIfPresent(','),
    namedCapture('year', permissiveYearPattern),
        ignoreIfPresent('\\.'),
])

# like mdyPattern, but allows typos like "June 126, 1883"
# currently, that's the only occurrence of that, but making a separate
# pattern lets use reuse the other parsing infrastructure we already have.
# NOTE: Out-of-range days will be flagged during validation.
mdyDayTypoPattern = anyWhitespace.join([
    namedCapture('month', monthPattern),
        ignoreIfPresent('\\.'),
        ignoreIfPresent(','),
    namedCapture('day', permissiveDayPattern),
        ignoreIfPresent('th|nd|st|rd'),
        ignoreIfPresent('\\.'),
        ignoreIfPresent(','),
    namedCapture('year', yearPattern),
        ignoreIfPresent('\\.'),
])

myPattern = anyWhitespace.join([
    namedCapture('month', monthPattern),
        ignoreIfPresent('\\.|,'),
    namedCapture('year', permissiveYearPattern),
        ignoreIfPresent('\\.'),
])

mdPattern = anyWhitespace.join([
    namedCapture('month', monthPattern),
        ignoreIfPresent('\\.|,'),
    namedCapture('day', dayPattern),
        ignoreIfPresent('th|nd|st|rd'),
        ignoreIfPresent('\\.'),
])

def fixYear(year):
    if year is None:
        return None
    return int(year)

def fixMonth(month):
    if month is None:
        return None

    # TODO: Flag as passthrough
    if month in missingDataMarkers:
        return None

    # convert to title case
    month = month[0].upper() + month[1:]

    if month in typoMonthMap:
        month = typoMonthMap[month]
    
    if month in monthMap:
        month = monthMap[month]

    return monthNumbers[month]

def fixDay(day):
    if day is None:
        return None
    
    # TODO: Flag as passthrough
    if day in missingDataMarkers:
        return None
    if day == 0:
        day = 1

    return int(day)


datePrefix = '|'.join([
    'Dicumnet dated',
    'Document dated',
    'Dicumnet dated',
    'Documented dated',
    'Letter dated', 
    re.escape('"Restored" on'),
    'illegally siezed in ',
])

# NOTE: The case of "30 July 183(?)" will be caught by this, but that
#       will be properly handled during validation.
uncertaintySuffix = '|'.join([re.escape(s) for s in [
    '(?)',
    '(??)',
    '(???)',
    '?',
    '??',
    '???',
    '? [sic]'
]])

extraDataMarkers = set()
def captureExtraData(name, pattern):
    extraDataMarkers.add(name)
    return namedCapture(name, pattern)

namedDatePrefix = captureExtraData('datePrefix', datePrefix)
namedUncertainty = captureExtraData('uncertaintyQ', uncertaintySuffix)
namedParenComment = captureExtraData('parenComment', '\\([\w ]+\\)')
namedParenRelaxedComment = captureExtraData('parenRelaxedComment', '\\(.+\\)')
namedParenRelaxedComment2 = captureExtraData('parenRelaxedComment2', '\\(.+\\)')
namedSemiComment = captureExtraData('semiComment', '; ([\w ]+) ')
rangeMarkerBetween = captureExtraData('between', 'Between')
rangeMarkerToDash = captureExtraData('to_dash', 'to|-')

dmyBracketedYearPattern = anyWhitespace.join([
    dmPattern,
    captureExtraData('bracketedYear', ''.join([
        re.escape('['),
        namedCapture('year', yearPattern),
        re.escape(']'),
    ]))
])

def dateMatcher(regex):
    return re.compile(f"^{namedDatePrefix}?{anyWhitespace}(?:{regex})\\s*{namedUncertainty}?$")

baseSingleDatePatterns = {
    (dmyPattern, ('day', 'month', 'year')),
    (mdyPattern, ('month', 'day', 'year')),
    (mdyDayTypoPattern, ('month', 'day', 'year')),
    (namedCapture('month', monthPattern), ('month', )),
    (myPattern, ('month', 'year')),
    (mdPattern, ('month', 'day')),
    (namedCapture('year', yearPattern), ('year', )),
    # Example: 15 April 1836 (arrived for adjudication)
    (f'{dmyPattern} {namedParenComment}', ('day', 'month', 'year',)),
    # Example: 10 December [1819]
    (dmyBracketedYearPattern, ('day', 'month', 'year')),
}

singleDatePatterns = [(dateMatcher(pat), fields) for pat, fields in baseSingleDatePatterns] + \
    [(dateMatcher("\\[%s\\]" % date), fields) for date, fields in baseSingleDatePatterns]

mdySimplePattern = ('(?:\\s+)'.join([
    capture(monthPattern),
    capture(dayPattern) + ',?',
    capture(yearPattern)
]))

# Common patterns of date fields that are composed of multiple actual dates.
def makeMultiDatePattern(md):
    whole, elem, fields = md
    return (dateMatcher(removeNamedCaptures(whole)), re.compile(elem), fields)

multiDatePatterns = [makeMultiDatePattern(md) for md in [
    # month-day-year separated with dots, slashes, commas, or just spaces
    (f'(?:{mdySimplePattern}\\.\\s*)+(?:{mdySimplePattern})\\.?', mdyPattern, ('month', 'day', 'year')),
    (f'(?:{mdyPattern}(?:,|\\/) )+(?:{mdyPattern})(?:,|\\/?)', mdyPattern, ('month', 'day', 'year')),
    (f'(?:{mdyPattern}) (?:{mdyPattern})', mdyPattern, ('month', 'day', 'year')),

    # day-month-year separated with commas or common conjunctions
    (f'(?:{dmyPattern}, )+(?:{dmyPattern})', dmyPattern, ('day', 'month', 'year')),
    (f'{dmyPattern} (?:and|&) {dmyPattern}', dmyPattern, ('day', 'month', 'year')),

    # a list of years
    (f'(?:{yearPattern}, )+(?:{yearPattern})', namedCapture('year', yearPattern), ('year',)),

    # month-day separated with common conjunctions
    (f'{mdPattern} (?:and|&) {mdPattern}', mdPattern, ('month', 'day')),
    (f'{mdPattern}, {mdPattern}', mdPattern, ('month', 'day')),

    # month-year separated with common conjunctions
    (f'{myPattern} (?:and|&) {myPattern}', myPattern, ('month', 'year')),
    (f'{myPattern}, {myPattern}', myPattern, ('month', 'year')),

    # TODO: to - handle as date range? This would be a massive edge case but technically this is not correct.
    (f'{dmyPattern} {rangeMarkerToDash} {dmyPattern}', dmyPattern, ('day', 'month', 'year')),
    (f'{rangeMarkerBetween} {dmyPattern} and {dmyPattern}', dmyPattern, ('day', 'month', 'year')),
    (f'{rangeMarkerBetween} {mdyPattern} and {mdyPattern}', mdyPattern, ('month', 'day', 'year')),
    (f'{yearPattern} {rangeMarkerToDash} {yearPattern}', namedCapture('year', yearPattern), ('year',)),

    (f'(?:{dmyPattern} {namedParenRelaxedComment}),? (?:{dmyPattern} {namedParenRelaxedComment2})', dmyPattern, ('day', 'month', 'year')),
    (f'(?:{mdyPattern}){namedSemiComment}(?:{mdyPattern})', mdyPattern, ('month', 'day', 'year')),
]]

# Common patterns of date fields that are composed of shorthand methods of
# writing multiple dates. Shorthand dates comprise of a variable part that is
# different for each date, and a fixed part that is the same for each date.
#
# The value captured by the named <FIXED> match group of the whole pattern
# is passed to the `felem` pattern, while the whole string is passed to the
# `velem` pattern.
def makeShorthandMultiDatePattern(md):
    whole, velem, vfields, ffields = md

    # Leave in the named captures for the fixed fields.
    for vf in vfields:
        whole = removeSpecificNamedCapture(whole, vf)

    return (dateMatcher(whole), re.compile(velem), vfields, ffields)

ignDaySuffix = ignoreIfPresent('th|nd|st|rd')

pairSeparatorPattern = '|'.join([
    # 'and' MUST have whitespace surrounding...
    '((\\s+)(and)(\\s+))',
    # but it's OK if '/', '&', and ',' do not.
    '((\\s*)(\\/|,|&)(\\s*))',
])

dayPairPattern = ''.join([capture(s) for s in [
    f'({dayPattern}){ignDaySuffix}',
    ignoreIfPresent(','),
    pairSeparatorPattern,
    f'({dayPattern}){ignDaySuffix}',
]])

yearSepPrefix = '((,\\s*)|(\\s+))(of\\s+)?'
dayPairAndSepPattern = f'{dayPairPattern}{yearSepPrefix}'

monthPairPattern = ''.join([capture(s) for s in [
    monthPattern,
    pairSeparatorPattern,
    monthPattern
]])

namedDayPattern = namedCapture('day', dayPattern)

shorthandMultiDatePatterns = [makeShorthandMultiDatePattern(smd) for smd in [
    # Example: "September 24, January 27, March 19 1848"
    (f'(?:{mdPattern},\\s*)+\\s*(?:{mdPattern}),?\\s*(?:(?P<year>{yearPattern}))',
        mdPattern, ('month', 'day'), ('year',)),
    # 17 Mar and 12 Jul 1855
    (f'({dmPattern})({pairSeparatorPattern})({dmPattern})({yearSepPrefix})(?P<year>{yearPattern})',
        dmPattern, ('day', 'month'), ('year',)),
    # Example: "March 30 & April 28, 1890"
    (f'(?:{mdPattern})(\\s*)(&|and)(\\s*)(?:{mdPattern}),?\\s*(?:(?P<year>{yearPattern}))',
        mdPattern, ('month', 'day'), ('year',)),
    # Example: "April 21, 22,23, 1888"
    (f'((?P<month>{monthPattern})\\s+)' \
        f'(({dayPattern}){ignDaySuffix},\\s*)+(({dayPattern}){ignDaySuffix}((,\\s*)|(\\s+)))(of\\s+)?' \
        f'(?P<year>{yearPattern})',
        # Capture just the day, pretty simple, just make sure whitespace or comma follows it.
        f'(?:{namedDayPattern}{ignDaySuffix})(?:\\s|,)',
        ('day',), ('month', 'year',)),
    # Example: "January 14/15,1888"
    # Example: "January 10 & 12, 1854"
    # Example: "February 9 and 10, 1876"
    (f'((?P<month>{monthPattern})(,?)\\s+)' +
        dayPairAndSepPattern +
        f'(?P<year>{yearPattern})(\\.?)',
        # Capture just the day, pretty simple, just make sure a separator of some form follows the date.
        f'(?:{namedDayPattern}{ignDaySuffix})(?:\\s|\\.|\\/|,)',
        ('day',), ('month', 'year',)),
    # Example: "Jul/Aug 1849"
    (f'{monthPairPattern}(\\s+)(?P<year>{yearPattern})',
        # Capture just the day, pretty simple, just make sure whitespace or comma follows it.
        namedCapture('month', monthPattern),
        ('month',), ('year',)),
    # Example: "10 & 18 Sept 1857"
    # Example: "29th/30th June 1829"
    (dayPairAndSepPattern +
        f'((?P<month>{monthPattern})(,?)\\s+)' \
        f'(?P<year>{yearPattern})(\\.?)',
        # Capture just the day, pretty simple, just make sure a separator of some form follows the date.
        f'(?:{namedDayPattern}{ignDaySuffix})(?:\\s|\\.|\\/|,)',
        ('day',), ('month', 'year',)),
]]

ommissionPattern = re.compile('|'.join([
    'Not given',
    'Unknown',
    'acquitted',
    'date not given',
    'no',
    'no date given',
    'not given',
    'not guilty',
    '_',
    'pending',
    'released',
    'requested',
    'Various',
    'Shortly thereafter',
    'Proposed arrangments for maintaining at a reduced cost the liberated african establishment',
    'Returned',
    re.escape('Flor de Mozambique acquitted; Fatte Mabruque/Emalada acquitted over confusion of name/"planks"; Esperança acquitted as no "sufficient cause of detention" could be found'),
    'Continuation of number 284 case reagerding the status of the bounty',
    '3 dates given p. 117',
    '"pending"',
    '"21st Week"',
    '^' + re.escape('(illegible)') + '$',
]))

# Sometimes cases are just a bit too odd for us to parse easily, making it
# easier to just reformat that case a little bit to make one of the parsers catch
# it.
rewrites = {
    # remove duplicate day ("11, 11" -> "11") declaration causing parse issue
    'April 1, 1847, February 5, 1846, March 11, 11, 1847, April 22, 1847': \
        'April 1, 1847, February 5, 1846, March 11, 1847, April 22, 1847',
    # massage into (MD)+Y pattern by removing "1861/" part.
    'April 17, 1861/ April 18, April 19, April 20, April 21, 1861': \
        'April 17, April 18, April 19, April 20, April 21, 1861',
    # massage into the Between ... and ... format without shorthand
    'Between April 17th and May 5th 1837': \
        'Between April 17th 1837 and May 5th 1837',
    # use consistent date format...
    'November 7,1833-6th nov 1834': \
        '7th November 1833 - 6th nov 1834',
    # transcriber meant to write a comma
    'November 11/1837': 'November 11, 1837',
    # transcription typos
    'February 23,1836c': 'February 23, 1836',
    'March 2, 1862/ April 5, 1862/ March 24, 1`862': 'March 2, 1862/ April 5, 1862/ March 24, 1862',
    'January 14,1837)': 'January 14,1837',
    # massage into easier format
    'January 20/28, 1885 and January 16, 1885': 'January 20,28,16 1885',
    'January 1, 1884 - June 30': '1 January 1884 to 30 June 1884',
    'Feburary 18, 28 and March 9, 1881': 'Feburary 18, February 28, March 9, 1881',
    'May, 24/ June 19, 1889.': 'May 24, June 19, 1889',
    'September 24 and 25': 'September 24 and September 25',
    'October 21st. Nov 1st, 8th 1846': 'October 21st, Nov 1st, Nov 8th, 1846',
    'November 18, 21 1864/ November 28, 1865': \
        'November 18, 1864. November 21, 1864. November 28, 1865',
    'April 26,1831/ Sept 3, Sept 7, Spet 8 1832. Nov 24,1832':
        'April 26, 1831. Sept 3, 1832. Sept 7, 1832. Spet 8 1832. Nov 24, 1832.',
    "April 14, 1841 ( 8 degrees 0' South, 12 degrees 40' East) / May 11, 1841.( 12 degrees 24' S, 13 degrees 20' E)":
        "14 April 1841 ( 8 degrees 0' South, 12 degrees 40' East) 11 May 1841 ( 12 degrees 24' S, 13 degrees 20' E)"
}

# And sometimes, we just need to hardcode the date since it's too hard
# to write a general pattern or the probability of that date format is
# too low to justify writing a general pattern.
hardcoded = {
    'July 14, 1845/ September 1844': [
        { 'year': 1845, 'month': 7, 'day': 14 },
        { 'year': 1844, 'month': 9 },
    ],
    'March and May 1834; 19 June 1834': [
        { 'year': 1834, 'month': 3 },
        { 'year': 1834, 'month': 5 },
        { 'year': 1834, 'month': 6, 'day': 19 },
    ],
    'July 1,1831,July 2 1832, June 1834 , aug 1834': [
        { 'year': 1831, 'month': 7, 'day': 1 },
        { 'year': 1832, 'month': 7, 'day': 2 },
        { 'year': 1834, 'month': 6 },
        { 'year': 1834, 'month': 8 },
    ],
}

hardcodedUncertain = {
    'December 1878 - January 6 , 1879': [
        { 'year': 1878, 'month': 12 },
        { 'year': 1879, 'month': 1, 'day': 6 }
    ],
    '22 January (?)': [
        { 'month': 1, 'day': 22 }
    ],
    'Aug 4(?) 1827': [
        { 'year': 1827, 'month': 8, 'day': 4 }
    ],
    'June? 11th 1837': [
        { 'year': 1837, 'month': 6, 'day': 11 }
    ],
    'August 29, last': [
        { 'month': 8, 'day': 29 }
    ],
    '8 May (?) 1835': [
        { 'year': 1835, 'month': 5, 'day': 8 }
    ],
    '26th May or June 1838': [
        { 'year': 1838, 'month': 5, 'day': 26 },
        { 'year': 1838, 'month': 6, 'day': 26 },
    ],
    '29 November 1822/23?': [
        { 'year': 1822, 'month': 11, 'day': 29 },
        { 'year': 1823, 'month': 11, 'day': 29 },
    ],
    '31 August 1819 [1820]': [
        { 'year': 1819, 'month': 8, 'day': 31 },
        { 'year': 1820, 'month': 8, 'day': 31 },
    ],
}

def access(match, fields, field, fixer):
    if field in fields:
        val = match.group(field)
        if fixer:
            return fixer(val)
        else:
            return val
    else:
        return None

def checkUncertain(pattern, match):
    for extra in extraDataMarkers:
        if extra in pattern.groupindex:
            if match.group(extra):
                return True
    return False

def parseDate(date):
    if isinstance(date, int):
        parsedDate = { 'year': date, 'month': None, 'day': None }
        return { 'dates': [parsedDate], 'passthrough': False }

    if date in rewrites:
        date = rewrites[date]

    # NOTE: Match early or else this matches the "Month" date pattern.
    if date == '(illegible)':
        return { 'dates': [], 'passthrough': True }

    for pat, fields in singleDatePatterns:
        match = pat.match(date)
        if not match:
            continue

        uncertain = checkUncertain(pat, match)

        parsedDate = {
            'year': access(match, fields, 'year', fixYear),
            'month': access(match, fields, 'month', fixMonth),
            'day': access(match, fields, 'day', fixDay),
        }

        return { 'dates': [parsedDate], 'passthrough': uncertain }

    for wholePat, elemPat, fields in multiDatePatterns:
        match = wholePat.match(date)
        if not match:
            continue

        uncertain = checkUncertain(wholePat, match)
        
        dates = []
        
        for m in re.finditer(elemPat, date):
            dates.append({
                'year': access(m, fields, 'year', fixYear),
                'month': access(m, fields, 'month', fixMonth),
                'day': access(m, fields, 'day', fixDay),
            })
        
        return { 'dates': dates, 'passthrough': uncertain }

    for wholePat, velemPat, vfields, ffields in shorthandMultiDatePatterns:
        match = wholePat.match(date)
        if not match:
            continue

        uncertain = checkUncertain(wholePat, match)

        dates = []

        defaults = {
            'year': None,
            'month': None,
            'day': None,
        }

        for field in ffields:
            try:
                defaults[field] = match.group(field)
            except IndexError:
                print(wholePat.groupindex)
                raise IndexError("Match group didn't contain field " + field)

        defaults['year'] = fixYear(defaults['year'])
        defaults['month'] = fixMonth(defaults['month'])
        defaults['day'] = fixDay(defaults['day'])

        for m in re.finditer(velemPat, date):
            try:
                unpacked = {
                    'year': access(m, vfields, 'year', fixYear),
                    'month': access(m, vfields, 'month', fixMonth),
                    'day': access(m, vfields, 'day', fixDay),
                }
            except IndexError:
                raise IndexError(f"Match group {velemPat.groupindex} didn't contain fields {vfields}")

            for field in ['year', 'month', 'day']:
                if unpacked[field] is None:
                    unpacked[field] = defaults[field]

            dates.append(unpacked)

        return { 'dates': dates, 'passthrough': uncertain }

    if ommissionPattern.match(date):
        return { 'dates': [], 'passthrough': True }
    elif date in hardcoded:
        return { 'dates': hardcoded[date], 'passthrough': False }
    elif date in hardcodedUncertain:
        return { 'dates': hardcodedUncertain[date], 'passthrough': True }
    else:
        return None

def validateDate(date, original):
    if date is None:
        return None

    problems = []
    year = date.get('year', None)
    month = date.get('month', None)
    day = date.get('day', None)

    if year is not None:
        if year < 1700 or year >= 1900:
            problems.append(f'validation failure: year {year} in date "{original}" is out of range. Please re-check against the HCA 35 originals.')
            year = None
    
    if month is not None:
        if month > 12 or month <= 0:
            problems.append(f'validation failure: month {month} in date "{original}" is out of range. Please re-check against the HCA 35 originals.')
            month = None
    
    if day is not None:
        if day > 31 or day <= 0:
            problems.append(f'validation failure: day {day} in date "{original}" is out of range. Please re-check against the HCA 35 originals.')
            day = None
        if month is not None and month == 4 or month == 6 or month == 9 or month == 11:
            if day is not None and day > 30:
                problems.append(f'validation failure: day {day} in date "{original}" is out of range for given month "{month}". Please re-check against the HCA 35 originals.')
                day = None
        if month is not None and month == 2:
            if day is not None and day > 28:
                problems.append(f'validation failure: day {day} in date "{original}" is out of range for given month "{month}". Please re-check against the HCA 35 originals.')
                day = None

    return { 'year': year, 'month': month, 'day': day }, problems

def validateResult(result, original):
    if result is None:
        return None, [f'date "{original}" was not understood']

    dates = []
    problems = []
    passthrough = result['passthrough']

    for date in result['dates']:
        newDate, newProblems = validateDate(date, original)
        dates.append(newDate)
        problems += newProblems

    if len(problems) != 0:
        passthrough = True

    verbatim = None
    if passthrough:
        verbatim = original
    
    return { 'dates': dates, 'verbatim': verbatim }, problems
