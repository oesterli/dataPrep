###
### My utilitis

# imports
import datetime
import os


# ------------
# opening file in read mode
def inspect_file(file, mode, en_type):
    """
    This function opens a file specified as input and prints it.
    Return value str.
    """
    with open(file, mode, encoding=en_type) as f:
        my_file = f.read()
    #print('Done')   
    #print(my_file)
    
    return my_file

#'./data/ASCII.dat', 'r'
#inspect_file('./data/ASCII.dat', 'r', None)



# ------------
# Logging

#import datetime

def logger(text):
    '''
    This function write a message to stdout and file
    '''
    
    # define current date and time
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    
    # print date, time and message to stdout
    print(now, text, sep=';')
    
    # write date, time and message to file
    with open('log.txt', 'a') as f:
        print(now, text, sep=';', file=f)
    return   
    

# ------------
# Logging

#import datetime

def logger_2(text, fname='log'):
    '''
    This function write a message to stdout and file.
    Extension to function logger()
    
    text: message to be written
    fname=: filename of the log file
    
    Example:
    [in] logger('hallo_4', fname='test_log')
    [out] 2020-11-09_22:33:36;hallo_4
    file: test_log_2020-11-09.txt
    
    '''
    
    # define current date and time
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    
    # write date, time and message to file
    
    filenow = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = fname + '_' + filenow + '.txt'
    
    with open(filename, 'a') as f:
        print(now, text, sep=';', file=f)
    
        
    # print date, time and message to stdout
    print(now, text, filename)
    return



# ------------
# Logging

#import datetime
#import os

def logger_3(text, fname='log', fpath='./data/output/'):
    '''
    This function write a message to stdout and file.
    Extension to function logger()
    
    text: message to be written
    fname=: filename of the log file
    
    Example:
    [in] logger('hallo_4', fname='test_log')
    [out] 2020-11-09_22:33:36;hallo_4
    file: test_log_2020-11-09.txt
    
    '''
    
    # define current date and time
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    
    # write date, time and message to file
    filenow = datetime.datetime.now().strftime('%Y-%m-%d')
    filepath = fpath
    filename = fname + '_' + filenow + '.txt'
    log_file = os.path.join(filepath, filename)
    
    with open(log_file, 'a') as f:
        print(now, text, sep=';', file=f)
    
        
    # print date, time and message to stdout
    print(now, text, log_file)
    return


# ------------
# Exporting data

def exporter(data, fname, out_dir, now, run_num):
    '''
    Exports data to a given output location
    
    Parameter:
    data: DataFrame to be exportet
    fname: Name of the export file
    out_dir: Directory where to export the file
    now: Date defined
    run_num: Number of the current run
    '''
    in_file = '_'.join([fname, str(now), str(run_num).zfill(2),]) +'.csv'
    out_path = os.path.join(out_dir, in_file)
    data.to_csv(out_path,index=None)
    
    bh_raw_file = '_'.join(['bh_raw', str(now), str(run_num).zfill(2),]) +'.csv'
    bh_raw_path = os.path.join(out_dir_run,bh_raw_file)
    all_data_sorted.to_csv(bh_raw_path,index=None)

# ------------
# Test function
def test():
    '''
    Add Doc-string
    '''
    print('hello!')
    return