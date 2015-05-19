#!/usr/bin/env python

#------------------------------------------
# information from the "prefilled form" URL should be pasted between the ''
# https://support.google.com/docs/answer/160000?hl=en
form_id = ''
form_fields = [ 'entry.',
                'entry.',
                'entry.']
#-------------------------------------------

import Tkinter
import tkFileDialog
import csv
import time
# for submitting to shortening services
import requests # http://docs.python-requests.org/en/latest/
import xml.etree.ElementTree as ET # in case we want to use psbe.co as a shortener

def tinyurl(payload):
    r = requests.get('http://tinyurl.com/api-create.php?url=https://docs.google.com/forms/d/' + form_id + '/viewform?', params=payload)
    short_url = r.text
    return short_url

def psbe(payload):
    r = requests.get('http://psbe.co/API.asmx/CreateUrl?real_url=https://docs.google.com/forms/d/' + form_id + '/viewform?', params=payload)
    r = requests.get(post_this)
    root = ET.fromstring(r.text)
    #id = root[0].text
    #clicks = root[1].text
    #real_url = root[2].text
    short_url = root[3].text
    #create_date = root[4].text
    #created_by = root[5].text
    return short_url

def write_row(row):
    for entry in row:
        new_file.write(entry)
        new_file.write(',')

# ask the user for the CSV file of interest
Tkinter.Tk().withdraw() # so the Tk window doesn't show
csv_file = tkFileDialog.askopenfile(mode='rb', title='Select the CSV file', filetypes=[('CSV Files', '*.csv')])
read_this = csv.reader(csv_file)

# start a new CSV file, this will show up in the same directory as the script
new_file_name = 'with_short_URLs_' + time.strftime('%Y-%m-%d_%H%M%S') + '.csv'
new_file = open(new_file_name, 'w') # open the file for writing

for row_index, row in enumerate(read_this):
    payload = {} # initialize an empty dictionary
    if row_index == 0:
        print 'header row'
        write_row(row)
        new_file.write('URL\n')
    else:
        write_row(row)
        for entry_index, entry in enumerate(row): # add values to the dictionary
            if entry_index <= len(form_fields)-1: # only parse through the number of columns that corresponds to the number of form fields
                payload[form_fields[entry_index]] = row[entry_index] # take the nth form_field and match it to the nth row entry
        shortened_url = tinyurl(payload) # call the function, either tinyurl or psbe
        new_file.write(shortened_url)
        new_file.write('\n') # write the newline character
        print row_index, email, shortened_url # in case anyone is watching the output
        time.sleep(0.5) # optional, so we don't hit rate limits or bandwidth limits

# close the files
csv_file.close()
new_file.close()

print '' # display a blank line
raw_input('Done. You can close this window now.') # using this as a pause before close :)
