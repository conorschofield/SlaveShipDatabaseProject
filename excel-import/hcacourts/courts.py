from collections import Counter
import courtData

courtRewriteGroups = {
    (None, None): {
        'various': {},
        'Unlisted': {},
        'not given': {},
        'Unknown': {},
        'High Court of Admiralty': {},
        'High Court of the Admiralty': {},
    },
    ('Sierra Leone', None): {
        "Sierra Leone": {},
        "Sierre Leone": {},
        "sierra Leone": {},
        "Sierra Lenoe": {},
        "Seirra Leone": {},
        "sierra Leone": {},
        "SIerra Leone": {},
        "[Sierra Leone]": {},
        "Sierra eonne": {},
        "Sierra eone": {},
    },
    ('Sierra Leone', 'Vice Admiralty Court'): {
        'Vice Admiralty Court at Sierra Leone': {},
        'Vice Admiralty of Sierra Leone': {},
    },
    ('Sierra Leone', 'Yes'): {
        "Mixed Comission Courts of Sierra Leone": {},
    },
    ('Sierra Leone', 'Yes, British and Spanish'): {
        "British & Spanish Mixed Comission Court at Sierra Leone": {},
        "Briish & Spanish Mixed Comission Court at Sierra Leone": {},
        "British Spanish Mixed Comission Court at Sierra Leone": {},
        "British Spanish Court of Mixed Comission at Sierra Leone": {},
        "British & Spanish Mixed Comissin Court at Sierra Leone": {},
    },
    ('Sierra Leone', 'Yes, British and Portuguese'): {
        "British & Protuguese Mixed Comission Court at Sierra Leone": {},
        "British & Portuguese Mixed Comission Court at Sierra Leone": {},
        "British & Portuguese Mixed Comission Courtat Sierra Leone": {},
    },
    ('Sierra Leone', 'Yes, British and Brazilian'): {
        "British & Brazillian Mixed Comission Court at Sierra Leone": {},
    },
    ('Sierra Leone', 'Yes, British, Spanish, and Portuguese'): {
        "British & Spanish & Portuguese Mixed Comission Courts at Sierra Leone": {},
    },
    ('Saint Helena', None): {
        'Saint Helena': {},
        "St. Helena": {},
        "St. elena": {},
        "st. Helena": {},
        "St Helena": {},
        "St. elena": {},
    },
    ('Havana', None): {
        "Havana": {},
        "Havanna": {},
        "Havannah": {},
    },
    ('Havana', 'Yes, British and Spanish'): {
        "British Spanish? Mixed Comission Court at Havana": {},
        "British & Spanish Mixed Comission Court at Havana (that Island)?": {},
        "British & Spanish Mixed Comission Court at Havana": {},
        'British Spanish Mixed Comission Court in Cuba': {},
        'British & Spanish Mixed Comission Court (likely at Havana)': { 'uncertain': True },
    },
    ('Rio de Janeiro', None): {
        "Rio de Janeiro": {},
        "Rio de Janiero": {},
        "Rio de janeiro": {},
        "Rio De Janeiro": {},
        "Rio De Janiero": {},
        "rio De Janeiro": {},
        "rio de Janeiro": {},
    },
    ('Rio de Janeiro', 'Yes, British and Brazilian'): {
        "British Brazillain Mixed Comission Court at Rio de Janeiro": {},
        "British & Brazillian Mixed Comission Court at Rioi de Janeiro": {},
        "British & Brazillian Mixed Comission Court at Rio de Janeiro": {},
    },
    ("Saint Christopher's", None): {
        "St. Christopher": {},
        "St. Christophers": {},
        "St. Chrstophers": {},
        "St. Chrstopher": {},
        "St. Chistophers": {},
        "St. Chrisophers": {},
        "St.Christophers": {},
    },
    ('Cape of Good Hope', None): {
        "Cape of Good Hope": {},
        "Cape of Good Hope.": {},
        "Cape of good Hope": {},
        "Cape of Good hope": {},
        "Cape of Goode Hope": {},
    },
    (None, 'Yes, British and Spanish'): {
        'British Spanish Mixed Comission Court': {},
        'British Spanish Mixed Comission Court at ____': {},
        'British & Spanish Court of Justice': {},
        'British & Spanish mixed Comission Court': {},
        'British & Spanish Mixed Comission Court': {},
        'British Spanish Court of Mixed Comission': {},
    },
    (None, 'Yes, British and Brazilian'): {
        'British & Brazillian Mixed Comission Court': {},
    },
    (None, 'Yes, British and Portuguese'): {
        'British & Protuguese Mixed Comission Court': {},
        '"British-Portuguese Commission Court"': {},
        'British & Portuguese Mixed Comission Court': {},
    },
    ('Mauritius', None): {
        'Mauritius': {},
        "Mauritus": {},
        "Maurititus": {}, 
    },
    ('Trinidad', None): {
        'Trinidad': {},
        'Trinida': {},
    },
    ('Gibraltar', None): {
        'Gibraltar': 'Gibraltar',
        "Gibraltor": {},
    },
    ('Nassau', None): {
        'Nassau': {},
        "Nassau, Bahamas": {},
        "Nassua, Bahamas": {},
    },
    ('Bermuda', None): {
        'Bermuda': {},
        'Bermuda, Bahamas': {},
    },
    ('Puerto Rico', None): {
        'Porto Rico': {},
        'Puerto Rico': {},
    },
    ('Barbados', None): {
        'Barbados': {},
        'Barbadoes': {},
    },
    (None, 'Vice Admiralty Court'): {
        'Vice Admiralty': {},
        'Vice Admiralty Court': {},
    },
    (None, 'Admiralty Court'): {
        'Admiralty Court': {},
        'Admrialty Court': {},
    },
    ('Saint Lucia', None): {
        "Saint Lucia": {},
        "St. Lucia": {},
        "St.Lucia": {},
    },
    ('Genoa', None): {
        "Genoa": {},
        "Port of Genoa": {},
    }
}

