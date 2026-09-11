import csv


# =========================================================
# LOAD JOB DATA
# =========================================================

def load_jobs():

    jobs = []


    with open(
        "data/jobs.csv",
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)


        for row in reader:

            required_skills = [

                skill.strip().lower()

                for skill in row["required_skills"].split("|")

            ]


            jobs.append({

                "title": row["title"],

                "description": row["description"],

                "skills": required_skills

            })


    return jobs


# =========================================================
# MATCH JOBS
# =========================================================

def match_jobs(resume_text, resume_skills):

    jobs = load_jobs()


    resume_skill_set = {

        skill.lower()

        for skill in resume_skills

    }


    results = []


    for job in jobs:

        required_skills = set(job["skills"])


        matched_skills = (

            required_skills
            & resume_skill_set

        )


        missing_skills = (

            required_skills
            - resume_skill_set

        )


        # -------------------------------------------------
        # Match percentage
        # -------------------------------------------------

        if required_skills:

            match_score = (

                len(matched_skills)
                / len(required_skills)
            ) * 100

        else:

            match_score = 0


        results.append({

            "title": job["title"],

            "description": job["description"],

            "match_score": round(match_score),

            "matched_skills": sorted(
                matched_skills
            ),

            "missing_skills": sorted(
                missing_skills
            )

        })


    # -----------------------------------------------------
    # Highest match first
    # -----------------------------------------------------

    results.sort(

        key=lambda x: x["match_score"],

        reverse=True

    )


    return results