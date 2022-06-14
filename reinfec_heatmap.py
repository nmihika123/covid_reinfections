import pandas as pd
import seaborn as sb

#Store reinfection date, prior infection date, and time between infections in days for each patient
def get_reinfections():
  d = {}
  for pid in df.NFER_PID.unique():
      pid_chunk = df[df["NFER_PID"]==pid]
      tests =pid_chunk.NFER_DTM.tolist()
      diffs = []
      for i in range(0, len(tests)):
          curr_test = tests[i] 
          for test in tests:
              if test != curr_test:
                  diffs.append(((test - curr_test)/np.timedelta64(1, "D"), curr_test, test))
      d[pid] = diffs
  reinfections = []
  for key, val in d.items():
      l = d[key]
      for time in l:
          if time[0] <=-60:
              reinf = (str(time[1].month), str(time[1].day), str(time[1].year))
              prev = (str(time[2].month), str(time[1].day), str(time[2].year))
              reinfections.append((key, time[0], reinf,prev)) #time[1] = reinfection, time[2] = previous test
  return d, reinfections

#Generate heatmap with monthly bins based on reinfections
def generate_heatmap(): #bins=monthly
  dates = ["June 2020", "July 2020", "Aug 1 2020", "Aug 2020","Sept 2020",\
          "Oct 2020", "Nov 2020", "Dec 2020",\
          "Jan 2021", "Feb 2021",\
          "March 2021","April 2021", "May 2021",\
          "June 2021", "July 2021",\
          "Aug 2021","Sept 2021",\
          "Oct 2021", "Nov 2021", "Dec 2021", \
          "Jan 2022","Feb 2022",\
          "March 2022"]
  l = [[0] *len(dates)  for i in range(0, len(dates))]
  date_dict = dict(zip(dates, np.arange(0, len(dates), 1)))
  month_dict = {"1": "Jan", "2": "Feb", "3": "March", "4": "April" , "5":"May", "6":"June",
                "7":"July", "8":"Aug", "9":"Sept", "10":"Oct", "11":"Nov", "12": "Dec"}
  #bin by month
  for r in reinfections:
      reinfect_month = month_dict[r[2][0]]
      reinfect_day = int(r[2][1])
      reinfect_year = r[2][2]
      original_month = month_dict[r[3][0]]
      original_day = int(r[2][1])
      original_year = r[3][2]

      num_1 = date_dict[str(reinfect_month) + " " +str(reinfect_year)] #reinfection
      num_2 = date_dict[str(original_month) + " " + str(original_year)] #prior infection
      l[int(num_2)][int(num_1)]+=1
  df = pd.DataFrame(l, columns = dates, index=dates)
  df = df.div(df.sum(axis=1), axis=0 #normalize each row
  fig, ax = plt.subplots(figsize=(7, 7))
  c = sns.color_palette("crest", as_cmap=True)
  sb.heatmap(df, cmap =c, mask=(df==0))
  plt.xlabel("Reinfection Date")
  plt.ylabel("Prior Infection Date")
  plt.show()
