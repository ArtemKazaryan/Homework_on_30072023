CREATE TABLE IF NOT EXISTS menu(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
url TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS transacts(
id INTEGER PRIMARY KEY AUTOINCREMENT,
date DATE NOT NULL,
income_expenditure TEXT NOT NULL,
product TEXT NOT NULL,
price INTEGER NOT NULL,
quantity INTEGER NOT NULL
);
