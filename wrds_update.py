#!/usr/bin/env python3
import argparse, os, sys
from sqlalchemy import create_engine
from wrds_fetch import wrds_update

def get_env_input():
	"""Get pg variables from command line, otherwise grep from OS."""
	parser = argparse.ArgumentParser(description='Download tables from WRDS and upload to PostgreSQL.')
	parser.add_argument('-H', type=str, dest='host', action='store', nargs='?',
	                   help='pghost address')
	parser.add_argument('-P', type=int, dest='port', action='store', nargs='?', default=5432, help='pgport')
	parser.add_argument('-D', type=str, dest='dbname', action='store', nargs='?', help='pgdatabase')
	# parser.add_argument('-F', type=str, dest='fpath', action='store', nargs='?', help='file path')
	parser.add_argument('-T', type=str, dest='table', action='store', nargs='?', help='table name')
	parser.add_argument('-S', type=str, dest='schema', action='store', nargs='?', help='schema name')
	parser.add_argument('-W', type=str, dest='wrds_id', action='store', nargs='?', help='wrds id')
	parser.add_argument('-U', type=str, dest='pguser', action='store', nargs='?', help='wrds id')

	parser.add_argument('--fix_missing', type=bool, dest='fix_missing', action='store', nargs='?', 
		help='fix missing value')
	parser.add_argument('--fix_cr', type=bool, dest='fix_cr', action='store', nargs='?', 
		help='fix character')
	parser.add_argument('--drop', type=str, dest='drop', action='store', nargs='?', 
		help='columns to drop')
	parser.add_argument('--obs', type=str, dest='obs', action='store', nargs='?', 
		help='number of observations to return')
	parser.add_argument('--rename', type=str, dest='rename', action='store', nargs='?', 
		help='rename columns')


	args = parser.parse_args()

	# Check for connection variables
	if not args.host:
		args.host = os.getenv("PGHOST")
		if args.host:
			print("Using default pghost: ", args.host)
		else:
			print("Error: missing pghost. Specify database with -H.")
			quit()
	if not args.dbname:
		args.dbname = os.getenv("PGDATABASE")
		if args.host:
			print("Using default pghost: ", args.host)
		else:
			print("Error: missing pgdatabase. Specify database with -D.")
			quit()
	# if not args.fpath:
	# 	print("Error: missing file. Specify file path with -P.")
	# 	quit()
	if not args.table:
		print("Error: missing table name. Specify file path with -T.")
		quit()		
	if not args.schema:
		print("Error: missing sql server schema. Specify schema with -S.")
		quit()
	if not args.wrds_id:
		args.wrds_id = os.getenv("WRDS_ID")
		if args.wrds_id:
			print("Using default pghost: ", args.wrds_id)
		else:
			print("Error: missing wrds_id. Specify database with -W.")
			quit()
	if not args.pguser:
		args.pguser = os.getenv("PGUSER")
		if args.pguser:
			print("Using default pguser: ", args.pguser)
		else:
			print("Error: missing pguser. Specify database with -U.")
			quit()
	
	print("\n**********************")
	print("Basic settings: ")
	print('pghost=', args.host)
	print('pgport=', args.port)
	print('pgdatabase=', args.dbname)
	# print('file path=', args.fpath)
	print('table=', args.table)
	print('schema=', args.schema)
	print('wrds_id=', args.wrds_id)
	print('pguser=', args.pguser)
	print("**********************")
	return args
if __name__ == "__main__":
	args = get_env_input()
	engine = create_engine("postgresql://" + args.host + "/" + args.dbname)
	wrds_update(args.table, args.schema, engine, args.wrds_id)