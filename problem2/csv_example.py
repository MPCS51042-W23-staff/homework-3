import csv
import pathlib


def main():
    # this will ensure that the file can be found relative to the current directory
    with open(pathlib.Path(__file__).parent / "schools.csv") as fd:
        # see https://docs.python.org/3/library/csv.html#csv.DictReader
        reader = csv.DictReader(fd)
        for line in reader:
            print(line)


if __name__ == "__main__":
    main()
