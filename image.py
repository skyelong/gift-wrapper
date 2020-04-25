import pathlib
import shutil
import subprocess
from typing import Union

import colors

import latex


def tex_to_pdf(source_file: Union[str, pathlib.Path], timeout: int = 10) -> pathlib.Path:
	"""
	Compiles a TeX file.

	Parameters
	----------
	source_file : str or pathlib.Path
		TeX file.
	timeout: int
		Seconds that are given to compile the source.

	Returns
	-------
	out: str
		The path to the compiled pdf.

	"""

	source_file = pathlib.Path(source_file)

	try:

		exit_status = latex.compile_tex(source_file, timeout=timeout)

	except subprocess.TimeoutExpired:

		print(
			f'{colors.error}could not compile {colors.reset}{source_file + ".tex"}'
			f' {colors.error}in {colors.reset}{timeout}{colors.error} seconds'
		)

		raise SystemExit

	assert exit_status == 0, f'{colors.error}errors were found while compiling {colors.reset}{source_file}'

	return source_file.with_suffix('.pdf')


def pdf_to_svg(input_file: Union[str, pathlib.Path]) -> pathlib.Path:
	"""
	Converts a pdf file into an svg.

	Parameters
	----------
	input_file : str or pathlib.Path
		pdf file.

	Returns
	-------
	out: str
		The path to the svg file.

	"""

	input_file = pathlib.Path(input_file)
	output_file = input_file.with_suffix('.svg')

	path_to_pdf2svg = shutil.which('pdf2svg')

	assert path_to_pdf2svg, "couldn't find pdf2svg"

	command = [path_to_pdf2svg, input_file.name, output_file.name]

	run_summary = subprocess.run(command, capture_output=True, cwd=input_file.parent)

	assert run_summary.returncode == 0,\
		f"{colors.error}could not convert {colors.reset}{input_file}{colors.error} to svg"

	return output_file
