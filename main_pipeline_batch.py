import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from google.cloud import bigquery
import re
import logging
import sys

PROJECT='user-logs-237110'
schema = 'remote_addr:STRING, timelocal:STRING, request_type:STRING, status:STRING, body_bytes_sent:STRING, http_referer:STRING, http_user_agent:STRING'


src_path = "user_log_fileC.txt"

def regex_clean(data):

    PATTERNS =  [r'(^\S+\.[\S+\.]+\S+)\s',r'(?<=\[).+?(?=\])',
           r'\"(\S+)\s(\S+)\s*(\S*)\"',r'\s(\d+)\s',r"(?<=\[).\d+(?=\])",
           r'\"[A-Z][a-z]+', r'\"(http|https)://[a-z]+.[a-z]+.[a-z]+']
    result = []
    for match in PATTERNS:
      try:
        reg_match = re.search(match, data).group()
        if reg_match:
          result.append(reg_match)
        else:
          result.append(" ")
      except:
        print("There was an error with the regex search")
    result = [x.strip() for x in result]
    result = [x.replace('"', "") for x in result]
    res = ','.join(result)
    return res


class Split(beam.DoFn):

    def process(self, element):
        """
          Transforms data into PCollection for BQ
        """
        element = element.split(",")

        return [{ 
            'remote_addr': element[0],
            'timelocal': element[1],
            'request_type': element[2],
            'status': element[3],
            'body_bytes_sent': element[4],
            'http_referer': element[5],
            'http_user_agent': element[6]
    
        }]

def main():
   # argv = [
   #    '--project={0}'.format(PROJECT),
   #    '--staging_location=gs://{0}/staging/'.format(BUCKET),
   #    '--temp_location=gs://{0}/staging/'.format(BUCKET),
   #    '--runner=DataflowRunner'
   # ]

   p = beam.Pipeline()

   (p
      | 'ReadData' >> beam.io.textio.ReadFromText(src_path)
      | "clean address" >> beam.Map(regex_clean)
      | 'ParseCSV' >> beam.ParDo(Split())
      | 'WriteToBigQuery' >> beam.io.WriteToBigQuery('{0}:userlogs.streaminglogs'.format(PROJECT), schema=schema,
        write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE)
   )

   p.run()

if __name__ == '__main__':
  logger = logging.getLogger().setLevel(logging.INFO)
  main()
