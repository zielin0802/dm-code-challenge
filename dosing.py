import os, sys, getopt, pandas
from plotly.offline import plot

class Dosing:
    def __init__(self, ec_input_file_name, registry_input_file_name, output_file_name):
        self.output_file_name = output_file_name
        self.data_ec = self.load_input_file(ec_input_file_name)
        self.data_registry = self.load_input_file(registry_input_file_name)

    def load_input_file(self, input_file_name):
        return pandas.read_csv(input_file_name)

    def merge(self):
        return pandas.merge(self.data_registry[['ID', 'RID', 'USERID', 'VISCODE', 'SVDOSE']], 
                            self.data_ec[['ECSDSTXT', 'RID', 'VISCODE']], 
                            on=['RID', 'VISCODE'], 
                            how='left')

    def report_filter(self, data, viscode, svdose, ecsdstxt):
        return data[(data.VISCODE == viscode) 
                     & (data.SVDOSE == svdose) 
                     & (data.ECSDSTXT != ecsdstxt)]

    def graph_filter(self, svperf, viscode):
        return self.data_registry[(self.data_registry.SVPERF == svperf) & (self.data_registry.VISCODE != viscode)]

    def to_csv(self, data, output_file_dir):
        try:
            if (not os.path.isdir(output_file_dir)):
                os.mkdir(output_file_dir)
        except:
            print("Could not create directory " + output_file_dir)
            sys.exit(2)
        data.to_csv(output_file_dir + "/" + self.output_file_name, index = None, header = True)

def main(argv):
   usage = 'usase: dosing.py -v <viscode> -s <svdose> -e <ecsdstxt> -o <output directory>'
   viscode, svdose, ecsdstxt, output_file_dir = '', '', None, ''

   #get command line args
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

   #generate report
   dos = Dosing("t2_ec 20190619.csv", "t2_registry 20190619.csv", "results.csv")
   merge_result_data = dos.merge()
   filter_result_data = dos.report_filter(merge_result_data, viscode, svdose, ecsdstxt)
   dos.to_csv(filter_result_data, output_file_dir)

   #create graph
   filtered_graph_data = dos.graph_filter('Y', 'bl')
   fig = {
    'data': [{'labels': filtered_graph_data.VISCODE, 'type': 'pie'}],
    'layout': {'title': 'Viscodes from Registry'}
    
     }
   #print('rendering graph...')
   plot(fig)


if __name__ == "__main__":
   main(sys.argv[1:])





