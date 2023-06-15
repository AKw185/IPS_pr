import graphene
import psycopg2

conn = psycopg2.connect(host="localhost", port="5432", database="app", user="postgres", password="password")


class Article(graphene.ObjectType):
    id = graphene.ID()
    title = graphene.String()


class Query(graphene.ObjectType):
    articles = graphene.List(Article)

    def resolve_articles(self, info):
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, title FROM articles")
                result = cur.fetchall()

        articles = []
        for row in result:
            article = Article(
                id=row[0],
                title=row[1]
            )
            articles.append(article)

        return articles


# Create the GraphQL schema
schema = graphene.Schema(query=Query)

# Define the GraphQL query
query = '''
    query {
        articles {
            id
            title
        }
    }
'''

# Execute the GraphQL query
result = schema.execute(query)

# Print the query result
print(result.data)

