import csv
import json
from connect import get_connection


def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday YYYY-MM-DD: ")
    group_name = input("Group: ")
    phone = input("Phone: ")
    phone_type = input("Phone type home/work/mobile: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO groups(name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
    """, (group_name,))

    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    group_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (name) DO UPDATE
        SET email = EXCLUDED.email,
            birthday = EXCLUDED.birthday,
            group_id = EXCLUDED.group_id
        RETURNING id
    """, (name, email, birthday, group_id))

    contact_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO phones(contact_id, phone, type)
        VALUES (%s, %s, %s)
    """, (contact_id, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact saved.")


def add_phone():
    name = input("Contact name: ")
    phone = input("Phone: ")
    phone_type = input("Phone type home/work/mobile: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()

    print("Phone added.")


def move_to_group():
    name = input("Contact name: ")
    group = input("New group: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL move_to_group(%s, %s)", (name, group))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact moved.")


def search_contacts():
    query = input("Search query: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def filter_by_group():
    group = input("Group name: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON p.contact_id = c.id
        WHERE g.name = %s
    """, (group,))

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def sort_contacts():
    allowed = {
        "name": "c.name",
        "birthday": "c.birthday",
        "date": "c.date_added"
    }

    field = input("Sort by name/birthday/date: ")

    if field not in allowed:
        print("Invalid sort field.")
        return

    conn = get_connection()
    cur = conn.cursor()

    query = f"""
        SELECT c.name, c.email, c.birthday, g.name, c.date_added
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY {allowed[field]}
    """

    cur.execute(query)
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def paginated_contacts():
    page = 0
    limit = 5

    conn = get_connection()
    cur = conn.cursor()

    while True:
        offset = page * limit

        cur.execute("""
            SELECT c.name, c.email, c.birthday, g.name, c.date_added
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY c.name
            LIMIT %s OFFSET %s
        """, (limit, offset))

        rows = cur.fetchall()

        print(f"\nPage {page + 1}")
        for row in rows:
            print(row)

        command = input("\nnext / prev / quit: ")

        if command == "next":
            page += 1
        elif command == "prev":
            if page > 0:
                page -= 1
        elif command == "quit":
            break
        else:
            print("Unknown command.")

    cur.close()
    conn.close()


def export_to_json():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON p.contact_id = c.id
        ORDER BY c.name
    """)

    rows = cur.fetchall()

    contacts = []

    for row in rows:
        contacts.append({
            "name": row[0],
            "email": row[1],
            "birthday": str(row[2]) if row[2] else None,
            "group": row[3],
            "phone": row[4],
            "phone_type": row[5]
        })

    with open("contacts_export.json", "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=4, ensure_ascii=False)

    cur.close()
    conn.close()

    print("Exported to contacts_export.json")


def import_from_json():
    filename = input("JSON file name: ")

    with open(filename, "r", encoding="utf-8") as f:
        contacts = json.load(f)

    conn = get_connection()
    cur = conn.cursor()

    for item in contacts:
        name = item["name"]

        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        existing = cur.fetchone()

        if existing:
            action = input(f"{name} exists. skip/overwrite: ")

            if action == "skip":
                continue

        group_name = item.get("group") or "Other"

        cur.execute("""
            INSERT INTO groups(name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING
        """, (group_name,))

        cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
        group_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (name) DO UPDATE
            SET email = EXCLUDED.email,
                birthday = EXCLUDED.birthday,
                group_id = EXCLUDED.group_id
            RETURNING id
        """, (
            name,
            item.get("email"),
            item.get("birthday"),
            group_id
        ))

        contact_id = cur.fetchone()[0]

        if item.get("phone"):
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (
                contact_id,
                item.get("phone"),
                item.get("phone_type", "mobile")
            ))

    conn.commit()
    cur.close()
    conn.close()

    print("Import completed.")


def import_from_csv():
    filename = input("CSV file name: ")

    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            group_name = row.get("group") or "Other"

            cur.execute("""
                INSERT INTO groups(name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING
            """, (group_name,))

            cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
            group_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (name) DO UPDATE
                SET email = EXCLUDED.email,
                    birthday = EXCLUDED.birthday,
                    group_id = EXCLUDED.group_id
                RETURNING id
            """, (
                row["name"],
                row["email"],
                row["birthday"],
                group_id
            ))

            contact_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (
                contact_id,
                row["phone"],
                row["phone_type"]
            ))

    conn.commit()
    cur.close()
    conn.close()

    print("CSV import completed.")


def menu():
    while True:
        print("""
1. Add contact
2. Add phone
3. Move to group
4. Search contacts
5. Filter by group
6. Sort contacts
7. Paginated contacts
8. Export to JSON
9. Import from JSON
10. Import from CSV
0. Exit
""")

        choice = input("Choose: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            add_phone()
        elif choice == "3":
            move_to_group()
        elif choice == "4":
            search_contacts()
        elif choice == "5":
            filter_by_group()
        elif choice == "6":
            sort_contacts()
        elif choice == "7":
            paginated_contacts()
        elif choice == "8":
            export_to_json()
        elif choice == "9":
            import_from_json()
        elif choice == "10":
            import_from_csv()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()