mixedCommissionRewriteGroups = {
    (None, 'N/A'): {
        'N/A': {},
        # Used for Treasury reports. Not a real court.
        'some': {},
    },
    # Redundant
    (None, None): {
        'High Court of Admiralty': {},
    },
    # Definitive yes/no without further detail
    (None, 'No'): {
        'No': {},
        'no': {},
        'No(?)': { 'uncertain': True },
    },
    (None, 'Yes'): {
        'Yes': {},
        'yes': {},
        'yes?': { 'uncertain': True },
        'Mixed Commisions': {},
        'British Mixed Commisions Court': {},
        'British Mixed commisions court': {},
        'British Mixed Commision Court': {},
        'British Mixed Commisions': {},
        'Briish Mixed Commisions Court': {},
    },
    ('Sierra Leone', 'Yes'): {
        'yes, Sierra Leone Mixed Commisions': {},
    },
    ('Cape of Good Hope', 'Yes'): {
        'yes, Cape of Good Hope': {},
    },
    # Definitive yes, with further detail
    (None, 'Yes, British and Spanish'): {
        'yes, Spanish': {},
        'British and Spanish Mixed Commisions Court': {},
        'yes, British and Spanish': {},
        'yes, English/Spanish': {},
        'Yes, Spanish': {},
        'British and Spanish Mixed Commisions court': {},
        'yes Spanish': {},
        'Yes, British and Spanish Mixed Commisions Court': {},
        'Yes, British/Spanish': {},
        'British and Spanish Mixed commisions': {},
        'Yes; Spanish': {},
        'Yes, English/Spanish': {},
        'yes British/Spanish': {},
        'British and Spanish Mixed Commisions Courft': {},
        'British and Spanish Mixed commisions court': {},
        'British and Spanish Mixed Commision Court': {},
        'British and Spanish Mixed commisions Court': {},
        'Spanish & British Mixed Commisions': {},
        'British and Spanish Mixed Commisions': {},
        'British and Spanish': {},
        'yes, Spanish and British': {},
        'Yes, British and Spanish': {},
        'Yes, British and Spanish Mixed Commisions court': {},
        'Yes; Spanish(?)': { 'uncertain': True },
    },
    (None, 'Yes, British and Portuguese'): {
        'yes, Portuguese': {},
        'British and Portuguese Mixed Commisions Court': {},
        'yes Portuguese': {},
        'Yes, British/Portuguese': {},
        'British and Portuguese Mixed commisions Court': {},
        'British and Portuguese Mixed Commision Court': {},
        'yes, British and Portuguese': {},
        'British and Portuguese Mixed commision Court': {},
        'Yes, Portuguese': {},
        'British and Portuguese  Mixed commisions': {},
        'yes, English/Portugese': {},
        'Yes, Portugese': {},
        'British and Portuguese Mixed commisions court': {},
        'Yes, English/Portuguese': {},
        'yes, Portugual': {},
        'yes, English/Portuguese': {},
        'British and Portuguese Mixed Commisions': {},
        'British and Portuguese mixed commisions court': {},
        'Yes, British and Portuguese Mixed Commisions Court': {},
        'Yes, British and Portuguese Mixed Commisions court': {},
        'Portugal': {},
        'yes British/Portuguese': {},
        'yes? Portuguese': {'uncertain': True},
        'yes, British and Portuguese Mixed Commisions Court': {},
        'Yes, British and Portuguese Court of Mixed Commisions': {},
        'Portuguese': {},
    },
    ('Sierra Leone', 'Yes, British and Portuguese'): {
        'Yes, British Portuguese  Mixed commisions court Sierra Leone': {},
    },
    (None, 'Yes, British and Brazilian'): {
        'British and Brazilian Mixed Commisions Court': {},
        'yes, Brazilian': {},
        'yes, British and Brazillian': {},
        'yes, Brazil': {},
        'British and Brazilian Mixed commisions court': {},
        'Yes, Brazilian': {},
        'British and Brazilian Mixed commisions Court': {},
        'Yes, British and Brazilian Mixed Commisions Court': {},
        'yes, English/Brazilian': {},
        'Yes, British and Brazilian Court of Mixed Commisions': {},
        'Yes, British and Brazilian Mixed Commisions Court.': {},
        'British and Brazilian Mixed Commisions court': {},
        'Yes; Brazilian': {},
        'British and Brazlian Mixed commisions court': {},
        'British and Brazilian Mixed commisions': {},
    },
    ('Rio de Janiero', 'Yes, British and Brazilian'): {
        'yes, Brtish and Brazilian mixed commisions court at Rio De Janiero': {},
    },
    ('Sierra Leone', 'Yes, British and Brazilian'): {
        'Yes, British Brazialian Mixed commisions court Sierra Leone': {},
    },
    (None, 'Yes, British and Dutch'): {
        'yes, Dutch': {},
        'yes Dutch': {},
        'British and Netherlands Mixed Commision court': {},
        'Yes, British/Netherlands': {},
        'British and Netherlands Mixed commisions court': {},
        'Yes, English/Netherlands': {},
        'yes British/Dutch': {},
    },
    (None, 'Yes, British and French'): {
        'Yes, French': {},
        'French': {},
        'France': {},
        'British and French Mixed Commisions Court': {},
    },
    ('Egypt', 'Yes, British and Egyptian'): {
        'Yes - Egypt': {},
    },
    # TODO: Are these mixed commission courts?
    (None, 'Vice Admiralty Court'): {
        'British Vice Admiralty Court': {},
        'Vice Admiralty Court': {},
        'British vice Admiralty Court': {},
        'British Vice Admiralty court': {},
        'Vice Admiralty': {},
        'Vice-Admiralty': {},
        'yes, Britsh Vice Admiralty court': {},
        'Yes, British Vice Admiralty Court': {},
        'Court of Vice Admirality': {},
        'Vice Admiralty court': {},
        'Vice Admirality Court': {},
        'YEs, British Vice Admiralty Court': {},
    },
    ('St. Helena', 'Vice Admiralty Court'): {
        'Yes, Vice Admiralty Court  St. Helena': {},
        'yes, Vice Admiralty court St. Helena': {},
        'yes, Vice Admiralty Court, St. Helena': {},
    },
    ('Sierra Leone', 'Vice Admiralty Court'): {
        'Yes, Vice Admiralty Court Sierra Leone': {},
        'yes, Vice Admiralty Court, Sierra Leone': {},
        'Vice Admiralty, Sierra Leone': {},
    },
    ('Cape of Good Hope', 'Vice Admiralty Court'): {
        'Yes, Vice Admiralty court, Cape of Good Hope': {},
        'Yes, Vice Admiralty Court Cape of Good Hope': {},
        'Vice Admiralty, Cape of Good Hope': {},
    },
    ('New Providence', 'Vice Admiralty Court'): {
        'Vice Admirality Court of New Providence': {},
    },
    ('Mauritius', 'Vice Admiralty Court'): {
        'yes, Vice Admiralty Mauritius': {},
    },
    ('Barbados', 'Vice Admiralty Court'): {
        'Yes, Vice Admiralty Court Barbadoes': {},
    },
    (None, 'British Customs House'): {
        'British Customs House': {},
        'Custom House': {},
        'Customs House': {},
        'British custom House': {},
    },
    (None, 'British and United States'): {
        'British and United Stated Mixed Commisions Court': {},
    },
    (None, 'British Liberated African Department'): {
        'British Liberated African Department': {},
        'British Liberated African department': {},
    },
    (None, 'British Vice Counsel at Bremen'): {
        'Britsh Vice Counsel at Bremen': {},
    },
}

