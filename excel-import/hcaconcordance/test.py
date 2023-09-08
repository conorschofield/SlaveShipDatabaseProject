from concordance import generateConcordance

from sys import argv, exit

if len(argv) < 2:
    print("Usage: test.py <case image directory>")
    exit(-1)

records = generateConcordance(argv[1])

for (volumeNumber, pageNumber, path, fileSizeWeight, otherPageNumber) in records:
    print(f'volume={volumeNumber}, pageNumber={pageNumber}, path={path}, weight={fileSizeWeight}, otherPageNumber={otherPageNumber}')

def fillInRange(volume, start, end):
    # with narrowedRecords as (select pageNumber, path, weight, otherPageNumber from images where volume=%d and page>=%d and page<=%d)
    groupedRecords = {}
    for record in records:
        (volumeNumber, pageNumber, path, weight, otherPageNumber) = record
        if volumeNumber != volume:
            continue
        if pageNumber >= start and pageNumber <= end:
            groupedRecords.setdefault(pageNumber, []).append((path, weight, otherPageNumber))
    
    print(groupedRecords)

    coveredUnique = set()
    pages = set()

    # with uniqueRecords as (select pageNumber, path, weight, otherPageNumber from narrowedRecords group by pageNumber having count(pageNumber) == 1)
    # with uniquePages as (select min(pageNumber, otherPageNumber) as start, max(pageNumber, otherPageNumber) as end from uniqueRecords)
    # with coveredUnique as ((select pageNumber from uniquePages) union (select otherPageNumber from uniquePages))
    for pageNumber in groupedRecords:
        candidates = groupedRecords[pageNumber]
        if len(candidates) == 1:
            (path, weight, otherPageNumber) = candidates[0]
            coveredUnique.add(pageNumber)
            coveredUnique.add(otherPageNumber)
            pages.add((min(pageNumber, otherPageNumber), max(pageNumber, otherPageNumber), path))

    # with neededPages as (select pageNumber from narrowedRecords where pageNumber not in coveredUnique)
    needed = groupedRecords.keys() - coveredUnique
    singles = []

    print(pages)
    print(needed)

    # with 
    for pageNumber in needed:
        candidates = groupedRecords[pageNumber]
        selected = max(candidates, key=lambda candidate: candidate[1])
        selectedPath = selected[0]
        pages.add((pageNumber, pageNumber, selectedPath))
        print(selectedPath)

    print(coveredUnique)

    pages = sorted(pages, key=lambda page: page[0])

    for selected in pages:
        print(selected)

fillInRange(1, 365, 379)
