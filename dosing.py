import os, sys, getopt, pandas

def report_csv(viscode, svdose, ecsdstxt, output_file_dir):
    ec_input_file_name = "t2_ec 20190619.csv"
    registry_input_file_name = "t2_registry 20190619.csv"
    output_file_name = "results.csv"

    #Read the following files into a dataframe
    data_ec = pandas.read_csv(ec_input_file_name)
    data_registry = pandas.read_csv(registry_input_file_name)

    #Merge the dataframes:
    merge_result_data = pandas.merge(data_registry[['ID', 'RID', 'USERID', 'VISCODE', 'SVDOSE']], 
                            data_ec[['ECSDSTXT', 'RID', 'VISCODE']], 
                            on=['RID', 'VISCODE'], 
                            how='left')

    #Filter records where:
    merge_result_data = merge_result_data[(merge_result_data.VISCODE == viscode) 
                                          & (merge_result_data.SVDOSE == svdose) 
                                          & (merge_result_data.ECSDSTXT != ecsdstxt)]
    
    #Create and output a .csv file of the filtered records:
    try:
        if (not os.path.isdir(output_file_dir)):
            os.mkdir(output_file_dir)
    except:
        print("Could not create directory " + output_file_dir)
        sys.exit(2)
    merge_result_data.to_csv(output_file_dir + "/" + output_file_name, index = None, header = True)

    #print(merge_result_data.head())

def main(argv):
   usage = 'dosing.py -v <viscode> -s <svdose> -e <ecsdstxt> -o <output directory>'
   viscode, svdose, ecsdstxt, outputfile = '', '', None, ''
   try:
      opts, args = getopt.getopt(argv,"hv:s:e:o:",["viscode=", "svdose=", "ecsdstxt=", "odir="])
   except getopt.GetoptError:
      print(usage)
      sys.exit(2)

   for opt, arg in opts:
      if opt == '-h':
         print(usage)
         sys.exit()
      elif opt in ("-v", "--viscode"):
        viscode = arg
      elif opt in ("-s", "--svdose"):
        svdose = arg
      elif opt in ("-e", "--ecsdstxt"):
        try:
            ecsdstxt = int(arg)
        except:
            ecsdstxt = None
      elif opt in ("-o", "--odir"):
        output_file_dir = arg

   report_csv(viscode, svdose, ecsdstxt, output_file_dir)

if __name__ == "__main__":
   main(sys.argv[1:])





