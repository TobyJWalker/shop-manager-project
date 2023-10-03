from lib.database_connection import DatabaseConnection


# Connect to the database
connection = DatabaseConnection()
connection.connect()

# Seed with some seed data
connection.seed("seeds/blog_posts_tags.sql")
