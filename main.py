import pandas as pd
import numpy as np
import openpyxl
import time
import sys
from pathlib import Path

import utils.fixed_BOM
import utils.summary

# show the timelapse
def show_timelapse(start_time, end_time):
    print("----- Total Timelapse in %s seconds -----" % (end_time - start_time))
    
# main CLI function
def main():
    path = input(r"Enter the path to the file: ") # User enters their file path
    if not Path(path).exists():
        raise FileNotFoundError("Invalid file path: File not found")
    results = None # initialize results
    # Ask the user if they want scraped results and warns them the quotation procress may take longer as a result
    while True:
        print("-----------------------------------------------------------------------")
        scrape_prompt = str(input("Would you like to receive scraped results? y|n: "))
        time.sleep(1)
        
        if scrape_prompt == 'y': 
            # user answers 'yes' then print the warning
            print("\nYou answered YES. Please note that this feature is still in beta and may not be available in this version.")
            print("Choosing this option can extend the process up to 30 minutes or more due to the additional time required. Use caution when using the BOM Quoter with web scraping.")
            print("\nTo continue to receive scraped results enter 'y'. For quicker processing enter 'n'.")
            
            while True:
                # loop over prompt to continue
                print("-----------------------------------------------------------------------")
                scrape_confirm = str(input("Would you like to continue with web scraping? y|n: "))
                if scrape_confirm == 'y':
                    # FIXME: get results with scraping
                    # start = time.time() # get start time
                    # results = utils.fixed_BOM.scrape_saved(path)
                    # end = time.time() # get end time
                    # break
                    print("\nRetrieving scraped results is current unavailable. Please enter 'n' to continue:")
                    continue
                elif scrape_confirm == 'n':
                    start = time.time()
                    try:
                        results = utils.fixed_BOM.df_result_without_scraping(path) # get results without scraping (APIs only)
                    except Exception as err:
                        raise Exception ("Unable to get data:", str(err))
                    end = time.time()
                    break
                else:
                    # if the user inputs an answer besides 'y' or 'n' as instructed, make them do it again
                    print("\nInvalid answer. Enter 'y' for scraped results or 'n' for faster processing:")
                    continue # go back to the beginning of the inner loop
            break # break out of the outer for loop
        elif scrape_prompt == 'n':
            print("\nYou answered NO. Continuing without web scraping..")
            start = time.time() # get start time
            results = utils.fixed_BOM.df_result_without_scraping(path)
            end = time.time() # get end time
            break # break out of the outer for loop 
        else:
            print("Invalid answer. Enter 'y' for scraped results or 'n' for faster processing:")
            continue
    if results is None:
        raise RuntimeError("Was not able to get results. Please try again.")
    utils.fixed_BOM.save_RFQ_BOM(path, results)
    utils.summary.save_summary(path)
    print("\nBOM Quotation completed! Results were stylized and saved in the original file.")
    show_timelapse(start, end)
    

if __name__ in "__main__":
    main()
