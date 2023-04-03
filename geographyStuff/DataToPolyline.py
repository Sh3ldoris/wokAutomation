import csv
import polyline

input_filename = "data/input.csv"
output_filename = "data/output.txt"
query: str

with open(input_filename, "r") as input_file, open(output_filename, "w") as output_file:
    csv_reader = csv.reader(input_file, delimiter="\t")

    query = """
MERGE INTO WF_CODEBOOK_VALUE v
USING (
    select ID, POLYLINE
        from (values
    """

    for row in csv_reader:
        id = row[0] # takse ID
        coordinates = row[1] # takes JSON array of array with coordinates
        # Strip the outer brackets and split the string into a list of (lat, lon) tuples
        coordinates = coordinates.strip("[]").split("],[")
        # Convert the string coordinates to floats and create a list of (lat[0], lon[1]) tuples
        coordinates = [(float(c.split(",")[0]), float(c.split(",")[1])) for c in coordinates]
        # Encode the coordinates into a polyline string
        polyline_string = polyline.encode(coordinates)
        # Write the ID and encoded polyline string to the output file
        query += ("\t\t\t({}, {}),\n".format(id, polyline_string))

    query += """
    ) newPolyline (ID, POLYLINE)
) n
ON (v.ID = n.ID)
WHEN MATCHED THEN
    UPDATE
        SET POLYLINE = n.POLYLINE
WHEN NOT MATCHED THEN
"""
    output_file.write(query)

print("Encoded polyline strings written to", output_filename)