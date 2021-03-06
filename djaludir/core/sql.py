# for some reason alt_name does not work here so we use aname
SEARCH = '''
    SELECT
        alum.cl_yr AS class_year, TRIM(NVL(ids.firstname,"")) AS fname,
        TRIM(NVL(aname_rec.line1,"")) AS aname,
        maiden.lastname AS maiden_name, ids.lastname, ids.id,
        NVL(
            TRIM(aaEmail.line1) ||
            TRIM(aaEmail.line2) ||
            TRIM(aaEmail.line3), ""
        ) AS email,
        LOWER(ids.lastname) AS sort1,
        LOWER(ids.firstname) AS sort2
    FROM
        alum_rec alum
    INNER JOIN
        id_rec ids ON alum.id = ids.id
    LEFT JOIN (
        SELECT
            prim_id, MAX(active_date) active_date
        FROM
            addree_rec
        WHERE
            style = "M"
        GROUP BY prim_id
        )
        prevmap
    ON
        ids.id = prevmap.prim_id
    LEFT JOIN
        aa_rec as aname_rec
    ON
        (
            ids.id = aname_rec.id AND aname_rec.aa = "ANDR"
        )
    LEFT JOIN
        addree_rec maiden
    ON
        maiden.prim_id = prevmap.prim_id
    AND
        maiden.active_date = prevmap.active_date
    AND
        maiden.style = "M"
    LEFT JOIN
        aa_rec aaEmail
    ON
        alum.id = aaEmail.id
    AND
        aaEmail.aa = "EML2"
    AND
        TODAY BETWEEN aaEmail.beg_date AND NVL(aaEmail.end_date, TODAY)
    LEFT JOIN
        hold_rec holds
    ON
        alum.id = holds.id
    AND
        holds.hld = "DDIR"
    AND
        CURRENT BETWEEN holds.beg_date AND NVL(holds.end_date, CURRENT)
'''

ACTIVITY_SEARCH = '''
    SELECT
        TRIM(invl_table.txt) txt
    FROM
        invl_table
    WHERE
        invl_table.invl MATCHES "S[0-9][0-9][0-9]"
    AND
        LOWER(invl_table.txt) LIKE "%%{search_string}%%"
    ORDER BY
        TRIM(invl_table.txt)
'''.format

ACTIVITY_SEARCH_JX = '''
SELECT
    TRIM(attribute_type.value) as txt
FROM
    attribute_type
WHERE
    LOWER(attribute_type.value) LIKE "%{search_string}%"
ORDER BY
    TRIM(attribute_type.value)
'''.format

MAJORS = '''
    SELECT
        DISTINCT TRIM(major) AS major_code,
        TRIM(txt) AS major_name
    FROM
        major_table
    ORDER BY TRIM(txt)
'''

PRIVACY =  '''
    SELECT
        TRIM(fieldname) AS fieldname, TRIM(display) AS display
    FROM
        stg_aludir_privacy
    WHERE
        id = {cid}
    ORDER BY
        fieldname
'''.format

RELATIVES_ORIG = '''
    SELECT
        TRIM(
            CASE
                WHEN    rel.prim_id = {cid}
                THEN    sec.firstname
                ELSE    prim.firstname
            END
        ) AS firstName,
        TRIM(
            CASE
                WHEN    rel.prim_id = {cid}
                THEN    sec.lastname
                ELSE    prim.lastname
            END
       ) AS lastName,
       TRIM(
            CASE
                WHEN    rel.prim_id = {cid}
                THEN    reltbl.sec_txt
                ELSE    reltbl.prim_txt
            END
        ) AS relText,
        TRIM(reltbl.rel) ||
            CASE
                WHEN    rel.prim_id = {cid}
                THEN    "2"
                ELSE    "1"
            END
        AS relCode
    FROM
        relation_rec rel
    INNER JOIN
        id_rec prim
    ON
        rel.prim_id = prim.id
    INNER JOIN
        id_rec sec
    ON
        rel.sec_id = sec.id
    INNER JOIN
        rel_table reltbl
    ON
        rel.rel = reltbl.rel
    WHERE
        TODAY BETWEEN
            rel.beg_date
        AND
            NVL(rel.end_date, TODAY)
    AND
        rel.rel IN ("AUNN","COCO","GPGC","HW","HWNI","PC","SBSB")
    AND
        (prim_id = {cid} OR sec_id = {cid})
'''.format

ACTIVITIES = '''
    SELECT
        TRIM(invl_table.txt) AS {fieldname}
    FROM
        invl_table
    INNER JOIN
        involve_rec
    ON
        invl_table.invl = involve_rec.invl
    WHERE
        involve_rec.id  = {cid}
    AND
        invl_table.invl MATCHES "S[0-9][0-9][0-9]"
    AND
        invl_table.invl {comparison} IN (
            "S019","S020","S021","S022","S228","S043","S044","S056","S057",
            "S073","S079","S080","S083","S090","S095","S220","S100","S101",
            "S109","S126","S131","S156","S161","S172","S173","S176","S186",
            "S187","S196","S197","S204","S205","S207","S208","S253","S215",
            "S216"
        )
    ORDER BY
        TRIM(invl_table.txt)
'''.format

