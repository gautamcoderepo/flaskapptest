import csv
import json
import uuid
import os
from config import config
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_file_handler = logging.FileHandler(os.path.join(config['log_folder_path'],'file.log'), mode='w')
log_file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_file_handler.setFormatter(log_file_format)
logger.addHandler(log_file_handler)


class ParseCsv(object):
    def __init__(self, filename, headers=True, id=None):
        self.processing_id = id if id else uuid.uuid4().hex
        self.filename = filename
        self.headers = headers

    def get_data(self):
        """
        :param filename: name of the csv file
        :param headers: True if csv has headers else False
        :return: list of row data (basically a list of lists)
        """
        data = []
        status = False
        input_filepath = os.path.join(config['input_folder_path'], self.filename)
        try:
            with open(input_filepath, 'r') as csvfile:
                filereader = csv.reader(csvfile)

                for id, row in enumerate(filereader):
                    # Skip the first row if it is the header
                    if self.headers and id == 0:
                        continue
                    else:
                        data.append(row)

            status = True

        except FileNotFoundError:
            status = False
            logger.error(f"ID:{self.processing_id} FILENAME:{self.filename} MESSAGE:File not found input directory")

        except Exception as e:
            status = False
            logger.error(f"ID:{self.processing_id} FILENAME:{self.filename} MESSAGE:{str(e)}")

        finally:
            return status, data


    def create_json(self, final_list):
        status = False

        try:
            output_filepath = os.path.join(config['output_folder_path'],os.path.splitext(self.filename)[0]+'.json')

            with open(output_filepath, 'w') as output_json:
                output_json.write(json.dumps(final_list, indent=3))
        except Exception as e:
            logger.error(f"ID:{self.processing_id} FILENAME:{self.filename} MESSAGE:{str(e)}")



    def remove_irrelevant_records(self, list_of_records):
        """
        :param list_of_records:
        :return: filtered_list_of_records : removing junk rows
        """
        filtered_list_of_records = []

        for record in list_of_records:
            # Do not need the base url column
            new_record = record[1:]

            print('New Record', new_record)

            if any(new_record):
                nodeslist = [new_record[pos:pos + 3] for pos in range(0, len(new_record), 3)]
                filtered_list_of_records.append(nodeslist)

        return filtered_list_of_records


    def get_node_hierarchy(self, key, data, repl_dictionary):
        """
        :param key: id of the node
        :param data: all child data
        :param repl_dictionary: id to {id, label, url} mapping
        :return: final version of a particular node with all children
        """
        node = repl_dictionary.get(key)

        if len(data.keys()) > 0:
            node["children"] = [self.get_node_hierarchy(key, value, repl_dictionary) for key, value in data.items()]
        return node


    def create_final_list(self, filtered_list_of_records):
        """
        :param filtered_list_of_records: obtained after remove_irrelevant_records
        :return: final data as lkist of dictionaries
        """
        final_list = []
        hierarchy_dictionary = {}
        repl_dictionary = {}

        for nodeslist in filtered_list_of_records:
            root_label, root_id, root_url = nodeslist[0]

            if root_id not in hierarchy_dictionary:
                hierarchy_dictionary[root_id] = {}
            if root_id not in repl_dictionary:
                repl_dictionary[root_id] = {
                    'label': root_label,
                    'id': root_id,
                    'url': root_url,
                }

            temp = hierarchy_dictionary[root_id]

            for node in nodeslist[1:]:
                label, id, url = node

                if id != '':
                    if id not in temp:
                        temp[id] = {

                        }

                    temp = temp[id]

                    if id not in repl_dictionary:
                        repl_dictionary[id] = {
                            'label': label,
                            'id': id,
                            'url': url,
                        }


        for key, value in hierarchy_dictionary.items():
            final_list.append(self.get_node_hierarchy(key, value, repl_dictionary))

        return final_list


    def process(self):
        logger.info(f"ID:{self.processing_id} FILENAME:{self.filename} Process Started")

        status, data = self.get_data()

        if status:
            logger.info(f"ID:{self.processing_id} FILENAME:{self.filename} File Data Extracted Successfully")
            filtered_data = self.remove_irrelevant_records(data)
            print(filtered_data)
            logger.info(f"ID:{self.processing_id} FILENAME:{self.filename} Data Cleaned Successfully")
            final_list = self.create_final_list(filtered_data)
            print(final_list)
            logger.info(f"ID:{self.processing_id} FILENAME:{self.filename} Hierarchies Created Successfully")
            self.create_json(final_list)
            logger.info(f"ID:{self.processing_id} FILENAME:{self.filename} Process Completed")






