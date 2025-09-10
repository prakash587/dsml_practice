def main(csvfile, country):
    try:
        # --- STEP 1: READ FILE ---
        with open(csvfile, "r", encoding="utf-8") as f:
            lines = f.read().strip().split("\n")

        if len(lines) < 2:
            return [], [], -2

        # --- STEP 2: Parse header and rows ---
        header = [h.strip() for h in lines[0].split("\t") if h.strip() != ""]
        rows = [line.split("\t") for line in lines[1:] if line.strip() != ""]

        # Create column index mapping
        col_index = {}
        for i, h in enumerate(header):
            col_index[h.lower()] = i

        # Standard column names in dataset
        name_idx = col_index.get("name")
        country_idx = col_index.get("country")
        founded_idx = col_index.get("founded")
        emp_idx = col_index.get("number of employees")
        salary_idx = col_index.get("median salary")
        profit20_idx = col_index.get("profits in 2020(million)")
        profit21_idx = col_index.get("profits in 2021(million)")

        # --- STEP 3: Convert rows to usable records ---
        records = []
        for r in rows:
            try:
                rec = {
                    "name": r[name_idx].strip(),
                    "country": r[country_idx].strip().lower(),
                    "founded": int(r[founded_idx]),
                    "employees": int(r[emp_idx]),
                    "salary": float(r[salary_idx]),
                    "profit20": float(r[profit20_idx]),
                    "profit21": float(r[profit21_idx]),
                }
                records.append(rec)
            except:
                continue  # skip malformed rows

        if not records:
            return [], [], -2

        country_lc = country.lower()

        # --- TASK 1: OP1 ---
        filtered = [rec for rec in records if rec["country"] == country_lc and 1981 <= rec["founded"] <= 2000]
        if filtered:
            max_emp_org = max(filtered, key=lambda x: x["employees"])["name"]
            min_emp_org = min(filtered, key=lambda x: x["employees"])["name"]
            OP1 = [max_emp_org, min_emp_org]
        else:
            OP1 = []

        # --- TASK 2: OP2 (Standard deviation of median salary) ---
        def stddev(values):
            if not values:
                return 0.0
            mean = sum(values) / len(values)
            var = sum((x - mean) ** 2 for x in values) / len(values)
            return var ** 0.5

        salaries_country = [rec["salary"] for rec in records if rec["country"] == country_lc]
        salaries_all = [rec["salary"] for rec in records]

        std_country = stddev(salaries_country)
        std_all = stddev(salaries_all)

        OP2 = [round(std_country, 4), round(std_all, 4)]

        # --- TASK 3: OP3 (Correlation) ---
        valid_recs = [rec for rec in records if rec["country"] == country_lc and rec["profit21"] > rec["profit20"]]

        if len(valid_recs) < 2:
            OP3 = -2
        else:
            xs = [rec["salary"] for rec in valid_recs]
            ys = [rec["profit21"] for rec in valid_recs]

            mean_x = sum(xs) / len(xs)
            mean_y = sum(ys) / len(ys)

            num = sum((xs[i] - mean_x) * (ys[i] - mean_y) for i in range(len(xs)))
            den_x = sum((x - mean_x) ** 2 for x in xs) ** 0.5
            den_y = sum((y - mean_y) ** 2 for y in ys) ** 0.5

            if den_x == 0 or den_y == 0:
                OP3 = -2
            else:
                OP3 = round(num / (den_x * den_y), 4)

        return OP1, OP2, OP3

    except:
        return [], [], -2
