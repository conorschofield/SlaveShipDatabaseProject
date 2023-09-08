import os
import re

optionalDashP = '(?:-?)'
hca35P = f'HCA{optionalDashP}35-'
volumeNumberP = '(?P<volume_number>\d+)'
pageNumbersP = '(?P<page_numbers>(-(?:\d+))+)'
disambiguatorP = '(?P<disambiguator>-copy(\d*))?'

volumeNameP = re.compile(f'{hca35P}{volumeNumberP}')
imageNameP = re.compile(f'{hca35P}{volumeNumberP}{pageNumbersP}{disambiguatorP}.JPG')

def generateConcordance(basePath):
    records = []

    for volume in os.listdir(basePath):
        volPath = f'{basePath}/{volume}'
        volumeNumber = int(volumeNameP.match(volume).group('volume_number'))

        groups = {}

        for image in os.listdir(volPath):
            if image.startswith('DSC'):
                continue

            imageMatch = imageNameP.match(image)
            if imageMatch is None:
                print(f'Skipping {image} as it does not conform to our pattern')
                continue

            imageVolNum = int(imageMatch.group('volume_number'))
            if imageVolNum != volumeNumber:
                print(f'Skipping {image} as it is in the directory for volume {volumeNumber}')
                continue

            imagePath = f'{volPath}/{image}'
            fileSize = os.path.getsize(imagePath)

            pageNumbersS = imageMatch.group('page_numbers')
            pageNumbers = tuple([int(pn) for pn in pageNumbersS.split('-') if pn])
            disambiguator = imageMatch.group('disambiguator')

            if len(pageNumbers) > 2:
                print(f'Skipping {image} as it contains more than two pages. Please crop the image into multiple smaller images.')
                continue
            elif len(pageNumbers) == 2 and pageNumbers[0] + 1 != pageNumbers[1]:
                raise ValueError(f'The file name {image} does not specify page numbers in increasing order.')

            # By taking the size in bytes of the image and dividing it by
            # the number of pages the bytes are "spread over", we can get
            # a scuffed estimate of how much detail a given image contains
            # of a given page. This provides a way to pick a single image to
            # represent a page if needed.
            fileSizeWeight = int(fileSize / len(pageNumbers))

            path = f'{volume}/{image}'
            groups.setdefault(pageNumbers, []).append((path, fileSizeWeight))

        # Pick a single image per given page range.
        for pageRange in groups:
            options = groups[pageRange]
            # Pick the option with the highest weight
            best = max(options, key=lambda tup: tup[1])
            path = best[0]
            fileSizeWeight = best[1]

            if len(pageRange) == 2:
                records.append((volumeNumber, pageRange[0], path, fileSizeWeight, pageRange[1]))
                records.append((volumeNumber, pageRange[1], path, fileSizeWeight, pageRange[0]))
            else:
                records.append((volumeNumber, pageRange[0], path, fileSizeWeight, pageRange[0]))

    def recordKey(record):
        (volumeNumber, pageNumber, path, fileSizeWeight, otherPageNumber) = record
        return (volumeNumber, pageNumber)

    records.sort(key=recordKey)

    return records

