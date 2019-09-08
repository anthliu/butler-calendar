import argparse
import yaml
from pprint import pprint

from cal import Calendar

def main(args):
    with open(args.constraints, 'r') as f:
        constraints = yaml.safe_load(f)
    calendar = Calendar()
    calendar.weekly_events('primary', 1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Butler - Automatic scheduling tool')
    parser.add_argument('constraints', type=str, help='Constraints file. (YAML)')

    args = parser.parse_args()
    main(args)
