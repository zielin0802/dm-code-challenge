import getopt, os, pandas, sys
import plotly.graph_objs as go
from plotly.offline import plot

class Dosing:
    output_file_name = ""

    #raw data frames
    ec_df = None
    registry_df = None

    #report data frames
    merged_df = None
    merged_filtered_df = None

    #graph data frames
    filtered_graph_df = None

    def __init__(self, ec_input_file_name, registry_input_file_name, output_file_name):
        self.output_file_name = output_file_name
        self.ec_df = self.__load_input_file(ec_input_file_name)
        self.registry_df = self.__load_input_file(registry_input_file_name)

    def __load_input_file(self, input_file_name):
        return pandas.read_csv(input_file_name)

    def __report_merge(self):
        self.merged_df = pandas.merge(self.registry_df[['ID', 'RID', 'USERID', 'VISCODE', 'SVDOSE']], 
                                      self.ec_df[['ECSDSTXT', 'RID', 'VISCODE']], 
                                      on=['RID', 'VISCODE'], 
                                      how='left')

    def __report_filter(self, viscode, svdose, ecsdstxt):
        self.merged_filtered_df = self.merged_df[(self.merged_df.VISCODE == viscode) 
                                                & (self.merged_df.SVDOSE == svdose) 
                                                & (self.merged_df.ECSDSTXT != ecsdstxt)]

    def __df_to_csv(self, data, output_file_dir):
        try:
            if (not os.path.isdir(output_file_dir)):
                os.mkdir(output_file_dir)
        except:
            print("Could not create directory " + output_file_dir)
            sys.exit(2)
        data.to_csv(os.path.join(output_file_dir, self.output_file_name), index = None, header = True)

    def __graph_filter(self, svperf, viscode):
        self.filtered_graph_df = self.registry_df[(self.registry_df.SVPERF == svperf) & (self.registry_df.VISCODE != viscode)]

    def create_report(self, viscode, svdose, ecsdstxt):
        self.__report_merge()
        self.__report_filter(viscode, svdose, ecsdstxt)

    def write_report(self, output_file_dir):
        self.__df_to_csv(self.merged_filtered_df, output_file_dir)

    def draw_graph(self, svperf, viscode):
        self.__graph_filter(svperf, viscode)
        fig = go.Figure(go.Pie(
            name="",
            labels = self.filtered_graph_df.VISCODE,
            hovertemplate = "Viscode: <b>%{label}</b><br>Count: <b>%{value} (%{percent})</b>"
        ))

        fig.update_layout(
            title="<b>Viscodes from Registry</b>",
            font=dict(
                size=18
            )   
        )

        plot(fig)

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

   #generate report and graph
   dos = Dosing("t2_ec 20190619.csv", "t2_registry 20190619.csv", "results.csv")
   dos.create_report(viscode, svdose, ecsdstxt)
   dos.write_report(output_file_dir)
   dos.draw_graph('Y', 'bl')

if __name__ == "__main__":
   main(sys.argv[1:])





