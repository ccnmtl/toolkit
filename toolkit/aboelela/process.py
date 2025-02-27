import csv
import re
from django.core.files.base import ContentFile


# Django File objects don't like to be opened and closed, so just keep them
# open and remember to close the files at the end of the processing.
def open_files(files):
    for file in files:
        file.open('r')
    return files


def close_files(files):
    for file in files:
        file.close()
    return files


def find_nth(haystack: str, needle: str, n: int) -> int:
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start


def sanitize(func, file):
    """
    Modify a file using the function provided.
    """
    file.open('r')
    body = file.read().decode('utf-8')
    file.open('w')
    file.write(func(body).encode('utf-8'))


def sanitizeIDs(file):
    """
    Sanitize the data from the ID file. Sanitization is file specific and
    likely needs to be refactored later for more general use
    """
    results = file.open('r').read().decode('utf-8')
    ids = csv.DictReader(results.splitlines())
    id_set = {}
    for id in ids:
        if id.get('UNI (ID)') and id['UNI (ID)'] == 'Item ID / Rev':
            i = 1
            key = 'Q1'
            while id.get(key):
                id_set[key] = id[key].split('/')[0].strip()
                i += 1
                key = f'Q{i}'
    return id_set


def highest_bloom_lvl(categories):
    """
    Pulls the highest bloom level and the topic category from the list of
    categories provided. There should not be more than one topic.
    """
    bloom = ''
    subcategory = ''
    for category in categories:
        if 'Bloom' in category:
            clean_cat = category.title()
            if clean_cat > bloom:
                bloom = clean_cat
        # Find the subcategory
        elif len(category) > len(subcategory):
            subcategory = category
    return bloom, subcategory


def extract_items(items, clean, count, verbose):
    for item in items:
        if item['Item #'].isnumeric():
            if verbose:
                print('Item #', item['Item #'])
            # Clean up the categories
            categories = [
                x.strip() for x in item['Categories'].split(',')]
            bloom, subcategory = highest_bloom_lvl(categories)

        # Drop unnecessary columns
        # Reformat category as "Bloom Level, Category/Subcategory"
        if subcategory != '' and bloom != '':
            short_bloom = bloom[
                re.search(r'.loom.{1,3}evel', bloom).start():]
            bloom_parts = short_bloom.split(' - ')
            bloom_parts[1] = re.sub(' ', '', bloom_parts[1])
            short_bloom = ' - '.join(bloom_parts)
            if verbose:
                print(item['ItemID'], '\t', short_bloom)
            short_cat = subcategory[find_nth(subcategory, '/', 2) + 1:]
            cat = ', '.join([short_bloom.title(), short_cat])
            clean[item['ItemID']] = cat
            if cat not in count:
                count[cat] = 2
            else:
                count[cat] += 2


def sanitizeItems(file, verbose):
    """
    Sanitize the data from the Items file. Sanitization if file specific and
    likely needs to be refactored later for more general use.
    """
    file = file.open('r')
    tables = ['Item #' + x for x in file.read().decode('utf-8').split('Item #')
              if len(x) > 0]
    if verbose:
        print('Tables Found:', len(tables))
    clean = {}
    count = {}

    for table in tables:
        items = csv.DictReader(table.splitlines())
        extract_items(items, clean, count, verbose)

    return clean, count


def get_file_ref(files: list, verbose: bool) -> dict:
    """
    Given a list of files, do some data sanitization. Returns a
    dictionary containing data about the files.
    """
    file_ref = {}

    for file in files:
        name = file.name
        if verbose:
            print(f' -- Sanitizing {name}...')
        sanitize(lambda x: re.sub(r'⁄', '/', x), file)
        if 'result' in name.lower():
            file_ref['item_dir'] = file
            sanitize(lambda x: ''.join(
                re.sub(r' ?[^\w\s\(\),/\-<>\*\?%]', '', x)), file)
        elif 'item' in name.lower():
            file_ref['items'] = file
            sanitize(lambda x: x[x.find('Item #'):], file)

    return file_ref


def accumulator(processed, results, items, item_dir, cat_count, verbose):
    """
    Collects processed data in the output file.
    """
    # Write the header
    header = ['UNI (ID)', 'Category', 'Max Score', 'Student Score',
              '% Correct']
    writer = csv.DictWriter(processed, fieldnames=header)
    writer.writeheader()

    for row in results:
        if row['UNI (ID)'] and row['UNI (ID)'] != 'Item ID / Rev':
            out_data = {}
            categories = {}

            # Iterate through the questions to get the category scores
            for key in item_dir:
                category = items[item_dir[key]]
                if category not in categories:
                    categories[category] = 0
                try:
                    categories[category] += int(row[f'{key} Pts'])
                except ValueError:
                    pass

            # Check for consistent category length
            if len(cat_count) != len(categories):
                if verbose:
                    print('Inconsistent category length for (',
                          row['UNI (ID)'], '\t', len(categories), ')')

            # Write the row to the file
            for category in categories:
                out_data['UNI (ID)'] = row['UNI (ID)']
                out_data['Category'] = category
                out_data['Max Score'] = cat_count[category]
                out_data['Student Score'] = categories[category]
                percentage = int(
                    categories[category] / cat_count[category] * 100)
                out_data['% Correct'] = f'{percentage}%'
                writer.writerow(out_data)


def process(files, verbose=True):
    file_ref = get_file_ref(files, verbose)

    # Sanitize Item data
    items, cat_count = sanitizeItems(file_ref['items'], verbose)
    if verbose:
        print('Number of Questions:', len(items))
        print('Category Count:', len(cat_count))

    # Sanitize the Results Data
    item_dir = sanitizeIDs(file_ref['item_dir'])
    results_file = file_ref['item_dir'].open('r').read().decode('utf-8')
    results = csv.DictReader(results_file.splitlines())
    if verbose:
        print('Item Directory:', item_dir)
        print('Item Directory Size:', len(item_dir))

    # Process the results into a new CSV
    processed = ContentFile('', name='processed.csv')
    processed.open('w')

    # Accumulate the data for each student
    accumulator(processed, results, items, item_dir, cat_count, verbose)

    # Files need to be closed for saftey
    close_files(files)
    # Returns a SINGLE compiled file from the processed data
    return processed
