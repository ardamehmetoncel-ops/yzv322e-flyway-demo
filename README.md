# Flyway — Database Migration & Version Control Tool

> **YZV 322E Applied Data Engineering — Spring 2026**  
> Individual Tool Presentation | Mehmet Arda Öncel (150230312)

---

## 1. What is this tool?

Flyway is an open-source database migration tool that tracks, manages, and applies versioned SQL scripts to evolve a database schema in a controlled, repeatable way — similar to how Git versions source code. It solves the "works on my machine" problem for databases: instead of manually running DDL scripts, every schema change is a numbered migration file that Flyway applies automatically and tracks in a metadata table (`flyway_schema_history`).

Flyway was first released in 2010 by Axel Fontaine and is now maintained by Redgate Software. The Community Edition is licensed under Apache 2.0.

---

## 2. Prerequisites

| Requirement | Version |
|-------------|---------|
| Docker Desktop | v24+ |
| Docker Compose | v2.20+ (included with Docker Desktop) |
| Git | any recent version |
| Python | 3.10+ (only for `scripts/verify.py`) |

> **No JDK or local Flyway installation needed.** Everything runs inside Docker.

---

## 3. Installation

```bash
# 1. Clone the repository
git clone https://github.com/ardamehmetoncel-ops/yzv322e-flyway-demo.git
cd yzv322e-flyway-demo

# 2. Create your environment file from the example
cp .env.example .env
# (Optional) Edit .env to change credentials — defaults work fine

# 3. Install Python dependencies (for verify.py only)
pip install -r requirements.txt
```

---

## 4. Running the Example

```bash
# Step 1 — Start PostgreSQL (waits until healthy)
docker compose up -d postgres

# Step 2 — Run all Flyway migrations
docker compose run --rm flyway

# Step 3 — Verify results with Python
python scripts/verify.py

# (Optional) Open a psql shell
docker compose exec postgres psql -U flyway_user -d flyway_demo
```

To run a clean demo from scratch:

```bash
docker compose down -v   # removes containers + volume
docker compose up -d postgres
docker compose run --rm flyway
python scripts/verify.py
```

---

## 5. Expected Output

After running `python scripts/verify.py` you should see:

```
──── flyway_schema_history ──────────────────────────────
Version    Description               Type       Success
────────────────────────────────────────────────────────
1          create schema             SQL        ✅
2          seed data                 SQL        ✅
3          add indexes               SQL        ✅

──── products table ─────────────────────────────────────
ID    Name                                 Price Category
────────────────────────────────────────────────────────
1     Laptop                             1299.99 Electronics
2     Mechanical Keyboard                  79.90 Electronics
3     4K Monitor                          499.00 Electronics
4     Standing Desk                       349.00 Furniture
5     Ergonomic Chair                     599.00 Furniture
6     USB-C Hub                            45.50 Accessories
7     Webcam HD                            89.99 Accessories
8     Noise Cancelling Headphones         249.00 Electronics

──── category_summary view ──────────────────────────────
Category        Count   Avg Price      Min      Max
────────────────────────────────────────────────────────
Electronics         4     543.38     79.90  1299.99
Furniture           2     474.00    349.00   599.00
Accessories         2      67.75     45.50    89.99

✅ All checks passed. Database is healthy.
```

---

## 6. Migration Files

| File | Description |
|------|-------------|
| `migrations/V1__create_schema.sql` | Creates the `products` table |
| `migrations/V2__seed_data.sql` | Inserts 8 sample products |
| `migrations/V3__add_indexes.sql` | Adds indexes + `category_summary` view |

Flyway naming convention: `V{version}__{description}.sql` — double underscore is required.

---

## 7. How Flyway Tracks Migrations

Flyway automatically creates a `flyway_schema_history` table in your database. Every migration that runs is recorded with its version, checksum, and execution timestamp. If you run `flyway migrate` again, only new (unapplied) migrations will execute — already-applied ones are skipped.

```sql
SELECT version, description, installed_on, success
FROM flyway_schema_history;
```

---

## 8. AI Usage Disclosure

This project was created with assistance from **Claude (Anthropic)** for the following purposes:

- Scaffolding the initial `docker-compose.yml` structure
- Drafting the `README.md` template and section headings
- Generating the `verify.py` boilerplate

All code was reviewed, understood, tested, and modified by the student before submission. The SQL migration files and final configuration were written and verified independently. No AI-generated output was submitted without review.

---

## References

- [Flyway Official Documentation](https://flywaydb.org/documentation)
- [Flyway Docker Hub Image](https://hub.docker.com/r/flyway/flyway)
- [Flyway GitHub Repository](https://github.com/flyway/flyway)
- [Database Migrations with Flyway — Baeldung](https://www.baeldung.com/database-migrations-with-flyway)
- [Flyway vs. Liquibase — Redgate](https://www.red-gate.com/hub/product-learning/flyway/flyway-vs-liquibase)