def makeRewrites(grouped):
    rewrites = {}
    for court, mixed in grouped:
        group = grouped[(court, mixed)]
        for member in group:
            data = group[member]
            rewrites[member] = (court, mixed)
    return rewrites

def rewriteCounts(rewrites, data):
    rewrittenCourts = Counter()
    missedCourts = Counter()
    for court in data:
        count = data[court]
        if court in rewrites:
            rewrittenCourts[rewrites[court]] += count
        elif court is not None:
            missedCourts[court] += count
    return rewrittenCourts, missedCourts

def printCounts(counts):
    for court in counts:
        count = counts[court]
        print('% 5d %s' % (count, court))

def go(groups, data):
    rewrites = makeRewrites(groups)
    rewrittenCourts, missedCourts = rewriteCounts(rewrites, data)
    print('Rewritten:')
    printCounts(rewrittenCourts)
    print('Missed:')
    printCounts(missedCourts)

def makeXlsx(filename):
    from openpyxl import Workbook

    out_wb = Workbook(write_only=True)

    col_widths = [
        ('A', 65),
        ('B', 35),
        ('C', 35),
    ]

    candidates = [
        ("Court", "Mixed", courtRewriteGroups, lambda oc, nc, nm: oc == nc and nm is None),
        ("Mixed", "Court", mixedCommissionRewriteGroups, lambda om, nc, nm: om == nm and nc is None),
    ]

    for (name, other, groups, is_no_op) in candidates:
        out_ws = out_wb.create_sheet(f'{name}')

        for (col, width) in col_widths:
            out_ws.column_dimensions[col].width = width

        out_ws.append([
            "",
            f"(If the Court or Mixed replacements are blank, replacements from {other} will also be considered before erasing.)",
            "",
        ])

        out_ws.append([
            f"When I see this value in the {name} column...",
            "Replace Court with:",
            "Replace Mixed with:"
        ])

        rewrites = makeRewrites(groups)
        for original in rewrites:
            (nCourt, nMixed) = rewrites[original]
            if (is_no_op(original, nCourt, nMixed)):
                continue
            if nCourt is None:
                nCourt = ""
            if nMixed is None:
                nMixed = ""
            out_ws.append([original, nCourt, nMixed])
    
    out_wb.save(filename)

makeXlsx("HCA Court Rewrites.xlsx")

#go(mixedCommissionRewriteGroups, courtData.mixed)
#go(courtRewriteGroups, courtData.courts)