ALUMNA = '''
    SELECT DISTINCT
        ids.id AS carthage_id,
        TRIM(ids.firstname) AS first_name,
        TRIM(NVL(aname_rec.line1,"")) AS alt_name,
        TRIM(ids.lastname) AS last_name,
        TRIM(ids.suffix) AS suffix,
        TRIM(INITCAP(ids.title)) AS prefix,
        TRIM(NVL(email.line1,"")) email,
        CASE
            WHEN NVL(ids.decsd, "N") = "Y"
            THEN 1
        END AS is_deceased,
        TRIM(NVL(maiden.lastname,"")) AS birth_last_name,
        TRIM(NVL(progs.deg,"")) AS degree,
        CASE
            WHEN TRIM(progs.deg) IN ("BA","BS")
            THEN alum.cl_yr
        END AS class_year,
        TRIM(NVL(aawork.line1, "")) AS business_address_line1,
        TRIM(NVL(aawork.line2,"")) AS business_address_line2,
        TRIM(NVL(aawork.line3,"")) AS business_address_line3,
        TRIM(NVL(aawork.city,"")) AS business_city,
        TRIM(aawork.st) AS business_state,
        TRIM(NVL(aawork.zip,"")) AS business_postal_code,
        TRIM(aawork.ctry) AS business_country,
        TRIM(NVL(aawork.phone,"")) AS business_phone,
        TRIM(ids.addr_line1) AS home_address_line1,
        TRIM(ids.addr_line2) AS home_address_line2,
        TRIM(ids.addr_line3) AS home_address_line3,
        TRIM(ids.city) AS home_city,
        TRIM(ids.st) AS home_state,
        TRIM(ids.zip) AS home_postal_code,
        TRIM(ids.ctry) AS home_country, TRIM(ids.phone) AS home_phone,
        TRIM(
            CASE
                WHEN TRIM(progs.deg) IN ("BA","BS")
                THEN major1.txt
                ELSE conc1.txt
            END
        ) AS major1,
        TRIM(
            CASE
                WHEN TRIM(progs.deg) IN ("BA","BS")
                THEN major2.txt
                ELSE conc2.txt
            END
        ) AS major2,
        TRIM(
            CASE
                WHEN TRIM(progs.deg) IN ("BA","BS")
                THEN major3.txt
                ELSE ""
            END
        ) AS major3,
        CASE
            WHEN TRIM(progs.deg) NOT IN ("BA","BS")
            THEN alum.cl_yr
            ELSE 0
        END AS masters_grad_year,
        "" AS job_title
    FROM
        alum_rec alum
        INNER JOIN
            id_rec ids          ON  alum.id = ids.id
        LEFT JOIN (
            SELECT   prim_id, MAX(active_date) active_date
            FROM     addree_rec
            WHERE    style = "M"
            GROUP BY prim_id
        )
            prevmap             ON  ids.id              = prevmap.prim_id
        LEFT JOIN
            aa_rec as aname_rec
        ON
            (
                ids.id = aname_rec.id AND aname_rec.aa = "ANDR"
            )
        LEFT JOIN
            addree_rec maiden   ON  maiden.prim_id      = prevmap.prim_id
                                AND maiden.active_date  = prevmap.active_date
                                AND maiden.style        = "M"
        LEFT JOIN
            aa_rec email        ON  ids.id              = email.id
                                AND email.aa            = "EML2"
                                AND TODAY
                                    BETWEEN
                                        email.beg_date
                                    AND
                                        NVL(
                                            email.end_date,
                                            TODAY
                                        )
        LEFT JOIN
            aa_rec aawork       ON  ids.id              = aawork.id
                                AND aawork.aa           = "WORK"
                                AND TODAY
                                    BETWEEN
                                        aawork.beg_date
                                    AND
                                        NVL(
                                            aawork.end_date,
                                            TODAY
                                        )
        LEFT JOIN
            prog_enr_rec progs  ON  ids.id          = progs.id
                                AND progs.acst      = "GRAD"
        LEFT JOIN
            major_table major1  ON  progs.major1    = major1.major
        LEFT JOIN
            major_table major2  ON  progs.major2    = major2.major
        LEFT JOIN
            major_table major3  ON  progs.major3    = major3.major
        LEFT JOIN
            conc_table conc1    ON  progs.conc1     = conc1.conc
        LEFT JOIN
            conc_table conc2    ON  progs.conc2     = conc2.conc
    WHERE
        ids.id = {cid}
    {deceased}
'''.format
