/* SPDX-License-Identifier: GPL-3.0-or-later */

/* This program is free software: you can redistribute it and/or modify */
/* it under the terms of the GNU General Public License as published by */
/* the Free Software Foundation, either version 3 of the License, or */
/* (at your option) any later version. */

/* This program is distributed in the hope that it will be useful, */
/* but WITHOUT ANY WARRANTY; without even the implied warranty of */
/* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the */
/* GNU General Public License for more details. */

/* You should have received a copy of the GNU General Public License */
/* along with this program.  If not, see <https://www.gnu.org/licenses/>. */

int
main(int argc, char **argv)
{
	// Allocate a new array and delete it.
	int *array = new int[argc + 1];
	array[argc] = 0;
	delete[] array;

	/* Access element of the deleted array. This will cause an memory error with
	 * address sanitizer.
	 */
	return array[argc];
}
