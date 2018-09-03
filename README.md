#Budget

This project aims to aggregate all your spending information by extracting transaction information from bank statements.  Budget is an end to end solution for those like myself who don't want to give out bank passwords to online services.  The goal is to be able to select a folder that contains your bank (or other) statements and Budget will generate a graph that details your monthly spending, with customizable categories.  

1. Extract Text

return transaction date, name, location (if applicable), and amount

methods:
PyPDF2 pdf parser (unreliable)
computer vision for detecting tables
machine learning? lol rip

Tesseract - pretty good!
need to deal with bad transcriptions somehow

convert -density 300 Statement-2018-05-15.PDF -depth 8 -strip -background white -alpha off starone.jpg

tesseract image output

text = "04/02 H» TRADER JOE'S #234 QPS LOS ANGELES CA 41.36"
text = raw_input("input: ")



2. Determine Category

database of past transaction names
keyword identifier ie. ramen yamadaya -> ramen -> dining out
use graph
have each word connect to the one after it
keyword also a starting point

for new transactions:
starting searching from first word
then continue until one matches
if no match, ask user for category, and name of business
optional: select keyword

transactions db schema
	transaction ID -> hash name and date
	date
	name
	amount $$
	category

categories db schema
	keyword
	category

regex parse
chase
^([0-1]\d/[0-3]\d)\s(.+)\s(\d+\.\d\d)$

star one
^

to find the year:
.*\s([0-1]\d/[0-3]\d/\d\d).*

ask user to input if unsure

Categories

dining out
transportation
entertainment
groceries
hobby
clothes
personal care

3. Save Transaction Data

transaction date, name, location (if applicable), and amount, business matched, category
use balanced binary search tree sorted by date
180115 <- year, month, date

serialize to a sorted list of transactions

create some way of group transactions by category and totals by month

4. Data Analysis

create graph to show combined spending month over month
allow finer grain detail like viewing spending of different categories
^ can be plotted in a multiple line graph?
allow flexible date viewing

matplotlib

class BudgetGrapher:
pass in TransactionItem (price, category), and name of category or ID or something
insert item: pass date, cost, category
monthly_total: month -> total $$
spend_groups: category string -> SpendGroup

SpendGroup
line_color, label
timeline: date -> $ int
print_timeline()


