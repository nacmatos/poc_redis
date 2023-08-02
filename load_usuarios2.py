import csv
import argparse
import redis
import xml.etree.ElementTree as ET

def csv_to_xml(csv_file):
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        xml_data = []
        for row in csv_reader:
            root = ET.Element("data")
            item = ET.SubElement(root, "item")
            for i, field in enumerate(row):
                ET.SubElement(item, header[i]).text = field
            xml_data.append(ET.tostring(root, encoding='utf-8').decode())

    return xml_data

def main():
    parser = argparse.ArgumentParser(description='Convert CSV to XML and store in Redis')
    parser.add_argument('csv_file', type=str, help='Path to the CSV file')
    parser.add_argument('redis_host', type=str, help='Redis host address')
    parser.add_argument('redis_port', type=int, help='Redis port number')
    parser.add_argument('redis_db', type=int, help='Redis database number')
    args = parser.parse_args()

    xml_data_list = csv_to_xml(args.csv_file)

    redis_client = redis.Redis(host=args.redis_host, port=args.redis_port, db=args.redis_db)

    with open(args.csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        for i, row in enumerate(csv_reader):
            redis_key = row[0]  # Assuming the first column is the key for Redis
            xml_data = xml_data_list[i]

            redis_client.set(redis_key, xml_data)
            #print(f"Data from row {i+1} stored in Redis with key '{redis_key}'.")

if __name__ == '__main__':
    main()

