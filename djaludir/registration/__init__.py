SEARCH = """
    SELECT
        id_rec.id,profile_rec.birth_date,
        id_rec.firstname, aname_rec.line1,
        id_rec.lastname, SUBSTRING(id_rec.ss_no FROM 8 FOR 4) as ss_no,
        id_rec.city, id_rec.st, NVL(id_rec.zip,"") as postal_code,
        id_rec.phone, email_rec.line1 as email, cvid_rec.ldap_name,
        MIN(stu_acad_rec.yr) AS start_year, MAX(stu_acad_rec.yr) AS end_year
    FROM
        id_rec
    LEFT JOIN
        cvid_rec on id_rec.id = cvid_rec.cx_id
    LEFT JOIN
        profile_rec on id_rec.id = profile_rec.id
    LEFT JOIN
        stu_acad_rec on
        (id_rec.id = stu_acad_rec.id AND stu_acad_rec.yr > 0)
    LEFT JOIN aa_rec as aname_rec on
        (id_rec.id = aname_rec.id AND aname_rec.aa = "ANDR")
    LEFT JOIN aa_rec as email_rec on
        (id_rec.id = email_rec.id AND email_rec.aa = "EML1")
    WHERE
        (UPPER(id_rec.valid) = 'Y' or NVL(id_rec.valid, '') = '')
    AND
"""
SEARCH_GROUP_BY = """
    GROUP by id,birth_date,firstname,line1,lastname,ss_no,city,st,postal_code,phone,email,ldap_name
"""
SEARCH_ORDER_BY = """
    ORDER BY id_rec.lastname, id_rec.firstname, profile_rec.birth_date
"""
CONFIRM_USER = """
    SELECT
        id_rec.id,profile_rec.birth_date,
        id_rec.firstname, aname_rec.line1,
        id_rec.lastname, SUBSTRING(id_rec.ss_no FROM 8 FOR 4) as ss_no,
        cvid_rec.ldap_name
    FROM
        id_rec
    LEFT JOIN
        cvid_rec on id_rec.id = cvid_rec.cx_id
    LEFT JOIN aa_rec as aname_rec on
        (id_rec.id = aname_rec.id AND aname_rec.aa = "ANDR")
    LEFT JOIN
        profile_rec on id_rec.id = profile_rec.id
"""
