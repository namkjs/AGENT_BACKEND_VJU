from pipeline.run_pipeline import download_file_from_url
import asyncio
asyncio.run(download_file_from_url("http://13.238.116.61:3001/attachments?path=attachments%2Ftest-20a8aedc-2625-47b7-b374-5e9756eab3a4.docx"))