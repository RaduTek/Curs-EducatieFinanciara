import json

import os


def extract_title_and_body(file):
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    title = None
    body = "".join(lines)

    for line in lines:
        stripped_line = line.strip()
        if stripped_line:
            title = stripped_line.lstrip("#").strip()
            break

    title = title.strip()

    return title, body


def explore_directory(base_dir="content", current_prefix=""):
    content = []
    index = 1
    entries = sorted(os.listdir(base_dir))

    for entry in entries:
        path = os.path.join(base_dir, entry)

        if os.path.isfile(path) and entry.endswith(".md"):
            if entry == "0.md":
                prefix = current_prefix
            else:
                prefix = f"{current_prefix}{index}."

            title, body = extract_title_and_body(path)
            if title:
                content.append({"title": f"{prefix} {title}", "body": body})
            index += 1

        elif os.path.isdir(path):
            new_prefix = f"{current_prefix}{index}."
            content.extend(explore_directory(path, new_prefix))
            index += 1

    return content


def get_course_data():
    with open("meta/meta.json", "r", encoding="utf-8") as f:
        course = json.load(f)

    with open("meta/quiz.json", "r", encoding="utf-8") as f:
        quiz = json.load(f)
        course["quiz"] = quiz

    with open("meta/description.md", "r", encoding="utf-8") as f:
        description = "\n".join(f.readlines())
        course["description"] = description

    return course


def build():

    course = get_course_data()

    content = explore_directory()

    course["content"] = content

    with open("course.json", "w") as f:
        json.dump(course, f)


build()
