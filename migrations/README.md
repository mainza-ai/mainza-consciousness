# Neo4j Schema Migrations

- Place all Cypher migration scripts in this folder (e.g., `001_initial_schema.cypher`).
- To apply a migration, run the script in Neo4j Browser or cypher-shell:
  ```sh
  cypher-shell -u $NEO4J_USER -p $NEO4J_PASSWORD -f migrations/001_initial_schema.cypher
  ```
- Keep migration scripts numbered and documented for easy upgrades and rollbacks. 