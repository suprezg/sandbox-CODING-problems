# Sandbox Coding Problems

## Abstract

A dedicated repository for storing and cataloging solutions to various Coding problems. It serves as a personal archive for tracking solved challenges.

## Objective

The main objective of this repository is to store solved Coding questions for personal reference and progress tracking. It provides a simple space to showcase solutions, with no plans for external contributions, issues, pull requests, licensing documentation, or dependency requirements. It exists purely as a personal log and a resource for anyone interested in viewing the solved problems.

## Getting Started

Question Seggregation is based on from which platform the questions are coming from.

* **Codeforces**: Organized by contest number, grouped into sets of 500.
  * **Structure:** `core/codeforces/<interval>/<contest_number>/<question_character>/`
  * **Example:** `core/codeforces/501-1000/1002/B/`
* **AtCoder**: Separated by contest type, then grouped into intervals (50 for ABC/ARC, 10 for AGC/AWC).
  * **Structure:** `core/atcoder/<contest_type>/<interval>/<contest_number>/<question_character>/`
  * **Example:** `core/atcoder/AGC/40-50/43/C/`
* **LeetCode**: Organized by their sequential Question ID, grouped into sets of 500.
  * **Structure:** `core/leetcode/<interval>/<question_id>/`
  * **Example:** `core/leetcode/2001-2500/2498/`
* **CodeChef**: Organized by their numerical difficulty rating, grouped into sets of 500.
  * **Structure:** `core/codechef/<interval>/<difficulty>_<question_code>/`
  * **Example:** `core/codechef/3501-4000/3563_NYRES/`
* **Advent of Code**: Organized by year, grouped into 5-year blocks.
  * **Structure:** `core/adventofcode/<year_interval>/<year>-<day>/`
  * **Example:** `core/adventofcode/2011-2015/2015-1/`
